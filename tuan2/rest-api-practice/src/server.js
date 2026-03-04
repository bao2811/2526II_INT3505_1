// src/server.js
// ============================================================
// Entry point - Khoi dong Express server
// Muc dich: Thuc hanh REST API - INT3505 Tuan 2
// ============================================================

const express = require("express");
const app = express();
const PORT = process.env.PORT || 3000;

// ===================== MIDDLEWARE TOAN CUC =====================

// Parse JSON body
app.use(express.json());

// Log moi request (minh hoa Layered System - logging layer)
const requestLogger = require("./middleware/requestLogger");
app.use(requestLogger);

// Them X-Request-ID vao tat ca responses
app.use((req, res, next) => {
  res.setHeader("X-Request-ID", req.requestId || "unknown");
  next();
});

// Rate limiting (minh hoa 429 Too Many Requests)
const rateLimit = require("./middleware/rateLimit");
app.use("/api/", rateLimit);

// ===================== ROUTES =====================

const usersRouter = require("./routes/users");
const postsRouter = require("./routes/posts");
const productsRouter = require("./routes/products");
const ordersRouter = require("./routes/orders");

// Versioned API (v1) - minh hoa Uniform Interface
app.use("/api/v1/users", usersRouter);
app.use("/api/v1/posts", postsRouter);
app.use("/api/v1/products", productsRouter);
app.use("/api/v1/orders", ordersRouter);

// ===================== ENDPOINT KHAM PHA =====================

// GET / — Trang chu, liet ke cac endpoints co san (HATEOAS-style)
app.get("/", (req, res) => {
  res.status(200).json({
    name: "REST API Practice - INT3505 Tuan 2",
    version: "1.0.0",
    description: "Thuc hanh kien truc REST voi Node.js + Express",
    _links: {
      users: { href: "/api/v1/users", methods: ["GET", "POST"] },
      posts: { href: "/api/v1/posts", methods: ["GET", "POST"] },
      products: { href: "/api/v1/products", methods: ["GET"] },
      orders: { href: "/api/v1/orders", methods: ["GET", "POST"] },
    },
    auth: {
      type: "Bearer Token",
      tokens: {
        "token-admin": "Admin access (full permissions)",
        "token-user": "User access (limited permissions)",
        "token-user3": "User access (limited permissions)",
      },
      usage: "Authorization: Bearer token-admin",
    },
  });
});

// GET /api/v1 — API info
app.get("/api/v1", (req, res) => {
  res.status(200).json({
    version: "v1",
    endpoints: [
      { path: "/api/v1/users", methods: "GET POST PUT PATCH DELETE" },
      { path: "/api/v1/users/:id", methods: "GET PUT PATCH DELETE" },
      { path: "/api/v1/posts", methods: "GET POST" },
      { path: "/api/v1/posts/:id", methods: "GET PATCH DELETE" },
      { path: "/api/v1/products", methods: "GET" },
      { path: "/api/v1/products/:id", methods: "GET" },
      { path: "/api/v1/orders", methods: "GET POST" },
      { path: "/api/v1/orders/:id", methods: "GET" },
    ],
  });
});

// ===================== XU LY LOI TOAN CUC =====================

// 404 — Route khong ton tai
app.use((req, res) => {
  res.status(404).json({
    error: "NOT_FOUND",
    message: `Cannot ${req.method} ${req.path}`,
    hint: "Check GET / for available endpoints",
  });
});

// 500 — Loi server khong xu ly duoc
// eslint-disable-next-line no-unused-vars
app.use((err, req, res, next) => {
  // Khong bao gio lo stack trace cho client (bao mat!)
  console.error(`[ERROR] ${req.method} ${req.path}`, err.stack);

  res.status(500).json({
    error: "INTERNAL_SERVER_ERROR",
    message: "An unexpected error occurred. Our team has been notified.",
    requestId: req.requestId,
    timestamp: new Date().toISOString(),
  });
});

// ===================== START SERVER =====================
app.listen(PORT, () => {
  console.log("=".repeat(55));
  console.log("  REST API Practice Server - INT3505 Tuan 2");
  console.log("=".repeat(55));
  console.log(`  Server:  http://localhost:${PORT}`);
  console.log(`  API v1:  http://localhost:${PORT}/api/v1`);
  console.log("");
  console.log("  Tokens de test:");
  console.log("    Admin: Authorization: Bearer token-admin");
  console.log("    User:  Authorization: Bearer token-user");
  console.log("=".repeat(55));
});

module.exports = app;
