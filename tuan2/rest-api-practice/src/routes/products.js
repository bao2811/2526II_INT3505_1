// src/routes/products.js
// ============================================================
// Products - minh hoa tinh huong 5 (tim kiem + cache public)
//   - GET /api/v1/products        → Danh sach / tim kiem san pham
//   - GET /api/v1/products/:id    → Chi tiet san pham
// ============================================================

const express = require("express");
const router = express.Router();

const { products } = require("../data/db");
const { cachePublic } = require("../middleware/cacheHeaders");
const { paginate, generateETag } = require("../utils/helpers");

// ------------------------------------------------------------------
// TINH HUONG 5: GET /api/v1/products
// Tim kiem + filter san pham (co cache public)
// Query: q, category, brand, price_min, price_max, in_stock, sort, order, page, limit
// ------------------------------------------------------------------
router.get("/", cachePublic, (req, res) => {
  const {
    q,
    category,
    brand,
    price_min,
    price_max,
    in_stock,
    sort = "createdAt",
    order = "desc",
    page,
    limit,
  } = req.query;

  let filtered = [...products];

  // Full-text search tren name va brand
  if (q) {
    const query = q.toLowerCase();
    filtered = filtered.filter(
      (p) =>
        p.name.toLowerCase().includes(query) ||
        p.brand.toLowerCase().includes(query) ||
        p.category.toLowerCase().includes(query),
    );
  }

  // Filter theo category
  if (category) {
    filtered = filtered.filter(
      (p) => p.category.toLowerCase() === category.toLowerCase(),
    );
  }

  // Filter theo brand (co the nhieu brand, phan cach bang dau phay)
  if (brand) {
    const brands = brand.split(",").map((b) => b.trim().toLowerCase());
    filtered = filtered.filter((p) => brands.includes(p.brand.toLowerCase()));
  }

  // Filter theo khoang gia
  if (price_min)
    filtered = filtered.filter((p) => p.price >= parseInt(price_min));
  if (price_max)
    filtered = filtered.filter((p) => p.price <= parseInt(price_max));

  // Filter con hang
  if (in_stock === "true") filtered = filtered.filter((p) => p.stock > 0);

  // Sap xep
  const validSortFields = ["price", "rating", "name", "createdAt"];
  if (validSortFields.includes(sort)) {
    filtered.sort((a, b) => {
      if (a[sort] < b[sort]) return order === "asc" ? -1 : 1;
      if (a[sort] > b[sort]) return order === "asc" ? 1 : -1;
      return 0;
    });
  }

  // Tinh facets (thong ke theo nhom - dung cho sidebar filter)
  const allCategories = {};
  const allBrands = {};
  products.forEach((p) => {
    allCategories[p.category] = (allCategories[p.category] || 0) + 1;
    allBrands[p.brand] = (allBrands[p.brand] || 0) + 1;
  });

  const facets = {
    categories: Object.entries(allCategories).map(([name, count]) => ({
      name,
      count,
    })),
    brands: Object.entries(allBrands).map(([name, count]) => ({ name, count })),
    priceRange: {
      min: Math.min(...products.map((p) => p.price)),
      max: Math.max(...products.map((p) => p.price)),
    },
  };

  const { data, pagination } = paginate(filtered, page, limit);

  // ETag de ho tro caching hop le
  const etag = generateETag(data);
  res.setHeader("ETag", etag);

  // Kiem tra If-None-Match (client co cache cu khong?)
  if (req.headers["if-none-match"] === etag) {
    return res.status(304).end(); // Not Modified - dung cache cu
  }

  // Neu khong co ket qua van tra 200 (khong dung 404)
  res.status(200).json({
    query: q || null,
    results: data,
    pagination,
    facets,
    _meta: {
      searchTime: `${Math.floor(Math.random() * 30 + 5)}ms`,
      total: filtered.length,
    },
  });
});

// ------------------------------------------------------------------
// GET /api/v1/products/:id
// ------------------------------------------------------------------
router.get("/:id", cachePublic, (req, res) => {
  const product = products.find((p) => p.id === req.params.id);

  if (!product) {
    return res.status(404).json({
      error: "PRODUCT_NOT_FOUND",
      message: `Product with id '${req.params.id}' not found`,
    });
  }

  const etag = generateETag(product);
  res.setHeader("ETag", etag);

  if (req.headers["if-none-match"] === etag) {
    return res.status(304).end();
  }

  res.status(200).json({
    data: product,
    _links: {
      self: { href: `/api/v1/products/${product.id}`, method: "GET" },
      addToCart: { href: "/api/v1/orders", method: "POST" },
    },
  });
});

module.exports = router;
