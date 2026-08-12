# SVED Solution — Project Brief

Upload this as knowledge to a claude.ai Project, or keep it alongside
`CLAUDE.md` for Cowork. It carries the business context that `CLAUDE.md`
deliberately leaves out to stay lean.

---

## 1. The business

**SVED Solution** — an AI visibility and 360° SEO agency, operating since 2018.
Founder: **Ved Prakash**. Sister/subsidiary: **Web3Tech Network**
(web3technetwork.com), covering blockchain and Web3 marketing.

- **Site:** https://svedsolution.com
- **Repo:** https://github.com/ved9871/svedsolution
- **Booking:** https://cal.com/sved-solution/15min
- **Email:** hello@svedsolution.com → forwards to prakashved155@gmail.com
- **Phone / WhatsApp:** +91 78460 45690
- **Offices:** Dubai (HQ), Kolkata (delivery), Oswego NY (representative)

### Positioning

> **Google ranks pages. AI recommends brands.**

The strongest asset the brand owns: six words, states the category shift, needs
no proof, nobody else is saying it. Kept as the hero H1.

Tagline in use: *Top 1% SEO Service Provider in India*. Note this is
unverifiable — always pair it with a hard number.

### Vision
A web where the best answer wins, whoever gives it.

### Mission
To make every client the answer, not just a result — and to prove it with a number.

### Core values
Diagnosis before prescription · honest timelines · we ship, we don't suggest ·
every claim carries a number · documented, not improvised · we will tell you no.

---

## 2. Team

| Name | Role | Notes |
|---|---|---|
| Ved Prakash | Founder & Head of Strategy | LinkedIn: /in/ved-prakash-s1990/ |
| Amit Kumar | Technical Head | Title taken from RanqOne — confirm SVED title |
| Rahul Dhiman | Head of Growth | Listed as *Founder* at RanqOne — confirm |

⚠️ Amit's and Rahul's titles were imported from ranqone.com/about, a sister
operation. Rahul is RanqOne's founder, so his SVED title is an assumption that
should be confirmed before any pitch uses it.

---

## 3. Services (18)

**AI Search (the lead product):** Generative Engine Optimization · Answer Engine
Optimization · LLM SEO · AI Citation & Entity Building · AI Visibility
Monitoring · Google AI Overviews Optimization

**Core SEO:** Technical · Semantic & On-Page · Content Strategy · Link Building
& Digital PR · Ecommerce · SaaS & B2B · Local · International · Programmatic ·
Site Migrations · White-Label · Consulting ($30/hr)

GEO lives at `/generative-engine-optimization/` (root, not under `/services/`)
because it shipped there first and is indexed. A 301 covers the guessable path.

## 4. Industries (10)

Healthcare/IVF & Clinics · Ecommerce & D2C · SaaS & AI Products · Web3/Crypto ·
IT Services & App Development · Education & EdTech · Financial Services ·
Local/Retail/Studios · Security & Loss Prevention · Agencies & White-Label

Each page names the sector, not the client.

## 5. Client roster — 19 brands, anonymised on the site

| Real client | How it appears publicly |
|---|---|
| Origyn IVF, Mothers Lap IVF | "2 × IVF & fertility clinic groups, Delhi NCR" |
| Srisa Laser Cosmoderma | "Laser & cosmetic dermatology clinic, India" |
| Ameei Care | "Physiotherapy & rehabilitation practice" |
| Crawford's Metal Detecting (UK) | "Specialist hobby retailer, UK — 1,393 keywords" |
| Kass Care | "Bio-active skincare D2C brand, India" |
| BD Herbals | "Ayurvedic & herbal wellness brand, India" |
| Monisha London | "Fashion & lifestyle label, London" |
| Konch.ai | "AI transcription & translation platform" |
| DXB Apps | "Mobile app development firm, Dubai UAE" |
| Inceptial Tech | "Enterprise software & GCC provider, Kolkata" |
| ARS Web Tech | "Independent technology publishing platform" |
| Medhavi Skills University | "UGC-recognised skills university" |
| Sesame Bankhall Group (UK) | "Mortgage & insurance network group, UK" |
| Smoke Screen (UK) | "Security fog & loss-prevention manufacturer, UK" |
| NodeWaves | "Layer-2 staking & node protocol on Polygon" |
| Web3Tech Network | named — it is the subsidiary |
| Jhulelal Trading | "Trading & distribution business" |
| Oasis Art Play Studio | "Creative arts & play studio" |

`bdherbals.in` and `oasisartplaystudio.com` did not resolve when checked.

---

## 6. Real proof — use these, they are measured

**AI citations (Crawford's, April 2026):** 2,923 citations in 29 days across
131 distinct pages, ~101/day, top page 307 citations. This is the single most
valuable asset the brand has; almost no agency can show measured AI citation
volume.

**Rankings (same client):** #1 for "metal detectors" (27,100 searches/mo), plus
#1 for "metal detector shops near me", "minelab manticore", "waterproof metal
detector", "pinpointer metal detector", "gold panning kit". 1,393 keywords,
853 referring domains, DA 30.

**Growth from zero (Smoke Screen):** 2 → 95 ranking keywords and 0 → 213
monthly sessions, Aug 2025 → Jul 2026. 7 keywords now top-3. 316 ref domains.
Small numbers that matter — a single installation is a five-figure contract.

**Market (Dimension Market Research):** GEO market $1.09B in 2026 → $17.1B by
2034, 40.6% CAGR. APAC fastest at 45.1%. 65% of digital enterprises already
investing. Up to 30% CAC reduction.

**Methodology timeline (published, honest):** entity indexing 30–45 days →
first citations ~day 60 → consistent mentions ~day 90 → stable 4–6 months →
category authority 9–12 months.

---

## 7. Current site state

47 URLs in the sitemap, all returning 200. 14 core pages, 17 service pages,
10 industry pages, 3 blog posts, terms, privacy, HTML sitemap, 404.

**Core Web Vitals (verified after optimisation):**

| | Mobile | Desktop |
|---|---|---|
| LCP | 2.4s ✅ | 0.57s ✅ |
| FCP | 2.0s | 0.56s |
| CLS | 0 ✅ | 0.001 ✅ |
| TBT | 10ms ✅ | 9ms ✅ |

Mobile LCP started at 4.53s (POOR). Fixed by self-hosting fonts (1.5MB → 121KB
WOFF2), deferring gtag.js, replacing the YouTube iframe with a click-to-load
facade, dropping the masked hero grid below 680px, and adding
`content-visibility:auto` to off-screen sections.

**Working:** all pages, free AI visibility audit (12 real checks), WhatsApp
widget, contact + newsletter forms, robots.txt allowing 15 AI crawlers,
llms.txt, sitemap.xml, Decap CMS scaffolding, leads dashboard with CSV export.

**Not working yet — all blocked on account-level actions:**
1. Bot Fight Mode blocks Ubersuggest and LLM crawlers (Security → Bots → off)
2. `RESEND_KEY` unset → no lead emails send
3. `LEADS_KV` + `ADMIN_TOKEN` unset → leads not stored, `/admin/leads` won't open
4. GitHub OAuth unset → `/admin/` CMS won't sign in
5. Apps Script returns 401 → nothing reaches the Google Sheet
6. HSTS preload not submitted

---

## 8. Competitive landscape

| Competitor | Position | Gap to exploit |
|---|---|---|
| searchable.com | AI visibility SaaS, self-serve | Software, no strategist |
| trailblazermktg.com | Productized retainers, public pricing | LLM SEO is an add-on, not core |
| organichackers.com | "We scale big websites", technical-first | Enterprise only, no entry point |
| trioseo.com | "Search to Sales", lead-gen framing | Classic SEO with ChatGPT bolted on |

**None lead with GEO as the primary product backed by citation data.** That is
the lane, and the Crawford's export is the receipt.

### Keyword targets (Ahrefs reads — these SERPs are still soft)

| Keyword | Volume | KD | Note |
|---|---|---|---|
| generative engine optimization | 12,000 | 62 | every top-10 result UR ≤ 9 |
| answer engine optimization | 3,700 | 45 | softer than GEO |
| geo vs seo | 2,600 | 12 | fastest available win |
| llm seo | 1,400 | 14 | defensible with a case study |

---

## 9. Source material

`Documents/SEO data/` holds the research this was built from. Note: PDFs need
`pypdf` (no `pdftoppm` available), DOCX needs `python-docx`, XLSX needs
`openpyxl`.

- `AI-SEARCH-PLAYBOOK.pdf` — the GEO methodology: 4 pillars, Tier-1 citation
  stack, 30-day refresh loop, the results timeline quoted across the site
- `[OHK] Agent A Sample Strategy.docx` — real Ahrefs SV/KD/UR reads
- `The 21-Step Semantic SEO Playbook.pdf`
- `Move Pages From Position 8–20 to Top 3.pdf` — became a blog post and use case
- `SEO SOP-*.zip` — 39 documented SOPs, ~10 WordPress-specific
- `crawfordsmd.com_AIPageStatsReport*.csv` — the citation data

Ubersuggest MCP is authenticated as `marketing@web3technetwork.com` with live
projects for crawfordsmd, smoke-screen, web3technetwork, nodewaves, ranqone and
svedsolution.

---

## 10. How to brief a new session

Paste this as the Project's custom instructions:

> You are working on svedsolution.com, an AI visibility and 360° SEO agency
> site. It is a Python-generated static site on Cloudflare Pages with Pages
> Functions. Read CLAUDE.md before changing anything — it documents build
> commands and several non-obvious failure modes that have already caused
> production bugs (asset cache pinning, CSS escape sequences, canonical
> mismatches, acronym casing).
>
> Content rules: never name clients, never mention GST or tax details, never
> promise rankings or AI citations, and every claim carries a real number.
>
> Verify before claiming. This project has a history of bugs that looked fine
> in source and broke in production — measure the live site rather than assuming
> a change worked.
