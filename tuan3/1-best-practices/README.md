# Flow 1: Best Practices trong Thiết kế API

## Mục tiêu
Hiểu và áp dụng các best practices chính trong thiết kế API:
- **Consistency** (Nhất quán)
- **Clarity** (Dễ hiểu)
- **Extensibility** (Dễ mở rộng)

## 1. Consistency (Nhất quán)

### Định nghĩa
Tất cả các endpoint và response của API nên tuân theo cùng một pattern, cùng một format và cùng một cách tổ chức.

### Nguyên tắc:
- **Response format nhất quán**: Tất cả response nên có cùng cấu trúc
- **Error handling nhất quán**: Tất cả lỗi nên được format giống nhau
- **HTTP methods nhất quán**: Sử dụng GET, POST, PUT, DELETE theo đúng purpose
- **Status codes nhất quán**: Sử dụng status codes đúng cho từng tình huống

### Ví dụ Good vs Bad:

#### ❌ Bad - Không nhất quán
```json
// GET /api/users -> Response 1
{
  "data": [
    {"userId": 1, "userName": "john"},
    {"userId": 2, "userName": "jane"}
  ]
}

// GET /api/products -> Response 2 (format khác)
{
  "products": [
    {"id": 1, "name": "Product A"},
    {"id": 2, "name": "Product B"}
  ]
}
```

#### ✅ Good - Nhất quán
```json
// GET /api/users
{
  "status": "success",
  "data": [
    {"id": 1, "name": "john"},
    {"id": 2, "name": "jane"}
  ],
  "meta": {"total": 2}
}

// GET /api/products
{
  "status": "success",
  "data": [
    {"id": 1, "name": "Product A"},
    {"id": 2, "name": "Product B"}
  ],
  "meta": {"total": 2}
}
```

## 2. Clarity (Dễ hiểu)

### Định nghĩa
API nên dễ hiểu, dễ sử dụng và tài liệu rõ ràng.

### Nguyên tắc:
- **Endpoint names rõ ràng**: Tên endpoint nên mô tả chính xác chức năng
- **Request/Response rõ ràng**: Dễ hiểu request cần gì và response trả gì
- **Documentation chi tiết**: Có documentation đủ chi tiết
- **Error messages rõ ràng**: Lỗi nên có message rõ ràng

### Ví dụ Good vs Bad:

#### ❌ Bad - Không rõ ràng
```
GET /api/getusr -> Viết tắt, khó hiểu
POST /api/data -> Quá generic, không biết là gì
GET /api/fn123 -> Tên không mô tả gì
```

#### ✅ Good - Rõ ràng
```
GET /api/users -> Rõ ràng là lấy danh sách users
GET /api/users/{id} -> Rõ ràng là lấy user theo ID
POST /api/users -> Rõ ràng là tạo user mới
```

## 3. Extensibility (Dễ mở rộng)

### Định nghĩa
API nên được thiết kế sao cho dễ thêm tính năng mới mà không phá vỡ code cũ.

### Nguyên tắc:
- **Versioning**: Sử dụng version trong API (v1, v2, ...)
- **Backward compatibility**: Code cũ vẫn hoạt động khi update API
- **Modular design**: Tách riêng các module/component
- **Optional fields**: Thêm fields mới mà không bắt buộc

### Ví dụ:

#### ❌ Bad - Không dễ mở rộng
```
GET /api/users/{id}
Response: {"id": 1, "name": "john", "email": "john@email.com"}

// Sau này muốn thêm phone - phá vỡ tất cả client cũ
// Nếu thêm required: GET /api/users/{id}/{phone}
```

#### ✅ Good - Dễ mở rộng
```
GET /api/v1/users/{id}
Response: {
  "id": 1,
  "name": "john",
  "email": "john@email.com",
  "phone": null  // Optional field, backward compatible
}

// Sau này thêm version mới mà code cũ vẫn hoạt động
GET /api/v2/users/{id}
Response: {
  "id": 1,
  "name": "john",
  "email": "john@email.com",
  "phone": "0123456789",
  "address": "123 Main St"  // Thêm field mới
}
```

## Tóm tắt Best Practices

| Nguyên tắc | Mô tả | Lợi ích |
|-----------|-------|---------|
| **Consistency** | Cùng format, cùng pattern | Dễ dự đoán, dễ maintain |
| **Clarity** | Rõ ràng, dễ hiểu | Dễ sử dụng, ít bug |
| **Extensibility** | Dễ mở rộng | Lâu dài, ít phá vỡ |

## Bài tập thực hành

1. Phân tích API hiện tại của bạn, liệt kê các điểm vi phạm từng best practice
2. Đề xuất cải thiện để tuân theo 3 best practices này

---
**Tiếp theo**: [Flow 2 - Naming Conventions](../2-naming-conventions/README.md)
