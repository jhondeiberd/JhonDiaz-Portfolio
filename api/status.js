// GET /api/status : configuration check for the owner. Returns only true/false flags, never secrets.
//   /api/status           -> which environment variables are present
//   /api/status?ping=1    -> also pings Redis to prove the connection works
// Regions: 1. Configuration flags   2. Optional Redis ping

const { isConfigured, pipeline } = require('./_redis');
const { send } = require('./_util');

module.exports = async (req, res) => {
  // #region 1. Configuration flags
  const redis = isConfigured();
  const out = {
    redis_configured: redis,
    resend_key_present: Boolean(process.env.RESEND_API_KEY),
    contact_to: process.env.CONTACT_TO ? 'custom' : 'default (jhondeiberd@gmail.com)',
    contact_from: process.env.CONTACT_FROM
      ? 'custom'
      : 'default (onboarding@resend.dev, only delivers to the Resend account owner)',
  };
  // #endregion

  // #region 2. Optional Redis ping
  const url = new URL(req.url, 'http://localhost');
  if (redis && url.searchParams.get('ping')) {
    try {
      const [pong] = await pipeline([['PING']]);
      out.redis_ping = pong;
    } catch (e) {
      out.redis_ping = 'failed: ' + e.message;
    }
  }
  // #endregion

  out.ready_for_counter = redis;
  out.ready_for_contact_form = redis || out.resend_key_present;
  send(res, 200, out);
};
