# Tuần 2 — Kiến Trúc REST & HTTP

> **Môn**: INT3505 - Phát triển ứng dụng Web  
> **Ngày**: 04/03/2026

---

## 📚 Mục tiêu học tập

### Kiến thức

- [x] Nắm 6 nguyên tắc của kiến trúc REST
- [x] Hiểu HTTP methods (GET, POST, PUT, DELETE, PATCH)
- [x] Hiểu HTTP status codes và ý nghĩa
- [x] Hiểu HTTP headers quan trọng

### Kỹ năng

- [x] Thiết kế request/response HTTP cơ bản
- [x] Đánh giá mức độ RESTful của một API

---

## 📁 Cấu trúc tài liệu

```
tuan2/
├── README.md                          ← File này (mục lục)
├── 01_REST_Principles.md              ← 6 nguyên tắc REST
├── 02_HTTP_Methods_StatusCodes.md     ← HTTP methods, status codes, headers
├── 03_HTTP_Request_Design_Practice.md ← Thực hành: 5 tình huống thiết kế
├── 04_HTTP_Error_Analysis.md          ← Phân tích mã lỗi HTTP
└── 05_RESTful_API_Evaluation.md       ← Đánh giá mức độ RESTful
```

---

## 🗺️ Lộ trình học

```
[1] Đọc 01_REST_Principles.md
        ↓ Nắm 6 nguyên tắc
[2] Đọc 02_HTTP_Methods_StatusCodes.md
        ↓ Hiểu methods, status codes, headers
[3] Thực hành 03_HTTP_Request_Design_Practice.md
        ↓ 5 tình huống thiết kế thực tế
[4] Nghiên cứu 04_HTTP_Error_Analysis.md
        ↓ Phân tích và xử lý lỗi
[5] Đánh giá 05_RESTful_API_Evaluation.md
        ↓ Richardson Maturity Model + Checklist
```

---

## 🔑 Kiến thức cốt lõi cần nhớ

### 6 Nguyên tắc REST

| #   | Nguyên tắc        | Từ khóa                         |
| --- | ----------------- | ------------------------------- |
| 1   | Client-Server     | Tách biệt UI và Data            |
| 2   | Stateless         | Mỗi request độc lập, JWT token  |
| 3   | Cacheable         | Cache-Control, ETag             |
| 4   | Uniform Interface | URI + HTTP methods + HATEOAS    |
| 5   | Layered System    | Load balancer, CDN, API Gateway |
| 6   | Code on Demand    | (Optional) JavaScript từ server |

### HTTP Methods

| Method | Mục đích          | Idempotent | Safe |
| ------ | ----------------- | ---------- | ---- |
| GET    | Đọc               | ✅         | ✅   |
| POST   | Tạo mới           | ❌         | ❌   |
| PUT    | Thay thế toàn bộ  | ✅         | ❌   |
| PATCH  | Cập nhật một phần | ❌\*       | ❌   |
| DELETE | Xóa               | ✅         | ❌   |

### Status Codes quan trọng

| Code                      | Ý nghĩa                          |
| ------------------------- | -------------------------------- |
| 200 OK                    | Thành công                       |
| 201 Created               | Tạo mới thành công               |
| 204 No Content            | Thành công, không có body        |
| 400 Bad Request           | Client gửi data sai              |
| 401 Unauthorized          | Chưa xác thực                    |
| 403 Forbidden             | Không có quyền                   |
| 404 Not Found             | Không tìm thấy                   |
| 409 Conflict              | Xung đột dữ liệu                 |
| 422 Unprocessable Entity  | Data đúng format nhưng sai logic |
| 429 Too Many Requests     | Vượt rate limit                  |
| 500 Internal Server Error | Lỗi server                       |
| 503 Service Unavailable   | Server tạm ngưng                 |

---

## ✍️ Tóm tắt thực hành

### 5 Tình huống thiết kế HTTP Request

| #   | Tình huống          | Method | Endpoint                     | Status      |
| --- | ------------------- | ------ | ---------------------------- | ----------- |
| 1   | Lấy danh sách users | GET    | `/api/users?page=2&limit=10` | 200         |
| 2   | Cập nhật email      | PATCH  | `/api/users/{id}`            | 200/409/422 |
| 3   | Tạo đơn hàng        | POST   | `/api/orders`                | 201/409     |
| 4   | Xóa bài viết        | DELETE | `/api/posts/{id}`            | 200/403/404 |
| 5   | Tìm kiếm sản phẩm   | GET    | `/api/products?q=laptop`     | 200         |

### Richardson Maturity Model

```
Level 0 → Level 1 → Level 2 → Level 3
  RPC      URIs    HTTP Verbs  HATEOAS
  ❌        🟡        ✅          ✅✅
```

---

## 🔗 Tài liệu tham khảo

- [RFC 7231 - HTTP/1.1 Semantics](https://tools.ietf.org/html/rfc7231)
- [Roy Fielding's Dissertation (REST)](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)
- [HTTP Status Codes — MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [REST API Design Best Practices](https://restfulapi.net/)
- [Richardson Maturity Model](https://martinfowler.com/articles/richardsonMaturityModel.html)
