/**
 * GET /api/auth — starts the GitHub OAuth flow for Decap CMS.
 * Cloudflare Pages replaces Netlify Identity here.
 *
 * Env vars required:
 *   GITHUB_CLIENT_ID
 *   GITHUB_CLIENT_SECRET   (used by /api/callback)
 */
export async function onRequestGet({ request, env }) {
  if (!env.GITHUB_CLIENT_ID) {
    return new Response('GITHUB_CLIENT_ID is not configured in Pages environment variables.', { status: 500 });
  }
  const origin = new URL(request.url).origin;
  const auth = new URL('https://github.com/login/oauth/authorize');
  auth.searchParams.set('client_id', env.GITHUB_CLIENT_ID);
  auth.searchParams.set('redirect_uri', `${origin}/api/callback`);
  auth.searchParams.set('scope', 'repo,user');
  auth.searchParams.set('state', crypto.randomUUID());
  return Response.redirect(auth.toString(), 302);
}
