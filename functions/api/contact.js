/**
 * POST /api/contact — contact + newsletter form handler.
 *
 * Bindings (set in Cloudflare Pages > Settings > Environment variables):
 *   RESEND_KEY   Resend API key (free tier: 3,000 emails/month)
 *   TO_EMAIL     where enquiries land (defaults to hello@svedsolution.com)
 *   AUDIT_KV     optional — reuses the audit KV namespace for spam rate limiting
 */

const json = (o, s = 200) => new Response(JSON.stringify(o), {
  status: s,
  headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' }
});

const esc = s => String(s || '').replace(/[<>&"]/g, c => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;' }[c]));

export async function onRequestPost({ request, env }) {
  let d;
  try { d = await request.json(); } catch { return json({ error: 'Invalid request.' }, 400); }

  // Honeypot — bots fill hidden fields, humans do not.
  if (d.company_website) return json({ ok: true });

  const email = String(d.email || '').trim();
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(email)) {
    return json({ error: 'Please enter a valid email address.' }, 400);
  }

  const ip = request.headers.get('cf-connecting-ip') || 'anon';
  if (env.AUDIT_KV) {
    const key = `form:${ip}`;
    const hits = parseInt(await env.AUDIT_KV.get(key) || '0', 10);
    if (hits >= 5) return json({ error: 'Too many submissions. Please email us directly.' }, 429);
    await env.AUDIT_KV.put(key, String(hits + 1), { expirationTtl: 3600 });
  }

  const to = env.TO_EMAIL || 'hello@svedsolution.com';
  const kind = d.type === 'newsletter' ? 'Newsletter signup' : 'New enquiry';

  const rows = [
    ['Name', d.name], ['Email', email], ['Website', d.website],
    ['Service', d.service], ['Revenue', d.revenue], ['Message', d.message],
    ['Audit score', d.score], ['Source page', d.page]
  ].filter(([, v]) => v).map(([k, v]) =>
    `<tr><td style="padding:6px 12px;color:#666">${esc(k)}</td><td style="padding:6px 12px"><strong>${esc(v)}</strong></td></tr>`
  ).join('');

  if (!env.RESEND_KEY) {
    // Not configured yet — accept the submission rather than showing the user an error.
    console.log('CONTACT (no RESEND_KEY):', JSON.stringify(d));
    return json({ ok: true, note: 'received' });
  }

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      authorization: `Bearer ${env.RESEND_KEY}`,
      'content-type': 'application/json'
    },
    body: JSON.stringify({
      from: 'SVED Solution <noreply@svedsolution.com>',
      to: [to],
      reply_to: email,
      subject: `${kind} — ${esc(d.name || email)}`,
      html: `<h2 style="font-family:sans-serif">${kind}</h2>
             <table style="font-family:sans-serif;font-size:14px;border-collapse:collapse">${rows}</table>`
    })
  });

  if (!res.ok) {
    console.log('Resend error', res.status, await res.text());
    return json({ error: 'Could not send right now. Please email hello@svedsolution.com directly.' }, 502);
  }
  return json({ ok: true });
}
