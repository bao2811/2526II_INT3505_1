# Flow 3: API Endpoints - Thiết kế Endpoint theo Đúng Quy tắc

## Mục tiêu
Áp dụng các quy tắc đặt tên và thiết kế để tạo ra các endpoint chất lượng cao, dễ sử dụng và dễ maintain.

## Quy tắc thiết kế Endpoint

### 1. CRUD Operations - Mapping to HTTP Methods

Mỗi endpoint nên map chính xác với CRUD operation tương ứng:

```
CREATE → POST
READ   → GET
UPDATE → PUT / PATCH
DELETE → DELETE
LIST   → GET (collection)
```

### 2. Endpoint Pattern chuẩn

#### Pattern 1: Single Resource

```
# CREATE
POST   /api/v1/users
Body: {
  "name": "John Doe",
  "email": "john@example.com"
}
Response 201: { "id": 1, "name": "John Doe", "email": "john@example.com" }

# READ (List)
GET    /api/v1/users
Response 200: [
  { "id": 1, "name": "John Doe" },
  { "id": 2, "name": "Jane Doe" }
]

# READ (Single)
GET    /api/v1/users/1
Response 200: { "id": 1, "name": "John Doe", "email": "john@example.com" }

# UPDATE (Full)
PUT    /api/v1/users/1
Body: { "name": "Johnny Doe", "email": "johnny@example.com" }
Response 200: { "id": 1, "name": "Johnny Doe", "email": "johnny@example.com" }

# UPDATE (Partial)
PATCH  /api/v1/users/1
Body: { "name": "Johnny Doe" }
Response 200: { "id": 1, "name": "Johnny Doe", "email": "john@example.com" }

# DELETE
DELETE /api/v1/users/1
Response 204: (No Content)
```

#### Pattern 2: Nested Resources

```
# CREATE nested resource
POST   /api/v1/users/1/orders
Body: { "product_id": 5, "quantity": 2 }
Response 201: { "id": 100, "user_id": 1, "product_id": 5 }

# READ nested resources (list)
GET    /api/v1/users/1/orders
Response 200: [ { "id": 100, ... }, { "id": 101, ... } ]

# READ specific nested resource
GET    /api/v1/users/1/orders/100
Response 200: { "id": 100, "user_id": 1, "product_id": 5 }

# UPDATE nested resource
PUT    /api/v1/users/1/orders/100
Body: { "quantity": 3 }

# DELETE nested resource
DELETE /api/v1/users/1/orders/100
```

### 3. Query Parameters cho Collection

```
# Pagination
GET /api/v1/users?page=1&limit=20
GET /api/v1/users?offset=0&limit=20

# Filtering
GET /api/v1/users?status=active&role=admin
GET /api/v1/products?category=electronics&min-price=100&max-price=5000

# Sorting
GET /api/v1/users?sort-by=created-date&order=desc
GET /api/v1/products?sort=price:asc,name:desc

# Searching
GET /api/v1/users?search=john
GET /api/v1/products?q=laptop

# Include related resources
GET /api/v1/users/1?include=orders,profile,addresses

# Select specific fields
GET /api/v1/users?fields=id,name,email
```

### 4. HTTP Status Codes - Khi nào dùng cái gì?

| Code | Meaning | Khi dùng |
|------|---------|----------|
| **200** | OK | Request thành công, có response body |
| **201** | Created | Resource được tạo thành công |
| **204** | No Content | Request thành công nhưng không có response body |
| **400** | Bad Request | Client error (format sai, validation fail) |
| **401** | Unauthorized | Không authenticate (chưa login) |
| **403** | Forbidden | Không có quyền access |
| **404** | Not Found | Resource không tồn tại |
| **409** | Conflict | Conflict (vd: duplicate email) |
| **422** | Unprocessable Entity | Validation error (chi tiết) |
| **500** | Internal Server Error | Server error |
| **503** | Service Unavailable | Server maintenance/overload |

### 5. Response Body Format chuẩn

```json
// Success Response
{
  "status": "success",
  "data": { ... },
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 20
  }
}

// Error Response
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Email is required"
      },
      {
        "field": "name",
        "message": "Name must be at least 3 characters"
      }
    ]
  }
}
```

## Ví dụ thực tế: Blog API

### Base URL: `https://api.myblog.com/v1`

```
# ============ POSTS ============

# Create post
POST   /posts
Body: {
  "title": "Getting Started with API Design",
  "content": "...",
  "status": "draft"
}
Response 201: { "id": 1, "title": "...", "slug": "getting-started..." }

# Get all posts
GET    /posts?status=published&sort-by=published-date&order=desc&page=1&limit=10

# Get specific post
GET    /posts/1

# Get posts by category
GET    /posts?category=web-development

# Search posts
GET    /posts?search=api

# Update post
PUT    /posts/1
Body: { "title": "Updated Title", "content": "..." }

# Partial update post
PATCH  /posts/1
Body: { "status": "published" }

# Delete post
DELETE /posts/1

# ============ COMMENTS ============

# Create comment on post
POST   /posts/1/comments
Body: { "content": "Great article!" }

# Get comments of post
GET    /posts/1/comments?page=1&limit=20

# Get specific comment
GET    /posts/1/comments/5

# Update comment
PUT    /posts/1/comments/5
Body: { "content": "Updated comment" }

# Delete comment
DELETE /posts/1/comments/5

# ============ LIKES ============

# Like a post
POST   /posts/1/likes
Response 201: { "id": 1, "post_id": 1, "user_id": 123 }

# Unlike a post
DELETE /posts/1/likes

# Get likes count
GET    /posts/1/likes/count
Response 200: { "count": 42 }

# ============ AUTHORS ============

# Get author info
GET    /authors/1

# Get author's posts
GET    /authors/1/posts

# ============ TAGS ============

# Get all tags
GET    /tags

# Get posts with specific tag
GET    /tags/web-development/posts
```

## Endpoint Design Checklist

### Resource Design
- [ ] Endpoint sử dụng plural nouns (`/users` không phải `/user`)
- [ ] Sử dụng lowercase và hyphens (`/user-profiles` không phải `/UserProfiles`)
- [ ] Có API versioning (`/v1/` không phải không có version)
- [ ] Nested resources rõ ràng (`/users/1/orders` không phải `/get-user-orders`)

### HTTP Methods
- [ ] GET cho retrieval operations
- [ ] POST cho creation operations
- [ ] PUT/PATCH cho update operations
- [ ] DELETE cho deletion operations
- [ ] Không mix methods (không dùng GET để create/delete)

### Status Codes
- [ ] 201 Created cho successful POST
- [ ] 204 No Content cho DELETE (nếu không return data)
- [ ] 400/422 cho validation errors
- [ ] 401 cho unauthenticated requests
- [ ] 403 cho unauthorized requests
- [ ] 404 cho not found resources

### Query Parameters
- [ ] Pagination (page/limit hoặc offset/limit)
- [ ] Filtering theo common attributes
- [ ] Sorting support
- [ ] Search/query support nếu cần
- [ ] Include/expand cho related resources

### Response Format
- [ ] Consistent response structure
- [ ] Có status field
- [ ] Error responses có clear messages
- [ ] List responses có pagination metadata
- [ ] Timestamps for created/updated

## Anti-patterns - Cái gì KHÔNG nên làm

```
❌ GET    /users/create              # Tạo mới nên dùng POST
❌ GET    /users/delete/1            # Xóa nên dùng DELETE
❌ POST   /getUser                   # GET không POST
❌ POST   /users?action=delete       # Dùng query string cho action
❌ /api/getUserById/123              # Verb + không cần /id
❌ /api/users/1/get-orders           # Verb ở cuối
❌ /v2.0.1/users                     # Quá specific version
❌ /API/Users/123                    # Inconsistent casing/plural
```

## Bài tập thực hành

1. **Design Blog API**: Tạo danh sách 10-15 endpoints cho blog system
   - Posts, Comments, Categories, Tags, Authors
   - Include tất cả CRUD operations
   - Sử dụng nested resources thích hợp

2. **Review một API**: Lấy một public API, phân tích endpoints
   - Check xem có follow naming conventions không
   - List các anti-patterns
   - Đề xuất improvements

3. **Refactor Exercise**: Cho một list bad endpoints, refactor thành good endpoints

---
**Tiếp theo**: [Flow 4 - Design Evaluation](../4-design-evaluation/README.md)
