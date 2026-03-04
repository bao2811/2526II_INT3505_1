// src/middleware/rateLimit.js
// Middleware: Gioi han so request (minh hoa 429 Too Many Requests)
// Moi IP chi duoc goi toi da MAX_REQUESTS lan trong WINDOW_MS mili-giay

const { rateLimitStore } = require("../data/db");

const WINDOW_MS = 60 * 1000; // 1 phut
const MAX_REQUESTS = 30; // Toi da 30 request/phut/IP (thap de de test)

const rateLimit = (req, res, next) => {
  const ip = req.ip || req.connection.remoteAddress || "127.0.0.1";
  const now = Date.now();

  // Lay hoac khoi tao buc anh rate limit cho IP nay
  if (!rateLimitStore[ip] || now > rateLimitStore[ip].resetAt) {
    rateLimitStore[ip] = {
      count: 0,
      resetAt: now + WINDOW_MS,
    };
  }

  rateLimitStore[ip].count += 1;

  const remaining = MAX_REQUESTS - rateLimitStore[ip].count;
  const resetAt = Math.ceil(rateLimitStore[ip].resetAt / 1000); // Unix timestamp

  // Luon them rate limit headers vao response
  res.setHeader("X-RateLimit-Limit", MAX_REQUESTS);
  res.setHeader("X-RateLimit-Remaining", Math.max(0, remaining));
  res.setHeader("X-RateLimit-Reset", resetAt);

  if (rateLimitStore[ip].count > MAX_REQUESTS) {
    const retryAfterSec = Math.ceil((rateLimitStore[ip].resetAt - now) / 1000);
    res.setHeader("Retry-After", retryAfterSec);

    return res.status(429).json({
      error: "RATE_LIMIT_EXCEEDED",
      message: `Too many requests. You have exceeded ${MAX_REQUESTS} requests per minute.`,
      retryAfter: retryAfterSec,
      retryAt: new Date(rateLimitStore[ip].resetAt).toISOString(),
      limit: MAX_REQUESTS,
      window: "1 minute",
    });
  }

  next();
};

module.exports = rateLimit;
