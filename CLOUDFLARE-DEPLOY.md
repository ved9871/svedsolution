# svedsolution.com — Cloudflare Pages Deploy Guide

**Total cost: $10.44/year** (the domain). Everything else is free tier.

```
Domain            Cloudflare Registrar    $10.44/yr  at cost, no markup
Hosting           Cloudflare Pages        $0         unlimited bandwidth
Audit tool        Pages Functions         $0         100,000 req/day
Rate limit/cache  Workers KV              $0         100k reads, 1k writes/day
Email forwarding  Cloudflare Email        $0         hello@ -> your Gmail
Form delivery     Resend                  $0         3,000 emails/month
CMS               Decap                   $0         open source
Repo              GitHub                  $0         private repo
```

---

## Step 1 — Buy the domain (5 min)

You said you've already signed up. In the Cloudflare dashboard:

**Domain Registration → Register Domains** → search `svedsolution.com` → purchase.

Because you're registering *inside* Cloudflare, DNS is configured automatically. There are no nameservers to point and no propagation wait.

---

## Step 2 — Email: hello@svedsolution.com → your Gmail (5 min)

**Dashboard → your domain → Email → Email Routing → Get started.**

1. Cloudflare offers to add the required MX and TXT records — accept.
2. **Destination address:** `svedsolution@gmail.com` → verify via the email Cloudflare sends.
3. **Create custom address:** `hello@svedsolution.com` → forward to your Gmail.
4. Optionally add a catch-all so nothing addressed to the domain is lost.

**To send *from* hello@ in Gmail:** Gmail → Settings → Accounts → *Send mail as* → Add another email address. Use an [app password](https://myaccount.google.com/apppasswords) with SMTP host `smtp.gmail.com`, port 587, TLS. You then reply from `hello@svedsolution.com` inside the Gmail interface you already use.

> Add SPF and DMARC once sending works, or your mail lands in spam:
> ```
> TXT  @              v=spf1 include:_spf.google.com ~all
> TXT  _dmarc         v=DMARC1; p=none; rua=mailto:hello@svedsolution.com
> ```

---

## Step 3 — Push to GitHub (10 min)

Create a **private** repo named `svedsolution`, then from the project folder:

```bash
cd "C:/Users/Ved Prakash/Documents/SEO data/svedsolution-preview"
```

```bash
git init && git add . && git commit -m "SVED Solution site" && git branch -M main
```

```bash
git remote add origin https://github.com/YOUR_USERNAME/svedsolution.git && git push -u origin main
```

Add a `.gitignore` first so the build output isn't committed:

```
dist/
__pycache__/
.DS_Store
```

---

## Step 4 — Connect Cloudflare Pages (5 min)

**Workers & Pages → Create → Pages → Connect to Git** → select the repo.

Build settings:

| Field | Value |
|---|---|
| Framework preset | **None** |
| Build command | `pip install -r requirements.txt && python build.py` |
| Build output directory | `dist` |
| Root directory | *(leave blank)* |

Deploy. First build takes ~90 seconds and gives you `svedsolution.pages.dev`.

> The `functions/` folder is detected automatically and compiled into Workers. You do not configure it — `/api/audit`, `/api/contact`, `/api/auth` and `/api/callback` become live endpoints.

---

## Step 5 — Custom domain (2 min)

**Your Pages project → Custom domains → Set up a custom domain** → `svedsolution.com`. Repeat for `www.svedsolution.com`.

DNS and SSL are configured automatically. The `_redirects` file already forces `www` → apex.

---

## Step 6 — KV namespace for rate limiting (5 min)

Without this, someone can run your audit crawler as a free DDoS amplifier. **Do not skip it.**

1. **Workers & Pages → KV → Create namespace** → name it `SVED_AUDIT`.
2. **Pages project → Settings → Functions → KV namespace bindings → Add binding:**
   - Variable name: `AUDIT_KV`
   - KV namespace: `SVED_AUDIT`
3. Add for **both** Production and Preview environments.

This gives you 3 audits per IP per hour and 24-hour result caching per domain.

---

## Step 7 — Environment variables (10 min)

**Pages project → Settings → Environment variables → Production.**

| Variable | Value | Required? | Where to get it |
|---|---|---|---|
| `PSI_KEY` | PageSpeed Insights API key | **Yes** | See below |
| `RESEND_KEY` | `re_...` | Yes, for forms | [resend.com](https://resend.com) → API Keys |
| `TO_EMAIL` | `hello@svedsolution.com` | Yes | — |
| `GITHUB_CLIENT_ID` | OAuth app ID | Only for the CMS | Step 8 |
| `GITHUB_CLIENT_SECRET` | OAuth secret | Only for the CMS | Step 8 |

### PSI_KEY is effectively required

I tested it: **without a key the PageSpeed API returns HTTP 429** almost immediately, and the Core Web Vitals check degrades to "not measured". It's free:

1. [console.cloud.google.com](https://console.cloud.google.com) → create a project
2. **APIs & Services → Library** → enable **PageSpeed Insights API**
3. **Credentials → Create credentials → API key**
4. Restrict it to the PageSpeed Insights API only

### Resend, for the contact form

Sign up, verify `svedsolution.com` by adding the DNS records they give you (in Cloudflare DNS), then create an API key. Free tier is 3,000 emails/month.

> If `RESEND_KEY` is missing, the form still accepts submissions and logs them rather than showing the user an error — but nothing reaches your inbox. Set it before launch.

---

## Step 8 — Decap CMS: the WordPress-style editor (15 min)

Gives you `svedsolution.com/admin/` where you write posts in a visual editor. Saving commits markdown to GitHub, which triggers a rebuild. **New post is live in about 60 seconds.**

### 8a. Create the GitHub OAuth app

GitHub → **Settings → Developer settings → OAuth Apps → New OAuth App**

| Field | Value |
|---|---|
| Application name | `SVED Solution CMS` |
| Homepage URL | `https://svedsolution.com` |
| Authorization callback URL | `https://svedsolution.com/api/callback` |

Copy the **Client ID**, generate a **Client Secret**, add both to Pages environment variables (Step 7), then **redeploy** so the Functions pick them up.

### 8b. Point the config at your repo

Edit `admin/config.yml` — two lines:

```yaml
repo: YOUR_GITHUB_USERNAME/svedsolution
base_url: https://svedsolution.com
```

Commit and push. Visit `https://svedsolution.com/admin/` and sign in with GitHub.

### How you'll write posts

Fields are already set up for GEO: **Title**, **URL slug**, **Meta description**, **Direct answer block** (the 30–80 word passage AI is most likely to quote), **Category**, **Date**, **Author**, **Read time**, **Body**.

The direct-answer field is the important one. It renders as the highlighted block at the top of every post — that's the passage designed to get extracted and cited.

---

## Step 9 — Verify (15 min)

```bash
curl -s -X POST https://svedsolution.com/api/audit -H "content-type: application/json" -d "{\"url\":\"https://www.web3technetwork.com\"}"
```

Check each of these:

- [ ] `https://svedsolution.com` loads over HTTPS
- [ ] `www` redirects to apex
- [ ] `/robots.txt` returns **plain text** (not HTML)
- [ ] `/llms.txt` returns **plain text**
- [ ] `/sitemap.xml` returns XML
- [ ] `/audit`, `/geo`, `/blog` redirect correctly
- [ ] Audit tool returns a real score on the live site
- [ ] Rate limit fires on the 4th audit within an hour
- [ ] Contact form delivers to your Gmail — **send a real test**
- [ ] `/admin/` signs in and saves a test post
- [ ] `/admin/` is `noindex` (already set in `_headers`)

Then:

1. **Google Search Console** — add `svedsolution.com`, verify by DNS TXT (survives migrations), submit `sitemap.xml`
2. **Bing Webmaster Tools** — import from GSC in one click. Bing feeds Copilot.
3. **Analytics** — Cloudflare Web Analytics is free, privacy-friendly and needs no cookie banner. Add GA4 via GTM only if you need the deeper reports.

---

## Working on the site day to day

| Task | How |
|---|---|
| Write a blog post | `/admin/` → New blog post → Publish |
| Edit page copy | Edit `build.py`, commit, push |
| Change design | Edit `assets/style.css`, commit, push |
| Preview locally | `python build.py` then `python -m http.server 8787 --directory dist` |
| Roll back | Cloudflare Pages → Deployments → *Rollback* on any previous build |

Every push to `main` deploys automatically. Every pull request gets its own preview URL.

---

## What the audit tool actually measures

I ran it live against `web3technetwork.com` while building it — **score 42/100, 4 fail / 6 partial / 2 pass.** These are real measurements, not placeholders:

| Check | Method |
|---|---|
| Organization schema | Parses all JSON-LD, walks `@graph`, counts `sameAs` |
| Person / author schema | JSON-LD type detection |
| FAQPage schema | Detects `FAQPage` / `QAPage` |
| llms.txt | Fetches it **and verifies it's plain text, not a soft-404 HTML page** |
| AI crawler access | Fetches robots.txt, parses per-bot `Disallow` across 9 AI agents |
| Answer-first structure | Extracts first real paragraph, word-counts it, detects narrative openers |
| Freshness | `dateModified`, `article:modified_time`, `<time datetime>`; reports age in days |
| Heading hierarchy | H1 count plus skipped-level detection |
| Citation-ready formats | Counts tables and lists |
| Core Web Vitals | PageSpeed Insights API (needs `PSI_KEY`) |
| Entity consistency | Compares schema `name` values against `og:site_name` |
| Tier-1 footprint | Checks 12 Tier-1 domains in `sameAs` and page links |

**Security:** the endpoint blocks `localhost`, all RFC-1918 ranges, link-local `169.254.x`, and every non-http(s) scheme (`file:`, `data:`, `ftp:`) — verified against each. It's a public endpoint that makes outbound fetches, so this matters.

---

## Three things found on web3technetwork.com

Real output from the tool, worth acting on:

1. **No Organization schema** — the single highest-impact fix. The site is not a resolvable entity to any AI model.
2. **No Person/author schema** — anonymous content is systematically discounted.
3. **No freshness signals** — no `dateModified` anywhere, so every page reads as undated.

Credit where due: it **does** serve a genuine `llms-full.txt` indexing 88 pages, and brand naming is consistent. Those two are already right.

---

## If you later want WordPress

Nothing here is wasted. Content lives as markdown in `content/blog/`, which imports cleanly into WordPress. Keep the domain on Cloudflare either way — it should sit in front of any host you use.

Honestly though: at $0/year, with edge performance and an audit tool that a WordPress plugin would struggle to match, the reason to switch is only if you hire writers who refuse to use anything but WordPress.
