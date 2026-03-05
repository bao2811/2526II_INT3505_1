# 6 Nguyên Tắc Kiến Trúc REST

> **REST** (Representational State Transfer) là một kiểu kiến trúc phần mềm được Roy Fielding định nghĩa năm 2000 trong luận án tiến sĩ của ông. Một hệ thống được gọi là **RESTful** khi tuân thủ đầy đủ 6 ràng buộc sau.

---

## 1. 🖥️ Client-Server (Tách biệt Client và Server)

### Định nghĩa

Client và Server hoàn toàn **độc lập** với nhau, giao tiếp qua một interface thống nhất (thường là HTTP).

### Đặc điểm

- Client chịu trách nhiệm về **giao diện người dùng** (UI/UX).
- Server chịu trách nhiệm về **lưu trữ dữ liệu** và **xử lý logic nghiệp vụ**.
- Hai bên có thể phát triển **độc lập** miễn là không thay đổi interface.

### Ví dụ

```
[React App]  --HTTP Request-->  [Node.js API Server]
[Mobile App] --HTTP Request-->  [Node.js API Server]
                                        |
                                 [PostgreSQL DB]
```

### Lợi ích

- Tăng khả năng **portability** của client (web, mobile, desktop dùng chung API).
- Tăng khả năng **scalability** của server.

---

## 2. 🚫 Stateless (Phi trạng thái)

### Định nghĩa

Mỗi request từ client đến server phải chứa **đầy đủ thông tin** cần thiết để server xử lý. Server **không lưu trữ** bất kỳ trạng thái session nào giữa các request.

### Đặc điểm

- Server không nhớ gì về client sau khi response.
- Mọi context (authentication, preferences) phải được gửi **trong từng request**.
- Session state được quản lý hoàn toàn **phía client**.

### Ví dụ SO SÁNH

❌ **Không Stateless (Session-based):**

```
Request 1: POST /login  → Server tạo session, lưu sessionId
Request 2: GET /profile → Server dùng session đã lưu (phụ thuộc Request 1)
```

✅ **Stateless (Token-based):**

```
Request 1: POST /login  → Server trả về JWT token
Request 2: GET /profile
           Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...
           (Token chứa đầy đủ thông tin, server không cần nhớ gì)
```

### Lợi ích

- Dễ **scale horizontal** (bất kỳ server nào cũng xử lý được request).
- Tăng **độ tin cậy** (một server chết không ảnh hưởng đến các request khác).
- Dễ **monitor** và **debug** từng request độc lập.

---

## 3. 💾 Cacheable (Có thể Cache)

### Định nghĩa

Response phải được đánh dấu rõ ràng là **có thể cache** hay **không thể cache**. Nếu cacheable, client/proxy có thể tái sử dụng response cho các request tương tự.

### Các HTTP Cache Headers

| Header          | Mô tả                   | Ví dụ                                          |
| --------------- | ----------------------- | ---------------------------------------------- |
| `Cache-Control` | Chỉ thị cache chính     | `Cache-Control: max-age=3600`                  |
| `ETag`          | Phiên bản của resource  | `ETag: "abc123"`                               |
| `Last-Modified` | Thời gian thay đổi cuối | `Last-Modified: Wed, 04 Mar 2026 10:00:00 GMT` |
| `Expires`       | Thời điểm hết hạn cache | `Expires: Thu, 05 Mar 2026 10:00:00 GMT`       |

### Ví dụ

✅ **Response có thể cache (danh sách sản phẩm):**

```http
HTTP/1.1 200 OK
Cache-Control: public, max-age=3600
ETag: "products-v42"
Content-Type: application/json

[{"id": 1, "name": "Laptop"}, ...]
```

❌ **Response không nên cache (thông tin cá nhân):**

```http
HTTP/1.1 200 OK
Cache-Control: no-store, no-cache
Content-Type: application/json

{"id": 1, "name": "Nguyen Van A", "balance": 5000000}
```

### Lợi ích

- Giảm **latency** cho client.
- Giảm tải cho **server** và **băng thông mạng**.

---

## 4. 🔗 Uniform Interface (Giao diện đồng nhất)

### Định nghĩa

Đây là ràng buộc **cốt lõi** của REST, gồm 4 sub-constraints:

### 4a. Resource Identification (Định danh tài nguyên)

Mỗi tài nguyên được xác định bằng **URI duy nhất**.

```
/users          → Tập hợp users
/users/42       → User có id=42
/users/42/posts → Các bài đăng của user 42
```

### 4b. Resource Manipulation Through Representations

Client thao tác tài nguyên thông qua **representations** (JSON, XML...), không trực tiếp.

```json
// Representation của một User resource
{
  "id": 42,
  "name": "Nguyen Van A",
  "email": "nva@example.com"
}
```

### 4c. Self-descriptive Messages (Thông điệp tự mô tả)

Mỗi message chứa đủ thông tin để hiểu cách xử lý nó.

```http
GET /users/42 HTTP/1.1
Host: api.example.com
Accept: application/json          ← Nói rõ muốn nhận JSON
Authorization: Bearer <token>     ← Đủ thông tin xác thực
```

### 4d. HATEOAS (Hypermedia As The Engine Of Application State)

Response chứa **links** hướng dẫn client các hành động tiếp theo.

```json
{
  "id": 42,
  "name": "Nguyen Van A",
  "_links": {
    "self": { "href": "/users/42" },
    "posts": { "href": "/users/42/posts" },
    "update": { "href": "/users/42", "method": "PUT" },
    "delete": { "href": "/users/42", "method": "DELETE" }
  }
}
```

---

## 5. 🏗️ Layered System (Hệ thống phân lớp)

### Định nghĩa

Client **không biết** mình đang kết nối trực tiếp với server hay thông qua một intermediary (proxy, load balancer, CDN, API Gateway...).

### Kiến trúc minh họa

```
Client
  │
  ▼
[CDN / Cache Layer]        ← Cache static resources
  │
  ▼
[API Gateway]              ← Authentication, Rate limiting, Routing
  │
  ▼
[Load Balancer]            ← Phân phối tải
  │      │
  ▼      ▼
[Server1] [Server2]        ← Xử lý business logic
  │
  ▼
[Database]
```

### Lợi ích

- Tăng **bảo mật** (có thể thêm firewall layer).
- Tăng **scalability** (thêm server mà client không hay biết).
- Cho phép **caching** tại nhiều tầng.

---

## 6. 📦 Code on Demand (Tùy chọn - Optional)

### Định nghĩa

Server có thể gửi **executable code** (JavaScript, applets) cho client để mở rộng chức năng. Đây là ràng buộc **duy nhất** không bắt buộc trong REST.

### Ví dụ

```http
GET /widgets/chart-widget HTTP/1.1

HTTP/1.1 200 OK
Content-Type: application/javascript

// Server gửi code JavaScript về client
class ChartWidget {
  render(data) { ... }
}
```

### Ứng dụng thực tế

- Trình duyệt tải và chạy JavaScript từ server.
- Google Maps API gửi JS library cho client.

---

## 📊 Tóm tắt 6 Nguyên tắc

| #   | Nguyên tắc        | Bắt buộc      | Mục đích chính                       |
| --- | ----------------- | ------------- | ------------------------------------ |
| 1   | Client-Server     | ✅            | Tách biệt concerns, tăng portability |
| 2   | Stateless         | ✅            | Scalability, reliability             |
| 3   | Cacheable         | ✅            | Performance, giảm tải server         |
| 4   | Uniform Interface | ✅            | Tính nhất quán, interoperability     |
| 5   | Layered System    | ✅            | Security, scalability                |
| 6   | Code on Demand    | ⭕ (Optional) | Mở rộng client functionality         |
