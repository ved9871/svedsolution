/**
 * Worker entry point — used when the project is deployed as a
 * "Worker with static assets" rather than a classic Pages project.
 *
 * Cloudflare's newer "import a repository" flow creates a Worker, where the
 * Pages `functions/` directory convention does not apply. This module routes
 * /api/* to the exact same handlers and lets everything else fall through to
 * the static assets in dist/.
 *
 * Classic Pages deployments ignore this file and use functions/ directly, so
 * the repo works under either model with one copy of the handler code.
 */
import * as audit from '../functions/api/audit.js';
import * as contact from '../functions/api/contact.js';
import * as auth from '../functions/api/auth.js';
import * as callback from '../functions/api/callback.js';

const ROUTES = {
  '/api/audit': audit,
  '/api/contact': contact,
  '/api/auth': auth,
  '/api/callback': callback
};

const HANDLER = { GET: 'onRequestGet', POST: 'onRequestPost', OPTIONS: 'onRequestOptions' };

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    // Normalise a trailing slash so /api/audit/ hits the same handler.
    const path = url.pathname.length > 1 ? url.pathname.replace(/\/+$/, '') : url.pathname;

    const mod = ROUTES[path];
    if (mod) {
      const fn = mod[HANDLER[request.method]] || mod.onRequest;
      if (!fn) {
        return new Response(JSON.stringify({ error: `Method ${request.method} not allowed.` }), {
          status: 405,
          headers: { 'content-type': 'application/json', allow: 'GET, POST, OPTIONS' }
        });
      }
      try {
        return await fn({
          request,
          env,
          // Pages Functions hand handlers a context object with these fields;
          // mirror it so the handler code needs no changes.
          params: {},
          data: {},
          waitUntil: ctx.waitUntil.bind(ctx),
          passThroughOnException: ctx.passThroughOnException.bind(ctx),
          next: () => env.ASSETS.fetch(request)
        });
      } catch (err) {
        return new Response(JSON.stringify({ error: 'Internal error: ' + err.message }), {
          status: 500,
          headers: { 'content-type': 'application/json' }
        });
      }
    }

    return env.ASSETS.fetch(request);
  }
};
