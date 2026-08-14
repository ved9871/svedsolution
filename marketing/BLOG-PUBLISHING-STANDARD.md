# Blog Publishing Standard — SVED Solution

Every blog post ships with four things, not one: the **article**, a **social pack**, a **design instruction**, and a **video script**. This is the repeatable checklist. Promo packs live in `marketing/packs/<slug>.md`.

---

## 1. Article compliance (AI SEO + Traditional SEO + Technical SEO)

Do not publish unless every box is true.

### AI SEO / GEO / AEO
- [ ] Answer-first: a direct 40–60 word answer to the title question in the first 100 words (the `answer:` frontmatter → renders as the answer block).
- [ ] Question-shaped H2s an LLM can lift as standalone answers.
- [ ] Dense, extractable blocks: at least one comparison table or numbered process.
- [ ] A `## Frequently asked questions` section (feeds FAQPage schema + AEO).
- [ ] Every claim carries a real number; visible "Updated <date>" and named author.
- [ ] An honest caveat where relevant (no guaranteed rankings/citations).

### Traditional SEO
- [ ] One primary keyword in title, H1, first 100 words, and slug.
- [ ] `title` ≤ ~60 chars where possible; `description` 140–160 chars, benefit-led.
- [ ] 3–6 internal links: to relevant service/pillar pages **and** at least one sibling post (bidirectional).
- [ ] Descriptive link anchors (not "click here").
- [ ] Logical H2/H3 hierarchy; scannable; 1,200–1,800 words for a pillar-support post.

### Technical SEO
- [ ] Per-post OG image set via `image:` frontmatter (1200×630 in `assets/`).
- [ ] JSON-LD emitted automatically: `BlogPosting` + `BreadcrumbList` + `FAQPage` (see `build.py` → `post_ld`). Validate in Rich Results Test after deploy.
- [ ] Canonical correct, `robots: index,follow`, appears in `sitemap.xml`.
- [ ] Renders server-side (it does — static build), AI crawlers not blocked.

### Content rules (non-negotiable)
Never name clients · no tax/GST details · no promised rankings or AI citations · every claim carries a real number.

---

## 2. Social pack (per post)
Captions/titles/hooks/hashtags for: **LinkedIn, Facebook, Instagram, Reddit, Medium, YouTube.**
- Voice: evidence-led, specific, no hype. Minimal emojis. Signature line available: "Google ranks pages. AI recommends brands."
- Reddit: value-first, non-promotional, follow each subreddit's self-promo rule.
- Medium: republish with **canonical URL** pointing to svedsolution.com to avoid duplicate-content dilution.
- Always end with a soft CTA to the free AI visibility audit.

## 3. Design instruction (per post)
One creative brief for Claude to design a promo asset (usually a 4–6 slide carousel for LinkedIn/Instagram). Brand system: navy `#0B1219`/`#101A24`, electric green `#00FFB2`→`#00A5FF`, Poppins headings, JetBrains Mono labels, real SVED mark, bottom green→blue accent bar.

## 4. Video script (per post)
One 45–90s script (Reel/Short/YouTube) with hook (first 3s), body, CTA, and on-screen text cues.

---

## Publish sequence
1. Draft article to the checklist → save `content/blog/<slug>.md` + OG creative in `assets/`.
2. Write the promo pack → `marketing/packs/<slug>.md`.
3. `python build.py` locally, preview, then commit + push (Cloudflare auto-deploys).
4. Validate schema in Rich Results Test; Request Indexing in Search Console; resubmit sitemap.
5. Schedule the social pack; brief the carousel + film the short.
