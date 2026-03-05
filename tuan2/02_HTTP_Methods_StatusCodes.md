# HTTP Methods, Status Codes & Headers

---

## 🔧 HTTP Methods (Phương thức HTTP)

### Tổng quan

| Method  | Idempotent | Safe | Có Body | Mô tả                         |
| ------- | ---------- | ---- | ------- | ----------------------------- |
| GET     | ✅         | ✅   | ❌      | Lấy dữ liệu                   |
| POST    | ❌         | ❌   | ✅      | Tạo mới tài nguyên            |
| PUT     | ✅         | ❌   | ✅      | Thay thế toàn bộ tài nguyên   |
| PATCH   | ❌\*       | ❌   | ✅      | Cập nhật một phần tài nguyên  |
| DELETE  | ✅         | ❌   | ❌      | Xóa tài nguyên                |
| HEAD    | ✅         | ✅   | ❌      | Như GET nhưng chỉ trả headers |
| OPTIONS | ✅         | ✅   | ❌      | Hỏi server hỗ trợ methods nào |

> **Idempotent**: Gọi nhiều lần cho kết quả giống gọi 1 lần.
> **Safe**: Không thay đổi trạng thái server.
> \*PATCH có thể idempotent tùy implementation.

---

### 1️⃣ GET — Lấy dữ liệu

```http
GET /api/users HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGc...
Accept: application/json
```

**Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: max-age=60

[
  {"id": 1, "name": "Nguyen Van A", "email": "nva@example.com"},
  {"id": 2, "name": "Tran Thi B",  "email": "ttb@example.com"}
]
```

**Đặc điểm:**

- ✅ Không có request body
- ✅ Có thể được cache
- ✅ Idempotent — gọi 100 lần vẫn cho cùng kết quả
- ✅ Safe — không thay đổi dữ liệu server

---

### 2️⃣ POST — Tạo mới tài nguyên

```http
POST /api/users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer eyJhbGc...

{
  "name": "Le Van C",
  "email": "lvc@example.com",
  "password": "securePass123"
}
```

**Response:**

```http
HTTP/1.1 201 Created
Location: /api/users/3
Content-Type: application/json

{
  "id": 3,
  "name": "Le Van C",
  "email": "lvc@example.com",
  "createdAt": "2026-03-04T10:00:00Z"
}
```

**Đặc điểm:**

- ❌ Không idempotent — gọi 2 lần sẽ tạo 2 bản ghi
- ✅ Có request body
- 📍 Server quyết định URI của resource mới (trả về qua `Location` header)

---

### 3️⃣ PUT — Thay thế toàn bộ tài nguyên

```http
PUT /api/users/3 HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer eyJhbGc...

{
  "name": "Le Van C Updated",
  "email": "lvc_new@example.com",
  "phone": "0901234567"
}
```

**Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 3,
  "name": "Le Van C Updated",
  "email": "lvc_new@example.com",
  "phone": "0901234567",
  "updatedAt": "2026-03-04T11:00:00Z"
}
```

**Đặc điểm:**

- ✅ Idempotent — gọi nhiều lần cho cùng kết quả
- ⚠️ Phải gửi **toàn bộ** fields, trường nào không có sẽ bị xóa/null
- 📍 Client biết trước URI (khác POST)

---

### 4️⃣ PATCH — Cập nhật một phần tài nguyên

```http
PATCH /api/users/3 HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer eyJhbGc...

{
  "email": "lvc_patched@example.com"
}
```

**Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 3,
  "name": "Le Van C Updated",
  "email": "lvc_patched@example.com",
  "phone": "0901234567",
  "updatedAt": "2026-03-04T12:00:00Z"
}
```

**So sánh PUT vs PATCH:**
| | PUT | PATCH |
|-|-----|-------|
| Dữ liệu gửi | Toàn bộ object | Chỉ fields cần thay đổi |
| Fields bỏ sót | Bị xóa/null | Giữ nguyên |
| Bandwidth | Tốn hơn | Tiết kiệm hơn |
| Idempotent | ✅ | Tùy TH |

---

### 5️⃣ DELETE — Xóa tài nguyên

```http
DELETE /api/users/3 HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGc...
```

**Response (xóa thành công):**

```http
HTTP/1.1 204 No Content
```

**Response (xóa + trả về object đã xóa):**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "User deleted successfully",
  "deletedUser": {"id": 3, "name": "Le Van C Updated"}
}
```

**Đặc điểm:**

- ✅ Idempotent — xóa đã xóa rồi vẫn cho kết quả "không còn tồn tại"
- ✅ Thường không có request body

---

## 📊 HTTP Status Codes (Mã trạng thái HTTP)

### Nhóm 1xx — Informational (Thông tin)

| Code | Tên                 | Ý nghĩa                                              |
| ---- | ------------------- | ---------------------------------------------------- |
| 100  | Continue            | Server đã nhận headers, client tiếp tục gửi body     |
| 101  | Switching Protocols | Server đồng ý chuyển protocol (VD: HTTP → WebSocket) |

---

### Nhóm 2xx — Success (Thành công) ✅

| Code    | Tên             | Khi nào dùng                                 |
| ------- | --------------- | -------------------------------------------- |
| **200** | OK              | Request thành công, có response body         |
| **201** | Created         | POST tạo resource thành công                 |
| **202** | Accepted        | Request nhận được, đang xử lý async          |
| **204** | No Content      | Thành công nhưng không có body (DELETE, PUT) |
| 206     | Partial Content | Trả về một phần dữ liệu (range requests)     |

**Ví dụ 202 Accepted (xử lý bất đồng bộ):**

```http
HTTP/1.1 202 Accepted
Location: /api/jobs/task-123
Content-Type: application/json

{
  "jobId": "task-123",
  "status": "processing",
  "checkStatusAt": "/api/jobs/task-123"
}
```

---

### Nhóm 3xx — Redirection (Chuyển hướng) 🔄

| Code    | Tên                | Ý nghĩa                               |
| ------- | ------------------ | ------------------------------------- |
| **301** | Moved Permanently  | URL đổi vĩnh viễn                     |
| **302** | Found              | Redirect tạm thời                     |
| **304** | Not Modified       | Resource không thay đổi, dùng cache   |
| 307     | Temporary Redirect | Redirect tạm thời, giữ nguyên method  |
| 308     | Permanent Redirect | Redirect vĩnh viễn, giữ nguyên method |

**Ví dụ 304 (Cache validation):**

```http
GET /api/products HTTP/1.1
If-None-Match: "products-v42"

HTTP/1.1 304 Not Modified
ETag: "products-v42"
← Không có body, client dùng cache cũ
```

---

### Nhóm 4xx — Client Error (Lỗi phía Client) ❌

| Code    | Tên                  | Ý nghĩa                                         | Ví dụ tình huống                           |
| ------- | -------------------- | ----------------------------------------------- | ------------------------------------------ |
| **400** | Bad Request          | Request sai cú pháp/dữ liệu không hợp lệ        | JSON sai format, thiếu required field      |
| **401** | Unauthorized         | Chưa xác thực                                   | Không có/sai token                         |
| **403** | Forbidden            | Đã xác thực nhưng không có quyền                | User thường truy cập admin route           |
| **404** | Not Found            | Resource không tồn tại                          | `/api/users/999` không có user 999         |
| **405** | Method Not Allowed   | Method không được hỗ trợ                        | DELETE `/api/users` (không cho xóa tất cả) |
| **409** | Conflict             | Xung đột trạng thái                             | Email đã tồn tại khi tạo user mới          |
| **410** | Gone                 | Resource đã bị xóa vĩnh viễn                    | Bài viết đã bị xóa                         |
| **422** | Unprocessable Entity | Dữ liệu đúng format nhưng không hợp lệ về logic | `age: -5`, `email: "not-an-email"`         |
| **429** | Too Many Requests    | Vượt giới hạn rate limit                        | Gửi 1000 request/phút                      |

**Ví dụ 400 Bad Request:**

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": "VALIDATION_ERROR",
  "message": "Request validation failed",
  "details": [
    {"field": "email", "message": "Invalid email format"},
    {"field": "age",   "message": "Must be between 18 and 120"}
  ]
}
```

**Ví dụ 401 vs 403:**

```http
← 401: Bạn là ai? (Chưa đăng nhập)
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="api.example.com"

← 403: Tôi biết bạn là ai, nhưng bạn không được vào đây
HTTP/1.1 403 Forbidden
Content-Type: application/json
{"error": "INSUFFICIENT_PERMISSIONS", "required": "admin"}
```

**Ví dụ 429 Too Many Requests:**

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1741086660
Content-Type: application/json

{
  "error": "RATE_LIMIT_EXCEEDED",
  "message": "Too many requests. Retry after 60 seconds.",
  "retryAfter": 60
}
```

---

### Nhóm 5xx — Server Error (Lỗi phía Server) 🔥

| Code    | Tên                   | Ý nghĩa                                   | Nguyên nhân thường gặp        |
| ------- | --------------------- | ----------------------------------------- | ----------------------------- |
| **500** | Internal Server Error | Lỗi không xác định phía server            | Bug code, unhandled exception |
| **501** | Not Implemented       | Chức năng chưa được cài đặt               | Method chưa hỗ trợ            |
| **502** | Bad Gateway           | Gateway nhận response không hợp lệ        | Upstream server lỗi           |
| **503** | Service Unavailable   | Service tạm ngưng                         | Server quá tải, maintenance   |
| **504** | Gateway Timeout       | Gateway không nhận được response kịp thời | Upstream server quá chậm      |

**Ví dụ 500 Internal Server Error:**

```http
HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
  "error": "INTERNAL_ERROR",
  "message": "An unexpected error occurred",
  "requestId": "req-7f3a2b1c",
  "timestamp": "2026-03-04T10:30:00Z"
}
```

**Ví dụ 503 Service Unavailable:**

```http
HTTP/1.1 503 Service Unavailable
Retry-After: 300
Content-Type: application/json

{
  "error": "SERVICE_UNAVAILABLE",
  "message": "We are performing scheduled maintenance",
  "maintenanceWindow": {
    "start": "2026-03-04T10:00:00Z",
    "end":   "2026-03-04T11:00:00Z"
  }
}
```

---

## 📋 HTTP Headers Quan Trọng

### Request Headers

| Header              | Mô tả                              | Ví dụ                           |
| ------------------- | ---------------------------------- | ------------------------------- |
| `Authorization`     | Thông tin xác thực                 | `Bearer eyJhbGc...`             |
| `Content-Type`      | Kiểu dữ liệu của body              | `application/json`              |
| `Accept`            | Kiểu dữ liệu muốn nhận             | `application/json, text/xml`    |
| `Accept-Language`   | Ngôn ngữ mong muốn                 | `vi-VN, en-US;q=0.9`            |
| `If-None-Match`     | ETag để validate cache             | `"abc123"`                      |
| `If-Modified-Since` | Kiểm tra resource đã thay đổi chưa | `Wed, 04 Mar 2026 10:00:00 GMT` |
| `User-Agent`        | Thông tin về client                | `Mozilla/5.0...`                |
| `X-Request-ID`      | ID để trace request                | `req-7f3a2b1c`                  |

### Response Headers

| Header                        | Mô tả                          | Ví dụ                             |
| ----------------------------- | ------------------------------ | --------------------------------- |
| `Content-Type`                | Kiểu dữ liệu của response body | `application/json; charset=utf-8` |
| `Location`                    | URI của resource mới tạo (201) | `/api/users/3`                    |
| `Cache-Control`               | Chỉ thị caching                | `public, max-age=3600`            |
| `ETag`                        | Phiên bản của resource         | `"v42"`                           |
| `X-RateLimit-Limit`           | Giới hạn request tối đa        | `100`                             |
| `X-RateLimit-Remaining`       | Số request còn lại             | `45`                              |
| `Retry-After`                 | Thời gian chờ trước khi retry  | `60`                              |
| `Access-Control-Allow-Origin` | CORS policy                    | `https://app.example.com`         |
