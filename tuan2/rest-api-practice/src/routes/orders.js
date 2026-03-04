// src/routes/orders.js
// ============================================================
// Orders - minh hoa tinh huong 3 (tao don hang + Idempotency-Key)
//   - POST /api/v1/orders         → Tao don hang moi
//   - GET  /api/v1/orders         → Lay don hang cua toi
//   - GET  /api/v1/orders/:id     → Chi tiet don hang
// ============================================================

const express = require("express");
const router = express.Router();

const { orders, products, uuidv4 } = require("../data/db");
const { requireAuth } = require("../middleware/auth");
const { noCache, cachePrivate } = require("../middleware/cacheHeaders");

// Luu tru idempotency keys da xu ly (chong tao don trung)
// { key: orderId }
const processedIdempotencyKeys = {};

// ------------------------------------------------------------------
// GET /api/v1/orders — Lay danh sach don hang cua toi
// ------------------------------------------------------------------
router.get("/", requireAuth, cachePrivate, (req, res) => {
  const myOrders = orders.filter((o) => o.customerId === req.user.id);

  res.status(200).json({
    data: myOrders,
    total: myOrders.length,
  });
});

// ------------------------------------------------------------------
// GET /api/v1/orders/:id — Chi tiet don hang
// ------------------------------------------------------------------
router.get("/:id", requireAuth, cachePrivate, (req, res) => {
  const order = orders.find((o) => o.id === req.params.id);

  if (!order) {
    return res.status(404).json({
      error: "ORDER_NOT_FOUND",
      message: `Order '${req.params.id}' not found`,
    });
  }

  // Chi chu don hang hoac admin moi xem duoc
  if (order.customerId !== req.user.id && req.user.role !== "admin") {
    return res.status(403).json({
      error: "FORBIDDEN",
      message: "You can only view your own orders",
    });
  }

  res.status(200).json({ data: order });
});

// ------------------------------------------------------------------
// TINH HUONG 3: POST /api/v1/orders — Tao don hang
// Body: { items: [{productId, quantity}], shippingAddress, paymentMethod }
// Idempotency-Key header de tranh tao don trung khi retry
// ------------------------------------------------------------------
router.post("/", requireAuth, noCache, (req, res) => {
  const idempotencyKey = req.headers["idempotency-key"];

  // === Kiem tra Idempotency Key ===
  if (idempotencyKey && processedIdempotencyKeys[idempotencyKey]) {
    // Da xu ly request nay roi → tra ve don hang cu (khong tao moi)
    const existingOrder = orders.find(
      (o) => o.id === processedIdempotencyKeys[idempotencyKey],
    );
    if (existingOrder) {
      res.setHeader("X-Idempotent-Replayed", "true");
      return res.status(200).json({
        data: existingOrder,
        message: "Order already created (idempotent replay)",
      });
    }
  }

  // === Validation ===
  const { items, shippingAddress, paymentMethod, note } = req.body;

  const errors = [];
  if (!items || !Array.isArray(items) || items.length === 0) {
    errors.push({ field: "items", message: "At least one item is required" });
  }
  if (!shippingAddress || !shippingAddress.fullName || !shippingAddress.phone) {
    errors.push({
      field: "shippingAddress",
      message: "shippingAddress with fullName and phone is required",
    });
  }
  if (!paymentMethod) {
    errors.push({
      field: "paymentMethod",
      message: "paymentMethod is required",
    });
  }

  if (errors.length > 0) {
    return res.status(422).json({ error: "VALIDATION_ERROR", details: errors });
  }

  // === Kiem tra ton kho va tinh gia ===
  const stockErrors = [];
  const orderItems = [];

  for (const item of items) {
    const product = products.find((p) => p.id === item.productId);

    if (!product) {
      stockErrors.push({
        productId: item.productId,
        message: "Product not found",
      });
      continue;
    }

    if (product.stock < item.quantity) {
      stockErrors.push({
        productId: item.productId,
        name: product.name,
        requested: item.quantity,
        available: product.stock,
        message: `Only ${product.stock} unit(s) available`,
      });
      continue;
    }

    orderItems.push({
      productId: product.id,
      name: product.name,
      quantity: item.quantity,
      unitPrice: product.price,
      subtotal: product.price * item.quantity,
    });
  }

  if (stockErrors.length > 0) {
    return res.status(409).json({
      error: "INSUFFICIENT_STOCK",
      message: "Some items are out of stock",
      items: stockErrors,
    });
  }

  // === Tinh gia tong ===
  const subtotal = orderItems.reduce((sum, i) => sum + i.subtotal, 0);
  const shippingFee = subtotal > 10000000 ? 0 : 50000; // Mien phi ship > 10tr
  const tax = Math.round(subtotal * 0.1); // 10% VAT
  const total = subtotal + shippingFee + tax;

  // === Tao don hang ===
  const now = new Date().toISOString();
  const newOrder = {
    id: `ord_${uuidv4().slice(0, 8)}`,
    customerId: req.user.id,
    status: "PENDING_PAYMENT",
    items: orderItems,
    shippingAddress,
    paymentMethod,
    note: note || "",
    pricing: { subtotal, shippingFee, tax, total },
    estimatedDelivery: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000)
      .toISOString()
      .split("T")[0],
    createdAt: now,
    updatedAt: now,
  };

  orders.push(newOrder);

  // Giam ton kho
  for (const item of orderItems) {
    const product = products.find((p) => p.id === item.productId);
    if (product) product.stock -= item.quantity;
  }

  // Luu idempotency key
  if (idempotencyKey) {
    processedIdempotencyKeys[idempotencyKey] = newOrder.id;
  }

  res.setHeader("Location", `/api/v1/orders/${newOrder.id}`);
  res.status(201).json({
    data: {
      ...newOrder,
      paymentUrl: `https://payment.example.com/checkout/${newOrder.id}`,
    },
  });
});

module.exports = router;
