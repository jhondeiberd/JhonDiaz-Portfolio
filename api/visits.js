// Persistent visit counter.
//   GET  /api/visits  -> { count }             (read only)
//   POST /api/visits  -> { count, counted }    (counts this visit, at most once per visitor per 30 min)
//
// The number lives in Redis (Upstash), outside of the deployment, so redeploying or
// updating the site never resets it. Optional env var VISITS_START seeds the very first value
// (e.g. VISITS_START=250 if you want to begin from a number you already had).

const { isConfigured, pipeline } = require('./_redis');
const { clientIp, hashIp, isBot, send } = require('./_util');

// Regions: 1. Constants   2. GET (read)   3. POST (count a visit)

// #region 1. Constants
const KEY = 'portfolio:visits:total';
const WINDOW_SECONDS = 30 * 60; // one visitor is counted at most once per window
// #endregion

module.exports = async (req, res) => {
  if (!isConfigured()) {
    // Not connected to a database yet: the page simply hides the counter.
    return send(res, 200, { count: null, configured: false });
  }

  try {
    // #region 2. GET (read)
    if (req.method === 'GET') {
      const [value] = await pipeline([['GET', KEY]]);
      return send(res, 200, { count: Number(value || process.env.VISITS_START || 0) });
    }

    // #endregion

    // #region 3. POST (count a visit)
    if (req.method === 'POST') {
      const start = Number(process.env.VISITS_START || 0);
      const visitorKey = 'portfolio:visits:seen:' + hashIp(clientIp(req));

      if (isBot(req)) {
        const [value] = await pipeline([['GET', KEY]]);
        return send(res, 200, { count: Number(value || start), counted: false });
      }

      // 1) Has this visitor already been counted recently?  SET NX returns "OK" only the first time.
      const [fresh] = await pipeline([['SET', visitorKey, '1', 'NX', 'EX', String(WINDOW_SECONDS)]]);

      if (fresh === 'OK') {
        // 2) Seed once (only if the key does not exist) and increment atomically.
        const out = await pipeline([
          ['SETNX', KEY, String(start)],
          ['INCR', KEY],
        ]);
        return send(res, 200, { count: Number(out[1]), counted: true });
      }

      const [value] = await pipeline([['GET', KEY]]);
      return send(res, 200, { count: Number(value || start), counted: false });
    }

    // #endregion

    res.setHeader('Allow', 'GET, POST');
    return send(res, 405, { error: 'method_not_allowed' });
  } catch (err) {
    console.error('visits error:', err.message);
    return send(res, 200, { count: null, error: 'unavailable' });
  }
};
