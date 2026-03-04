# REST API Practice - Hướng dẫn sử dụng

> Thực hành xây dựng RESTful API với Node.js + Express  
> Môn INT3505 — Tuần 2

---

## 🚀 Khởi động nhanh

```bash
# 1. Vào thư mục project
cd tuan2/rest-api-practice

# 2. Cài đặt dependencies
npm install

# 3. Chạy server (development mode - tự reload khi sửa code)
npm run dev

# Hoặc chạy bình thường
npm start
```

Server chạy tại: **http://localhost:3000**

---

## 🔑 Xác thực (Authentication)

API dùng **Bearer Token** (minh họa nguyên tắc **Stateless**).

Thêm header vào mọi request cần xác thực:

```
Authorization: Bearer <token>
```

| Token         | Role  | Quyền                        |
| ------------- | ----- | ---------------------------- |
| `token-admin` | admin | Toàn quyền                   |
| `token-user`  | user  | Xem + sửa thông tin của mình |
| `token-user3` | user  | Xem + sửa thông tin của mình |

---

## 📋 Danh sách Endpoints

```
GET    /                           → API info + HATEOAS links
GET    /api/v1                     → Danh sách endpoints

GET    /api/v1/users               → Danh sách users (cần auth)
POST   /api/v1/users               → Tạo user (chỉ admin)
GET    /api/v1/users/:id           → Chi tiết user
PUT    /api/v1/users/:id           → Thay thế toàn bộ user
PATCH  /api/v1/users/:id           → Cập nhật một phần
DELETE /api/v1/users/:id           → Xóa user (soft delete, chỉ admin)
POST   /api/v1/users/:id/restore   → Phục hồi user đã xóa
GET    /api/v1/users/:id/posts     → Bài viết của user

GET    /api/v1/posts               → Danh sách bài viết
POST   /api/v1/posts               → Tạo bài viết (cần auth)
GET    /api/v1/posts/:id           → Chi tiết bài viết
PATCH  /api/v1/posts/:id           → Cập nhật bài viết
DELETE /api/v1/posts/:id           → Xóa bài viết (soft delete)

GET    /api/v1/products            → Tìm kiếm sản phẩm
GET    /api/v1/products/:id        → Chi tiết sản phẩm

GET    /api/v1/orders              → Đơn hàng của tôi (cần auth)
POST   /api/v1/orders              → Tạo đơn hàng (cần auth)
GET    /api/v1/orders/:id          → Chi tiết đơn hàng
```

---

## 🧪 Ví dụ thực hành với curl

### Tình huống 1 — Lấy danh sách users (phân trang, filter)

```bash
# Lấy trang 1, 2 người/trang, phòng Engineering
curl "http://localhost:3000/api/v1/users?department=Engineering&page=1&limit=2" \
  -H "Authorization: Bearer token-admin"
```

### Tình huống 2 — Cập nhật email (PATCH)

```bash
# PATCH: chỉ gửi trường cần thay đổi
curl -X PATCH "http://localhost:3000/api/v1/users/usr_002" \
  -H "Authorization: Bearer token-admin" \
  -H "Content-Type: application/json" \
  -d '{"email": "new_email@example.com"}'

# Test lỗi 409: email đã tồn tại
curl -X PATCH "http://localhost:3000/api/v1/users/usr_002" \
  -H "Authorization: Bearer token-admin" \
  -H "Content-Type: application/json" \
  -d '{"email": "nvan@example.com"}'

# Test lỗi 422: email sai format
curl -X PATCH "http://localhost:3000/api/v1/users/usr_002" \
  -H "Authorization: Bearer token-admin" \
  -H "Content-Type: application/json" \
  -d '{"email": "not-valid"}'
```

### Tình huống 3 — Tạo đơn hàng (POST + Idempotency-Key)

```bash
# Tạo đơn hàng
curl -X POST "http://localhost:3000/api/v1/orders" \
  -H "Authorization: Bearer token-user" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: my-order-key-001" \
  -d '{
    "items": [{"productId": "prod_001", "quantity": 1}],
    "shippingAddress": {
      "fullName": "Nguyen Van Test",
      "phone": "0901234567",
      "street": "123 Pho Hue",
      "city": "Ha Noi"
    },
    "paymentMethod": "CREDIT_CARD"
  }'

# Gọi lại với CÙNG Idempotency-Key → không tạo đơn mới
curl -X POST "http://localhost:3000/api/v1/orders" \
  -H "Authorization: Bearer token-user" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: my-order-key-001" \
  -d '{
    "items": [{"productId": "prod_001", "quantity": 1}],
    "shippingAddress": {
      "fullName": "Nguyen Van Test",
      "phone": "0901234567",
      "street": "123 Pho Hue",
      "city": "Ha Noi"
    },
    "paymentMethod": "CREDIT_CARD"
  }'
```

### Tình huống 4 — Xóa bài viết (Soft Delete)

```bash
# Xóa bài viết (admin)
curl -X DELETE "http://localhost:3000/api/v1/posts/post_001" \
  -H "Authorization: Bearer token-admin" \
  -H "X-Delete-Reason: SPAM_CONTENT"

# Xóa bởi user thường không phải tác giả → 403
curl -X DELETE "http://localhost:3000/api/v1/posts/post_003" \
  -H "Authorization: Bearer token-user"

# Truy cập bài đã xóa → 410 Gone
curl "http://localhost:3000/api/v1/posts/post_001"
```

### Tình huống 5 — Tìm kiếm sản phẩm (GET + Cache)

```bash
# Tìm kiếm laptop, lọc giá, brand
curl "http://localhost:3000/api/v1/products?q=laptop&brand=ASUS,MSI&price_min=20000000&in_stock=true&sort=price&order=asc"

# Không có kết quả → vẫn 200 OK (không phải 404)
curl "http://localhost:3000/api/v1/products?q=nonexistentproduct123"

# Cache: lần 2 với If-None-Match → 304 Not Modified
ETAG=$(curl -s -I "http://localhost:3000/api/v1/products" | grep -i etag | awk '{print $2}' | tr -d '\r')
curl -s -o /dev/null -w "%{http_code}" "http://localhost:3000/api/v1/products" \
  -H "If-None-Match: $ETAG"
```

---

## ⚠️ Kiểm tra các mã lỗi HTTP

```bash
# 401 — Không có token
curl "http://localhost:3000/api/v1/users"

# 401 — Token sai
curl "http://localhost:3000/api/v1/users" \
  -H "Authorization: Bearer invalid-token"

# 403 — User thường cố tạo user mới (cần admin)
curl -X POST "http://localhost:3000/api/v1/users" \
  -H "Authorization: Bearer token-user" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"t@t.com","age":20}'

# 404 — User không tồn tại
curl "http://localhost:3000/api/v1/users/usr_999" \
  -H "Authorization: Bearer token-admin"

# 409 — Email đã tồn tại
curl -X POST "http://localhost:3000/api/v1/users" \
  -H "Authorization: Bearer token-admin" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"nvan@example.com","age":20}'

# 422 — Dữ liệu không hợp lệ
curl -X POST "http://localhost:3000/api/v1/users" \
  -H "Authorization: Bearer token-admin" \
  -H "Content-Type: application/json" \
  -d '{"name":"X","email":"bad","age":200}'

# 429 — Gọi nhiều lần (rate limit: 30 req/phút)
for i in $(seq 1 35); do
  curl -s -o /dev/null -w "$i: %{http_code}\n" \
    "http://localhost:3000/api/v1/products"
done
```

---

## 🧪 Chạy test tự động

```bash
# Trong một terminal: chạy server
npm run dev

# Trong terminal khác: chạy tests
npm test
```

---

## 🗂️ Cấu trúc project

```
rest-api-practice/
├── package.json
├── src/
│   ├── server.js                  ← Entry point
│   ├── data/
│   │   └── db.js                  ← In-memory "database"
│   ├── middleware/
│   │   ├── auth.js                ← Xác thực Bearer token (Stateless)
│   │   ├── rateLimit.js           ← Rate limiting (429)
│   │   ├── cacheHeaders.js        ← Cache-Control headers (Cacheable)
│   │   └── requestLogger.js       ← Log requests (Layered System)
│   ├── routes/
│   │   ├── users.js               ← CRUD Users (tình huống 1, 2, 4)
│   │   ├── posts.js               ← CRUD Posts (tình huống 4)
│   │   ├── products.js            ← Search Products (tình huống 5)
│   │   └── orders.js              ← Orders (tình huống 3)
│   └── utils/
│       └── helpers.js             ← Paginate, ETag, validate...
└── tests/
    └── test-runner.js             ← Test thủ công (không cần lib)
```

---

## 🎯 Nguyên tắc REST được minh họa

| Nguyên tắc            | Được áp dụng ở đâu                                                    |
| --------------------- | --------------------------------------------------------------------- |
| **Stateless**         | `middleware/auth.js` — Bearer token, không session                    |
| **Client-Server**     | Express server tách biệt hoàn toàn với "client" (curl/test)           |
| **Cacheable**         | `middleware/cacheHeaders.js`, ETag trong products                     |
| **Uniform Interface** | URI `/api/v1/resource/:id`, HTTP methods đúng, HATEOAS `_links`       |
| **Layered System**    | `requestLogger.js`, `rateLimit.js`, `auth.js` như các tầng riêng biệt |
