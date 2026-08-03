# svedsolution.com — WordPress Setup Guide

**Stack decided:** Kadence + Kadence Blocks Pro · Rank Math Pro · Tier-1 audit tool · anonymised proof
**Status of domain:** `svedsolution.com` currently has **no DNS records** — it is either unregistered or unconfigured. Step 1 is yours.

---

## Phase 0 — Before anything else (yours, ~30 min)

| # | Action | Where | Notes |
|---|---|---|---|
| 0.1 | Register or confirm `svedsolution.com` | Namecheap / Cloudflare Registrar / Porkbun | Cloudflare Registrar sells at cost, no markup. ~$10/yr. |
| 0.2 | Buy hosting | See table below | |
| 0.3 | Point DNS | Registrar → host nameservers | Propagation 15 min–4 hrs |
| 0.4 | Email — using `svedsolution@gmail.com` per your instruction | Gmail | **Free upgrade available:** Cloudflare Email Routing forwards `hello@svedsolution.com` → your Gmail inbox at zero cost. You keep Gmail; the site shows a branded address. See note below. |

> **On the Gmail address.** It is wired everywhere as requested and it works. Be aware of the trade-off: a `@gmail.com` address on an agency site measurably reduces enterprise trust, and it cannot be used for cold outbound (Gmail's sending limits and reputation rules will throttle you). **Cloudflare Email Routing is free** and takes five minutes — it forwards `hello@svedsolution.com` into the same Gmail inbox you already use, with no migration and no monthly fee. Say the word and I'll swap the display address; nothing else changes.

> **NAP inconsistency found on web3technetwork.com.** Three issues worth fixing on that site, because inconsistent business data is exactly the entity-resolution problem you sell against:
> 1. The **USA phone number is listed as `+971 56 653 9682`** — a UAE number. Either it is a typo or the US office has no local line.
> 2. The **WhatsApp number (`+971 52 689 0270`) differs from the listed UAE phone (`+971 56 653 9682`)**. Two different UAE numbers presented as one contact path confuses both humans and entity extraction.
> 3. The **US address has no street line** — just "Oswego, New York 13126", which will not validate as a `PostalAddress` or support a Google Business Profile.
>
> I have carried the data across as-is rather than inventing corrections. Tell me the right numbers and I'll update both sites.

### Hosting recommendation

| Host | Price | Why |
|---|---|---|
| **Rocket.net** *(top pick)* | ~$25/mo | Cloudflare Enterprise built in, genuinely fast TTFB. An SEO agency's own site failing Core Web Vitals is a credibility problem. |
| **Cloudways** (Vultr HF) | ~$14/mo | Best price/performance. More knobs, slightly more admin. |
| **Hostinger** (Cloud) | ~$8/mo | Budget-first. Fine to launch on, plan to migrate at scale. |

Avoid shared cPanel hosts (Bluehost, GoDaddy, HostGator). Slow TTFB, and you will be selling technical SEO.

---

## Phase 1 — WordPress install (15 min)

1. Install WordPress via your host's one-click installer.
2. **Settings → General** — Site Title `SVED Solution`, Tagline `AI Visibility & 360° SEO Agency`.
3. **Settings → Permalinks → Post name** (`/%postname%/`). Do this *before* publishing anything.
4. **Settings → Reading** — uncheck "Discourage search engines". *(Check that it is unchecked. This single box has killed more launches than any other setting.)*
5. **Settings → Discussion** — disable comments sitewide unless you plan to moderate them.
6. Delete: Hello Dolly, Akismet (unless using), the "Hello world!" post, the sample page.
7. Force HTTPS — enable your host's free Let's Encrypt SSL, then confirm both `http://` and `www` redirect to `https://svedsolution.com`.

---

## Phase 2 — Theme (20 min)

### Install
1. **Appearance → Themes → Add New** → search `Kadence` → Install → Activate.
2. Buy **Kadence Pro bundle** (~$130/yr — includes Kadence Blocks Pro, Kadence Pro theme add-on). Upload both plugin ZIPs under **Plugins → Add New → Upload**.
3. Skip the starter templates. Our build supplies its own layouts — importing a starter template will fight them.

### Why Kadence over the alternatives

| Option | Verdict |
|---|---|
| **Kadence** ✅ | Block-native, fast, and *you* can edit it later without a developer. Best balance for an agency that will iterate weekly. |
| GeneratePress | Marginally lighter output, less visual editing. Choose if you want absolute CWV purity. |
| Bricks | Best-looking ceiling, cleanest markup, hardest to self-edit. |
| **Elementor** ❌ | Do not. DOM bloat and render-blocking CSS will cost you the Core Web Vitals argument in every sales call. |
| Divi / Avada ❌ | Same problem, worse. Shortcode lock-in on top. |

### Theme settings (Appearance → Customize)

**Colors**
```
Palette 1 (accent)   #00FFB2   Electric Green
Palette 2 (dark)     #1E2A38   Deep Navy
Palette 3 (darker)   #0B1219   Page background
Palette 4 (panel)    #101A24   Card background
Palette 5 (border)   #22303F   Hairlines
Palette 6 (body)     #C6D4E2   Body text
Palette 7 (muted)    #8496A9   Secondary text
Palette 8 (white)    #FFFFFF   Headings
```

**Typography**
- Headings: **Poppins** — 600/700, letter-spacing `-0.02em`
- Body: **Inter** — 400/500, 17px, line-height 1.7
- Accent/data: **JetBrains Mono** — 400/500
- Set **Load Google Fonts Locally = ON** and **Preload = ON** in Kadence → Typography. This removes a third-party request and improves LCP.

**Layout**
- Content width `1180px`
- Header: sticky, transparent-on-scroll off, background `#0B1219` at 82% with blur

---

## Phase 3 — Plugins (30 min)

Install in this order. **Keep the total under 20 active plugins.**

### Essential
| Plugin | Purpose | Cost |
|---|---|---|
| **Rank Math Pro** | SEO, schema, sitemaps, redirects | ~$79/yr |
| **Kadence Blocks Pro** | Layout blocks | in bundle |
| **WP Rocket** | Caching, critical CSS, delay JS | ~$59/yr |
| **Perfmatters** | Script manager — disable unused JS per page | ~$25/yr |
| **ShortPixel** | WebP/AVIF conversion | free tier fine |
| **Fluent Forms** | Contact + audit lead forms | free tier fine |
| **FluentCRM** | Newsletter ("The AI Visibility Brief") | ~$90/yr, self-hosted |
| **UpdraftPlus** | Backups to Google Drive | free |
| **WPS Hide Login** | Move `/wp-admin` | free |

### Skip these
- Jetpack (bloat), Yoast (Rank Math schema is better for GEO work), any "AIO SEO" duplicate, Elementor add-ons, slider plugins, Wordfence on managed hosts (host firewall covers it).

### Rank Math configuration — the parts that matter for GEO
1. **Titles & Meta → Local SEO** → Person or Organization → fill **completely**. This generates your Organization schema.
2. Add every social profile under **sameAs** — LinkedIn, YouTube, X, Instagram, Substack, Crunchbase. *This is a direct AI entity signal, not a nice-to-have.*
3. **Schema → Default for Posts** = `Article`; **for Pages** = `WebPage`. Service pages get `Service` schema manually.
4. Enable **FAQ block** and **HowTo block**.
5. **Sitemap** → include Pages, Posts, and your custom post types. Exclude author archives, tag archives, media attachments.
6. **404 monitor + Redirections** → ON.
7. Author boxes ON, with `Person` schema wired to a real LinkedIn URL.

---

## Phase 4 — Import the site (10 min)

I will hand you three files:

```
sved-content.xml          WordPress WXR — all 14 pages, blog posts, categories
sved-child-theme.zip      Kadence child theme with the full design system CSS
sved-ai-toolkit.zip       Custom plugin: schema, llms.txt, AI-crawler rules, audit tool
```

1. **Tools → Import → WordPress** → install importer → upload `sved-content.xml` → assign to your author → **do not** check "download and import file attachments" (images come separately).
2. **Appearance → Themes → Add New → Upload** → `sved-child-theme.zip` → Activate.
3. **Plugins → Add New → Upload** → `sved-ai-toolkit.zip` → Activate.
4. **Settings → Reading → Homepage displays → A static page** → Homepage = `Home`, Posts page = `Insights`.
5. **Appearance → Menus** → assign `Primary Menu` to the header location, `Footer Menu` to footer.

---

## Phase 5 — AI visibility layer (the part most sites skip)

The `sved-ai-toolkit` plugin handles all of this automatically, but here is what it does so you can verify it:

### 5.1 `robots.txt` — AI crawler declarations
```
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: CCBot
Allow: /

Sitemap: https://svedsolution.com/sitemap_index.xml
```
> **Decision point:** these are all set to `Allow` deliberately. You *want* to be cited — you are not a publisher monetising pageviews. Blocking these guarantees zero AI citations.

### 5.2 `/llms.txt`
Auto-generated at the domain root, listing your services, key pages and a one-paragraph brand description in the exact wording you want models to reuse. Consistency of description across sources is the entity signal.

### 5.3 Schema per page type
| Page type | Schema |
|---|---|
| Home | `ProfessionalService` + `WebSite` + `SearchAction` |
| Service pages | `Service` + `FAQPage` + `BreadcrumbList` |
| Blog posts | `BlogPosting` + `Person` (author) + `FAQPage` |
| Case studies | `Article` + `Organization` |
| Reviews page | `AggregateRating` + `Review` |
| Videos | `VideoObject` |
| Team | `Person` per member, `sameAs` → LinkedIn |

### 5.4 Answer-block pattern
Every service and blog page opens with a bordered "direct answer" block in the first 100 words. This is what gets extracted and quoted. It is a reusable Kadence block pattern in the child theme.

---

## Phase 6 — The free audit tool

`sved-ai-toolkit` ships a `[sved_audit]` shortcode. Drop it on `/ai-visibility-audit/`.

**Tier 1 (what you launch with — zero running cost):**
Server-side crawl of the submitted URL returning real values for the 12 checks: Organization schema, Person schema, FAQPage schema, `llms.txt`, AI crawler directives, answer-first structure, freshness, heading hierarchy, citation-ready formats, Core Web Vitals (via PageSpeed Insights API — free), entity consistency, Tier-1 citation footprint.

**Rate limiting is not optional.** The plugin caps at 3 audits per IP per hour and caches results for 24 hours per domain. Without this, a competitor can run your crawler as a free DDoS amplifier.

**Tier 2 (add later):** real ChatGPT / Perplexity / Gemini prompt testing. Needs your own API keys in `wp-config.php`, costs roughly $0.02–0.15 per audit. Gate it behind an email capture.

---

## Phase 7 — Measurement (20 min)

1. **Google Search Console** — verify via DNS TXT record (survives host migrations, unlike HTML-file verification).
2. **GA4** — create property, install via **Google Tag Manager**, not hardcoded. You will want GTM later for LinkedIn Insight and conversion events.
3. **GTM tags to add:** GA4 config, LinkedIn Insight Tag, form-submit event, audit-completed event, newsletter-signup event.
4. **Bing Webmaster Tools** — import from GSC in one click. Bing feeds Copilot; do not skip it.
5. **Exclude internal traffic** in GA4 (Admin → Data Streams → Configure tag settings → Define internal traffic).
6. Submit `sitemap_index.xml` in both GSC and Bing.

---

## Phase 8 — Launch checklist

- [ ] `Settings → Reading → Discourage search engines` is **unchecked**
- [ ] HTTPS forced; `www` and non-`www` resolve to one canonical version
- [ ] `robots.txt` live with AI crawler rules
- [ ] `/llms.txt` live
- [ ] `sitemap_index.xml` submitted to GSC + Bing
- [ ] Organization schema validates in [Rich Results Test](https://search.google.com/test/rich-results)
- [ ] Every page has a unique title ≤60 chars and description ≤155 chars
- [ ] All images have descriptive alt text and are WebP
- [ ] Contact form delivers to `svedsolution@gmail.com` — **send a real test**
- [ ] Audit tool rate limiting confirmed working
- [ ] Mobile PageSpeed ≥ 90, LCP < 2.5s, CLS < 0.1
- [ ] 404 page has navigation back to Services and the audit
- [ ] Backups scheduled to off-site storage
- [ ] Privacy Policy + Terms published (required for Google Ads/analytics compliance)

---

## Phase 9 — First 90 days (practise what you sell)

Your own site is your first case study. Run your own playbook on it.

**Days 1–30 — Entity foundation**
- Organization + Person schema live with complete `sameAs`
- Claim: Google Business Profile, LinkedIn Company, Crunchbase, Clutch, DesignRush, G2 (agency category), Product Hunt (for the audit tool)
- Ensure the brand is described **identically** everywhere — same one-paragraph description, verbatim
- Publish `geo-vs-seo` (KD 12) — the fastest win available to you

**Days 31–60 — Content**
- Publish the GEO pillar (targeting `generative engine optimization`, SV 12,000) — 4,000 words, original framework, real numbers
- Publish the AEO twin (SV 3,700)
- Ship the audit tool publicly and post it to Product Hunt and r/SEO
- Start the newsletter with the AI Search Playbook as the signup magnet

**Days 61–90 — Citations**
- Founder entity work: LinkedIn cadence, two podcast pitches, one guest post
- Reddit and Quora participation in r/SEO, r/TechSEO, r/bigseo — answer questions properly, link in passing
- Publish `llm seo` (KD 14) and the position 8–20 SOP as a public post
- Begin weekly controlled prompt testing on your **own** brand and log it — that log becomes your best sales asset

> Everything above is drawn from the frameworks already in your `SEO data` folder. You are not buying a methodology, you are publishing the one you already have.

---

## Budget summary

| Item | Year 1 |
|---|---|
| Domain | $10 |
| Hosting (Rocket.net) | $300 |
| Kadence Pro bundle | $130 |
| Rank Math Pro | $79 |
| WP Rocket | $59 |
| Perfmatters | $25 |
| FluentCRM | $90 |
| Google Workspace (1 seat) | $72 |
| **Total** | **~$765/yr** |

Optional: Ahrefs or SE Ranking for client delivery ($99+/mo), LLM API credits for Tier 2 audits (~$20/mo at low volume).
