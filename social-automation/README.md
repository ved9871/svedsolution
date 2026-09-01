# SVED Solution — Daily Social Auto-Poster

Posts one item from `posts.json` per day to your **Facebook Page**, **Instagram Business account**, and **LinkedIn Company Page**, automatically, via a Cloudflare Worker Cron Trigger. Runs on the same Cloudflare account as the website, so there's no server to maintain.

Images are served from `https://svedsolution.com/social/<file>` (published from `brand/social/` on the next site deploy).

---

## What you need to set up (one time)

### 1. Facebook + Instagram (Meta Graph API)
- A **Facebook Page** you admin.
- An **Instagram account** switched to **Business** or **Creator**, and **linked to that Facebook Page** (Instagram → Settings → linked Facebook Page).
- A **Meta app** at https://developers.facebook.com → create app (type "Business").
- Add the **Instagram Graph API** and **Facebook Login** products.
- Request permissions and submit for **App Review**: `pages_manage_posts`, `pages_read_engagement`, `instagram_basic`, `instagram_content_publish`, `business_management`.
- Generate a **long-lived Page access token** (60-day; refresh it, or use a System User token from Business Settings for a non-expiring token — recommended).

You will collect three values:
- `META_PAGE_ID` — your Facebook Page ID (Page → About, or Graph API Explorer `me/accounts`).
- `META_IG_USER_ID` — the IG Business account ID (`{page-id}?fields=instagram_business_account`).
- `META_PAGE_TOKEN` — the long-lived Page/System-User token.

### 2. LinkedIn (Community Management API)
- A **LinkedIn Company Page** you're an admin of.
- A **LinkedIn developer app** at https://www.linkedin.com/developers → create app, associate it with the Page.
- Request the **Community Management API** product (approval required) with scopes `w_organization_social` and `r_organization_social`.
- Generate an **access token** for the app authorized on the organization.

You will collect two values:
- `LINKEDIN_ORG_ID` — numeric org ID (from the Page admin URL, or the organizations API).
- `LINKEDIN_TOKEN` — the OAuth access token.

> Note: Meta and LinkedIn both require app review before publishing on your behalf. That approval is on your side and can take a few days — nothing here can bypass it. You never paste tokens into chat; they go into Cloudflare secrets (below).

---

## Deploy (from this folder)

```bash
npm install -g wrangler
wrangler login

# set the six secrets (you'll be prompted to paste each value privately)
wrangler secret put META_PAGE_ID
wrangler secret put META_IG_USER_ID
wrangler secret put META_PAGE_TOKEN
wrangler secret put LINKEDIN_ORG_ID
wrangler secret put LINKEDIN_TOKEN
wrangler secret put RUN_KEY        # any random string

wrangler deploy
```

The cron in `wrangler.toml` (`30 9 * * *` = 09:30 UTC / 15:00 IST daily) then posts one item per day, cycling through `posts.json`.

## Test it now (without waiting for the cron)

```bash
# posts item 0 immediately to all three platforms
curl "https://sved-social-poster.<your-subdomain>.workers.dev/?key=<RUN_KEY>&index=0"
```

It returns JSON showing success/failure per platform, so you can confirm each connection.

## Scheduling future blog posts (auto-publish)
Blog posts with a **future `date:`** in their front matter are hidden by the build until that date (not written, not in the sitemap or listings). To make them go live automatically:

1. In Cloudflare Pages → your project → Settings → **Builds & deployments → Deploy hooks**, create a hook and copy its URL.
2. `wrangler secret put CF_DEPLOY_HOOK` and paste it.

The daily cron then rebuilds the site each morning, so a post dated (say) 2026-09-02 publishes itself on 2026-09-02 with no action from you. Without this hook, future-dated posts publish only on your next manual `git push`.

## Add or change posts
Edit `posts.json` (each item: `title`, `url`, `image`, `caption`) and `wrangler deploy` again. The daily index cycles through the array, so add new posts to keep the queue fresh. New square images must be added to `brand/social/` and the site redeployed so `https://svedsolution.com/social/<file>` resolves.

## How each platform is posted
- **Facebook Page** — photo post: the square image + caption.
- **Instagram** — image + caption (two-step create → publish; requires the public image URL).
- **LinkedIn Page** — article/link share; LinkedIn auto-pulls the preview image from the post's Open Graph tag (already set on every blog).

## Guardrails
- Secrets live only in Cloudflare, never in the repo.
- `RUN_KEY` protects the manual test endpoint.
- If a token expires, that platform's call fails and is logged (check `wrangler tail`); the others still post. Refresh the token and redeploy.
