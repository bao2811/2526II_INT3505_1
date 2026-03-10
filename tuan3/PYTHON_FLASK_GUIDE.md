# Python Flask Code Examples - Tuan 3

Thư mục này chứa 6 ứng dụng Flask minh họa các khái niệm về thiết kế API trong tuần 3.

## 📦 Cài đặt Dependencies

```bash
cd /g/2526II_INT3505_1/tuan3
pip install -r requirements.txt
```

## 🚀 Chạy các ứng dụng

### Flow 1: Best Practices (Port 5000)
```bash
python 1-best-practices/app.py
```
**Minh họa:**
- ✅ Consistent response format cho tất cả endpoints
- ✅ Clear endpoint names (rõ ràng, dễ hiểu)
- ✅ Extensibility: versioning và pagination
- ✅ Unified error handling

**Endpoints test:**
```
GET    http://localhost:5000/api/v1/users
GET    http://localhost:5000/api/v1/users?page=1&limit=5
POST   http://localhost:5000/api/v1/users
GET    http://localhost:5000/api/v1/users/1
PUT    http://localhost:5000/api/v1/users/1
DELETE http://localhost:5000/api/v1/users/1
```

---

### Flow 2: Naming Conventions (Port 5001)
```bash
python 2-naming-conventions/app.py
```
**Minh họa:**
- ✅ Plural nouns: `/user-profiles` (không `/user-profile`)
- ✅ Lowercase: `/api/v1/` (không `/API/V1/`)
- ✅ Hyphens for multi-word: `/payment-methods` (không `/payment_methods`)
- ✅ Versioning: `/v1/`, `/v2/`
- ✅ Query parameters: `sort-by`, `search`, `page`, `limit`
- ✅ Nested resources: `/users/{id}/orders`
- ✅ Actions: `/users/{id}/verify-email`

**Endpoints test:**
```
GET    http://localhost:5001/api/v1/user-profiles
GET    http://localhost:5001/api/v1/user-profiles?sort-by=full_name&order=desc
GET    http://localhost:5001/api/v1/user-profiles/1
POST   http://localhost:5001/api/v1/user-profiles
GET    http://localhost:5001/api/v1/user-profiles/1/orders
GET    http://localhost:5001/api/v1/user-profiles/1/payment-methods
POST   http://localhost:5001/api/v1/user-profiles/1/verify-email
POST   http://localhost:5001/api/v1/user-profiles/1/reset-password
```

---

### Flow 3: API Endpoints - CRUD (Port 5002)
```bash
python 3-api-endpoints/app.py
```
**Minh họa:**
- ✅ CRUD Operations:
  - CREATE: `POST /api/v1/posts` → 201 Created
  - READ: `GET /api/v1/posts` → 200 OK
  - READ: `GET /api/v1/posts/{id}` → 200 OK
  - UPDATE: `PUT /api/v1/posts/{id}` → 200 OK (full update)
  - UPDATE: `PATCH /api/v1/posts/{id}` → 200 OK (partial update)
  - DELETE: `DELETE /api/v1/posts/{id}` → 204 No Content
- ✅ HTTP Status Codes: 200, 201, 204, 400, 404, 409, 422
- ✅ Nested Resources: `/posts/{id}/comments`
- ✅ Actions: `/posts/{id}/publish`, `/posts/{id}/unpublish`
- ✅ Pagination, Filtering, Sorting

**Endpoints test:**
```
POST   http://localhost:5002/api/v1/posts
       Body: {"title": "...", "content": "...", "author_id": 1}
GET    http://localhost:5002/api/v1/posts
GET    http://localhost:5002/api/v1/posts/1
GET    http://localhost:5002/api/v1/posts?status=published&page=1
PUT    http://localhost:5002/api/v1/posts/1
PATCH  http://localhost:5002/api/v1/posts/1
DELETE http://localhost:5002/api/v1/posts/1
GET    http://localhost:5002/api/v1/posts/1/comments
POST   http://localhost:5002/api/v1/posts/1/comments
GET    http://localhost:5002/api/v1/posts/1/comments/1
POST   http://localhost:5002/api/v1/posts/1/publish
```

---

### Flow 4: Design Evaluation (Port 5003)
```bash
python 4-design-evaluation/app.py
```
**Minh họa:**
- ✅ Evaluation Framework: 5 criteria × 20 points
  1. Consistency
  2. Clarity
  3. Extensibility
  4. Correctness
  5. Performance/Security
- ✅ Scoring: 0-100 points
  - 90-100: Excellent
  - 80-89: Good
  - 70-79: Fair
  - <70: Poor
- ✅ Real-world examples:
  - Good API (90+ score)
  - Fair API (70-79 score)
  - Poor API (<70 score)

**Endpoints test:**
```
GET    http://localhost:5003/api/v1/evaluations
GET    http://localhost:5003/api/v1/evaluations/good
GET    http://localhost:5003/api/v1/evaluations/fair
GET    http://localhost:5003/api/v1/evaluations/poor
GET    http://localhost:5003/api/v1/framework
GET    http://localhost:5003/api/v1/scoring-guidance
```

---

### Flow 5: Case Study - Poorly Designed API (Port 5004)
```bash
python 5-case-study-poorly-designed-api/app.py
```
**Minh họa 10 vấn đề thiết kế API tồi tệ:**
1. ❌ Verb-based endpoints: `/getallproducts`, `/getproduct`
2. ❌ Inconsistent response format: `{code, response}` vs `{status, data}`
3. ❌ Wrong HTTP methods: GET for logout, POST for search
4. ❌ Inconsistent parameter names: `prod_id`, `OrderID`, `orderid`
5. ❌ No API versioning
6. ❌ No pagination (returns all data)
7. ❌ No filtering/sorting
8. ❌ Wrong status codes (200 instead of 201)
9. ❌ No nested resources
10. ❌ Security issues (GET logout = CSRF)

**Endpoints test:**
```
GET    http://localhost:5004/api/getallproducts
GET    http://localhost:5004/api/getproduct?prod_id=1
GET    http://localhost:5004/api/logout
POST   http://localhost:5004/api/searchItems
GET    http://localhost:5004/api/getOrder?OrderID=ORD001
POST   http://localhost:5004/api/cancelorder?orderid=ORD001

Analysis:
GET    http://localhost:5004/api/issues-summary
GET    http://localhost:5004/api/refactored-comparison
```

---

### Flow 6: Peer Review - Well-Designed API (Port 5005)
```bash
python 6-peer-review/app.py
```
**Minh họa:**
- ✅ API sẵn sàng cho Peer Review
- ✅ Consistent naming conventions
- ✅ Proper HTTP methods
- ✅ Standardized response format
- ✅ Good error handling
- ✅ Pagination with metadata
- ✅ Nested resources
- ✅ API versioning
- ✅ Self-documenting endpoints

**Endpoints test:**
```
GET    http://localhost:5005/api/v1/projects
POST   http://localhost:5005/api/v1/projects
GET    http://localhost:5005/api/v1/projects/1
PUT    http://localhost:5005/api/v1/projects/1
PATCH  http://localhost:5005/api/v1/projects/1
DELETE http://localhost:5005/api/v1/projects/1
GET    http://localhost:5005/api/v1/projects/1/tasks
POST   http://localhost:5005/api/v1/team-members
GET    http://localhost:5005/api/v1/review-checklist
GET    http://localhost:5005/api/v1/peer-review-feedback
```

---

## 📊 Comparison Table

| Flow | Port | Focus | Status Codes | Notable |
|------|------|-------|--------------|---------|
| Flow 1 | 5000 | Best Practices | ✅ Consistent | Unified error format |
| Flow 2 | 5001 | Naming Conventions | ✅ Correct | Plural nouns, hyphens, versioning |
| Flow 3 | 5002 | CRUD Endpoints | ✅ Proper | 201, 204, 400, 404, 422 |
| Flow 4 | 5003 | Design Evaluation | ✅ Framework | Scoring system |
| Flow 5 | 5004 | Poorly Designed | ❌ Many issues | 10 anti-patterns |
| Flow 6 | 5005 | Peer Review | ✅ Excellent | Production-ready example |

---

## 🧪 Testing with curl

### Example: Flow 3 - Create a post
```bash
curl -X POST http://localhost:5002/api/v1/posts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My API Design Article",
    "content": "Learn about API design principles",
    "author_id": 1
  }'
```

### Example: Flow 2 - List with filtering
```bash
curl "http://localhost:5001/api/v1/user-profiles?sort-by=full_name&order=desc&limit=5"
```

### Example: Flow 5 - See issues
```bash
curl http://localhost:5004/api/issues-summary | python -m json.tool
```

---

## 📚 Learning Path

1. **Start with Flow 1** - Understand best practices (consistency, clarity, extensibility)
2. **Learn Flow 2** - Master naming conventions (plural, lowercase, hyphens, versioning)
3. **Build with Flow 3** - Design endpoints correctly (CRUD, HTTP methods, status codes)
4. **Evaluate with Flow 4** - Score API design quality using framework
5. **Analyze Flow 5** - Identify anti-patterns in poorly designed APIs
6. **Review with Flow 6** - See a well-designed API ready for production

---

## 💡 Key Concepts

### HTTP Methods
```
GET    - Retrieve data (safe, idempotent)
POST   - Create new resource (201 Created)
PUT    - Replace entire resource (full update)
PATCH  - Partial update to resource
DELETE - Remove resource (204 No Content)
```

### Status Codes
```
200 OK              - Request succeeded with response
201 Created         - Resource created successfully
204 No Content      - Success with no response body
400 Bad Request     - Invalid request format
401 Unauthorized    - Not authenticated
403 Forbidden       - Not authorized
404 Not Found       - Resource doesn't exist
409 Conflict        - Duplicate/conflict
422 Unprocessable   - Validation error
500 Server Error    - Server error
```

### Response Format
```json
// Success
{
  "status": "success",
  "data": { ... },
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 20
  }
}

// Error
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {"field": "email", "message": "Email is required"}
    ]
  }
}
```

---

## ❓ FAQ

**Q: Can I run all 6 apps at the same time?**
A: Yes! Each uses a different port (5000-5005), so you can run them all simultaneously.

**Q: How do I choose which app to study?**
A: Follow the learning path above, or jump to the flow that interests you.

**Q: Can I modify the code?**
A: Yes! These are examples. Modify them to experiment and learn.

**Q: How do I test without curl?**
A: Use Postman, Thunder Client, or any REST client. The endpoints accept JSON.

---

**Happy Learning! 🚀**
