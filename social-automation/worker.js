// SVED Solution — daily social auto-poster (Cloudflare Worker, Cron Trigger)
// Posts one queue item per day to Facebook Page, Instagram Business, and LinkedIn Page.
// Images are pulled from https://svedsolution.com/social/<file> (public after site deploy).
// All credentials are Worker SECRETS — never hard-coded. See README.md.

import posts from "./posts.json";

const GRAPH = "https://graph.facebook.com/v21.0";
const IMG_BASE = "https://svedsolution.com/social/";

export default {
  // Runs on the cron schedule defined in wrangler.toml
  async scheduled(event, env, ctx) {
    ctx.waitUntil((async () => {
      // Trigger a site rebuild so any future-dated blog posts publish on their day
      await triggerDeploy(env);
      // Post the day's social item
      await run(env);
    })());
  },
  // Manual trigger for testing: GET /?key=RUN_KEY
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.searchParams.get("key") !== env.RUN_KEY) {
      return new Response("forbidden", { status: 403 });
    }
    const result = await run(env, url.searchParams.get("index"));
    return new Response(JSON.stringify(result, null, 2), {
      headers: { "content-type": "application/json" },
    });
  },
};

async function run(env, forceIndex) {
  const post = pickPost(env, forceIndex);
  const image = IMG_BASE + post.image;
  const results = {};
  results.facebook = await safe(() => postFacebook(env, post, image));
  results.instagram = await safe(() => postInstagram(env, post, image));
  results.linkedin = await safe(() => postLinkedIn(env, post));
  console.log(JSON.stringify({ post: post.title, results }));
  return { post: post.title, image, results };
}

function pickPost(env, forceIndex) {
  if (forceIndex != null && forceIndex !== "") return posts[Number(forceIndex) % posts.length];
  const start = new Date(env.START_DATE || "2026-08-20T00:00:00Z");
  const dayIndex = Math.floor((Date.now() - start.getTime()) / 86400000);
  return posts[((dayIndex % posts.length) + posts.length) % posts.length];
}

async function safe(fn) {
  try { return { ok: true, data: await fn() }; }
  catch (e) { return { ok: false, error: String(e && e.message || e) }; }
}

// Hit the Cloudflare Pages Deploy Hook so the static site rebuilds daily.
// This is what publishes future-dated (scheduled) blog posts on their date.
async function triggerDeploy(env) {
  if (!env.CF_DEPLOY_HOOK) return;
  try { await fetch(env.CF_DEPLOY_HOOK, { method: "POST" }); }
  catch (e) { console.log("deploy hook error", String(e)); }
}

// ---- Facebook Page: photo post with caption --------------------------------
async function postFacebook(env, post, image) {
  const body = new URLSearchParams({
    url: image,
    caption: post.caption,
    access_token: env.META_PAGE_TOKEN,
  });
  const r = await fetch(`${GRAPH}/${env.META_PAGE_ID}/photos`, { method: "POST", body });
  const j = await r.json();
  if (!r.ok) throw new Error("FB " + JSON.stringify(j));
  return j;
}

// ---- Instagram Business: create media container, then publish --------------
async function postInstagram(env, post, image) {
  const create = await fetch(`${GRAPH}/${env.META_IG_USER_ID}/media`, {
    method: "POST",
    body: new URLSearchParams({
      image_url: image,
      caption: post.caption,
      access_token: env.META_PAGE_TOKEN,
    }),
  });
  const c = await create.json();
  if (!create.ok) throw new Error("IG create " + JSON.stringify(c));
  const publish = await fetch(`${GRAPH}/${env.META_IG_USER_ID}/media_publish`, {
    method: "POST",
    body: new URLSearchParams({ creation_id: c.id, access_token: env.META_PAGE_TOKEN }),
  });
  const p = await publish.json();
  if (!publish.ok) throw new Error("IG publish " + JSON.stringify(p));
  return p;
}

// ---- LinkedIn Company Page: article/link share -----------------------------
// LinkedIn auto-generates the preview image from the article URL's OG tags.
async function postLinkedIn(env, post) {
  const payload = {
    author: `urn:li:organization:${env.LINKEDIN_ORG_ID}`,
    commentary: post.caption,
    visibility: "PUBLIC",
    distribution: { feedDistribution: "MAIN_FEED", targetEntities: [], thirdPartyDistributionChannels: [] },
    lifecycleState: "PUBLISHED",
    content: { article: { source: post.url, title: post.title } },
  };
  const r = await fetch("https://api.linkedin.com/rest/posts", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.LINKEDIN_TOKEN}`,
      "Content-Type": "application/json",
      "LinkedIn-Version": "202408",
      "X-Restli-Protocol-Version": "2.0.0",
    },
    body: JSON.stringify(payload),
  });
  if (!r.ok) throw new Error("LinkedIn " + r.status + " " + (await r.text()));
  return { id: r.headers.get("x-restli-id") || "posted" };
}
