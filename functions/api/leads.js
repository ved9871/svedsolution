/**
 * GET /api/leads            -> JSON list of stored leads
 * GET /api/leads?format=csv -> CSV download
 * GET /api/leads?type=newsletter  -> filter by type (enquiry | newsletter | audit)
 *
 * Auth: send the admin token as `Authorization: Bearer <token>` or `?token=`.
 *
 * Bindings:
 *   LEADS_KV or AUDIT_KV   KV namespace holding the leads
 *   ADMIN_TOKEN            shared secret for the leads dashboard
 */

const COLUMNS = ['received', 'type', 'name', 'email', 'phone', 'website',
  'service', 'revenue', 'score', 'country', 'message', 'page', 'referer', 'id'];

const json = (o, s = 200) => new Response(JSON.stringify(o), {
  status: s,
  headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' }
});

/** Length-safe, non-short-circuiting comparison so timing does not leak the token. */
function safeEqual(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string' || a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

/**
 * RFC 4180 quoting, plus a leading apostrophe on values that spreadsheet apps
 * would otherwise evaluate as a formula (CSV injection).
 */
function csvCell(value) {
  let s = value == null ? '' : String(value);
  if (/^[=+\-@\t\r]/.test(s)) s = "'" + s;
  return '"' + s.replace(/"/g, '""') + '"';
}

export async function onRequestGet({ request, env }) {
  const url = new URL(request.url);
  const kv = env.LEADS_KV || env.AUDIT_KV;

  if (!env.ADMIN_TOKEN) {
    return json({ error: 'ADMIN_TOKEN is not set. Add it under Settings > Variables and Secrets, then redeploy.' }, 503);
  }
  if (!kv) {
    return json({ error: 'No KV namespace bound. Bind LEADS_KV (or AUDIT_KV) to store and read leads.' }, 503);
  }

  const supplied = (request.headers.get('authorization') || '').replace(/^Bearer\s+/i, '')
    || url.searchParams.get('token') || '';
  if (!safeEqual(supplied, env.ADMIN_TOKEN)) {
    return json({ error: 'Unauthorised.' }, 401);
  }

  const wantType = url.searchParams.get('type');
  const limit = Math.min(parseInt(url.searchParams.get('limit') || '1000', 10) || 1000, 5000);

  // Keys are stored with an inverted timestamp prefix, so KV's lexicographic
  // listing already returns newest first.
  const leads = [];
  let cursor;
  do {
    const page = await kv.list({ prefix: 'lead:', limit: 1000, cursor });
    for (const k of page.keys) {
      if (leads.length >= limit) break;
      const raw = await kv.get(k.name);
      if (!raw) continue;
      try {
        const lead = JSON.parse(raw);
        if (!wantType || lead.type === wantType) leads.push(lead);
      } catch { /* skip malformed record */ }
    }
    cursor = page.list_complete ? null : page.cursor;
  } while (cursor && leads.length < limit);

  if (url.searchParams.get('format') === 'csv') {
    const header = COLUMNS.map(csvCell).join(',');
    const rows = leads.map(l => COLUMNS.map(c => csvCell(l[c])).join(','));
    // BOM so Excel opens UTF-8 correctly.
    const body = '﻿' + [header, ...rows].join('\r\n');
    const stamp = new Date().toISOString().slice(0, 10);
    return new Response(body, {
      headers: {
        'content-type': 'text/csv; charset=utf-8',
        'content-disposition': `attachment; filename="sved-leads-${wantType || 'all'}-${stamp}.csv"`,
        'cache-control': 'no-store'
      }
    });
  }

  return json({
    count: leads.length,
    counts: leads.reduce((acc, l) => { acc[l.type] = (acc[l.type] || 0) + 1; return acc; }, {}),
    leads
  });
}

/** DELETE /api/leads?id=lead:...  — remove a single record. */
export async function onRequestDelete({ request, env }) {
  const url = new URL(request.url);
  const kv = env.LEADS_KV || env.AUDIT_KV;
  const supplied = (request.headers.get('authorization') || '').replace(/^Bearer\s+/i, '')
    || url.searchParams.get('token') || '';

  if (!env.ADMIN_TOKEN || !safeEqual(supplied, env.ADMIN_TOKEN)) return json({ error: 'Unauthorised.' }, 401);
  if (!kv) return json({ error: 'No KV namespace bound.' }, 503);

  const id = url.searchParams.get('id');
  if (!id || !id.startsWith('lead:')) return json({ error: 'Provide the full lead key.' }, 400);

  await kv.delete(id);
  return json({ ok: true });
}
