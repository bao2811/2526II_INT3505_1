# Đánh Giá Mức Độ RESTful của một API

> Làm thế nào để biết một API có đúng chuẩn REST không? Tài liệu này cung cấp framework đánh giá cụ thể với ví dụ thực tế.

---

## 🎯 Richardson Maturity Model — Mô hình đo độ RESTful

Được đề xuất bởi Leonard Richardson, mô hình chia API thành **4 cấp độ (Level 0-3)**:

```
Level 3: HATEOAS           ← RESTful thực sự
  ↑ Hypermedia controls
Level 2: HTTP Verbs         ← Đa số API "REST" hiện đại
  ↑ HTTP Methods + Status codes
Level 1: Resources          ← Có URI riêng cho mỗi resource
  ↑ Individual URIs
Level 0: The Swamp of POX   ← RPC qua HTTP (SOAP, XML-RPC)
```

---

## Level 0 — The Swamp of POX (Không REST)

### Đặc điểm

- Dùng HTTP chỉ như một transport protocol
- Một endpoint duy nhất cho tất cả operations
- Method chủ yếu là POST
- Không có khái niệm "resource"

### Ví dụ điển hình (SOAP-style)

```http
POST /api HTTP/1.1
Content-Type: application/xml

<request>
  <action>getUser</action>
  <params>
    <userId>42</userId>
  </params>
</request>
```

```http
POST /api HTTP/1.1
Content-Type: application/xml

<request>
  <action>deleteUser</action>
  <params>
    <userId>42</userId>
  </params>
</request>
```

### Đánh giá: ❌ Không REST (nhưng không sai — SOAP có use case riêng)

---

## Level 1 — Resources (Có URI riêng)

### Đặc điểm

- Mỗi resource có URI riêng
- Vẫn thường dùng POST cho mọi thứ
- Chưa dùng HTTP methods đúng cách

### Ví dụ

```http
POST /api/users/getById    ← Có URI nhưng dùng POST cho GET
Content-Type: application/json
{ "id": 42 }

POST /api/users/deleteById ← Action đưa vào URI
Content-Type: application/json
{ "id": 42 }

POST /api/users/updateEmail
Content-Type: application/json
{ "id": 42, "email": "new@email.com" }
```

### Đánh giá: 🟡 Tiến bộ nhưng chưa RESTful

---

## Level 2 — HTTP Verbs (Dùng đúng HTTP methods)

### Đặc điểm

- Dùng đúng HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Dùng đúng status codes
- URI là danh từ, không có động từ

### Ví dụ

```http
GET    /api/users/42       ← Lấy user
POST   /api/users          ← Tạo user mới
PUT    /api/users/42       ← Cập nhật toàn bộ user
PATCH  /api/users/42       ← Cập nhật một phần
DELETE /api/users/42       ← Xóa user
```

### Đánh giá: ✅ Đây là mức độ của hầu hết API "REST" hiện đại

---

## Level 3 — HATEOAS (RESTful hoàn chỉnh)

### Đặc điểm

- Response chứa links hướng dẫn các hành động tiếp theo
- Client không cần hardcode URLs
- API tự mô tả (self-descriptive)

### Ví dụ

```http
GET /api/users/42 HTTP/1.1

HTTP/1.1 200 OK
{
  "id": 42,
  "name": "Nguyen Van A",
  "email": "nva@example.com",
  "status": "active",
  "_links": {
    "self":      { "href": "/api/users/42",       "method": "GET" },
    "update":    { "href": "/api/users/42",       "method": "PUT" },
    "delete":    { "href": "/api/users/42",       "method": "DELETE" },
    "posts":     { "href": "/api/users/42/posts", "method": "GET" },
    "deactivate":{ "href": "/api/users/42/deactivate", "method": "POST" }
  }
}
```

### Đánh giá: ✅✅ RESTful thực sự theo định nghĩa của Roy Fielding

---

## 📋 Checklist Đánh Giá API RESTful

Dùng checklist này để đánh giá bất kỳ API nào:

### Nhóm 1: URI Design (Thiết kế URI)

| Tiêu chí                      | Tốt ✅                | Xấu ❌                    |
| ----------------------------- | --------------------- | ------------------------- |
| Dùng danh từ, không động từ   | `/api/users`          | `/api/getUsers`           |
| Dùng số nhiều cho collections | `/api/users`          | `/api/user`               |
| Quan hệ cha-con rõ ràng       | `/api/users/42/posts` | `/api/getUserPosts?id=42` |
| Lowercase và dùng dấu `-`     | `/api/order-items`    | `/api/OrderItems`         |
| Không có extension file       | `/api/users`          | `/api/users.json`         |
| Versioning trong URI          | `/api/v1/users`       | `/api/users?version=1`    |

### Nhóm 2: HTTP Methods

| Tiêu chí                         | Tốt ✅                 | Xấu ❌                 |
| -------------------------------- | ---------------------- | ---------------------- |
| GET chỉ đọc, không thay đổi data | `GET /users` → chỉ đọc | `GET /deleteUser?id=1` |
| POST để tạo mới                  | `POST /users`          | `GET /createUser`      |
| PUT/PATCH để cập nhật            | `PATCH /users/42`      | `POST /users/update`   |
| DELETE để xóa                    | `DELETE /users/42`     | `POST /users/delete`   |

### Nhóm 3: HTTP Status Codes

| Tiêu chí               | Tốt ✅               | Xấu ❌                          |
| ---------------------- | -------------------- | ------------------------------- |
| 201 khi tạo thành công | `201 Created`        | `200 OK` cho POST               |
| 204 khi không có body  | `204 No Content`     | `200 OK` với body rỗng          |
| 4xx cho lỗi client     | `404 Not Found`      | `200 OK {"error": "not found"}` |
| 5xx cho lỗi server     | `500 Internal Error` | `200 OK {"status": "error"}`    |

### Nhóm 4: Stateless

| Tiêu chí                           | Tốt ✅                          | Xấu ❌                          |
| ---------------------------------- | ------------------------------- | ------------------------------- |
| Auth trong từng request            | `Authorization: Bearer <token>` | Session cookie phụ thuộc server |
| Không có server-side session state | JWT token                       | PHP `$_SESSION`                 |

### Nhóm 5: Response Format

| Tiêu chí                 | Tốt ✅                                 | Xấu ❌                               |
| ------------------------ | -------------------------------------- | ------------------------------------ |
| Content-Type header đúng | `Content-Type: application/json`       | Thiếu Content-Type                   |
| Cấu trúc nhất quán       | Cùng format cho mọi endpoint           | Mỗi endpoint trả format khác nhau    |
| Error messages có nghĩa  | `{"error": "EMAIL_EXISTS"}`            | `{"error": "Error 1062"}` (DB error) |
| Pagination cho list      | `{"data": [...], "pagination": {...}}` | Trả về toàn bộ records               |

---

## 🔍 Ví dụ Thực Tế: Đánh Giá 2 API

### API A — Phân tích

```
Endpoints:
  POST /api/getAllUsers
  POST /api/getUserById       { "id": 42 }
  POST /api/createUser        { "name": "...", "email": "..." }
  POST /api/updateUserEmail   { "id": 42, "email": "new@..." }
  POST /api/deleteUser        { "id": 42 }

Response luôn trả về:
  HTTP 200 OK
  { "success": true/false, "data": ..., "error": "..." }
```

**Đánh giá API A:**

| Tiêu chí     | Điểm     | Ghi chú                                        |
| ------------ | -------- | ---------------------------------------------- |
| URI Design   | 1/3      | Có URI riêng nhưng dùng động từ, không danh từ |
| HTTP Methods | 0/3      | Dùng POST cho tất cả (kể cả GET, DELETE)       |
| Status Codes | 0/3      | Luôn trả 200 kể cả khi lỗi                     |
| Stateless    | 2/3      | Không rõ từ thông tin cho                      |
| HATEOAS      | 0/3      | Không có                                       |
| **Tổng**     | **3/15** | **Level 0-1 (Không RESTful)**                  |

---

### API B — Phân tích

```
Endpoints:
  GET    /api/v1/users                     → 200 + pagination
  GET    /api/v1/users/42                  → 200 hoặc 404
  POST   /api/v1/users                     → 201 + Location header
  PATCH  /api/v1/users/42                  → 200 hoặc 422
  DELETE /api/v1/users/42                  → 204 hoặc 404
  GET    /api/v1/users/42/posts            → 200

Response format nhất quán:
  Thành công: { "data": {...}, "_links": {...} }
  Lỗi:        { "error": "CODE", "message": "...", "details": [...] }

Headers:
  Cache-Control đúng cho từng endpoint
  Authorization: Bearer JWT
  Content-Type: application/json
```

**Đánh giá API B:**

| Tiêu chí     | Điểm      | Ghi chú                                         |
| ------------ | --------- | ----------------------------------------------- |
| URI Design   | 3/3       | Danh từ, số nhiều, versioning, nested resources |
| HTTP Methods | 3/3       | Dùng đúng GET/POST/PATCH/DELETE                 |
| Status Codes | 3/3       | 200/201/204/404/422 đúng ngữ cảnh               |
| Stateless    | 3/3       | JWT Bearer token                                |
| HATEOAS      | 2/3       | Có `_links` nhưng chưa đầy đủ                   |
| Cache        | 3/3       | Cache-Control headers đúng                      |
| **Tổng**     | **17/18** | **Level 3 (RESTful)**                           |

---

## 🎯 Thang Điểm Đánh Giá Nhanh

```
0-5  điểm:  ⭕ Not REST — RPC over HTTP (Level 0)
6-9  điểm:  🟡 REST-like — Level 1 (có URIs)
10-13 điểm: 🟠 Pragmatic REST — Level 2 (HTTP methods đúng)
14-16 điểm: 🟢 Good REST — Level 2-3
17-18 điểm: ✅ Full REST — Level 3 (HATEOAS)
```

---

## 💡 Nguyên tắc Thiết kế URI Chuẩn REST

```
✅ ĐÚNG:
GET    /products                   → Lấy danh sách products
GET    /products/123               → Lấy product id=123
POST   /products                   → Tạo product mới
PUT    /products/123               → Cập nhật toàn bộ product 123
PATCH  /products/123               → Cập nhật một phần product 123
DELETE /products/123               → Xóa product 123
GET    /products/123/reviews       → Lấy reviews của product 123
POST   /products/123/reviews       → Tạo review cho product 123
DELETE /products/123/reviews/456   → Xóa review 456 của product 123

❌ SAI:
GET    /getProducts
GET    /product/123/getDetails
POST   /createProduct
POST   /products/123/update
GET    /deleteProduct?id=123
POST   /products/123/reviews/deleteReview
```

---

## 📝 Bài Tập Tự Đánh Giá

Hãy đánh giá API sau theo checklist:

```
Cho API quản lý thư viện sách:
  GET  /api/books                  → { "books": [...100 books...] }
  GET  /api/books/search?q=python  → Tìm kiếm sách
  POST /api/addBook                → Thêm sách mới, trả về 200 OK
  POST /api/updateBook             → Cập nhật sách, trả về 200 OK
  POST /api/removeBook             → Xóa sách, trả về 200 OK
  GET  /api/getBooksByCategory     → Lấy theo danh mục

Response luôn:
  HTTP 200 OK
  { "status": "ok"/"error", "result": ... }
```

**Gợi ý trả lời:**

- URI: ❌ Có động từ (addBook, updateBook), không nhất quán
- Methods: ❌ POST dùng cho cả update và delete
- Status Codes: ❌ Luôn 200 kể cả khi lỗi
- Pagination: ❌ Trả về 100 books một lúc (không có pagination)
- **Level: 0-1 → Cần refactor toàn bộ**

**API sau khi refactor:**

```
GET    /api/v1/books               → 200 + pagination
GET    /api/v1/books?q=python&category=tech
POST   /api/v1/books               → 201 Created
GET    /api/v1/books/123           → 200 hoặc 404
PUT    /api/v1/books/123           → 200 hoặc 404
PATCH  /api/v1/books/123           → 200 hoặc 422
DELETE /api/v1/books/123           → 204 hoặc 404
GET    /api/v1/books/123/reviews   → 200
```
