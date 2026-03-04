// src/middleware/auth.js
// Middleware: Kiem tra xac thuc (minh hoa nguyen tac Stateless - dung token)
//
// He thong nay dung "fake token" de don gian hoa (khong can JWT library)
// Token hop le: "token-admin" (role: admin), "token-user" (role: user)

const FAKE_TOKENS = {
  "token-admin": { id: "usr_001", name: "Nguyen Van An", role: "admin" },
  "token-user": { id: "usr_002", name: "Tran Thi Bich", role: "user" },
  "token-user3": { id: "usr_003", name: "Le Van Cuong", role: "user" },
};

/**
 * Middleware bat buoc phai co token hop le
 * Neu khong co → 401 Unauthorized
 */
const requireAuth = (req, res, next) => {
  const authHeader = req.headers["authorization"];

  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return res.status(401).json({
      error: "UNAUTHORIZED",
      message:
        'Authentication required. Include "Authorization: Bearer <token>" header.',
      hint: "Valid tokens: token-admin, token-user, token-user3",
    });
  }

  const token = authHeader.slice(7); // Bỏ "Bearer "
  const user = FAKE_TOKENS[token];

  if (!user) {
    return res.status(401).json({
      error: "INVALID_TOKEN",
      message: "The provided token is invalid or has expired.",
      hint: "Valid tokens: token-admin, token-user, token-user3",
    });
  }

  // Gan thong tin user vao request de cac route su dung
  req.user = user;
  next();
};

/**
 * Middleware chi cho phep admin
 * Phai goi requireAuth truoc
 * Neu khong du quyen → 403 Forbidden
 */
const requireAdmin = (req, res, next) => {
  if (!req.user) {
    return res
      .status(401)
      .json({ error: "UNAUTHORIZED", message: "Authentication required." });
  }

  if (req.user.role !== "admin") {
    return res.status(403).json({
      error: "FORBIDDEN",
      message: "Insufficient permissions. Admin role required.",
      requiredRole: "admin",
      yourRole: req.user.role,
    });
  }

  next();
};

module.exports = { requireAuth, requireAdmin };
