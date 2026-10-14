// Shared helpers for the API routes. Files starting with "_" are not exposed as routes by Vercel.
// Regions: 1. Visitor identity   2. Bot detection   3. HTTP helpers
const crypto = require('crypto');

// #region 1. Visitor identity
// Best-effort client IP behind Vercel's proxy (first address of x-forwarded-for).
function clientIp(req) {
  const xff = req.headers['x-forwarded-for'];
  if (xff) return String(xff).split(',')[0].trim();
  return req.headers['x-real-ip'] || (req.socket && req.socket.remoteAddress) || 'unknown';
}

// Visitors' IPs are never stored in clear text: only a salted hash is used as a short-lived key.
// Set IP_HASH_SALT in production so the hashes cannot be reversed with a precomputed table.
function hashIp(ip) {
  const salt = process.env.IP_HASH_SALT || 'portfolio-jhon-diaz';
  return crypto
    .createHash('sha256')
    .update(salt + '|' + ip)
    .digest('hex')
    .slice(0, 32);
}

// #endregion

// #region 2. Bot detection
// Crawlers, link previews and monitors must not inflate the visit counter.
const BOT_RE =
  /bot|crawl|spider|slurp|preview|headless|lighthouse|monitor|curl|wget|python-requests|facebookexternalhit|embedly|whatsapp|telegram|linkedinbot/i;

function isBot(req) {
  return BOT_RE.test(String(req.headers['user-agent'] || ''));
}

// #endregion

// #region 3. HTTP helpers
// JSON response that is never cached.
function send(res, status, body) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify(body));
}

// Reads a JSON body (Vercel pre-parses it in most cases). Rejects bodies above 20 kB.
async function readJson(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  if (typeof req.body === 'string' && req.body) return JSON.parse(req.body);
  const chunks = [];
  let size = 0;
  for await (const c of req) {
    size += c.length;
    if (size > 20000) throw new Error('payload_too_large');
    chunks.push(c);
  }
  const raw = Buffer.concat(chunks).toString('utf8');
  return raw ? JSON.parse(raw) : {};
}

// #endregion

module.exports = { clientIp, hashIp, isBot, send, readJson };
