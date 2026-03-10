# Flow 4: Đánh giá Chất lượng Thiết kế API

## Mục tiêu
Học cách phân tích và đánh giá một API có tuân theo best practices hay không, và xác định các vấn đề thiết kế.

## API Design Quality Framework

### 1. Consistency (Nhất quán) - 20%

**Các thứ cần check:**

- [ ] Tất cả endpoints sử dụng cùng format response
- [ ] Tất cả errors sử dụng cùng format
- [ ] HTTP methods sử dụng consistently
- [ ] Status codes sử dụng consistently
- [ ] Naming conventions consistent (plural, lowercase, hyphens)

**Scoring:**
- ✅ Tất cả consistent: 20/20
- ⚠️ 1-2 lỗi: 15/20
- ❌ Nhiều lỗi: 10/20

### 2. Clarity (Dễ hiểu) - 20%

**Các thứ cần check:**

- [ ] Endpoint names rõ ràng, mô tả chức năng
- [ ] Request parameters rõ ràng
- [ ] Response fields rõ ràng
- [ ] Error messages rõ ràng, helpful
- [ ] Có documentation/examples

**Scoring:**
- ✅ Rất rõ ràng: 20/20
- ⚠️ Có chỗ không rõ: 15/20
- ❌ Khó hiểu: 10/20

### 3. Extensibility (Dễ mở rộng) - 20%

**Các thứ cần check:**

- [ ] Có API versioning
- [ ] Backward compatible (thêm fields mới = optional)
- [ ] Modular design (tách riêng resources)
- [ ] Query parameters cho filtering/pagination
- [ ] Support include/expand cho related resources

**Scoring:**
- ✅ Rất dễ mở rộng: 20/20
- ⚠️ Có chướng ngại: 15/20
- ❌ Khó mở rộng: 10/20

### 4. Correctness (Chính xác) - 20%

**Các thứ cần check:**

- [ ] HTTP methods map correctly (GET, POST, PUT, DELETE)
- [ ] Status codes phù hợp
- [ ] Nested resources thiết kế đúng
- [ ] CRUD operations đầy đủ
- [ ] Error handling comprehensive

**Scoring:**
- ✅ Hầu hết correct: 20/20
- ⚠️ Một vài lỗi: 15/20
- ❌ Nhiều lỗi: 10/20

### 5. Performance & Security - 20%

**Các thứ cần check:**

- [ ] Có pagination support
- [ ] Có filtering/sorting
- [ ] Rate limiting policy
- [ ] Authentication/Authorization
- [ ] Input validation errors (422)
- [ ] Sensitive data handling

**Scoring:**
- ✅ Có tất cả: 20/20
- ⚠️ Thiếu vài thứ: 15/20
- ❌ Thiếu nhiều: 10/20

## Evaluation Rubric - Bảng đánh giá

| Tiêu chí | Score | Ghi chú |
|---------|-------|---------|
| Consistency | /20 | Có lỗi consistency gì không? |
| Clarity | /20 | Có chỗ khó hiểu không? |
| Extensibility | /20 | Dễ mở rộng không? |
| Correctness | /20 | HTTP methods/status codes đúng không? |
| Performance/Security | /20 | Có high-level security không? |
| **TOTAL** | **/100** | |

**Score Interpretation:**
- **90-100**: Excellent - Production ready
- **80-89**: Good - Acceptable, minor improvements
- **70-79**: Fair - Needs improvements
- **Below 70**: Poor - Needs significant refactoring

## Checklist Evaluation

### Naming Conventions (10 points)

```
□ Plural nouns cho resources (+2)
□ Lowercase (+2)
□ Hyphens cho multi-word (+2)
□ Clear names (+2)
□ Versioning (+2)
```

### HTTP Methods (10 points)

```
□ GET cho retrieval (+2)
□ POST cho creation (+2)
□ PUT/PATCH cho update (+2)
□ DELETE cho deletion (+2)
□ No verb in URL (+2)
```

### Response Format (10 points)

```
□ Consistent JSON structure (+2)
□ Status field (+2)
□ Data field (+2)
□ Error format consistent (+2)
□ Metadata (pagination, etc) (+2)
```

### Status Codes (10 points)

```
□ 200 cho success (+1)
□ 201 cho created (+1)
□ 400 cho bad request (+1)
□ 401 cho unauthorized (+1)
□ 403 cho forbidden (+1)
□ 404 cho not found (+1)
□ 422 cho validation error (+1)
□ 500 cho server error (+2)
□ 5xx handling (+1)
```

### Features (10 points)

```
□ Pagination support (+2)
□ Filtering support (+2)
□ Sorting support (+2)
□ Search support (+2)
□ Include/expand related (+2)
```

**Total Checklist: 50 points** (Scale to 100 for final score)

## Ví dụ Evaluation thực tế

### API Sample 1: User Management API

```
GET    /api/getUsers
POST   /api/createUser
GET    /api/getUserById?id=1
PUT    /api/updateUser
DELETE /api/deleteUser?id=1

Response format:
{
  "success": true,
  "result": { ... }
}

Errors:
{
  "success": false,
  "message": "Some error"
}
```

**Evaluation:**

```
Consistency: 10/20
  ❌ Verb-based endpoints (getUsers, createUser)
  ❌ Inconsistent params (query string for ID, body for others)
  ❌ Response format OK but basic

Clarity: 12/20
  ⚠️ Endpoint names clear but verb-based
  ⚠️ Error message not detailed enough

Extensibility: 8/20
  ❌ No versioning
  ❌ No pagination support
  ❌ Tight coupling (verb in URL)

Correctness: 12/20
  ❌ GET for create/delete operations
  ❌ No proper status codes (always 200?)
  ❌ No proper nested resource design

Performance: 8/20
  ❌ No pagination
  ❌ No filtering
  ❌ No sorting

TOTAL: 50/100 - POOR (Needs significant refactoring)
```

### API Sample 2: Blog API

```
GET    /api/v1/posts
POST   /api/v1/posts
GET    /api/v1/posts/{id}
PUT    /api/v1/posts/{id}
DELETE /api/v1/posts/{id}

GET    /api/v1/posts/{id}/comments
POST   /api/v1/posts/{id}/comments
GET    /api/v1/posts/{id}/comments/{commentId}
DELETE /api/v1/posts/{id}/comments/{commentId}

Query support:
GET /api/v1/posts?page=1&limit=20&status=published&sort-by=date&order=desc

Response:
{
  "status": "success",
  "data": [ ... ],
  "meta": { "total": 100, "page": 1 }
}

Errors:
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "details": [ ... ]
  }
}
```

**Evaluation:**

```
Consistency: 18/20
  ✅ Plural nouns
  ✅ Consistent response format
  ✅ Nested resources correct
  ⚠️ Minor: error format could be more detailed

Clarity: 19/20
  ✅ Clear endpoint names
  ✅ Clear nesting
  ✅ Response structure clear
  ⚠️ Minor: could have more examples

Extensibility: 18/20
  ✅ API versioning (v1)
  ✅ Backward compatible
  ✅ Good modular design
  ⚠️ Could support include/expand

Correctness: 19/20
  ✅ Proper HTTP methods
  ✅ Proper nested design
  ✅ Status codes probably correct
  ⚠️ Minor: could document all status codes

Performance: 17/20
  ✅ Pagination support
  ✅ Filtering support
  ✅ Sorting support
  ⚠️ Minor: search support not mentioned

TOTAL: 91/100 - EXCELLENT (Production ready)
```

## Evaluation Worksheet

### API to Evaluate: ____________

**1. Naming Conventions (10 pts)**
- Resource names: □ Plural □ Lowercase □ Hyphens
- Score: ___/10

**2. HTTP Methods (10 pts)**
- Proper mapping: □ GET □ POST □ PUT □ DELETE □ No verbs
- Score: ___/10

**3. Response Format (10 pts)**
- Consistency: □ Yes □ No
- Has metadata: □ Yes □ No
- Error format: □ Clear □ Unclear
- Score: ___/10

**4. Status Codes (10 pts)**
- 2xx for success: □ Yes □ No
- 4xx for client errors: □ Yes □ No
- 5xx for server errors: □ Yes □ No
- Proper codes used: □ Yes □ No
- Score: ___/10

**5. Features (10 pts)**
- Pagination: □ Yes □ No □ N/A
- Filtering: □ Yes □ No □ N/A
- Sorting: □ Yes □ No □ N/A
- Search: □ Yes □ No □ N/A
- Versioning: □ Yes □ No
- Score: ___/10

**6. Issues Found:**
1. ________________
2. ________________
3. ________________

**7. Improvements Suggested:**
1. ________________
2. ________________
3. ________________

**TOTAL SCORE: ___/100**

## Bài tập thực hành

1. **Evaluate 3 public APIs**: (GitHub API, Stripe API, etc)
   - Use evaluation framework
   - Score each one
   - Document findings

2. **Compare 2 APIs**: So sánh thiết kế giữa 2 APIs
   - Cái nào tốt hơn?
   - Tại sao?

3. **Self-evaluate**: Evaluate API của chính bạn
   - Identify weaknesses
   - Plan improvements

---
**Tiếp theo**: [Flow 5 - Case Study](../5-case-study-poorly-designed-api/README.md)
