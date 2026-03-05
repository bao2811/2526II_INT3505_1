# Thực hành: Thiết kế HTTP Request cho 5 Tình huống

> Mỗi tình huống bao gồm: Mô tả bài toán → Phân tích → HTTP Request → HTTP Response → Giải thích.

---

## Tình huống 1: Lấy danh sách người dùng (Phân trang + Lọc)

### 📋 Bài toán

Hệ thống quản lý nhân sự cần lấy danh sách nhân viên thuộc phòng ban "Engineering", sắp xếp theo tên, hiển thị trang 2 với 10 người/trang.

### 🔍 Phân tích

- **Method**: `GET` — chỉ đọc dữ liệu, không thay đổi server
- **Resource**: `/api/users` — tập hợp users
- **Query params**: `department`, `page`, `limit`, `sort`
- **Auth**: Bearer token (dữ liệu nhân sự là private)
- **Cache**: Có thể cache ngắn hạn (5-10 phút)

### 📤 HTTP Request

```http
GET /api/users?department=Engineering&page=2&limit=10&sort=name&order=asc HTTP/1.1
Host: api.hrm-system.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyXzEiLCJyb2xlIjoiYWRtaW4ifQ.abc123
Accept: application/json
Accept-Language: vi-VN
X-Request-ID: req-a1b2c3d4
```

### 📥 HTTP Response

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Cache-Control: private, max-age=300
X-Request-ID: req-a1b2c3d4
X-Total-Count: 47

{
  "data": [
    {
      "id": "usr_011",
      "name": "Hoang Van K",
      "email": "hvk@company.com",
      "department": "Engineering",
      "position": "Senior Developer",
      "joinedAt": "2023-06-15"
    },
    {
      "id": "usr_012",
      "name": "Le Thi L",
      "email": "ltl@company.com",
      "department": "Engineering",
      "position": "DevOps Engineer",
      "joinedAt": "2024-01-10"
    }
  ],
  "pagination": {
    "page": 2,
    "limit": 10,
    "total": 47,
    "totalPages": 5,
    "hasNext": true,
    "hasPrev": true,
    "links": {
      "first": "/api/users?department=Engineering&page=1&limit=10&sort=name",
      "prev":  "/api/users?department=Engineering&page=1&limit=10&sort=name",
      "next":  "/api/users?department=Engineering&page=3&limit=10&sort=name",
      "last":  "/api/users?department=Engineering&page=5&limit=10&sort=name"
    }
  }
}
```

### 💡 Giải thích

- Dùng **query parameters** cho filter/sort/pagination (không đưa vào path)
- `X-Total-Count` header cho client biết tổng số records không cần parse body
- `Cache-Control: private` vì dữ liệu nhân sự không nên cache ở shared proxy
- `_links` trong pagination tuân thủ nguyên tắc **HATEOAS**
- `X-Request-ID` giúp trace request qua các logs

---

## Tình huống 2: Cập nhật email người dùng

### 📋 Bài toán

Người dùng muốn thay đổi email của mình từ `old@email.com` thành `new@email.com`. Chỉ cập nhật field email, không thay đổi các thông tin khác.

### 🔍 Phân tích

- **Method**: `PATCH` — chỉ cập nhật một phần, tiết kiệm băng thông hơn PUT
- **Resource**: `/api/users/{userId}` — một user cụ thể
- **Auth**: Bearer token của chính user đó
- **Validation**: Email phải hợp lệ và chưa được dùng bởi người khác
- **Security**: Chỉ user đó hoặc admin mới được sửa

### 📤 HTTP Request

```http
PATCH /api/users/usr_042 HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c3JfMDQyIn0.xyz789
X-Request-ID: req-update-email-001

{
  "email": "new_email@example.com"
}
```

### 📥 HTTP Response (Thành công)

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
X-Request-ID: req-update-email-001

{
  "id": "usr_042",
  "name": "Nguyen Van A",
  "email": "new_email@example.com",
  "updatedAt": "2026-03-04T10:30:00Z",
  "message": "Email updated successfully. Please verify your new email."
}
```

### 📥 HTTP Response (Email đã tồn tại — Lỗi 409)

```http
HTTP/1.1 409 Conflict
Content-Type: application/json; charset=utf-8

{
  "error": "EMAIL_ALREADY_EXISTS",
  "message": "This email address is already associated with another account",
  "field": "email"
}
```

### 📥 HTTP Response (Email không hợp lệ — Lỗi 422)

```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json; charset=utf-8

{
  "error": "VALIDATION_ERROR",
  "message": "Validation failed",
  "details": [
    {
      "field": "email",
      "value": "not-valid-email",
      "message": "Must be a valid email address format"
    }
  ]
}
```

### 💡 Giải thích

- Dùng **PATCH** thay vì PUT vì chỉ cập nhật 1 field (tiết kiệm bandwidth)
- Server trả về toàn bộ object đã cập nhật để client đồng bộ state
- **409 Conflict** khi email đã tồn tại (xung đột với dữ liệu hiện tại)
- **422 Unprocessable Entity** khi dữ liệu đúng format JSON nhưng sai logic
- Thông điệp verify email trong response nhắc user xác nhận email mới

---

## Tình huống 3: Tạo đơn hàng mới

### 📋 Bài toán

Khách hàng đặt mua 2 sản phẩm: 3 chiếc "Laptop Dell XPS" (id: prod_001) và 1 chiếc "Mouse Logitech" (id: prod_002), giao đến địa chỉ tại Hà Nội, thanh toán bằng thẻ tín dụng.

### 🔍 Phân tích

- **Method**: `POST` — tạo mới resource
- **Resource**: `/api/orders`
- **Auth**: Bearer token (phải đăng nhập mới đặt hàng)
- **Idempotency**: Nên dùng `Idempotency-Key` để tránh tạo đơn trùng khi retry
- **Transaction**: Server cần kiểm tra tồn kho trước khi tạo đơn

### 📤 HTTP Request

```http
POST /api/orders HTTP/1.1
Host: api.shop.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c3JfMTIzIn0.order123
Idempotency-Key: order-idem-key-20260304-usr123-1741086000
X-Request-ID: req-create-order-007

{
  "items": [
    {
      "productId": "prod_001",
      "name": "Laptop Dell XPS 15",
      "quantity": 3,
      "unitPrice": 35000000
    },
    {
      "productId": "prod_002",
      "name": "Mouse Logitech MX Master 3",
      "quantity": 1,
      "unitPrice": 2500000
    }
  ],
  "shippingAddress": {
    "fullName": "Nguyen Thi Mai",
    "phone": "0912345678",
    "street": "123 Pho Hue",
    "district": "Hai Ba Trung",
    "city": "Ha Noi",
    "country": "VN"
  },
  "paymentMethod": "CREDIT_CARD",
  "note": "Giao buoi sang truoc 12h"
}
```

### 📥 HTTP Response (Thành công)

```http
HTTP/1.1 201 Created
Content-Type: application/json; charset=utf-8
Location: /api/orders/ord_789abc
X-Request-ID: req-create-order-007

{
  "orderId": "ord_789abc",
  "status": "PENDING_PAYMENT",
  "customerId": "usr_123",
  "items": [
    {
      "productId": "prod_001",
      "name": "Laptop Dell XPS 15",
      "quantity": 3,
      "unitPrice": 35000000,
      "subtotal": 105000000
    },
    {
      "productId": "prod_002",
      "name": "Mouse Logitech MX Master 3",
      "quantity": 1,
      "unitPrice": 2500000,
      "subtotal": 2500000
    }
  ],
  "pricing": {
    "subtotal": 107500000,
    "shippingFee": 50000,
    "discount": 0,
    "tax": 10750000,
    "total": 118300000
  },
  "estimatedDelivery": "2026-03-06",
  "paymentUrl": "https://payment.shop.com/checkout/ord_789abc",
  "createdAt": "2026-03-04T10:00:00Z"
}
```

### 📥 HTTP Response (Hết hàng — Lỗi 409)

```http
HTTP/1.1 409 Conflict
Content-Type: application/json; charset=utf-8

{
  "error": "INSUFFICIENT_STOCK",
  "message": "Some items are out of stock",
  "items": [
    {
      "productId": "prod_001",
      "requested": 3,
      "available": 1,
      "message": "Only 1 unit available"
    }
  ]
}
```

### 💡 Giải thích

- **201 Created** + `Location` header cho biết URI của đơn hàng vừa tạo
- `Idempotency-Key` header phòng trường hợp client gửi request 2 lần (mạng lỗi, retry) → server nhận ra và trả về đơn hàng đã tạo thay vì tạo mới
- Server tính toán `pricing` và trả về để client hiển thị xác nhận
- `paymentUrl` là link HATEOAS dẫn đến bước tiếp theo (thanh toán)

---

## Tình huống 4: Xóa một bài viết (Soft Delete)

### 📋 Bài toán

Admin xóa bài viết spam có ID `post_555`. Hệ thống dùng **soft delete** (đánh dấu đã xóa, không xóa khỏi DB) để có thể phục hồi sau này.

### 🔍 Phân tích

- **Method**: `DELETE` — xóa tài nguyên
- **Resource**: `/api/posts/{postId}`
- **Auth**: Bearer token với role `admin`
- **Soft Delete**: Server đánh dấu `deletedAt`, không xóa vật lý
- **Audit**: Ghi lại ai xóa, lúc nào, lý do gì

### 📤 HTTP Request

```http
DELETE /api/posts/post_555 HTTP/1.1
Host: api.blog.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbl8xIiwicm9sZSI6ImFkbWluIn0.admintoken
X-Request-ID: req-delete-post-555
X-Delete-Reason: SPAM_CONTENT
```

### 📥 HTTP Response (Xóa thành công)

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
X-Request-ID: req-delete-post-555

{
  "message": "Post deleted successfully",
  "post": {
    "id": "post_555",
    "title": "Spam post title",
    "status": "DELETED",
    "deletedAt": "2026-03-04T10:45:00Z",
    "deletedBy": "admin_1",
    "reason": "SPAM_CONTENT"
  },
  "actions": {
    "restore": {
      "method": "POST",
      "href": "/api/posts/post_555/restore"
    }
  }
}
```

### 📥 HTTP Response (Không tìm thấy — Lỗi 404)

```http
HTTP/1.1 404 Not Found
Content-Type: application/json; charset=utf-8

{
  "error": "POST_NOT_FOUND",
  "message": "Post with id 'post_555' does not exist",
  "resourceType": "Post",
  "resourceId": "post_555"
}
```

### 📥 HTTP Response (Không có quyền — Lỗi 403)

```http
HTTP/1.1 403 Forbidden
Content-Type: application/json; charset=utf-8

{
  "error": "FORBIDDEN",
  "message": "You do not have permission to delete this post",
  "requiredRole": "admin",
  "currentRole": "user"
}
```

### 💡 Giải thích

- Trả **200 OK** với body thay vì **204 No Content** vì cần trả về thông tin audit
- Custom header `X-Delete-Reason` để ghi lại lý do xóa
- Response chứa link `restore` (HATEOAS) để admin có thể phục hồi nếu xóa nhầm
- **404 vs 410**: Dùng 404 nếu chưa tồn tại, 410 Gone nếu đã bị xóa vĩnh viễn
- **401 vs 403**: 401 khi chưa login, 403 khi đã login nhưng không đủ quyền

---

## Tình huống 5: Tìm kiếm sản phẩm (Full-text Search + Filter)

### 📋 Bài toán

Người dùng trên trang thương mại điện tử tìm kiếm "laptop gaming" với filter: giá từ 20 - 50 triệu, thương hiệu ASUS hoặc MSI, còn hàng, sắp xếp theo giá tăng dần.

### 🔍 Phân tích

- **Method**: `GET` — tìm kiếm không thay đổi dữ liệu
- **Resource**: `/api/products` với query params
- **Cache**: Có thể cache kết quả search phổ biến
- **Performance**: Cần pagination, tránh trả về toàn bộ catalog

### 📤 HTTP Request

```http
GET /api/products?q=laptop+gaming&price_min=20000000&price_max=50000000&brand=ASUS,MSI&in_stock=true&sort=price&order=asc&page=1&limit=12 HTTP/1.1
Host: api.ecommerce.com
Accept: application/json
Accept-Language: vi-VN
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJndWVzdCI6dHJ1ZX0.guest
X-Request-ID: req-search-laptop-001
```

### 📥 HTTP Response (Thành công)

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Cache-Control: public, max-age=120
Vary: Accept-Language
X-Request-ID: req-search-laptop-001
X-Search-Time: 45ms

{
  "query": "laptop gaming",
  "filters": {
    "priceRange": { "min": 20000000, "max": 50000000 },
    "brands": ["ASUS", "MSI"],
    "inStock": true
  },
  "results": [
    {
      "id": "prod_laptop_001",
      "name": "ASUS ROG Strix G15 2026",
      "brand": "ASUS",
      "price": 28500000,
      "originalPrice": 32000000,
      "discount": 11,
      "rating": 4.7,
      "reviewCount": 234,
      "inStock": true,
      "stockCount": 15,
      "thumbnail": "https://cdn.ecommerce.com/products/asus-rog-g15.jpg",
      "tags": ["gaming", "RTX4060", "144Hz"],
      "_links": {
        "self":     { "href": "/api/products/prod_laptop_001" },
        "addToCart": { "href": "/api/cart/items", "method": "POST" }
      }
    },
    {
      "id": "prod_laptop_002",
      "name": "MSI Katana 15 B13VFK",
      "brand": "MSI",
      "price": 24900000,
      "originalPrice": 24900000,
      "discount": 0,
      "rating": 4.5,
      "reviewCount": 89,
      "inStock": true,
      "stockCount": 8,
      "thumbnail": "https://cdn.ecommerce.com/products/msi-katana.jpg",
      "tags": ["gaming", "RTX4060", "144Hz"],
      "_links": {
        "self":      { "href": "/api/products/prod_laptop_002" },
        "addToCart": { "href": "/api/cart/items", "method": "POST" }
      }
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 12,
    "total": 28,
    "totalPages": 3
  },
  "facets": {
    "brands": [
      { "name": "ASUS", "count": 12 },
      { "name": "MSI",  "count": 16 }
    ],
    "priceRanges": [
      { "range": "20-30M", "count": 8 },
      { "range": "30-40M", "count": 13 },
      { "range": "40-50M", "count": 7 }
    ]
  }
}
```

### 📥 HTTP Response (Không có kết quả)

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "query": "laptop gaming xyz brand unknown",
  "results": [],
  "pagination": {
    "page": 1,
    "limit": 12,
    "total": 0,
    "totalPages": 0
  },
  "suggestions": [
    "Thử bỏ filter thương hiệu",
    "Mở rộng khoảng giá",
    "Kiểm tra lỗi chính tả"
  ]
}
```

### 💡 Giải thích

- Khi tìm kiếm không có kết quả → vẫn trả **200 OK** với `results: []`, không dùng 404
- `facets` trả về thống kê filter để client hiển thị số lượng sản phẩm theo từng nhóm
- `Cache-Control: public` vì kết quả search không nhạy cảm, có thể cache ở CDN
- `Vary: Accept-Language` báo cho cache biết response khác nhau theo ngôn ngữ
- `X-Search-Time` custom header để monitor performance
- `_links` trong mỗi product item tuân thủ HATEOAS

---

## 📊 Bảng Tổng Hợp 5 Tình Huống

| #   | Tình huống          | Method | Status Code | Đặc điểm nổi bật                  |
| --- | ------------------- | ------ | ----------- | --------------------------------- |
| 1   | Lấy danh sách users | GET    | 200         | Pagination, HATEOAS links         |
| 2   | Cập nhật email      | PATCH  | 200/409/422 | Partial update, validation errors |
| 3   | Tạo đơn hàng        | POST   | 201/409     | Idempotency-Key, Location header  |
| 4   | Xóa bài viết        | DELETE | 200/404/403 | Soft delete, audit trail          |
| 5   | Tìm kiếm sản phẩm   | GET    | 200         | Full-text search, facets, cache   |
