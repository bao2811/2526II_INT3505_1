// src/middleware/requestLogger.js
// Middleware: Log moi request vao console (minh hoa Layered System)

const requestLogger = (req, res, next) => {
  const start = Date.now();

  // Gan X-Request-ID cho moi request neu chua co
  req.requestId =
    req.headers["x-request-id"] ||
    `req-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;

  // Sau khi response duoc gui xong thi log
  res.on("finish", () => {
    const duration = Date.now() - start;
    const log = `[${new Date().toISOString()}] ${req.method} ${req.originalUrl} → ${res.statusCode} (${duration}ms) [${req.requestId}]`;
    console.log(log);
  });

  next();
};

module.exports = requestLogger;
