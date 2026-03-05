# Phân Tích Mã Lỗi HTTP

> Hướng dẫn chi tiết cách nhận diện, phân tích nguyên nhân và xử lý các HTTP error codes phổ biến.

---

## 🔴 400 Bad Request — Yêu cầu không hợp lệ

### Mô tả

Server không thể xử lý request vì **cú pháp không đúng** hoặc **dữ liệu không hợp lệ**. Lỗi hoàn toàn do **phía client**.

### Nguyên nhân phổ biến

- JSON/XML bị lỗi cú pháp (dấu phẩy thừa, thiếu ngoặc...)
- Thiếu required fields
- Sai kiểu dữ liệu (gửi string khi cần number)
- Query parameter không hợp lệ

### Ví dụ tình huống

```http
POST /api/users HTTP/1.1
Content-Type: application/json

{
  "name": "Nguyen Van A",
  "email": "not-an-email",  ← Email không hợp lệ
  "age": "twenty-five",      ← Nên là number, không phải string
                              ← Thiếu required field "password"
}                             ← JSON có trailing comma
```

### Response

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": "BAD_REQUEST",
  "message": "Request body contains invalid JSON or missing required fields",
  "details": [
    { "field": "email",    "message": "Invalid email format" },
    { "field": "age",      "message": "Must be a number between 1-150" },
    { "field": "password", "message": "This field is required" }
  ]
}
```

### Cách xử lý (phía client)

```
1. Kiểm tra lại format dữ liệu gửi lên
2. Validate dữ liệu phía client trước khi gửi
3. Đọc kỹ error.details để biết field nào sai
4. Không nên retry tự động → cần user fix dữ liệu
```

---

## 🔒 401 Unauthorized — Chưa xác thực

### Mô tả

Request thiếu credentials hợp lệ. Server không biết bạn là ai. **Tên gây nhầm lẫn** — thực ra nên gọi là "Unauthenticated".

### Nguyên nhân phổ biến

- Không có `Authorization` header
- Token đã hết hạn (expired)
- Token sai định dạng
- API key không hợp lệ

### Ví dụ tình huống

```http
GET /api/profile HTTP/1.1
← Không có Authorization header

HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="api.example.com", error="missing_token"
Content-Type: application/json

{
  "error": "UNAUTHORIZED",
  "message": "Authentication required",
  "hint": "Include 'Authorization: Bearer <token>' header"
}
```

### Ví dụ token hết hạn

```http
GET /api/profile HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.EXPIRED.signature

HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer error="invalid_token", error_description="Token has expired"

{
  "error": "TOKEN_EXPIRED",
  "message": "Your access token has expired",
  "expiredAt": "2026-03-04T09:00:00Z",
  "hint": "Use your refresh token to get a new access token"
}
```

### Cách xử lý

```
1. Kiểm tra token còn hạn không (check exp claim trong JWT)
2. Nếu có refresh token → tự động lấy access token mới
3. Nếu không có refresh token → redirect user đến trang đăng nhập
4. Lưu ý: 401 có thể retry sau khi re-authenticate
```

---

## 🚫 403 Forbidden — Không có quyền truy cập

### Mô tả

Server biết bạn là ai, nhưng bạn **không được phép** thực hiện hành động này. Khác với 401 — ở đây bạn đã xác thực rồi, nhưng thiếu quyền.

### Nguyên nhân phổ biến

- User thường cố truy cập endpoint của admin
- User cố xóa/sửa tài nguyên của người khác
- Feature bị tắt cho account của bạn
- IP bị block

### Ví dụ tình huống

```http
DELETE /api/users/42 HTTP/1.1
Authorization: Bearer <token_of_regular_user>

HTTP/1.1 403 Forbidden
Content-Type: application/json

{
  "error": "FORBIDDEN",
  "message": "Insufficient permissions to delete users",
  "requiredPermission": "users:delete",
  "yourPermissions": ["users:read", "users:update:self"]
}
```

### So sánh 401 vs 403

```
401 Unauthorized:
  → "Bạn là ai? Hãy đăng nhập đi"
  → Có thể fix bằng cách đăng nhập

403 Forbidden:
  → "Tôi biết bạn là ai, nhưng bạn không được vào đây"
  → KHÔNG thể fix bằng cách đăng nhập lại với cùng tài khoản
  → Cần quyền cao hơn (role admin, subscription premium...)
```

### Cách xử lý

```
1. KHÔNG retry tự động
2. Hiển thị thông báo "Bạn không có quyền thực hiện thao tác này"
3. Nếu cần, hướng dẫn user liên hệ admin để được cấp quyền
4. Log lại để phát hiện tấn công brute force
```

---

## 🔍 404 Not Found — Không tìm thấy tài nguyên

### Mô tả

Server không tìm thấy resource được yêu cầu. **Phổ biến nhất** trong các HTTP errors.

### Nguyên nhân phổ biến

- ID không tồn tại trong database
- URL sai (typo, đường dẫn đã thay đổi)
- Resource đã bị xóa (dùng 410 nếu muốn rõ ràng hơn)
- Case-sensitive URL

### Ví dụ tình huống

```http
GET /api/users/99999 HTTP/1.1

HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "error": "NOT_FOUND",
  "message": "User with id '99999' not found",
  "resourceType": "User",
  "resourceId": "99999"
}
```

### 404 vs 410 Gone

```
404 Not Found:
  → Resource chưa bao giờ tồn tại
  → Hoặc không tiết lộ thông tin về sự tồn tại (security)
  → Search engine sẽ retry sau

410 Gone:
  → Resource ĐÃ tồn tại nhưng bị xóa vĩnh viễn
  → Search engine sẽ xóa URL khỏi index
```

### Cách xử lý

```
1. Kiểm tra lại ID/URL có đúng không
2. Có thể retry sau (resource có thể được tạo lại)
3. Hiển thị trang 404 thân thiện với user
4. Log để theo dõi dead links
```

---

## 💥 500 Internal Server Error — Lỗi server

### Mô tả

Server gặp lỗi **không xác định** và không thể xử lý request. Đây là lỗi hoàn toàn phía server.

### Nguyên nhân phổ biến

- Unhandled exception trong code
- Database connection failed
- Null pointer exception
- Out of memory
- Infinite loop / timeout

### Ví dụ tình huống

```http
GET /api/reports/annual-summary HTTP/1.1

HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
  "error": "INTERNAL_SERVER_ERROR",
  "message": "An unexpected error occurred. Our team has been notified.",
  "requestId": "req-abc123",
  "timestamp": "2026-03-04T10:30:00Z"
}
```

### Lưu ý bảo mật quan trọng

```
❌ KHÔNG BAO GIỜ trả về stack trace cho client:
{
  "error": "NullPointerException at UserService.java:142\n
            at OrderController.java:89\n..."
}
← Tiết lộ cấu trúc code nội bộ cho kẻ tấn công

✅ Thay vào đó, log stack trace ở server và trả về requestId:
{
  "error": "INTERNAL_SERVER_ERROR",
  "requestId": "req-abc123"  ← Dùng ID này để tìm trong server logs
}
```

### Cách xử lý

```
→ Phía client:
  1. Hiển thị "Có lỗi xảy ra, vui lòng thử lại sau"
  2. Có thể retry với exponential backoff (chờ 1s, 2s, 4s...)
  3. Lưu requestId để báo cáo cho support

→ Phía server:
  1. Log đầy đủ thông tin (stack trace, request data, user ID)
  2. Alert team qua Slack/PagerDuty
  3. Fix bug và deploy
```

---

## ⏱️ 429 Too Many Requests — Vượt giới hạn tần suất

### Mô tả

Client gửi quá nhiều request trong một khoảng thời gian (Rate Limiting). Server từ chối để bảo vệ tài nguyên.

### Nguyên nhân phổ biến

- Script/bot gửi request liên tục
- Client không implement exponential backoff
- Nhiều tab/instance chạy cùng lúc
- DoS/DDoS attack

### Ví dụ tình huống

```http
POST /api/auth/login HTTP/1.1
← Đã gửi 10 lần trong 1 phút với sai mật khẩu

HTTP/1.1 429 Too Many Requests
Retry-After: 300
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1741090200
Content-Type: application/json

{
  "error": "RATE_LIMIT_EXCEEDED",
  "message": "Too many failed login attempts. Account temporarily locked.",
  "retryAfter": 300,
  "retryAt": "2026-03-04T11:00:00Z",
  "limitType": "LOGIN_ATTEMPT",
  "limit": 5,
  "window": "1 minute"
}
```

### Các loại Rate Limit phổ biến

```
1. Per-IP:      100 requests/minute per IP address
2. Per-User:    1000 requests/hour per authenticated user
3. Per-Endpoint: 10 requests/minute cho POST /login (chống brute force)
4. Global:      10,000 requests/second cho toàn hệ thống
```

### Rate Limit Headers

```http
X-RateLimit-Limit: 100       ← Giới hạn tối đa
X-RateLimit-Remaining: 45    ← Còn lại trong window hiện tại
X-RateLimit-Reset: 1741086660 ← Unix timestamp khi counter reset
Retry-After: 60              ← Giây chờ trước khi thử lại
```

### Cách xử lý

```
1. Đọc header Retry-After và chờ đúng thời gian đó
2. Implement exponential backoff với jitter:
   - Lần 1: chờ 1s
   - Lần 2: chờ 2s + random(0-1s)
   - Lần 3: chờ 4s + random(0-2s)
3. Cache kết quả để giảm số request
4. Hiển thị cho user: "Quá nhiều yêu cầu. Thử lại sau 5 phút."
5. KHÔNG spam retry ngay lập tức
```

---

## 🌐 502 Bad Gateway & 503 Service Unavailable

### 502 Bad Gateway

```
Nguyên nhân: API Gateway/Load Balancer nhận được response
             không hợp lệ từ upstream server

Ví dụ:
  [Client] → [Nginx] → [App Server]
                           ↑
                    App server bị crash
                    Nginx nhận lỗi → trả 502

Cách xử lý: Retry sau 10-30s
```

### 503 Service Unavailable

```
Nguyên nhân:
  - Server đang maintenance
  - Server quá tải (không đủ tài nguyên xử lý)
  - Circuit breaker đang OPEN

HTTP/1.1 503 Service Unavailable
Retry-After: 1800
Content-Type: application/json

{
  "error": "SERVICE_UNAVAILABLE",
  "message": "Scheduled maintenance in progress",
  "maintenanceWindow": {
    "start": "2026-03-04T22:00:00+07:00",
    "end":   "2026-03-05T02:00:00+07:00"
  },
  "statusPage": "https://status.example.com"
}

Cách xử lý:
  - Đọc Retry-After và thông báo cho user
  - Theo dõi status page
  - Implement circuit breaker phía client
```

### 504 Gateway Timeout

```
Nguyên nhân: Gateway không nhận được response từ upstream
             trong thời gian quy định (thường 30-60s)

Thường xảy ra khi:
  - Query database quá nặng
  - Gọi external API chậm
  - Xử lý file lớn

Cách xử lý:
  - Retry 1-2 lần
  - Nếu vẫn lỗi, thông báo user thử lại sau
  - Xem xét dùng async processing (202 Accepted) cho tác vụ nặng
```

---

## 📊 Bảng Tổng Hợp Mã Lỗi

| Code | Tên                   | Lỗi ở đâu      | Retry? | Hành động           |
| ---- | --------------------- | -------------- | ------ | ------------------- |
| 400  | Bad Request           | Client         | ❌     | Fix request data    |
| 401  | Unauthorized          | Client (auth)  | ✅     | Re-authenticate     |
| 403  | Forbidden             | Client (perms) | ❌     | Xin quyền           |
| 404  | Not Found             | Client/Server  | 🔶     | Kiểm tra URL/ID     |
| 409  | Conflict              | Client         | ❌     | Resolve conflict    |
| 422  | Unprocessable Entity  | Client         | ❌     | Fix logic data      |
| 429  | Too Many Requests     | Client         | ✅     | Wait + Retry        |
| 500  | Internal Server Error | Server         | ✅     | Exponential backoff |
| 502  | Bad Gateway           | Infrastructure | ✅     | Retry sau 30s       |
| 503  | Service Unavailable   | Server         | ✅     | Wait + Retry        |
| 504  | Gateway Timeout       | Infrastructure | ✅     | Retry 1-2 lần       |

---

## 🛠️ Bài Tập Phân Tích

### Câu 1: Xác định status code phù hợp

| Tình huống                                    | Status Code Đúng        | Giải thích                    |
| --------------------------------------------- | ----------------------- | ----------------------------- |
| User gửi form đăng ký với email đã tồn tại    | 409 Conflict            | Xung đột với dữ liệu hiện tại |
| User chưa đăng nhập truy cập /profile         | 401 Unauthorized        | Thiếu authentication          |
| Admin đã đăng nhập cố xóa user của admin khác | 403 Forbidden           | Đã auth nhưng thiếu quyền     |
| Tạo sản phẩm mới thành công                   | 201 Created             | Resource mới được tạo         |
| Xóa sản phẩm thành công                       | 204 No Content          | Thành công, không có body     |
| Gửi JSON với cú pháp sai                      | 400 Bad Request         | Client gửi data sai           |
| Database bị down                              | 503 Service Unavailable | Server không thể phục vụ      |

### Câu 2: Phân tích response lỗi sau

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer error="invalid_token"
```

**Phân tích:**

- Đây là lỗi **xác thực** (authentication), không phải phân quyền (authorization)
- Header `WWW-Authenticate` báo cho client biết cần dùng Bearer token
- `error="invalid_token"` cho biết token không hợp lệ (sai hoặc hết hạn)
- Giải pháp: Client cần refresh token hoặc đăng nhập lại

### Câu 3: Phân tích response lỗi sau

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 3600
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1741090200
```

**Phân tích:**

- Client đã gửi **quá 1000 request** trong khoảng thời gian giới hạn
- Không còn request nào được phép trong window hiện tại (`Remaining: 0`)
- Phải chờ **3600 giây (1 giờ)** trước khi thử lại
- Rate limit sẽ reset lúc timestamp `1741090200` = `2026-03-04T12:30:00Z`
- Giải pháp: Implement caching, giảm số request, chờ đủ thời gian
