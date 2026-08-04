/**
 * POST /api/contact — contact, audit-lead and newsletter form handler.
 *
 * Stores every submission in KV so it can be listed and exported as CSV from
 * /admin/leads/, and emails it if Resend is configured. Storage and email are
 * independent: a missing RESEND_KEY never loses the lead.
 *
 * Bindings:
 *   LEADS_KV or AUDIT_KV   KV namespace (required to persist leads)
 *   RESEND_KEY             Resend API key (optional; without it, leads are stored only)
 *   TO_EMAIL               where enquiries land (default hello@svedsolution.com)
 */

const json = (o, s = 200) => new Response(JSON.stringify(o), {
  status: s,
  headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' }
});

const esc = s => String(s == null ? '' : s)
  .replace(/[<>&"]/g, c => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;' }[c]));

const FIELDS = ['name', 'email', 'phone', 'website', 'service', 'revenue', 'message', 'score', 'page'];

export async function onRequestPost({ request, env }) {
  let d;
  try { d = await request.json(); } catch { return json({ error: 'Invalid request.' }, 400); }

  // Honeypot — bots fill hidden fields, humans do not.
  if (d.company_website) return json({ ok: true });

  const email = String(d.email || '').trim().toLowerCase();
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(email)) {
    return json({ error: 'Please enter a valid email address.' }, 400);
  }

  const kv = env.LEADS_KV || env.AUDIT_KV;
  const ip = request.headers.get('cf-connecting-ip') || 'anon';

  if (kv) {
    const key = `form:${ip}`;
    const hits = parseInt(await kv.get(key) || '0', 10);
    if (hits >= 5) return json({ error: 'Too many submissions. Please email us directly.' }, 429);
    await kv.put(key, String(hits + 1), { expirationTtl: 3600 });
  }

  const type = d.type === 'newsletter' ? 'newsletter'
    : d.type === 'audit' ? 'audit'
      : 'enquiry';

  const lead = {
    id: crypto.randomUUID(),
    type,
    email,
    received: new Date().toISOString(),
    country: request.headers.get('cf-ipcountry') || '',
    referer: request.headers.get('referer') || ''
  };
  for (const f of FIELDS) if (d[f]) lead[f] = String(d[f]).slice(0, 2000);

  // ---- Persist -----------------------------------------------------------
  let stored = false;
  if (kv) {
    // Sortable key: newest first when listed, since KV lists lexicographically.
    const inverse = (9999999999999 - Date.now()).toString().padStart(13, '0');
    try {
      await kv.put(`lead:${inverse}:${lead.id}`, JSON.stringify(lead));
      stored = true;
    } catch (e) {
      console.log('KV write failed', e.message);
    }
  }

  // ---- Notify ------------------------------------------------------------
  // Leads go straight to the Gmail inboxes rather than via
  // hello@svedsolution.com, so notifications keep working even if Cloudflare
  // Email Routing is unconfigured or later changed.
  const recipients = [...new Set(
    ['svedsolution@gmail.com', 'prakashved155@gmail.com', env.TO_EMAIL, env.CC_EMAIL]
      .filter(Boolean)
      .map(a => a.trim().toLowerCase())
  )];

  if (env.RESEND_KEY) {
    const rows = Object.entries(lead)
      .filter(([k]) => k !== 'id')
      .map(([k, v]) => `<tr><td style="padding:6px 12px;color:#666">${esc(k)}</td><td style="padding:6px 12px"><strong>${esc(v)}</strong></td></tr>`)
      .join('');
    try {
      const res = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: { authorization: `Bearer ${env.RESEND_KEY}`, 'content-type': 'application/json' },
        body: JSON.stringify({
          from: 'SVED Solution <noreply@svedsolution.com>',
          to: recipients,
          reply_to: email,
          subject: `${type === 'newsletter' ? 'Newsletter signup' : 'New enquiry'} — ${esc(d.name || email)}`,
          html: `<h2 style="font-family:sans-serif">${type}</h2>
                 <table style="font-family:sans-serif;font-size:14px;border-collapse:collapse">${rows}</table>`
        })
      });
      if (!res.ok) console.log('Resend error', res.status, await res.text());
    } catch (e) {
      console.log('Resend threw', e.message);
    }
  } else {
    console.log('LEAD (no RESEND_KEY):', JSON.stringify(lead));
  }

  if (!kv) console.log('LEAD NOT PERSISTED - no KV binding:', JSON.stringify(lead));
  return json({ ok: true, stored });
}
