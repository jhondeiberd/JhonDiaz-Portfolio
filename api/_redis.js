// Minimal Upstash Redis (REST) client with no dependencies.
// Files starting with "_" are helpers: Vercel does not expose them as routes.
//
// Regions: 1. Configuration   2. Commands
//
// Works with the Upstash integration from the Vercel Marketplace, which injects either
// KV_REST_API_URL / KV_REST_API_TOKEN or UPSTASH_REDIS_REST_URL / UPSTASH_REDIS_REST_TOKEN.

// #region 1. Configuration
const URL_ =
  process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL || process.env.REDIS_REST_URL || '';
const TOKEN =
  process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN || process.env.REDIS_REST_TOKEN || '';

// True when the REST URL and token are both present (otherwise callers degrade gracefully).
const isConfigured = () => Boolean(URL_ && TOKEN);
// #endregion

// #region 2. Commands

// Runs several commands in one round trip, e.g. [["SET","k","1"],["INCR","c"]].
async function pipeline(commands) {
  if (!isConfigured()) throw new Error('redis_not_configured');
  const res = await fetch(URL_.replace(/\/$/, '') + '/pipeline', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + TOKEN, 'Content-Type': 'application/json' },
    body: JSON.stringify(commands),
  });
  if (!res.ok) throw new Error('redis_http_' + res.status);
  const out = await res.json();
  return out.map((r) => {
    if (r && r.error) throw new Error('redis_error: ' + r.error);
    return r ? r.result : null;
  });
}

// Convenience wrapper for a single command, e.g. command('GET', 'key').
async function command(...args) {
  return (await pipeline([args]))[0];
}

// #endregion

module.exports = { isConfigured, pipeline, command };
