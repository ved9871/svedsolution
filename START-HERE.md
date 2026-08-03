# Get svedsolution.com live — 3 steps, ~10 minutes

Everything else is optional and can wait. After Step 3 the site is live and the
audit tool works.

---

## Step 1 — Push (2 min)

Open PowerShell, paste this one line:

```bash
cd "C:/Users/Ved Prakash/Documents/SEO data/svedsolution-preview" && git fetch origin && git rebase origin/main && git push -u origin main
```

A browser window opens asking you to sign in to GitHub. Click **Authorize**.
No token to create.

If it complains about the README:

```bash
cd "C:/Users/Ved Prakash/Documents/SEO data/svedsolution-preview" && git push -u origin main --force
```

**Done when:** github.com/ved9871/svedsolution shows `build.py`, `functions/`, `admin/`.

---

## Step 2 — Connect Pages (5 min)

dash.cloudflare.com → **Workers & Pages** → **Create** → **Pages** tab →
**Connect to Git** → authorize GitHub → pick **svedsolution** → **Begin setup**

| Field | Value |
|---|---|
| Framework preset | **None** |
| Build command | `pip install -r requirements.txt && python build.py` |
| Build output directory | `dist` |

**Save and Deploy.** Wait ~90 seconds.

**Done when:** you get a working `svedsolution.pages.dev` URL.

---

## Step 3 — Attach the domain (2 min)

In the Pages project → **Custom domains** → **Set up a custom domain** →
`svedsolution.com` → **Activate**. Repeat for `www.svedsolution.com`.

> **Do not add DNS records manually.** Your DNS page shows 0 records and 3
> warnings — ignore them. This step creates the right records automatically.
> Manual A records will conflict and break it.

**Done when:** https://svedsolution.com loads.

---

# 🎉 That's it. The site is live.

Working right now, with zero configuration:

- All 17 pages
- The AI visibility audit tool — **11 of 12 checks return real measured values**
- Rate limiting and 24h result caching (edge-cache fallback, no KV needed)
- robots.txt allowing 15 AI crawlers, llms.txt, sitemap.xml
- All 3 blog posts

---

# Later, when you have time

Each of these is independent. Do them in any order, or never.

| Want this? | Do this | Time |
|---|---|---|
| The 12th check (Core Web Vitals) | Google Cloud Console → enable PageSpeed Insights API → create API key → add as `PSI_KEY` | 5 min |
| Contact form delivers to your inbox | resend.com → verify domain → API key → add as `RESEND_KEY` + `TO_EMAIL` | 10 min |
| The CMS at /admin/ | GitHub OAuth app (callback: `https://svedsolution.com/api/callback`) → add `GITHUB_CLIENT_ID` + `GITHUB_CLIENT_SECRET` | 5 min |
| hello@svedsolution.com | Cloudflare → Email → Email Routing → forward to Gmail | 5 min |
| Exact global rate limiting | Workers & Pages → KV → create `SVED_AUDIT` → bind as `AUDIT_KV` | 3 min |

After adding any environment variable: **Deployments → Retry deployment.**
Functions only read variables at build time.

Full detail for each in [CLOUDFLARE-DEPLOY.md](CLOUDFLARE-DEPLOY.md).

---

## Until the CMS is set up

You can still publish. Add a `.md` file to `content/blog/`, copying the front
matter from any existing post, then commit and push. Pages rebuilds
automatically. Or send me the topic and I'll write and commit it for you.
