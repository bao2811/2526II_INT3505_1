// src/middleware/cacheHeaders.js
// Middleware: Dat Cache-Control headers (minh hoa nguyen tac Cacheable)

/**
 * Tra ve middleware set Cache-Control header
 * @param {string} directive - VD: 'public, max-age=60' hoac 'no-store'
 */
const setCacheControl = (directive) => (req, res, next) => {
  res.setHeader("Cache-Control", directive);
  next();
};

// Cache public 60 giay (cho danh sach san pham, bai viet public)
const cachePublic = setCacheControl("public, max-age=60");

// Cache private 30 giay (cho thong tin ca nhan)
const cachePrivate = setCacheControl("private, max-age=30");

// Khong cache (cho du lieu nhay cam: login, payment)
const noCache = setCacheControl("no-store, no-cache");

module.exports = { cachePublic, cachePrivate, noCache };
