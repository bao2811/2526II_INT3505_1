// src/routes/users.js
// ============================================================
// CRUD Users - minh hoa tinh huong 1 & 2:
//   - GET  /api/v1/users          → Lay danh sach (phan trang, loc)
//   - GET  /api/v1/users/:id      → Lay mot user
//   - POST /api/v1/users          → Tao moi user (chi admin)
//   - PUT  /api/v1/users/:id      → Cap nhat toan bo user
//   - PATCH /api/v1/users/:id     → Cap nhat mot phan (VD: doi email)
//   - DELETE /api/v1/users/:id    → Xoa user (soft delete, chi admin)
// ============================================================

const express = require("express");
const router = express.Router();

const { users, uuidv4 } = require("../data/db");
const { requireAuth, requireAdmin } = require("../middleware/auth");
const { cachePrivate, noCache } = require("../middleware/cacheHeaders");
const { paginate, isValidEmail, sanitize } = require("../utils/helpers");

// ------------------------------------------------------------------
// TINH HUONG 1: GET /api/v1/users
// Lay danh sach users co phan trang va filter
// Query params: page, limit, department, role, sort, order
// ------------------------------------------------------------------
router.get("/", requireAuth, cachePrivate, (req, res) => {
  const {
    page,
    limit,
    department,
    role,
    sort = "name",
    order = "asc",
  } = req.query;

  // Chi lay users chua bi xoa (soft delete)
  let filtered = users.filter((u) => u.deletedAt === null);

  // Filter theo department
  if (department) {
    filtered = filtered.filter(
      (u) => u.department.toLowerCase() === department.toLowerCase(),
    );
  }

  // Filter theo role
  if (role) {
    filtered = filtered.filter((u) => u.role === role);
  }

  // Sap xep
  const validSortFields = ["name", "email", "age", "createdAt"];
  if (validSortFields.includes(sort)) {
    filtered.sort((a, b) => {
      const aVal = a[sort];
      const bVal = b[sort];
      if (aVal < bVal) return order === "asc" ? -1 : 1;
      if (aVal > bVal) return order === "asc" ? 1 : -1;
      return 0;
    });
  }

  const { data, pagination } = paginate(filtered, page, limit);

  // An truong nhay cam truoc khi tra ve
  const safeData = data.map(sanitize);

  // Them X-Total-Count header (HATEOAS-style info)
  res.setHeader("X-Total-Count", pagination.total);
  res.setHeader("X-Request-ID", req.requestId);

  res.status(200).json({
    data: safeData,
    pagination,
  });
});

// ------------------------------------------------------------------
// GET /api/v1/users/:id
// Lay mot user theo ID
// ------------------------------------------------------------------
router.get("/:id", requireAuth, cachePrivate, (req, res) => {
  const user = users.find(
    (u) => u.id === req.params.id && u.deletedAt === null,
  );

  if (!user) {
    return res.status(404).json({
      error: "USER_NOT_FOUND",
      message: `User with id '${req.params.id}' not found`,
      resourceType: "User",
      resourceId: req.params.id,
    });
  }

  res.setHeader("X-Request-ID", req.requestId);

  // HATEOAS: Tra ve links huong dan cac hanh dong tiep theo
  res.status(200).json({
    data: sanitize(user),
    _links: {
      self: { href: `/api/v1/users/${user.id}`, method: "GET" },
      update: { href: `/api/v1/users/${user.id}`, method: "PUT" },
      patch: { href: `/api/v1/users/${user.id}`, method: "PATCH" },
      delete: { href: `/api/v1/users/${user.id}`, method: "DELETE" },
      posts: { href: `/api/v1/users/${user.id}/posts`, method: "GET" },
    },
  });
});

// ------------------------------------------------------------------
// GET /api/v1/users/:id/posts
// Lay cac bai viet cua mot user (nested resource)
// ------------------------------------------------------------------
router.get("/:id/posts", requireAuth, (req, res) => {
  const { posts } = require("../data/db");

  const user = users.find(
    (u) => u.id === req.params.id && u.deletedAt === null,
  );
  if (!user) {
    return res.status(404).json({
      error: "USER_NOT_FOUND",
      message: `User with id '${req.params.id}' not found`,
    });
  }

  const userPosts = posts.filter(
    (p) => p.authorId === req.params.id && p.deletedAt === null,
  );

  res.status(200).json({
    data: userPosts,
    total: userPosts.length,
    _links: {
      author: { href: `/api/v1/users/${user.id}`, method: "GET" },
    },
  });
});

// ------------------------------------------------------------------
// POST /api/v1/users
// Tao moi user (chi admin)
// Body: { name, email, role?, department?, age }
// ------------------------------------------------------------------
router.post("/", requireAuth, requireAdmin, noCache, (req, res) => {
  const { name, email, role = "user", department = "General", age } = req.body;

  // === Validation ===
  const errors = [];
  if (!name || name.trim().length < 2) {
    errors.push({
      field: "name",
      message: "Name is required and must be at least 2 characters",
    });
  }
  if (!email) {
    errors.push({ field: "email", message: "Email is required" });
  } else if (!isValidEmail(email)) {
    errors.push({ field: "email", message: "Must be a valid email address" });
  }
  if (age !== undefined && (isNaN(age) || age < 1 || age > 150)) {
    errors.push({
      field: "age",
      message: "Age must be a number between 1 and 150",
    });
  }
  if (!["user", "admin"].includes(role)) {
    errors.push({ field: "role", message: 'Role must be "user" or "admin"' });
  }

  if (errors.length > 0) {
    return res.status(422).json({
      error: "VALIDATION_ERROR",
      message: "Request validation failed",
      details: errors,
    });
  }

  // === Kiem tra email trung ===
  const emailExists = users.some(
    (u) => u.email === email && u.deletedAt === null,
  );
  if (emailExists) {
    return res.status(409).json({
      error: "EMAIL_ALREADY_EXISTS",
      message: "This email address is already associated with another account",
      field: "email",
    });
  }

  // === Tao user moi ===
  const now = new Date().toISOString();
  const newUser = {
    id: `usr_${uuidv4().slice(0, 8)}`,
    name: name.trim(),
    email: email.toLowerCase(),
    role,
    department,
    age: age ? parseInt(age) : null,
    createdAt: now,
    updatedAt: now,
    deletedAt: null,
  };

  users.push(newUser);

  res.setHeader("Location", `/api/v1/users/${newUser.id}`);
  res.setHeader("X-Request-ID", req.requestId);

  // 201 Created voi Location header
  res.status(201).json({
    data: sanitize(newUser),
    _links: {
      self: { href: `/api/v1/users/${newUser.id}`, method: "GET" },
    },
  });
});

// ------------------------------------------------------------------
// TINH HUONG 2: PATCH /api/v1/users/:id
// Cap nhat mot phan user (vi du: chi doi email)
// ------------------------------------------------------------------
router.patch("/:id", requireAuth, noCache, (req, res) => {
  const userIndex = users.findIndex(
    (u) => u.id === req.params.id && u.deletedAt === null,
  );

  if (userIndex === -1) {
    return res.status(404).json({
      error: "USER_NOT_FOUND",
      message: `User with id '${req.params.id}' not found`,
    });
  }

  const user = users[userIndex];

  // Phan quyen: chi admin hoac chinh user do moi sua duoc
  if (req.user.role !== "admin" && req.user.id !== user.id) {
    return res.status(403).json({
      error: "FORBIDDEN",
      message: "You can only update your own profile",
    });
  }

  const { name, email, department, age } = req.body;
  const errors = [];

  // Validate tung truong neu co trong request body
  if (name !== undefined && name.trim().length < 2) {
    errors.push({
      field: "name",
      message: "Name must be at least 2 characters",
    });
  }
  if (email !== undefined) {
    if (!isValidEmail(email)) {
      errors.push({
        field: "email",
        message: "Must be a valid email address format",
      });
    } else {
      // Kiem tra email trung voi nguoi khac
      const conflict = users.find(
        (u) => u.email === email && u.id !== user.id && u.deletedAt === null,
      );
      if (conflict) {
        return res.status(409).json({
          error: "EMAIL_ALREADY_EXISTS",
          message:
            "This email address is already associated with another account",
          field: "email",
        });
      }
    }
  }
  if (age !== undefined && (isNaN(age) || age < 1 || age > 150)) {
    errors.push({
      field: "age",
      message: "Age must be a number between 1 and 150",
    });
  }

  if (errors.length > 0) {
    return res.status(422).json({
      error: "VALIDATION_ERROR",
      message: "Validation failed",
      details: errors,
    });
  }

  // Chi cap nhat cac truong duoc gui len (PATCH - partial update)
  if (name !== undefined) users[userIndex].name = name.trim();
  if (email !== undefined) users[userIndex].email = email.toLowerCase();
  if (department !== undefined) users[userIndex].department = department;
  if (age !== undefined) users[userIndex].age = parseInt(age);
  users[userIndex].updatedAt = new Date().toISOString();

  res.setHeader("X-Request-ID", req.requestId);
  res.status(200).json({
    data: sanitize(users[userIndex]),
    message: "User updated successfully",
  });
});

// ------------------------------------------------------------------
// PUT /api/v1/users/:id
// Thay the toan bo user (can gui day du cac truong)
// ------------------------------------------------------------------
router.put("/:id", requireAuth, noCache, (req, res) => {
  const userIndex = users.findIndex(
    (u) => u.id === req.params.id && u.deletedAt === null,
  );

  if (userIndex === -1) {
    return res.status(404).json({
      error: "USER_NOT_FOUND",
      message: `User with id '${req.params.id}' not found`,
    });
  }

  if (req.user.role !== "admin" && req.user.id !== users[userIndex].id) {
    return res.status(403).json({
      error: "FORBIDDEN",
      message: "You can only update your own profile",
    });
  }

  const { name, email, department, age, role } = req.body;
  const errors = [];

  // PUT yeu cau day du cac truong bat buoc
  if (!name || name.trim().length < 2) {
    errors.push({
      field: "name",
      message: "Name is required and must be at least 2 characters",
    });
  }
  if (!email || !isValidEmail(email)) {
    errors.push({ field: "email", message: "Valid email is required" });
  }
  if (!department) {
    errors.push({ field: "department", message: "Department is required" });
  }
  if (age === undefined || isNaN(age) || age < 1 || age > 150) {
    errors.push({
      field: "age",
      message: "Age is required and must be between 1-150",
    });
  }

  if (errors.length > 0) {
    return res.status(422).json({
      error: "VALIDATION_ERROR",
      message: "Validation failed. PUT requires all fields.",
      details: errors,
    });
  }

  // Kiem tra email trung
  const conflict = users.find(
    (u) => u.email === email && u.id !== req.params.id && u.deletedAt === null,
  );
  if (conflict) {
    return res.status(409).json({
      error: "EMAIL_ALREADY_EXISTS",
      message: "This email is already in use",
      field: "email",
    });
  }

  // Thay the toan bo (giu lai id, createdAt, deletedAt)
  users[userIndex] = {
    ...users[userIndex],
    name: name.trim(),
    email: email.toLowerCase(),
    department,
    age: parseInt(age),
    role: role || users[userIndex].role,
    updatedAt: new Date().toISOString(),
  };

  res.status(200).json({
    data: sanitize(users[userIndex]),
    message: "User replaced successfully",
  });
});

// ------------------------------------------------------------------
// TINH HUONG 4: DELETE /api/v1/users/:id
// Xoa user - soft delete (chi admin)
// ------------------------------------------------------------------
router.delete("/:id", requireAuth, requireAdmin, noCache, (req, res) => {
  const userIndex = users.findIndex(
    (u) => u.id === req.params.id && u.deletedAt === null,
  );

  if (userIndex === -1) {
    // Kiem tra xem da bi xoa truoc do chua → 410 Gone
    const alreadyDeleted = users.find(
      (u) => u.id === req.params.id && u.deletedAt !== null,
    );
    if (alreadyDeleted) {
      return res.status(410).json({
        error: "GONE",
        message: `User '${req.params.id}' has already been deleted`,
        deletedAt: alreadyDeleted.deletedAt,
      });
    }
    return res.status(404).json({
      error: "USER_NOT_FOUND",
      message: `User with id '${req.params.id}' not found`,
    });
  }

  // Khong cho xoa chinh minh
  if (req.user.id === users[userIndex].id) {
    return res.status(403).json({
      error: "FORBIDDEN",
      message: "You cannot delete your own account",
    });
  }

  // Soft delete: danh dau deletedAt thay vi xoa khoi mang
  const deletedUser = { ...users[userIndex] };
  users[userIndex].deletedAt = new Date().toISOString();
  users[userIndex].updatedAt = new Date().toISOString();

  res.setHeader("X-Request-ID", req.requestId);

  // Tra ve 200 voi thong tin da xoa (audit trail)
  res.status(200).json({
    message: "User deleted successfully",
    user: {
      id: deletedUser.id,
      name: deletedUser.name,
      status: "DELETED",
      deletedAt: users[userIndex].deletedAt,
      deletedBy: req.user.id,
    },
    _actions: {
      restore: {
        href: `/api/v1/users/${deletedUser.id}/restore`,
        method: "POST",
      },
    },
  });
});

// ------------------------------------------------------------------
// POST /api/v1/users/:id/restore
// Phuc hoi user da xoa (soft delete restore)
// ------------------------------------------------------------------
router.post("/:id/restore", requireAuth, requireAdmin, noCache, (req, res) => {
  const userIndex = users.findIndex(
    (u) => u.id === req.params.id && u.deletedAt !== null,
  );

  if (userIndex === -1) {
    return res.status(404).json({
      error: "NOT_FOUND",
      message: `No deleted user found with id '${req.params.id}'`,
    });
  }

  users[userIndex].deletedAt = null;
  users[userIndex].updatedAt = new Date().toISOString();

  res.status(200).json({
    message: "User restored successfully",
    data: sanitize(users[userIndex]),
  });
});

module.exports = router;
