# Flow 5: Case Study - Phát hiện Lỗi trong API Poorly Designed

## Mục tiêu
Phân tích một API thiết kế tồi tệ, xác định các vấn đề, và đề xuất giải pháp cải thiện.

## Case Study 1: E-commerce API

### API Hiện tại (Poorly Designed)

```
Endpoint list:
1) GET /getallproducts → Lấy danh sách products
2) GET /getproduct → Lấy product chi tiết (query param: ?prod_id=123)
3) POST /addproduct → Thêm product mới (admin only)
4) GET /searchItems → Search products (query: ?keyword=xxx)
5) POST /checkout → Tạo order
6) GET /getOrder → Lấy order info (query: ?OrderID=123)
7) POST /cancelorder → Cancel order (query: ?orderid=123)
8) GET /user/profile → Lấy user info
9) POST /user/update → Cập nhật user
10) POST /login → Login
11) GET /logout → Logout
12) POST /payment/process → Process payment
13) GET /Admin/Reports → Admin reports
```

### Response Format

```json
// Success (sometimes):
{
  "code": 200,
  "response": [
    { "prod_id": 1, "prod_name": "Laptop", "price": 1000 }
  ]
}

// Success (sometimes khác):
{
  "status": "ok",
  "data": { "id": 1, "name": "John" }
}

// Error (inconsistent):
{
  "error": "Invalid request"
}

// Sometimes only:
{
  "message": "Product not found"
}
```

---

## Issues Found - Phát hiện các vấn đề

### ❌ Issue 1: Inconsistent Naming Convention

**Vấn đề:**
- Verb-based endpoints: `GET /getallproducts`, `GET /getproduct`
- Nên là: `GET /products`, `GET /products/{id}`
- Inconsistent naming: `prod_id` vs `OrderID` vs `orderid`
- CamelCase và lowercase mixed

**Impact:**
- Khó nhớ
- Khó maintain
- Không professional

**Fix:**
```
GET    /api/v1/products              → GET /getallproducts
GET    /api/v1/products/{id}         → GET /getproduct?prod_id=123
POST   /api/v1/products              → POST /addproduct
GET    /api/v1/products?search=xxx   → GET /searchItems?keyword=xxx
```

---

### ❌ Issue 2: Inconsistent Response Format

**Vấn đề:**
- Một endpoint trả `code`, một trả `status`
- Fields không consistent: `response` vs `data`
- Lúc success, lúc error không có pattern

**Impact:**
- Client code phức tạp
- Khó maintain
- Bug prone

**Fix:**
```json
// Consistent response format
{
  "status": "success",
  "data": { ... },
  "meta": { ... }
}

// Consistent error format
{
  "status": "error",
  "error": {
    "code": "INVALID_PRODUCT_ID",
    "message": "Product with ID 123 not found"
  }
}
```

---

### ❌ Issue 3: Wrong HTTP Methods

**Vấn đề:**
```
POST   /cancelorder          # Cancel nên dùng DELETE không POST
GET    /logout               # Logout nên dùng POST không GET
GET    /user/update          # Update nên dùng PUT/PATCH không GET
```

**Impact:**
- Vi phạm REST principles
- Caching issues (GET không nên có side effects)
- Security issues

**Fix:**
```
DELETE /api/v1/orders/{id}           → POST /cancelorder
POST   /api/v1/auth/logout           → GET /logout
PUT    /api/v1/users/{id}            → POST /user/update
PATCH  /api/v1/users/{id}            → POST /user/update
```

---

### ❌ Issue 4: Inconsistent Parameter Names

**Vấn đề:**
- `prod_id`, `OrderID`, `orderid` - 3 cách khác nhau
- Query params vs body params không clear
- Không có documentation

**Impact:**
- Client developers confused
- Typos easily happen
- Hard to maintain

**Fix:**
```
Standardize:
- Naming: id (không prod_id, OrderID, orderid)
- Case: lowercase (không OrderID)
- Documentation: Clear examples
```

---

### ❌ Issue 5: Missing Versioning

**Vấn đề:**
- Không có API version
- Nếu breaking change, clients break
- No deprecation path

**Impact:**
- Can't evolve API safely
- Old clients break

**Fix:**
```
Add versioning:
GET /api/v1/products
POST /api/v1/orders

Can have v2 for breaking changes:
GET /api/v2/products (nếu response format changes)
```

---

### ❌ Issue 6: No Proper Nested Resources

**Vấn đề:**
```
GET /getOrder?OrderID=123
GET /order/items?order_id=123
POST /checkout → Tạo order nhưng response không rõ
```

Nên có nested structure:
```
GET    /api/v1/orders/{id}           # Order details
GET    /api/v1/orders/{id}/items     # Order items
POST   /api/v1/orders/{id}/cancel    # Cancel action
GET    /api/v1/orders/{id}/status    # Status
```

**Fix:** Use nested resource pattern

---

### ❌ Issue 7: No Status Codes Documentation

**Vấn đề:**
- Responses không có clear status codes
- POST /addproduct - returns 200? 201? 400? 409?
- Error handling unclear

**Impact:**
- Clients don't know what to expect
- No proper error handling

**Fix:**
```
POST /api/v1/products
- 201 Created (success)
- 400 Bad Request (missing fields)
- 409 Conflict (product already exists)
- 422 Unprocessable Entity (validation fails)
```

---

### ❌ Issue 8: No Pagination

**Vấn đề:**
```
GET /getallproducts → Trả tất cả products?
```

Với 1 triệu products, response rất lớn:
- Slow network
- Memory issues
- Bad UX

**Fix:**
```
GET /api/v1/products?page=1&limit=20
Response:
{
  "status": "success",
  "data": [...],
  "meta": {
    "total": 1000000,
    "page": 1,
    "limit": 20,
    "pages": 50000
  }
}
```

---

### ❌ Issue 9: No Filtering/Sorting

**Vấn đề:**
```
GET /searchItems?keyword=xxx
```

- Chỉ search, không filter/sort
- Muốn products theo price? Không có endpoint
- Muốn products theo category? Không có endpoint

**Fix:**
```
GET /api/v1/products?category=electronics&min-price=100&max-price=1000&sort-by=price&order=asc
```

---

### ❌ Issue 10: Security Issues

**Vấn đề:**
```
GET /logout                  # LogOut via GET = CSRF issue
GET /Admin/Reports           # Admin endpoints not protected?
```

**Fix:**
```
POST /api/v1/auth/logout          # Use POST/DELETE for state change
GET  /api/v1/admin/reports        # Add auth header requirement
+ Include rate limiting
+ Input validation (422 errors)
```

---

## Summary of Issues

| Issue | Severity | Impact |
|-------|----------|--------|
| Inconsistent naming | High | Confusing, hard to remember |
| Inconsistent response format | High | Client code complex |
| Wrong HTTP methods | High | Not RESTful, CSRF issues |
| Missing versioning | High | Can't evolve safely |
| No pagination | High | Performance issues |
| Inconsistent parameter names | Medium | Easy to make mistakes |
| No nested resources | Medium | Hard to understand relationships |
| No status codes doc | Medium | Unclear error handling |
| No filtering/sorting | Medium | Limited functionality |
| Security concerns | Medium | CSRF, auth issues |

---

## Proposed Refactored API

### Base URL: `https://api.ecommerce.com/v1`

```
# ========== PRODUCTS ==========
GET    /products                          # List all products
POST   /products                          # Create product (admin)
GET    /products/{id}                     # Get product
PUT    /products/{id}                     # Update product (admin)
DELETE /products/{id}                     # Delete product (admin)
GET    /products?category=books&min-price=10&max-price=100&sort=price&order=asc

# ========== ORDERS ==========
GET    /orders                            # Get user's orders
POST   /orders                            # Create order
GET    /orders/{id}                       # Get order details
GET    /orders/{id}/items                 # Get order items
PATCH  /orders/{id}                       # Update order (partial)
DELETE /orders/{id}                       # Cancel order

# ========== CART ==========
GET    /cart                              # Get current cart
POST   /cart/items                        # Add to cart
PUT    /cart/items/{itemId}               # Update cart item quantity
DELETE /cart/items/{itemId}               # Remove from cart
POST   /cart/checkout                     # Create order from cart

# ========== PAYMENT ==========
POST   /payments                          # Process payment
GET    /payments/{id}                     # Get payment status

# ========== AUTH ==========
POST   /auth/login                        # Login
POST   /auth/logout                       # Logout
POST   /auth/register                     # Register
POST   /auth/refresh-token                # Refresh token

# ========== USERS ==========
GET    /users/me                          # Get current user
PUT    /users/me                          # Update current user
GET    /users/{id}                        # Get user (admin)
PUT    /users/{id}                        # Update user (admin)

# ========== ADMIN ==========
GET    /admin/reports                     # Admin reports
GET    /admin/products                    # Manage products
POST   /admin/products                    # Create product
```

### Consistent Response Format

```json
{
  "status": "success",
  "data": { ... },
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 20,
    "pages": 5
  }
}
```

### Status Codes

```
200 OK              - General success
201 Created         - Resource created
204 No Content      - Success with no body
400 Bad Request     - Invalid request format
401 Unauthorized    - Not authenticated
403 Forbidden       - Not authorized/allowed
404 Not Found       - Resource not found
409 Conflict        - Duplicate/conflict
422 Unprocessable   - Validation error
429 Too Many Req    - Rate limited
500 Server Error    - Server error
```

---

## Lesson Learned

### Anti-patterns to Avoid:
1. ❌ Verb-based endpoints
2. ❌ Inconsistent naming/response format
3. ❌ Wrong HTTP methods
4. ❌ No versioning
5. ❌ Missing pagination
6. ❌ No filtering/sorting
7. ❌ Security issues (GET for logout, etc)

### Best Practices to Follow:
1. ✅ Resource-based endpoints
2. ✅ Consistent naming & format
3. ✅ Correct HTTP methods
4. ✅ API versioning
5. ✅ Pagination support
6. ✅ Filtering/sorting
7. ✅ Security-first design

---

## Bài tập thực hành

1. **Analyze:** Chọn một poorly-designed API (có thể là API cũ của dự án bạn)
2. **Document:** List tất cả issues tương tự
3. **Evaluate:** Assign severity cho mỗi issue
4. **Refactor:** Propose refactored API design
5. **Justify:** Giải thích tại sao refactored design tốt hơn

---
**Tiếp theo**: [Flow 6 - Peer Review](../6-peer-review/README.md)
