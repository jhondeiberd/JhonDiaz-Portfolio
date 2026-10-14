// Contact form endpoint: POST /api/contact
// - Validates the message and blocks spam (honeypot + per-visitor rate limit).
// - Saves every message in Redis (list "portfolio:contact:messages") so none is ever lost.
// - Sends an email through Resend when RESEND_API_KEY is configured.
//
// Environment variables (all optional, but at least one of Redis or Resend must be set):
//   RESEND_API_KEY   API key from https://resend.com
//   CONTACT_TO       where messages are delivered (default: jhondeiberd@gmail.com)
//   CONTACT_FROM     sender, default "Portfolio <onboarding@resend.dev>"

// Regions: 1. Helpers   2. Request handling   3. Spam and validation   4. Configuration check   5. Rate limit, persist and notify

// #region 1. Helpers
const { isConfigured, pipeline } = require('./_redis');
const { clientIp, hashIp, send, readJson } = require('./_util');

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
// Removes control characters, trims and caps the length of every user-supplied value.
const clean = (v, max) =>
  String(v == null ? '' : v)
    .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '')
    .trim()
    .slice(0, max);
// Escapes user text before it is placed inside the HTML email.
const esc = (s) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
// #endregion

module.exports = async (req, res) => {
  // #region 2. Request handling
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return send(res, 405, { error: 'method_not_allowed' });
  }

  let body;
  try {
    body = await readJson(req);
  } catch (e) {
    return send(res, 400, { error: 'invalid_request' });
  }

  // #endregion

  // #region 3. Spam and validation
  // Honeypot: real people never fill this hidden field. Pretend success so bots move on.
  if (clean(body.website, 200)) return send(res, 200, { ok: true });

  const name = clean(body.name, 120);
  const email = clean(body.email, 200);
  const phone = clean(body.phone, 40);
  const message = clean(body.message, 4000);

  const errors = {};
  if (name.length < 2) errors.name = 'Please enter your name.';
  if (!EMAIL_RE.test(email)) errors.email = 'Please enter a valid email address.';
  if (message.length < 10) errors.message = 'Please write a message (at least 10 characters).';
  if (Object.keys(errors).length) return send(res, 422, { error: 'validation', fields: errors });

  // #endregion

  // #region 4. Configuration check
  const hasRedis = isConfigured();
  const hasEmail = Boolean(process.env.RESEND_API_KEY);
  if (!hasRedis && !hasEmail)
    return send(res, 503, { error: 'not_configured', reason: 'no_redis_and_no_resend_key' });

  // #endregion

  try {
    // Rate limit: 5 messages per hour per visitor (the key is a salted IP hash, never the raw IP).
    if (hasRedis) {
      const rlKey = 'portfolio:contact:rl:' + hashIp(clientIp(req));
      const [n] = await pipeline([
        ['INCR', rlKey],
        ['EXPIRE', rlKey, '3600', 'NX'],
      ]);
      if (Number(n) > 5) return send(res, 429, { error: 'rate_limited' });
    }

    // #region 5. Rate limit, persist and notify
    // The message is stored first, so it survives even if the email provider fails.
    const record = { name, email, phone, message, at: new Date().toISOString() };
    let stored = false;
    let emailed = false;
    let reason = hasEmail ? 'resend_failed' : 'no_resend_key';

    if (hasRedis) {
      await pipeline([['LPUSH', 'portfolio:contact:messages', JSON.stringify(record)]]);
      stored = true;
    }

    if (hasEmail) {
      const r = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          Authorization: 'Bearer ' + process.env.RESEND_API_KEY,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          from: process.env.CONTACT_FROM || 'Portfolio <onboarding@resend.dev>',
          to: [process.env.CONTACT_TO || 'jhondeiberd@gmail.com'],
          reply_to: email,
          subject: 'Portfolio contact: ' + name,
          html:
            '<p><strong>Name:</strong> ' +
            esc(name) +
            '</p>' +
            '<p><strong>Email:</strong> ' +
            esc(email) +
            '</p>' +
            (phone ? '<p><strong>Phone:</strong> ' + esc(phone) + '</p>' : '') +
            '<p><strong>Message:</strong></p><p>' +
            esc(message).replace(/\n/g, '<br>') +
            '</p>',
        }),
      });
      emailed = r.ok;
      if (!r.ok) {
        const text = await r.text();
        console.error('resend error', r.status, text);
        // Resend's test sender only delivers to the account owner's own address.
        reason =
          r.status === 403 && /own email|verify a domain|testing emails/i.test(text)
            ? 'resend_test_sender_only_delivers_to_account_owner'
            : r.status === 401 || r.status === 403
              ? 'resend_key_rejected'
              : 'resend_http_' + r.status;
      }
    }

    // #endregion

    if (!stored && !emailed) return send(res, 502, { error: 'delivery_failed', reason });
    return send(res, 200, { ok: true, stored, emailed });
  } catch (err) {
    console.error('contact error:', err.message);
    return send(res, 502, { error: 'delivery_failed', reason: 'exception' });
  }
};
