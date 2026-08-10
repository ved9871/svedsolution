/**
 * POST /api/audit  { url: "https://example.com" }
 *
 * Tier-1 AI visibility audit. Runs 12 eligibility checks against a live URL
 * entirely at the edge — no API keys required, no running cost.
 *
 * Optional bindings (all degrade gracefully if absent):
 *   AUDIT_KV   KV namespace — rate limiting + 24h result cache
 *   PSI_KEY    PageSpeed Insights API key — raises the CWV check quota
 */

const RATE_LIMIT = 3;          // audits per IP
const RATE_WINDOW = 3600;      // per hour
const CACHE_TTL = 86400;       // 24h per domain

const AI_BOTS = [
  'GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'PerplexityBot',
  'ClaudeBot', 'Claude-Web', 'Google-Extended', 'CCBot', 'Applebot-Extended'
];

const TIER1 = [
  'g2.com', 'capterra.com', 'trustpilot.com', 'crunchbase.com',
  'producthunt.com', 'reddit.com', 'quora.com', 'clutch.co',
  'linkedin.com', 'youtube.com', 'github.com', 'wikipedia.org'
];

const json = (obj, status = 200) => new Response(JSON.stringify(obj), {
  status,
  headers: {
    'content-type': 'application/json; charset=utf-8',
    'cache-control': 'no-store',
    'access-control-allow-origin': '*'
  }
});

export async function onRequestOptions() {
  return new Response(null, {
    headers: {
      'access-control-allow-origin': '*',
      'access-control-allow-methods': 'POST, OPTIONS',
      'access-control-allow-headers': 'content-type'
    }
  });
}

export async function onRequestPost({ request, env }) {
  let body;
  try { body = await request.json(); } catch { return json({ error: 'Invalid JSON body.' }, 400); }

  const candidates = candidateUrls(body && body.url);
  if (!candidates.length) {
    return json({ error: 'That does not look like a website address. Try something like example.com' }, 400);
  }

  const ip = request.headers.get('cf-connecting-ip') || 'anon';

  // ---- Rate limit -------------------------------------------------------
  // KV gives exact per-IP counting. Without it we fall back to the edge cache,
  // which is per-colo rather than global but still blunts abuse — so the
  // endpoint is never wide open just because the KV binding was skipped.
  if (env.AUDIT_KV) {
    const key = `rl:${ip}`;
    const hits = parseInt(await env.AUDIT_KV.get(key) || '0', 10);
    if (hits >= RATE_LIMIT) {
      return json({ error: `Rate limit reached (${RATE_LIMIT} audits per hour). Try again shortly, or request the full report.` }, 429);
    }
    await env.AUDIT_KV.put(key, String(hits + 1), { expirationTtl: RATE_WINDOW });
  } else if (await tooManyRecent(ip)) {
    return json({ error: `Rate limit reached (${RATE_LIMIT} audits per hour). Try again shortly, or request the full report.` }, 429);
  }

  // ---- Cache ------------------------------------------------------------
  // Keyed on the visitor's normalised input so example.com and
  // www.example.com share a cached result once they resolve to the same place.
  const cacheKey = `audit:${new URL(candidates[0]).hostname.replace(/^www\./, '')}`;
  if (env.AUDIT_KV) {
    const hit = await env.AUDIT_KV.get(cacheKey);
    if (hit) return json({ ...JSON.parse(hit), cached: true });
  } else {
    const hit = await edgeGet(cacheKey);
    if (hit) return json({ ...hit, cached: true });
  }

  // ---- Resolve ----------------------------------------------------------
  const resolved = await firstReachable(candidates);
  if (!resolved) {
    return json({
      error: `We could not reach that site. We tried ${candidates.length} variations ` +
             `including https, http and the www version. Check the address is public and online.`,
      tried: candidates
    }, 502);
  }

  let result;
  try {
    result = await runAudit(new URL(resolved.url), env, resolved);
  } catch (err) {
    return json({ error: `Could not complete the audit: ${err.message}` }, 502);
  }

  if (env.AUDIT_KV) {
    await env.AUDIT_KV.put(cacheKey, JSON.stringify(result), { expirationTtl: CACHE_TTL });
  } else {
    await edgePut(cacheKey, result, CACHE_TTL);
  }
  return json(result);
}

// ---- Edge-cache fallback (used when no KV binding is configured) ---------

const CACHE_ORIGIN = 'https://audit-cache.svedsolution.com/';

async function edgeGet(key) {
  try {
    const res = await caches.default.match(new Request(CACHE_ORIGIN + encodeURIComponent(key)));
    return res ? await res.json() : null;
  } catch { return null; }
}

async function edgePut(key, value, ttl) {
  try {
    await caches.default.put(
      new Request(CACHE_ORIGIN + encodeURIComponent(key)),
      new Response(JSON.stringify(value), {
        headers: { 'content-type': 'application/json', 'cache-control': `max-age=${ttl}` }
      })
    );
  } catch { /* cache unavailable — proceed uncached */ }
}

async function tooManyRecent(ip) {
  const key = `rl:${ip}`;
  const now = Date.now();
  const seen = (await edgeGet(key)) || { hits: [] };
  const recent = (seen.hits || []).filter(t => now - t < RATE_WINDOW * 1000);
  if (recent.length >= RATE_LIMIT) return true;
  recent.push(now);
  await edgePut(key, { hits: recent }, RATE_WINDOW);
  return false;
}

// ==========================================================================

/**
 * Build the ordered list of URLs worth trying for whatever the visitor typed.
 *
 * People enter "example.com", "www.example.com", "http://example.com" or a deep
 * path, and any single interpretation fails for someone: the apex may not
 * resolve while www does, the site may be http-only, or the pasted path may
 * 404. We try the most likely candidates and audit the first that responds.
 */
function candidateUrls(raw) {
  if (!raw || typeof raw !== 'string') return [];
  let s = raw.trim().replace(/\s+/g, '');
  if (!s) return [];

  // Reject non-http(s) schemes outright (file:, data:, javascript: ...) so they
  // can never be smuggled through by prefixing https://.
  if (/^[a-z][a-z0-9+.\-]*:/i.test(s) && !/^https?:\/\//i.test(s)) return [];

  const explicitScheme = /^https?:\/\//i.test(s) ? s.slice(0, s.indexOf(':')).toLowerCase() : null;
  if (!explicitScheme) s = 'https://' + s;

  let u;
  try { u = new URL(s); } catch { return []; }

  const host = u.hostname.toLowerCase();

  // A hostname must have at least one dot and a plausible TLD, otherwise a
  // typo like "example" turns into a confusing fetch failure instead of a
  // clear validation message.
  if (!/^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)*\.[a-z]{2,24}$/.test(host)) {
    return [];
  }
  if (isPrivateHost(host)) return [];

  const bare = host.replace(/^www\./, '');
  const hosts = host.startsWith('www.') ? [host, bare] : [host, 'www.' + host];
  const schemes = explicitScheme === 'http' ? ['http', 'https'] : ['https', 'http'];
  const path = (u.pathname && u.pathname !== '/') ? u.pathname + u.search : '';

  const out = [];
  const push = v => { if (!out.includes(v)) out.push(v); };

  // A supplied path is tried first, then the origin, so a stale deep link still
  // yields a useful audit of the site rather than a hard failure.
  for (const scheme of schemes) {
    for (const h of hosts) {
      if (path) push(`${scheme}://${h}${path}`);
      push(`${scheme}://${h}/`);
    }
  }
  return out;
}

function isPrivateHost(h) {
  return h === 'localhost' || h.endsWith('.local') || h.endsWith('.internal') ||
    /^(127\.|10\.|192\.168\.|169\.254\.|0\.)/.test(h) ||
    /^172\.(1[6-9]|2\d|3[01])\./.test(h) ||
    /^\[?::1\]?$/.test(h);
}

function normaliseUrl(raw) {
  if (!raw || typeof raw !== 'string') return null;
  let s = raw.trim();
  // Reject any non-http(s) scheme outright (file:, data:, ftp:, javascript: ...)
  // before defaulting, so they can never be smuggled through the https:// prefix.
  if (/^[a-z][a-z0-9+.\-]*:/i.test(s) && !/^https?:\/\//i.test(s)) return null;
  if (!/^https?:\/\//i.test(s)) s = 'https://' + s;
  let u;
  try { u = new URL(s); } catch { return null; }
  if (!/^https?:$/.test(u.protocol)) return null;
  // Block internal ranges — this endpoint is public, do not let it proxy a private network.
  const h = u.hostname.toLowerCase();
  if (h === 'localhost' || h.endsWith('.local') || h.endsWith('.internal') ||
      /^(127\.|10\.|192\.168\.|169\.254\.|0\.)/.test(h) ||
      /^172\.(1[6-9]|2\d|3[01])\./.test(h) ||
      /^\[?::1\]?$/.test(h)) return null;
  return u;
}

async function grab(url, timeoutMs = 10000) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const res = await fetch(url, {
      signal: ctrl.signal,
      redirect: 'follow',
      headers: { 'user-agent': 'SVEDSolutionAuditBot/1.0 (+https://svedsolution.com/ai-visibility-audit)' }
    });
    return {
      ok: res.ok,
      status: res.status,
      type: res.headers.get('content-type') || '',
      text: res.ok ? await res.text() : ''
    };
  } catch (e) {
    return { ok: false, status: 0, type: '', text: '', error: e.message };
  } finally {
    clearTimeout(t);
  }
}

/**
 * Many sites answer /llms.txt and /robots.txt with a 200 that is actually the
 * SPA shell or a styled 404 page. Treating that as "found" produces a false
 * pass, so a plain-text file must actually look like plain text.
 */
function isRealTextFile(res) {
  if (!res.ok || !res.text) return false;
  const head = res.text.slice(0, 1200).toLowerCase();
  if (/<!doctype html|<html[\s>]|<head[\s>]|<body[\s>]|<script[\s>]/.test(head)) return false;
  if (/\bhtml\b/.test(res.type)) return false;
  return true;
}

/**
 * Try each candidate in order and return the first that serves HTML.
 * Sequential rather than parallel so a site is not hit four times at once.
 */
async function firstReachable(candidates) {
  let lastStatus = 0;
  for (const url of candidates) {
    const res = await grab(url, 12000);
    if (res.ok && res.text) {
      return { url, page: res, attempts: candidates.indexOf(url) + 1 };
    }
    if (res.status) lastStatus = res.status;
  }
  return null;
}

async function runAudit(u, env, resolved) {
  // The page body is already in hand from the reachability probe, so this is
  // one fetch rather than two.
  const page = resolved && resolved.page ? resolved.page : await grab(u.href);
  const [robots, llms] = await Promise.all([
    grab(new URL('/robots.txt', u.origin).href, 6000),
    grab(new URL('/llms.txt', u.origin).href, 6000)
  ]);

  if (!page.ok) throw new Error(`returned HTTP ${page.status || 'no response'}`);

  const html = page.text;
  const ld = extractJsonLd(html);
  const types = ldTypes(ld);
  const checks = [];

  // 01 Organization schema
  const orgTypes = ['Organization', 'ProfessionalService', 'LocalBusiness', 'Corporation'];
  const hasOrg = types.some(t => orgTypes.includes(t));
  const sameAs = collectSameAs(ld);
  checks.push(check('Organization schema (JSON-LD)', hasOrg ? (sameAs.length >= 3 ? 'ok' : 'warn') : 'bad',
    hasOrg
      ? (sameAs.length >= 3
        ? `Present with ${sameAs.length} sameAs links. This is how models resolve you as an entity.`
        : `Present but only ${sameAs.length} sameAs link(s). Add every social and third-party profile — sameAs is the entity-resolution signal.`)
      : 'Missing. Without Organization schema you are a website, not a resolvable entity. This is the single highest-impact fix.'));

  // 02 Person / author schema
  const hasPerson = types.includes('Person');
  checks.push(check('Person / author schema', hasPerson ? 'ok' : 'bad',
    hasPerson
      ? 'Present. Named authorship is a primary E-E-A-T and AI-trust signal.'
      : 'Missing. Anonymous content is systematically discounted by AI systems. Add Person schema linked to real profiles.'));

  // 03 FAQPage schema
  const hasFaq = types.includes('FAQPage') || types.includes('QAPage');
  checks.push(check('FAQPage schema', hasFaq ? 'ok' : 'warn',
    hasFaq
      ? 'Present. Q&A markup is the highest-frequency format cited by generative engines.'
      : 'Not found on this page. FAQ blocks are the most-quoted structure in AI answers — add them to every service page.'));

  // 04 llms.txt
  const llmsReal = isRealTextFile(llms);
  checks.push(check('llms.txt file', llmsReal ? 'ok' : 'bad',
    llmsReal
      ? `Found (${llms.text.length} bytes). You are declaring your content to LLM crawlers explicitly.`
      : llms.ok
        ? 'Your server returns HTML at /llms.txt instead of a plain-text file — a catch-all route or soft 404. Crawlers will discard it. Serve a real text file.'
        : 'Not found at /llms.txt. Emerging standard for declaring content and structure to LLM crawlers. Cheap to add, removes ambiguity.'));

  // 05 AI crawler access
  const robotsReal = isRealTextFile(robots);
  let botState = 'warn', botMsg;
  if (!robotsReal) {
    botState = robots.ok ? 'bad' : 'warn';
    botMsg = robots.ok
      ? 'Your server returns HTML at /robots.txt rather than a plain-text file. Crawlers cannot parse this, so every directive you think you have is being ignored. Fix this first.'
      : 'No robots.txt found. Crawlers default to allowed, but you are not declaring intent. Add one.';
  } else {
    const txt = robots.text;
    const named = AI_BOTS.filter(b => new RegExp(`user-agent:\\s*${b}`, 'i').test(txt));
    const blocked = named.filter(b => isBlocked(txt, b));
    if (blocked.length) {
      botState = 'bad';
      botMsg = `${blocked.join(', ')} explicitly DISALLOWED. These crawlers cannot cite content they cannot read. If brand discovery matters to you, this is self-harm.`;
    } else if (named.length >= 4) {
      botState = 'ok';
      botMsg = `${named.length} AI crawlers explicitly declared and allowed: ${named.join(', ')}.`;
    } else {
      botMsg = `Only ${named.length} of ${AI_BOTS.length} AI crawlers declared. Undeclared bots default to allowed, but explicit rules remove ambiguity.`;
    }
  }
  checks.push(check('AI crawler access (robots.txt)', botState, botMsg));

  // 06 Answer-first structure
  const firstPara = firstParagraph(html);
  const wc = firstPara.split(/\s+/).filter(Boolean).length;
  const storyOpen = /^(in (today|this)|we all know|imagine|picture this|it was|once upon|have you ever|let'?s face it|as a|in the world of)/i.test(firstPara);
  const answerState = (wc >= 15 && wc <= 120 && !storyOpen) ? 'ok' : (storyOpen ? 'bad' : 'warn');
  checks.push(check('Answer-first content structure', answerState,
    answerState === 'ok'
      ? `Opens with a ${wc}-word direct statement. This is the passage most likely to be extracted and quoted.`
      : storyOpen
        ? 'Opens with a narrative hook. Models retrieve answers, not story intros — lead with the direct answer instead.'
        : `First paragraph is ${wc} words. Aim for a 30-80 word direct answer in the first 100 words of the page.`));

  // 07 Freshness
  const mod = findModified(html, ld);
  let freshState = 'bad', freshMsg = 'No dateModified, article:modified_time or visible update date found. Retrieval strongly favours pages with recent, verifiable timestamps.';
  if (mod) {
    const days = Math.round((Date.now() - mod.getTime()) / 86400000);
    freshState = days <= 90 ? 'ok' : days <= 365 ? 'warn' : 'bad';
    freshMsg = `Last modified ${mod.toISOString().slice(0, 10)} (${days} days ago). ` +
      (days <= 90 ? 'Within the freshness window.'
        : days <= 365 ? 'Ageing. Run a refresh pass — update stats, add FAQs, rebuild internal links.'
          : 'Stale. Stagnant pages lose retrieval priority to maintained competitors.');
  }
  checks.push(check('Content freshness signals', freshState, freshMsg));

  // 08 Heading hierarchy
  const h1 = (html.match(/<h1[\s>]/gi) || []).length;
  const levels = [...html.matchAll(/<h([1-6])[\s>]/gi)].map(m => +m[1]);
  let skipped = false;
  for (let i = 1; i < levels.length; i++) if (levels[i] - levels[i - 1] > 1) { skipped = true; break; }
  const hState = (h1 === 1 && !skipped) ? 'ok' : (h1 === 0 || h1 > 1) ? 'bad' : 'warn';
  checks.push(check('Heading hierarchy (H1-H3)', hState,
    h1 === 0 ? 'No H1 found. Models use heading structure to chunk and attribute passages.'
      : h1 > 1 ? `${h1} H1 tags found. Use exactly one — multiple H1s make the page topic ambiguous.`
        : skipped ? 'Single H1, but heading levels are skipped. Clean nesting improves passage extraction.'
          : `Clean: one H1 across ${levels.length} headings, no skipped levels.`));

  // 09 Citation-ready formats
  const tables = (html.match(/<table[\s>]/gi) || []).length;
  const lists = (html.match(/<(ul|ol)[\s>]/gi) || []).length;
  const fState = (tables >= 1 && lists >= 2) ? 'ok' : (tables + lists >= 2) ? 'warn' : 'bad';
  checks.push(check('Citation-ready formats', fState,
    `${tables} table(s), ${lists} list(s) detected. ` +
    (fState === 'ok' ? 'Good density of extractable structures.'
      : 'Models preferentially quote tables, comparison matrices and step frameworks over prose. Add them.')));

  // 10 Core Web Vitals
  checks.push(await cwvCheck(u.href, env));

  // 11 Entity consistency
  const ent = entityConsistency(html, ld);
  checks.push(check('Entity consistency (brand naming)', ent.state, ent.msg));

  // 12 Tier-1 citation footprint
  const found = TIER1.filter(d => sameAs.some(s => s.includes(d)) || html.includes(d));
  const t1State = found.length >= 6 ? 'ok' : found.length >= 3 ? 'warn' : 'bad';
  checks.push(check('Tier-1 citation footprint', t1State,
    `${found.length} of ${TIER1.length} Tier-1 sources referenced${found.length ? ': ' + found.join(', ') : ''}. ` +
    'AI weights independent third-party validation above your own site. This is where most brands fail — and it is measured here by declared links only, so the full report verifies actual presence.'));

  const ok = checks.filter(c => c.state === 'ok').length;
  const warn = checks.filter(c => c.state === 'warn').length;
  const bad = checks.filter(c => c.state === 'bad').length;
  const score = Math.round((ok * 100 + warn * 50) / checks.length);

  checks.sort((a, b) => ({ bad: 0, warn: 1, ok: 2 })[a.state] - ({ bad: 0, warn: 1, ok: 2 })[b.state]);

  return {
    url: u.href,
    host: u.hostname,
    // Surfaced so the visitor can see which variation was actually audited
    // when what they typed was not what resolved.
    auditedUrl: u.href,
    score,
    verdict: score >= 75 ? 'Strong AI visibility foundation'
      : score >= 50 ? 'Partially eligible for AI citation'
        : score >= 30 ? 'Currently invisible to most AI search engines'
          : 'Not eligible for AI citation',
    summary: { ok, warn, bad, total: checks.length },
    checks,
    generated: new Date().toISOString()
  };
}

// ---- helpers -------------------------------------------------------------

const check = (label, state, detail) => ({ label, state, detail });

function isBlocked(robotsTxt, bot) {
  const re = new RegExp(`user-agent:\\s*${bot}\\s*([\\s\\S]*?)(?=\\nuser-agent:|$)`, 'i');
  const m = robotsTxt.match(re);
  return !!(m && /disallow:\s*\/\s*$/im.test(m[1]));
}

function extractJsonLd(html) {
  const out = [];
  const re = /<script[^>]+application\/ld\+json[^>]*>([\s\S]*?)<\/script>/gi;
  let m;
  while ((m = re.exec(html))) {
    try {
      const parsed = JSON.parse(m[1].trim());
      Array.isArray(parsed) ? out.push(...parsed) : out.push(parsed);
    } catch { /* malformed block, skip */ }
  }
  return out;
}

function ldTypes(ld) {
  const t = [];
  const walk = n => {
    if (!n || typeof n !== 'object') return;
    if (Array.isArray(n)) return n.forEach(walk);
    if (n['@type']) [].concat(n['@type']).forEach(x => t.push(x));
    if (n['@graph']) walk(n['@graph']);
    Object.values(n).forEach(v => { if (v && typeof v === 'object') walk(v); });
  };
  ld.forEach(walk);
  return [...new Set(t)];
}

function collectSameAs(ld) {
  const out = [];
  const walk = n => {
    if (!n || typeof n !== 'object') return;
    if (Array.isArray(n)) return n.forEach(walk);
    if (n.sameAs) [].concat(n.sameAs).forEach(s => typeof s === 'string' && out.push(s));
    Object.values(n).forEach(v => { if (v && typeof v === 'object') walk(v); });
  };
  ld.forEach(walk);
  return [...new Set(out)];
}

function firstParagraph(html) {
  const body = html.replace(/<(script|style|nav|header|footer)[\s\S]*?<\/\1>/gi, '');
  const paras = [...body.matchAll(/<p[^>]*>([\s\S]*?)<\/p>/gi)]
    .map(m => m[1].replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/\s+/g, ' ').trim())
    .filter(t => t.split(/\s+/).length >= 8);
  return paras[0] || '';
}

function findModified(html, ld) {
  let raw = null;
  const walk = n => {
    if (raw || !n || typeof n !== 'object') return;
    if (Array.isArray(n)) return n.forEach(walk);
    if (n.dateModified) { raw = n.dateModified; return; }
    Object.values(n).forEach(v => { if (v && typeof v === 'object') walk(v); });
  };
  ld.forEach(walk);
  if (!raw) {
    const m = html.match(/<meta[^>]+(?:article:modified_time|og:updated_time)[^>]+content="([^"]+)"/i)
      || html.match(/<time[^>]+datetime="([^"]+)"/i);
    if (m) raw = m[1];
  }
  if (!raw) return null;
  const d = new Date(raw);
  return isNaN(d.getTime()) ? null : d;
}

function entityConsistency(html, ld) {
  const names = new Set();
  const walk = n => {
    if (!n || typeof n !== 'object') return;
    if (Array.isArray(n)) return n.forEach(walk);
    const t = [].concat(n['@type'] || []);
    if (n.name && t.some(x => /Organization|ProfessionalService|LocalBusiness|Corporation|WebSite/.test(x))) {
      names.add(String(n.name).trim());
    }
    Object.values(n).forEach(v => { if (v && typeof v === 'object') walk(v); });
  };
  ld.forEach(walk);

  const og = (html.match(/<meta[^>]+og:site_name[^>]+content="([^"]+)"/i) || [])[1];
  if (og) names.add(og.trim());

  const list = [...names];
  if (!list.length) {
    return { state: 'bad', msg: 'No brand name declared in schema or og:site_name. Models cannot confirm what you are called, which breaks entity resolution before it starts.' };
  }
  const norm = [...new Set(list.map(n => n.toLowerCase().replace(/[^a-z0-9]/g, '')))];
  return norm.length === 1
    ? { state: 'ok', msg: `Brand rendered consistently as "${list[0]}" across schema and metadata.` }
    : { state: 'warn', msg: `Brand rendered ${norm.length} different ways: ${list.map(n => `"${n}"`).join(', ')}. Inconsistent naming breaks the trust loop — pick one exact form and use it everywhere, including third-party profiles.` };
}

async function cwvCheck(url, env) {
  try {
    let api = `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=${encodeURIComponent(url)}&strategy=mobile&category=performance`;
    if (env.PSI_KEY) api += `&key=${env.PSI_KEY}`;
    const res = await grab(api, 28000);
    if (!res.ok) throw new Error('PSI unavailable');
    const data = JSON.parse(res.text);
    const audits = data.lighthouseResult && data.lighthouseResult.audits;
    if (!audits) throw new Error('no lighthouse result');
    const lcp = audits['largest-contentful-paint'];
    const cls = audits['cumulative-layout-shift'];
    const perf = Math.round((data.lighthouseResult.categories.performance.score || 0) * 100);
    const state = perf >= 90 ? 'ok' : perf >= 50 ? 'warn' : 'bad';
    return check('Core Web Vitals (mobile)', state,
      `Performance ${perf}/100. LCP ${lcp && lcp.displayValue || 'n/a'}, CLS ${cls && cls.displayValue || 'n/a'}. ` +
      (state === 'ok' ? 'Passing.' : 'Slow renders reduce crawl depth and weaken every downstream signal.'));
  } catch {
    return check('Core Web Vitals (mobile)', 'warn',
      env.PSI_KEY
        ? 'PageSpeed data was unavailable for this URL just now (the origin may be slow or blocking). Re-run shortly, or we will include it in the full report.'
        : 'Core Web Vitals not measured — the PageSpeed Insights API is rate-limited without a key. Add PSI_KEY in Pages environment variables to enable this check.');
  }
}
