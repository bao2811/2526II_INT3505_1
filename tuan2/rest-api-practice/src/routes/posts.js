// src/routes/posts.js
// ============================================================
// CRUD Posts - minh hoa tinh huong 4 (xoa bai viet - soft delete)
//   - GET    /api/v1/posts         → Danh sach bai viet
//   - GET    /api/v1/posts/:id     → Mot bai viet
//   - POST   /api/v1/posts         → Tao bai viet moi
//   - PATCH  /api/v1/posts/:id     → Cap nhat bai viet
//   - DELETE /api/v1/posts/:id     → Xoa bai viet (soft delete)
// ============================================================

const express = require("express");
const router = express.Router();

const { posts, uuidv4 } = require("../data/db");
const { requireAuth, requireAdmin } = require("../middleware/auth");
const { cachePublic, noCache } = require("../middleware/cacheHeaders");
const { paginate, sanitize } = require("../utils/helpers");

// ------------------------------------------------------------------
// GET /api/v1/posts
// Lay danh sach bai viet (public - co the cache)
// ------------------------------------------------------------------
router.get("/", cachePublic, (req, res) => {
  const { page, limit, status, authorId, tag } = req.query;

  let filtered = posts.filter((p) => p.deletedAt === null);

  // Neu chua dang nhap: chi thay published
  // (Lay tu header Authorization gia lap don gian)
  const isLoggedIn = req.headers["authorization"];
  if (!isLoggedIn) {
    filtered = filtered.filter((p) => p.status === "published");
  } else if (status) {
    filtered = filtered.filter((p) => p.status === status);
  }

  if (authorId) filtered = filtered.filter((p) => p.authorId === authorId);
  if (tag) filtered = filtered.filter((p) => p.tags.includes(tag));

  // Sap xep moi nhat len dau
  filtered.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

  const { data, pagination } = paginate(filtered, page, limit);

  res.setHeader("X-Total-Count", pagination.total);

  res.status(200).json({ data, pagination });
});

// ------------------------------------------------------------------
// GET /api/v1/posts/:id
// ------------------------------------------------------------------
router.get("/:id", (req, res) => {
  const post = posts.find(
    (p) => p.id === req.params.id && p.deletedAt === null,
  );

  if (!post) {
    // Kiem tra da xoa chua
    const deleted = posts.find(
      (p) => p.id === req.params.id && p.deletedAt !== null,
    );
    if (deleted) {
      return res.status(410).json({
        error: "GONE",
        message: "This post has been deleted",
        deletedAt: deleted.deletedAt,
      });
    }
    return res.status(404).json({
      error: "POST_NOT_FOUND",
      message: `Post with id '${req.params.id}' not found`,
    });
  }

  res.status(200).json({
    data: post,
    _links: {
      self: { href: `/api/v1/posts/${post.id}`, method: "GET" },
      author: { href: `/api/v1/users/${post.authorId}`, method: "GET" },
      update: { href: `/api/v1/posts/${post.id}`, method: "PATCH" },
      delete: { href: `/api/v1/posts/${post.id}`, method: "DELETE" },
    },
  });
});

// ------------------------------------------------------------------
// POST /api/v1/posts — Tao bai viet moi
// ------------------------------------------------------------------
router.post("/", requireAuth, noCache, (req, res) => {
  const { title, content, tags = [], status = "draft" } = req.body;

  const errors = [];
  if (!title || title.trim().length < 3) {
    errors.push({
      field: "title",
      message: "Title is required and must be at least 3 characters",
    });
  }
  if (!content || content.trim().length < 10) {
    errors.push({
      field: "content",
      message: "Content is required and must be at least 10 characters",
    });
  }
  if (!["published", "draft"].includes(status)) {
    errors.push({
      field: "status",
      message: 'Status must be "published" or "draft"',
    });
  }

  if (errors.length > 0) {
    return res.status(422).json({ error: "VALIDATION_ERROR", details: errors });
  }

  const now = new Date().toISOString();
  const newPost = {
    id: `post_${uuidv4().slice(0, 8)}`,
    title: title.trim(),
    content: content.trim(),
    authorId: req.user.id,
    status,
    tags: Array.isArray(tags) ? tags : [],
    createdAt: now,
    updatedAt: now,
    deletedAt: null,
  };

  posts.push(newPost);

  res.setHeader("Location", `/api/v1/posts/${newPost.id}`);
  res.status(201).json({ data: newPost });
});

// ------------------------------------------------------------------
// PATCH /api/v1/posts/:id
// ------------------------------------------------------------------
router.patch("/:id", requireAuth, noCache, (req, res) => {
  const postIndex = posts.findIndex(
    (p) => p.id === req.params.id && p.deletedAt === null,
  );

  if (postIndex === -1) {
    return res.status(404).json({
      error: "POST_NOT_FOUND",
      message: `Post with id '${req.params.id}' not found`,
    });
  }

  // Chi tac gia hoac admin moi sua duoc
  if (req.user.role !== "admin" && posts[postIndex].authorId !== req.user.id) {
    return res.status(403).json({
      error: "FORBIDDEN",
      message: "You can only update your own posts",
    });
  }

  const { title, content, status, tags } = req.body;
  if (title !== undefined) posts[postIndex].title = title.trim();
  if (content !== undefined) posts[postIndex].content = content.trim();
  if (status !== undefined) posts[postIndex].status = status;
  if (tags !== undefined) posts[postIndex].tags = tags;
  posts[postIndex].updatedAt = new Date().toISOString();

  res.status(200).json({ data: posts[postIndex] });
});

// ------------------------------------------------------------------
// TINH HUONG 4: DELETE /api/v1/posts/:id (Soft delete + audit)
// ------------------------------------------------------------------
router.delete("/:id", requireAuth, noCache, (req, res) => {
  const postIndex = posts.findIndex(
    (p) => p.id === req.params.id && p.deletedAt === null,
  );

  if (postIndex === -1) {
    return res.status(404).json({
      error: "POST_NOT_FOUND",
      message: `Post with id '${req.params.id}' not found`,
      resourceType: "Post",
      resourceId: req.params.id,
    });
  }

  // Phan quyen: chi tac gia hoac admin
  if (req.user.role !== "admin" && posts[postIndex].authorId !== req.user.id) {
    return res.status(403).json({
      error: "FORBIDDEN",
      message: "You do not have permission to delete this post",
      requiredRole: "admin or post author",
      currentRole: req.user.role,
    });
  }

  // Soft delete
  const reason = req.headers["x-delete-reason"] || "NO_REASON";
  posts[postIndex].deletedAt = new Date().toISOString();
  posts[postIndex].updatedAt = new Date().toISOString();
  posts[postIndex]._deletedBy = req.user.id;
  posts[postIndex]._deleteReason = reason;

  res.status(200).json({
    message: "Post deleted successfully",
    post: {
      id: posts[postIndex].id,
      title: posts[postIndex].title,
      status: "DELETED",
      deletedAt: posts[postIndex].deletedAt,
      deletedBy: req.user.id,
      reason,
    },
    _actions: {
      restore: {
        href: `/api/v1/posts/${posts[postIndex].id}/restore`,
        method: "POST",
      },
    },
  });
});

module.exports = router;
