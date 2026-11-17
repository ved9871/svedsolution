/**
 * POST /api/audit  { url: "https://example.com" }
 *
 * AI visibility check. Runs 20 checks in four groups against a live URL
 * entirely at the edge — no API keys required, no running cost.
 *
 * Optional bindings (all degrade gracefully if absent):
 *   AUDIT_KV   KV namespace — rate limiting + 24h result cache
 *   PSI_KEY    PageSpeed Insights API key — raises the CWV check quota
 */

const RATE_LIMIT = 3;          // audits per IP
const RATE_WINDOW = 3600;      // per hour
const CACHE_TTL = 86400;       // 24h per domain

// Crawlers that fetch pages to answer a live question. Blocking these keeps
// a site out of AI answers.
const SEARCH_BOTS = [
  'OAI-SearchBot', 'ChatGPT-User', 'PerplexityBot', 'Perplexity-User',
  'Claude-SearchBot', 'Claude-User'
];

// Crawlers that collect text to train models. Blocking these is a legitimate
// choice and does not remove a site from AI answers, so it is not penalised.
const TRAINING_BOTS = [
  'GPTBot', 'ClaudeBot', 'Google-Extended', 'Applebot-Extended', 'CCBot',
  'Meta-ExternalAgent', 'Amazonbot', 'Bytespider'
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
  const cacheKey = `audit2:${new URL(candidates[0]).hostname.replace(/^www\./, '')}`;
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
      xRobots: res.headers.get('x-robots-tag') || '',
      lastModified: res.headers.get('last-modified') || '',
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

// Checks are grouped by the question a site owner actually asks. Order here is the
// order groups are shown in and the order ties are broken in the fix list.
const GROUPS = [
  ['access', 'Can AI tools reach your site?'],
  ['identity', 'Do they know who you are?'],
  ['content', 'Is your content easy to quote?'],
  ['basics', 'Search basics']
];

async function runAudit(u, env, resolved) {
  // The page body is already in hand from the reachability probe, so this is
  // one fetch rather than two.
  const page = resolved && resolved.page ? resolved.page : await grab(u.href);
  const [robots, llms, sitemap] = await Promise.all([
    grab(new URL('/robots.txt', u.origin).href, 6000),
    grab(new URL('/llms.txt', u.origin).href, 6000),
    grab(new URL('/sitemap.xml', u.origin).href, 6000)
  ]);

  if (!page.ok) throw new Error(`returned HTTP ${page.status || 'no response'}`);

  const html = page.text;
  const ld = extractJsonLd(html);
  const types = ldTypes(ld);
  const sameAs = collectSameAs(ld);
  const checks = [];
  // A passing check needs no advice, so its fix is dropped.
  const add = (group, label, state, detail, fix) =>
    checks.push({ group, label, state, detail, fix: state === 'ok' ? '' : (fix || '') });

  // ======================================================================
  // 1. Can AI tools reach your site?
  // ======================================================================

  // AI crawlers. The ones that fetch pages for live answers matter for being
  // quoted; the training crawlers are a separate, legitimate choice to block.
  const robotsReal = isRealTextFile(robots);
  if (robots.ok && !robotsReal) {
    add('access', 'AI assistants are allowed in', 'bad',
      'The address /robots.txt returns a web page instead of a plain text file, so crawlers ignore whatever rules you meant to set.',
      'Serve a real plain-text robots.txt file at /robots.txt.');
  } else {
    const rules = robotsReal ? parseRobots(robots.text) : [];
    const blockedSearch = SEARCH_BOTS.filter(b => blockedFor(rules, b));
    const blockedTraining = TRAINING_BOTS.filter(b => blockedFor(rules, b));
    if (blockedSearch.length) {
      add('access', 'AI assistants are allowed in', 'bad',
        `Your robots.txt blocks ${blockedSearch.join(', ')}. These are the crawlers that fetch pages when someone asks an AI assistant a question, so a blocked site cannot be quoted or linked in the answer.`,
        'Remove the block on these crawlers in robots.txt, unless staying out of AI answers is a deliberate choice.');
    } else if (blockedTraining.length) {
      add('access', 'AI assistants are allowed in', 'ok',
        `The crawlers that fetch pages for live AI answers are allowed. You block ${blockedTraining.length} crawler(s) used for training AI models (${blockedTraining.join(', ')}), which is a fair choice and does not stop you appearing in answers.`);
    } else {
      add('access', 'AI assistants are allowed in', 'ok',
        robotsReal
          ? 'Your robots.txt does not block any of the AI crawlers we test for.'
          : 'There is no robots.txt file, so every crawler is allowed by default.');
    }
  }

  // Text present without JavaScript. Most AI crawlers do not run scripts.
  const words = visibleWords(html);
  add('access', 'Your text is readable without JavaScript',
    words >= 250 ? 'ok' : words >= 80 ? 'warn' : 'bad',
    words >= 250
      ? `${words} words of text are in the page before any scripts run, so crawlers that do not run JavaScript can still read it.`
      : words >= 80
        ? `Only ${words} words of text are in the page before scripts run. If more of your content loads later, most AI crawlers never see it.`
        : `Almost no text (${words} words) is in the page until JavaScript runs. Most AI crawlers do not run JavaScript, so they see a nearly empty page.`,
    'Send the main content from the server (server-side rendering or pre-rendering) so the text is in the page itself.');

  // Indexing and snippet rules, from the meta tags and the response header.
  const robotsMeta = [metaContent(html, 'robots'), metaContent(html, 'googlebot'), page.xRobots]
    .filter(Boolean).join(',').toLowerCase();
  if (/\bnoindex\b/.test(robotsMeta)) {
    add('access', 'Nothing stops the page being indexed or quoted', 'bad',
      'This page carries a "noindex" instruction, which tells search engines to leave it out. A page that is not indexed cannot appear in Google or in AI answers.',
      'Remove the noindex instruction from the page (meta robots tag or X-Robots-Tag header) if you want it found.');
  } else if (/\bnosnippet\b|max-snippet\s*:\s*0\b/.test(robotsMeta)) {
    add('access', 'Nothing stops the page being indexed or quoted', 'bad',
      'This page forbids snippets ("nosnippet" or "max-snippet:0"). Google will not quote it in search results or in AI Overviews.',
      'Remove the nosnippet or max-snippet:0 instruction so your text can be quoted.');
  } else {
    add('access', 'Nothing stops the page being indexed or quoted', 'ok',
      'No instruction on this page stops it being indexed or quoted.');
  }

  // Sitemap, either listed in robots.txt or sitting at the usual address.
  const sitemapListed = robotsReal && /^\s*sitemap:\s*\S+/im.test(robots.text);
  const sitemapFile = sitemap.ok && /<(urlset|sitemapindex)\b/i.test(sitemap.text.slice(0, 3000));
  add('access', 'A sitemap lists your pages',
    (sitemapListed || sitemapFile) ? 'ok' : 'warn',
    (sitemapListed || sitemapFile)
      ? `Sitemap found${sitemapListed ? ' and listed in robots.txt' : ' at /sitemap.xml'}. Crawlers can discover every page you want found.`
      : 'No sitemap found at /sitemap.xml or listed in robots.txt. Crawlers have to find your pages by following links, and can miss some.',
    'Publish an XML sitemap and add a "Sitemap:" line for it in robots.txt.');

  // llms.txt. Optional, and scored gently because no AI company has confirmed using it.
  const llmsReal = isRealTextFile(llms);
  add('access', 'A guide file for AI tools (llms.txt)',
    llmsReal ? 'ok' : 'warn',
    llmsReal
      ? 'An llms.txt file is in place. It gives AI tools a plain-text summary of your site and its key pages.'
      : llms.ok
        ? 'The address /llms.txt returns a web page instead of a plain text file, so it will be ignored.'
        : 'There is no llms.txt file. It is an optional plain-text summary of your site for AI tools. It is quick to add, though no AI company has confirmed relying on it yet.',
    'Add a short plain-text file at /llms.txt that describes your business and links to your main pages.');

  // Speed on phones.
  const speed = await speedCheck(u.href, env);
  // When Google returns no reading the speed is unknown, not slow, so no fix is
  // offered and it stays out of the "fix these first" list.
  add('access', 'The page loads quickly on a phone', speed.state, speed.detail,
    speed.unknown ? '' : 'Shrink large images, cut unused scripts and fix layout shifts. Slow pages get crawled less often and lose visitors.');

  // ======================================================================
  // 2. Do they know who you are?
  // ======================================================================

  const orgTypes = ['Organization', 'ProfessionalService', 'LocalBusiness', 'Corporation', 'OnlineStore', 'OnlineBusiness'];
  const hasOrg = types.some(t => orgTypes.includes(t));
  add('identity', 'Your business is described for machines',
    hasOrg ? (sameAs.length >= 3 ? 'ok' : 'warn') : 'bad',
    hasOrg
      ? (sameAs.length >= 3
        ? `The page describes your business in a machine-readable way and links to ${sameAs.length} of your profiles elsewhere. That is how AI tools confirm who you are.`
        : `The page describes your business in a machine-readable way but links to only ${sameAs.length} of your profiles elsewhere. More links make it easier to confirm who you are.`)
      : 'The page does not describe your business in a machine-readable way (this is called Organization schema). AI tools have to guess who you are from the text.',
    hasOrg
      ? 'Add links to your social, review and directory profiles in the "sameAs" field of your Organization schema.'
      : 'Add Organization schema with your name, logo, contact details and links to your profiles on other sites.');

  const hasPerson = types.includes('Person');
  add('identity', 'A real person is named', hasPerson ? 'ok' : 'warn',
    hasPerson
      ? 'A named person is attached to this page. Content with a real, named author is trusted more than anonymous content.'
      : 'No named person is attached to this page. Content with a real, named author is trusted more than anonymous content.',
    'Add author details (Person schema) with a link to a real profile such as LinkedIn.');

  const brand = brandConsistency(html, ld);
  add('identity', 'Your name is written the same way everywhere', brand.state, brand.detail,
    'Pick one exact spelling of your business name and use it in your page code, titles and profiles.');

  const found = TIER1.filter(d => sameAs.some(s => s.includes(d)) || html.includes(d));
  add('identity', 'You are on sites AI tools already trust',
    found.length >= 6 ? 'ok' : found.length >= 3 ? 'warn' : 'bad',
    `This page links to ${found.length} of ${TIER1.length} well-known sites${found.length ? ' (' + found.join(', ') + ')' : ''}. ` +
    'AI tools lean on what independent sites say about you more than on your own website. We can only see the links on this page here, not whether the profiles are complete.',
    'Create or claim profiles on the review, directory and social sites that fit your business, then link to them from your site.');

  // ======================================================================
  // 3. Is your content easy to quote?
  // ======================================================================

  const firstPara = firstParagraph(html);
  const wc = firstPara.split(/\s+/).filter(Boolean).length;
  const storyOpen = /^(in (today|this)|we all know|imagine|picture this|it was|once upon|have you ever|let'?s face it|as a|in the world of)/i.test(firstPara);
  const answerState = (wc >= 15 && wc <= 120 && !storyOpen) ? 'ok' : (storyOpen ? 'bad' : 'warn');
  add('content', 'The page gets to the point', answerState,
    answerState === 'ok'
      ? `The page opens with a clear ${wc}-word statement. The opening is the part most likely to be quoted.`
      : storyOpen
        ? 'The page opens with a scene-setting introduction. AI tools quote direct answers, not warm-ups.'
        : wc
          ? `The first paragraph is ${wc} words. An opening of roughly 30 to 80 words that says plainly what you do works best.`
          : 'We could not find a proper opening paragraph on this page.',
    'Start the page with a short, direct statement of what you offer and for whom.');

  const heads = [...html.matchAll(/<h([23])\b[^>]*>([\s\S]*?)<\/h\1>/gi)]
    .map(m => m[2].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim());
  const questions = heads.filter(h => /\?\s*$/.test(h) ||
    /^(who|what|when|where|why|how|can|does|do|is|are|should|which)\b/i.test(h)).length;
  add('content', 'Headings ask the questions people ask',
    questions >= 2 ? 'ok' : 'warn',
    questions >= 2
      ? `${questions} of your headings are written as questions. They match the way people ask AI tools for help.`
      : `${questions ? 'Only one heading is' : 'None of your headings are'} written as a question. People ask AI tools questions, and pages that repeat the question and then answer it are easier to match.`,
    'Rewrite a few headings as the questions your customers ask, and answer each one directly underneath.');

  const hasFaq = types.includes('FAQPage') || types.includes('QAPage');
  add('content', 'Questions and answers are marked up', hasFaq ? 'ok' : 'warn',
    hasFaq
      ? 'The page marks up its questions and answers (FAQ schema), which makes them easy to lift into an answer.'
      : 'The page has no marked-up questions and answers (FAQ schema).',
    'Add a short FAQ section to your key pages and mark it up with FAQ schema.');

  const tables = (html.match(/<table[\s>]/gi) || []).length;
  const lists = (html.match(/<(ul|ol)[\s>]/gi) || []).length;
  const formatState = (tables >= 1 && lists >= 2) ? 'ok' : (tables + lists >= 2) ? 'warn' : 'bad';
  add('content', 'Facts are set out in lists and tables', formatState,
    `We found ${tables} table(s) and ${lists} list(s). ` +
    (formatState === 'ok' ? 'Facts set out this way are easy to quote.'
      : 'AI tools quote lists, tables and step-by-step instructions far more readily than long paragraphs.'),
    'Turn comparisons into tables and processes into numbered steps.');

  const h1 = (html.match(/<h1[\s>]/gi) || []).length;
  const levels = [...html.matchAll(/<h([1-6])[\s>]/gi)].map(m => +m[1]);
  let skipped = false;
  for (let i = 1; i < levels.length; i++) if (levels[i] - levels[i - 1] > 1) { skipped = true; break; }
  add('content', 'Headings are in a sensible order',
    (h1 === 1 && !skipped) ? 'ok' : (h1 === 0 || h1 > 1) ? 'bad' : 'warn',
    h1 === 0 ? 'The page has no main heading. Headings are how machines work out what each part of a page is about.'
      : h1 > 1 ? `The page has ${h1} main headings. There should be exactly one, so the page's subject is clear.`
        : skipped ? 'There is one main heading, but some heading levels are skipped, which makes the page harder to break into sections.'
          : `One main heading and ${levels.length} headings in a clean order.`,
    'Use one main heading (H1), then H2 and H3 in order without skipping levels.');

  const mod = findModified(html, ld) || headerDate(page.lastModified);
  if (mod) {
    const days = Math.max(0, Math.round((Date.now() - mod.getTime()) / 86400000));
    add('content', 'The page shows it is kept up to date',
      days <= 90 ? 'ok' : days <= 365 ? 'warn' : 'bad',
      `Last updated ${mod.toISOString().slice(0, 10)}, ${days} days ago. ` +
      (days <= 90 ? 'Recently updated pages are favoured.'
        : days <= 365 ? 'It is starting to age.'
          : 'Pages that have not been touched in over a year lose out to ones that are maintained.'),
      'Review the page, update anything out of date and show the date it was last updated.');
  } else {
    add('content', 'The page shows it is kept up to date', 'bad',
      'We could not find a date showing when this page was last updated. AI tools and search engines favour pages they can see are maintained.',
      'Show a "last updated" date on the page and include it in the page code (dateModified).');
  }

  // ======================================================================
  // 4. Search basics
  // ======================================================================

  const title = decode(((html.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1] || '').replace(/\s+/g, ' ').trim());
  const desc = metaContent(html, 'description') || '';
  const titleOk = title.length >= 10 && title.length <= 65;
  const descOk = desc.length >= 50 && desc.length <= 170;
  add('basics', 'Page title and description',
    (!title || !desc) ? 'bad' : (titleOk && descOk) ? 'ok' : 'warn',
    !title ? 'The page has no title. The title is the headline shown in search results.'
      : !desc ? `The title is ${title.length} characters, but there is no description for search results to show under it.`
        : `Title ${title.length} characters, description ${desc.length} characters. ` +
          ((titleOk && descOk) ? 'Both are a good length.'
            : 'Aim for a title under 65 characters and a description of 50 to 170, or they get cut off or rewritten.'),
    'Write a clear title under 65 characters and a one or two sentence description of the page.');

  const canonTag = (html.match(/<link\b[^>]*rel\s*=\s*["']canonical["'][^>]*>/i) || [])[0];
  const canonHref = canonTag && (canonTag.match(/href\s*=\s*["']([^"']+)["']/i) || [])[1];
  let canonState = 'warn';
  let canonDetail = 'The page does not say which address is its official one (a canonical tag). If the same page is reachable at several addresses, search engines may split its value between them.';
  if (canonHref) {
    let sameSite = false;
    try {
      sameSite = new URL(canonHref, u.href).hostname.replace(/^www\./, '') === u.hostname.replace(/^www\./, '');
    } catch { /* unparseable address counts as pointing elsewhere */ }
    canonState = sameSite ? 'ok' : 'bad';
    canonDetail = sameSite
      ? 'The page names its own official address, so duplicates do not compete with it.'
      : 'The page says its official address is on a different website. Search engines will credit that other site instead of this page.';
  }
  add('basics', 'The page names its official address', canonState, canonDetail,
    'Add a canonical tag that points to the one address you want this page known by.');

  const secure = u.protocol === 'https:';
  const viewport = metaContent(html, 'viewport');
  add('basics', 'Secure and set up for phones',
    (secure && viewport) ? 'ok' : 'bad',
    (secure && viewport) ? 'The page is served securely (HTTPS) and is set up to fit phone screens.'
      : !secure ? 'The page is not served securely (it loads over HTTP, not HTTPS). Browsers warn visitors about this.'
        : 'The page is not set up to fit phone screens (the viewport setting is missing).',
    !secure ? 'Install an SSL certificate and redirect all visitors to the HTTPS address.'
      : 'Add a viewport meta tag so the page scales to phone screens.');

  const preview = ['og:title', 'og:description', 'og:image'].filter(k => metaContent(html, k));
  add('basics', 'Links to your page show a proper preview',
    preview.length === 3 ? 'ok' : preview.length ? 'warn' : 'bad',
    preview.length === 3
      ? 'When your page is shared, it shows a title, a description and an image.'
      : `${preview.length} of 3 preview details are set (title, description, image). Without them, shared links look bare.`,
    'Add Open Graph tags for the title, description and image.');

  // ---- Scoring -----------------------------------------------------------
  const points = c => c.state === 'ok' ? 100 : c.state === 'warn' ? 50 : 0;
  const tally = list => ({
    score: Math.round(list.reduce((t, c) => t + points(c), 0) / list.length),
    ok: list.filter(c => c.state === 'ok').length,
    warn: list.filter(c => c.state === 'warn').length,
    bad: list.filter(c => c.state === 'bad').length
  });
  const order = GROUPS.map(g => g[0]);
  const rank = { bad: 0, warn: 1, ok: 2 };
  const groups = GROUPS.map(([id, name]) => ({ id, name, ...tally(checks.filter(c => c.group === id)) }));
  const total = tally(checks);

  const topFixes = checks
    .filter(c => c.state !== 'ok' && c.fix)
    .sort((a, b) => rank[a.state] - rank[b.state] || order.indexOf(a.group) - order.indexOf(b.group))
    .slice(0, 3)
    .map(c => ({ label: c.label, fix: c.fix }));

  checks.sort((a, b) => order.indexOf(a.group) - order.indexOf(b.group) || rank[a.state] - rank[b.state]);

  return {
    version: 2,
    url: u.href,
    host: u.hostname,
    // Surfaced so the visitor can see which variation was actually audited
    // when what they typed was not what resolved.
    auditedUrl: u.href,
    score: total.score,
    verdict: total.score >= 80 ? 'AI tools can read and understand your site well'
      : total.score >= 60 ? 'A solid base, with a few gaps to close'
        : total.score >= 40 ? 'AI tools can only partly read or trust your site'
          : 'AI tools will struggle to find or trust your site',
    summary: { ok: total.ok, warn: total.warn, bad: total.bad, total: checks.length },
    groups,
    topFixes,
    checks,
    generated: new Date().toISOString()
  };
}

// ---- helpers -------------------------------------------------------------

/** Minimal entity decoding for text lifted out of attributes and titles. */
function decode(s) {
  return String(s || '')
    .replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#0?39;|&apos;/g, "'")
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&nbsp;/g, ' ');
}

/** Content of a <meta name|property="key"> tag, or null when the tag is absent. */
function metaContent(html, key) {
  const want = key.toLowerCase();
  for (const tag of (html.match(/<meta\b[^>]*>/gi) || [])) {
    const k = (tag.match(/\b(?:name|property)\s*=\s*["']([^"']+)["']/i) || [])[1];
    if (!k || k.toLowerCase() !== want) continue;
    const c = tag.match(/\bcontent\s*=\s*"([^"]*)"/i) || tag.match(/\bcontent\s*=\s*'([^']*)'/i);
    return c ? decode(c[1].trim()) : '';
  }
  return null;
}

/** Words of visible text present in the raw HTML, before any script has run. */
function visibleWords(html) {
  const text = html
    .replace(/<(script|style|noscript|svg|template)\b[\s\S]*?<\/\1>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&[a-z#0-9]+;/gi, ' ');
  return text.split(/\s+/).filter(w => /[a-z0-9]/i.test(w)).length;
}

function headerDate(value) {
  if (!value) return null;
  const d = new Date(value);
  return isNaN(d.getTime()) ? null : d;
}

/**
 * Parse robots.txt into groups of { agents, rules }. Consecutive User-agent
 * lines share the rules that follow them, which is how the format works and
 * what a per-bot regular expression gets wrong.
 */
function parseRobots(txt) {
  const groups = [];
  let current = null;
  let lastWasAgent = false;
  for (const rawLine of txt.split(/\r?\n/)) {
    const line = rawLine.replace(/#.*$/, '').trim();
    const colon = line.indexOf(':');
    if (!line || colon === -1) continue;
    const field = line.slice(0, colon).trim().toLowerCase();
    const value = line.slice(colon + 1).trim();
    if (field === 'user-agent') {
      if (!lastWasAgent) { current = { agents: [], rules: [] }; groups.push(current); }
      current.agents.push(value.toLowerCase());
      lastWasAgent = true;
    } else {
      lastWasAgent = false;
      if (current && (field === 'allow' || field === 'disallow')) current.rules.push({ type: field, path: value });
    }
  }
  return groups;
}

/**
 * Is this crawler shut out of the whole site? A crawler follows the group that
 * names it, and only falls back to the "*" group when no group does.
 */
function blockedFor(groups, bot) {
  const name = bot.toLowerCase();
  const own = groups.filter(g => g.agents.includes(name));
  const rules = (own.length ? own : groups.filter(g => g.agents.includes('*'))).flatMap(g => g.rules);
  const blocksRoot = rules.some(r => r.type === 'disallow' && r.path === '/');
  const allowsRoot = rules.some(r => r.type === 'allow' && (r.path === '/' || r.path === '/*'));
  return blocksRoot && !allowsRoot;
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

function brandConsistency(html, ld) {
  const names = new Set();
  const isBusiness = n => [].concat(n['@type'] || [])
    .some(x => /Organization|ProfessionalService|LocalBusiness|Corporation|WebSite|OnlineStore|OnlineBusiness/.test(x));
  // Only the page's own top-level business counts as "your name". Organisations
  // nested inside it (a parent company, a publisher, a sister brand) are other
  // businesses, and counting them reported a spelling mismatch that was not one.
  const top = ld.flatMap(n => (n && Array.isArray(n['@graph'])) ? n['@graph'] : [n]);
  for (const n of top) {
    if (n && typeof n === 'object' && n.name && isBusiness(n)) names.add(String(n.name).trim());
  }

  const og = metaContent(html, 'og:site_name');
  if (og) names.add(og);

  const list = [...names];
  if (!list.length) {
    return { state: 'bad', detail: 'The page code does not state your business name anywhere a machine would look for it, so AI tools cannot confirm what you are called.' };
  }
  const distinct = [...new Set(list.map(n => n.toLowerCase().replace(/[^a-z0-9]/g, '')))];
  return distinct.length === 1
    ? { state: 'ok', detail: `Your name appears as "${list[0]}" wherever the page code states it.` }
    : { state: 'warn', detail: `Your name is written ${distinct.length} different ways in the page code: ${list.map(n => `"${n}"`).join(', ')}. Mixed spellings make it harder to be sure they are the same business.` };
}

async function speedCheck(url, env) {
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
    return {
      state: perf >= 90 ? 'ok' : perf >= 50 ? 'warn' : 'bad',
      detail: `Google scores this page ${perf} out of 100 for speed on a phone. ` +
        `Main content appears after ${lcp && lcp.displayValue || 'an unknown time'}; layout shift is ${cls && cls.displayValue || 'unknown'}.`
    };
  } catch {
    return {
      state: 'warn',
      unknown: true,
      detail: 'We could not get a speed reading from Google for this page just now. Run the check again in a few minutes.'
    };
  }
}
