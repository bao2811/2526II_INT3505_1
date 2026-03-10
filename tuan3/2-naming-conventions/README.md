# Flow 2: Naming Conventions - Quy tắc đặt tên API

## Mục tiêu
Hiểu và áp dụng các quy tắc đặt tên chuẩn cho API endpoint, resource, và parameters.

## Các Naming Conventions Chính

### 1. Sử dụng Plural Nouns (Danh từ số nhiều)

**Nguyên tắc**: Resource nên là danh từ ở dạng số nhiều

#### ❌ Bad - Singular
```
GET /api/user
GET /api/product
POST /api/order
GET /user/123
```

#### ✅ Good - Plural
```
GET /api/users              # Lấy danh sách users
GET /api/users/123          # Lấy user cụ thể
GET /api/products           # Lấy danh sách products
POST /api/orders            # Tạo order mới
```

**Tại sao?**
- Consistent - tất cả resource là danh từ số nhiều
- Rõ ràng - biết ngay là collection
- Dễ hiểu - tự nhiên hơn "users" vs "user"

### 2. Lowercase (Chữ thường)

**Nguyên tắc**: Tất cả endpoint nên sử dụng chữ thường

#### ❌ Bad - Mixed case
```
GET /api/Users
GET /api/UserProfiles
GET /api/GetUserById
POST /api/CreateProduct
```

#### ✅ Good - Lowercase
```
GET /api/users
GET /api/user-profiles
GET /api/users/{id}
POST /api/products
```

**Tại sao?**
- Standards hầu hết theo HTTP là lowercase
- URL encoding dễ hơn
- Consistent với programming conventions

### 3. Hyphens (Dấu gạch ngang) cho Multi-word

**Nguyên tắc**: Khi tên có nhiều từ, sử dụng hyphens không phải underscores

#### ❌ Bad - Underscores
```
GET /api/user_profiles
GET /api/product_categories
GET /api/order_items
GET /api/payment_methods
```

#### ✅ Good - Hyphens
```
GET /api/user-profiles
GET /api/product-categories
GET /api/order-items
GET /api/payment-methods
```

**Tại sao?**
- URL standards là hyphens
- Underscores có thể không hiển thị đúng trong một số trình duyệt
- Consistent với REST standards

### 4. Versioning (Phiên bản API)

**Nguyên tắc**: Sử dụng version trong URL để hỗ trợ backward compatibility

#### Cách 1: Trong URL path (Common)
```
GET /api/v1/users
GET /api/v2/users
GET /api/v3/users
```

#### Cách 2: Trong subdomain
```
GET /v1.api.example.com/users
GET /v2.api.example.com/users
```

#### Cách 3: Trong header (không recommend)
```
GET /api/users
Headers: API-Version: 1
```

**Best Practice**: Sử dụng version trong URL path
```
https://api.example.com/v1/users
https://api.example.com/v1/products
https://api.example.com/v2/users  # Nếu có breaking changes
```

## Quy tắc đặt tên Hierarchy

### Ví dụ: E-commerce API

```
# Collection endpoints (danh sách)
GET    /api/v1/users                          # Lấy danh sách users
GET    /api/v1/products                       # Lấy danh sách products
GET    /api/v1/orders                         # Lấy danh sách orders

# Specific resource endpoints (tài nguyên cụ thể)
GET    /api/v1/users/{id}                     # Lấy user cụ thể
GET    /api/v1/products/{id}                  # Lấy product cụ thể
GET    /api/v1/orders/{id}                    # Lấy order cụ thể

# Nested resources (tài nguyên con)
GET    /api/v1/users/{userId}/orders          # Orders của user cụ thể
GET    /api/v1/orders/{orderId}/items         # Items trong order cụ thể
GET    /api/v1/users/{userId}/addresses       # Địa chỉ của user

# Actions (nếu cần)
POST   /api/v1/orders/{id}/cancel             # Action trên resource
POST   /api/v1/users/{id}/reset-password      # Action trên resource
```

### Pattern: `/{resource}/{id}/{sub-resource}/{sub-id}`

```
/api/v1/users/{userId}/orders/{orderId}/items
└────┬───┘└──┬──┘└───┬───┘└─────┬─────┘└───┬──┘
   base   version resource  nesting    sub-resource
```

## Parameter Naming Conventions

### Query Parameters (Lowercase, hyphens)

```
# Pagination
GET /api/v1/users?page=1&limit=10
GET /api/v1/users?skip=0&take=20

# Filtering
GET /api/v1/users?status=active
GET /api/v1/products?category=electronics&min-price=100

# Sorting
GET /api/v1/users?sort-by=created-date&order=desc

# Searching
GET /api/v1/users?search=john
GET /api/v1/products?q=laptop

# Include related data
GET /api/v1/users/123?include=orders,profile
```

### Best Practices:

```
✅ /api/v1/products?min-price=100&max-price=1000
✅ /api/v1/users?sort-by=created-date&order=desc
❌ /api/v1/products?MinPrice=100&MaxPrice=1000
❌ /api/v1/users?sortBy=created_date&order=desc
```

## HTTP Methods Conventions

```
GET    /api/v1/users              # Lấy danh sách
POST   /api/v1/users              # Tạo mới
GET    /api/v1/users/{id}         # Lấy chi tiết
PUT    /api/v1/users/{id}         # Cập nhật toàn bộ
PATCH  /api/v1/users/{id}         # Cập nhật một phần
DELETE /api/v1/users/{id}         # Xóa
```

## Checklist: Naming Conventions

- [ ] Sử dụng plural nouns cho tất cả resources
- [ ] Tất cả lowercase (không CamelCase)
- [ ] Multi-word sử dụng hyphens (không underscores)
- [ ] Có API versioning (v1, v2, ...)
- [ ] Query parameters consistent (lowercase, hyphens)
- [ ] HTTP methods đúng với intent
- [ ] Nested resources có hierarchy rõ ràng
- [ ] Parameter names rõ ràng, dễ hiểu

## Ví dụ API Well-designed

```
# Base URL: https://api.example.com/v1

GET    /users                      # Get all users
POST   /users                      # Create new user
GET    /users/{id}                 # Get specific user
PUT    /users/{id}                 # Update user
PATCH  /users/{id}                 # Partial update
DELETE /users/{id}                 # Delete user

GET    /users/{id}/orders          # Get user's orders
POST   /users/{id}/orders          # Create order for user
GET    /users/{id}/orders/{orderId}
DELETE /users/{id}/orders/{orderId}

GET    /products?category=electronics&min-price=100
GET    /products?search=laptop&sort-by=price&order=asc
```

## Bài tập thực hành

1. Phân tích API của bạn, check xem có tuân theo naming conventions không
2. List các endpoint vi phạm quy tắc
3. Đề xuất cải thiện

---
**Tiếp theo**: [Flow 3 - API Endpoints](../3-api-endpoints/README.md)
