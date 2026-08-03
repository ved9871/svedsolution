/**
 * GET /api/callback — completes GitHub OAuth and hands the token back to Decap CMS
 * via postMessage, which is the handshake Decap expects.
 */
export async function onRequestGet({ request, env }) {
  const url = new URL(request.url);
  const code = url.searchParams.get('code');
  if (!code) return new Response('Missing authorization code.', { status: 400 });

  const res = await fetch('https://github.com/login/oauth/access_token', {
    method: 'POST',
    headers: { accept: 'application/json', 'content-type': 'application/json' },
    body: JSON.stringify({
      client_id: env.GITHUB_CLIENT_ID,
      client_secret: env.GITHUB_CLIENT_SECRET,
      code
    })
  });

  const data = await res.json();
  const payload = data.access_token
    ? { token: data.access_token, provider: 'github' }
    : { error: data.error_description || 'Authentication failed' };

  const status = data.access_token ? 'success' : 'error';
  const body = `<!doctype html><meta charset="utf-8"><title>Signing in…</title>
<body style="font-family:system-ui;background:#0B1219;color:#C6D4E2;display:grid;place-items:center;height:100vh;margin:0">
<p>Completing sign-in…</p>
<script>
(function () {
  var msg = 'authorization:github:${status}:' + ${JSON.stringify(JSON.stringify(payload))};
  function send(e) {
    if (!window.opener) return;
    window.opener.postMessage(msg, e && e.origin ? e.origin : '*');
  }
  window.addEventListener('message', send, false);
  if (window.opener) {
    window.opener.postMessage('authorizing:github', '*');
    setTimeout(function () { send(); setTimeout(function(){ window.close(); }, 400); }, 100);
  }
})();
</script></body>`;

  return new Response(body, { headers: { 'content-type': 'text/html; charset=utf-8' } });
}
