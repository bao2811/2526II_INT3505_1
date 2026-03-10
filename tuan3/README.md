# Tuần 3: Nguyên Tắc Thiết Kế API (API Design Principles)

## Mục tiêu khóa học

Sau tuần 3, bạn sẽ có khả năng:

### Kiến thức Cần Đạt
- ✅ Hiểu các best practices: consistency, clarity, extensibility
- ✅ Nắm vững naming conventions: plural nouns, lowercase, hyphens, versioning
- ✅ Biết cách đánh giá chất lượng thiết kế API
- ✅ Nhận diện lỗi trong một API poorly designed
- ✅ Đưa feedback xây dựng trong peer review

### Kỹ Năng Cần Làm Được
- ✅ Áp dụng quy tắc đặt tên endpoint (ví dụ: `/users`, `/orders/{id}`)
- ✅ Thiết kế CRUD endpoints đúng theo REST principles
- ✅ Sử dụng HTTP methods và status codes chính xác
- ✅ Đánh giá API design quality theo framework
- ✅ Conduct peer review hiệu quả

---

## Cấu trúc Tuần 3

Tuần này được chia thành 6 flows, mỗi flow đi sâu vào một khía cạnh của API design:

### 📚 **Flow 1: Best Practices**
**File**: [1-best-practices/README.md](./1-best-practices/README.md)

Tìm hiểu 3 best practices chính:
- **Consistency** - Nhất quán format, pattern, naming
- **Clarity** - Dễ hiểu, rõ ràng, có documentation
- **Extensibility** - Dễ mở rộng, versioning, backward compatible

**Thời gian**: 45 phút
**Kết quả**: Hiểu rõ làm sao để thiết kế API theo best practices

---

### 📚 **Flow 2: Naming Conventions**
**File**: [2-naming-conventions/README.md](./2-naming-conventions/README.md)

Học các quy tắc đặt tên chuẩn:
- Plural nouns: `/users` không phải `/user`
- Lowercase: `/api/users` không phải `/api/Users`
- Hyphens: `/user-profiles` không phải `/user_profiles`
- Versioning: `/v1/users` không phải `/users`
- Query parameters cũng phải consistent

**Thời gian**: 1 giờ
**Kết quả**: Biết cách đặt tên endpoint, parameter, query string

---

### 📚 **Flow 3: API Endpoints**
**File**: [3-api-endpoints/README.md](./3-api-endpoints/README.md)

Thiết kế endpoints đúng theo quy tắc:
- CRUD mapping: CREATE→POST, READ→GET, UPDATE→PUT/PATCH, DELETE→DELETE
- HTTP status codes: 201 Created, 400 Bad Request, 401 Unauthorized, etc.
- Response format consistent
- Nested resources
- Query parameters cho filtering, pagination, sorting

**Thời gian**: 1.5 giờ
**Kết quả**: Thiết kế được một bộ endpoints chất lượng cao

---

### 📚 **Flow 4: Design Evaluation**
**File**: [4-design-evaluation/README.md](./4-design-evaluation/README.md)

Đánh giá chất lượng API design:
- Framework: Consistency, Clarity, Extensibility, Correctness, Performance/Security
- Scoring rubric (0-100 points)
- Evaluation checklist
- Real-world examples

**Thời gian**: 45 phút
**Kết quả**: Có thể đánh giá bất kỳ API nào và cho score

---

### 📚 **Flow 5: Case Study - Poorly Designed API**
**File**: [5-case-study-poorly-designed-api/README.md](./5-case-study-poorly-designed-api/README.md)

Phân tích một API thiết kế tồi tệ:
- Phát hiện 10 lỗi chính
- Giải thích tại sao là lỗi
- Impact analysis
- Refactored solution
- Lessons learned

**Thời gian**: 1 giờ
**Kết quả**: Biết nhận diện vấn đề và cải thiện

---

### 📚 **Flow 6: Peer Review**
**File**: [6-peer-review/README.md](./6-peer-review/README.md)

Conduct peer review hiệu quả:
- Review process & preparation
- Review checklist
- Review template
- Best practices DO's & DON'Ts
- Meeting agenda
- Follow-up actions

**Thời gian**: 1 giờ
**Kết quả**: Có thể review API của team mate một cách chuyên nghiệp

---

## Learning Path

```
Flow 1: Best Practices (Kiến thức nền)
   ↓
Flow 2: Naming Conventions (Chi tiết 1)
   ↓
Flow 3: API Endpoints (Chi tiết 2)
   ↓
Flow 4: Design Evaluation (Ứng dụng)
   ↓
Flow 5: Case Study (Thực hành)
   ↓
Flow 6: Peer Review (Kỹ năng mềm)
```

**Khuyến cáo**: Theo thứ tự này để hiểu từng bước.

---

## Practical Exercises

### Bài 1: Naming Convention Check (30 phút)
**Quy tắc:**
- Chọn 1 API đã học ở tuan trước
- Check xem có follow naming conventions không
- List các vi phạm
- Đề xuất cải thiện

**Output:** 1 file: `exercise-1-naming-check.md`

---

### Bài 2: Design Your Blog API (1 giờ)
**Yêu cầu:**
- Thiết kế API cho Blog system
- Endpoints: Posts, Comments, Categories, Tags, Authors
- Phải có: CRUD, nested resources, filtering, pagination, sorting
- Sử dụng `/api/v1/` versioning
- Viết ví dụ requests/responses

**Output:** 1 file: `exercise-2-blog-api-design.md`

---

### Bài 3: Evaluate an API (45 phút)
**Yêu cầu:**
- Chọn 1 public API (GitHub, Stripe, Postman, etc)
- Evaluate sử dụng framework từ Flow 4
- Score từng category (0-20)
- List issues & suggestions
- Write report

**Output:** 1 file: `exercise-3-api-evaluation-report.md`

---

### Bài 4: Case Study Analysis (1 giờ)
**Yêu cầu:**
- Analyze API poorly designed
- Identify tất cả lỗi (tương tự case study)
- Assign severity levels
- Propose refactored design
- Create comparison table

**Output:** 1 file: `exercise-4-case-study-analysis.md`

---

### Bài 5: Peer Review (1.5 giờ)
**Yêu cầu:**
- Conduct peer review trên API của 1 teammate
- Sử dụng review template
- Document all feedback
- Schedule follow-up
- Create action items

**Output:** 1 file: `exercise-5-peer-review-report.md`

---

## Resources

### External Resources
- [REST API Best Practices](https://restfulapi.net/)
- [OpenAPI/Swagger Specification](https://swagger.io/resources/articles/best-practices-in-api-design/)
- [HTTP Status Codes](https://httpwg.org/specs/rfc7231.html#status.codes)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [JSON:API Specification](https://jsonapi.org/)

### Key Concepts
- **REST**: Representational State Transfer
- **HTTP Methods**: GET, POST, PUT, PATCH, DELETE
- **Status Codes**: 2xx, 4xx, 5xx
- **Versioning**: API versioning strategies
- **Resources**: Core REST concepts

---

## Assessment Criteria

Sau tuần 3, bạn sẽ được đánh giá dựa trên:

### Knowledge (30%)
- [ ] Hiểu 3 best practices chính
- [ ] Nắm vững naming conventions
- [ ] Biết HTTP methods & status codes

### Skills (50%)
- [ ] Thiết kế endpoints đúng quy tắc
- [ ] Evaluate API design
- [ ] Phát hiện issues trong poorly designed APIs
- [ ] Propose improvements

### Soft Skills (20%)
- [ ] Điểm peer review quality
- [ ] Communication clarity
- [ ] Collaboration

---

## Next Steps

### Tuần 4 sẽ học
- Advanced API patterns
- Authentication & Authorization
- API Security Best Practices
- Rate Limiting & Throttling
- Caching Strategies

---

## Quick Reference Checklist

```
✅ API Design Checklist

Naming:
  □ Plural nouns (/users)
  □ Lowercase (/api/v1/)
  □ Hyphens for multi-word (/user-profiles)
  □ Versioning (/v1/)

HTTP Methods:
  □ GET for retrieval
  □ POST for creation
  □ PUT/PATCH for update
  □ DELETE for deletion
  □ No verbs in URL

Status Codes:
  □ 201 Created for POST
  □ 200 OK for success
  □ 400 Bad Request for client error
  □ 401 Unauthorized
  □ 403 Forbidden
  □ 404 Not Found
  □ 422 Validation Error
  □ 500 Server Error

Response Format:
  □ Consistent structure
  □ Has status field
  □ Error format defined
  □ Metadata (pagination)

Features:
  □ Pagination
  □ Filtering
  □ Sorting
  □ Search
  □ Related resources
```

---

## Tóm tắt Tuần 3

| Flow | Title | Focus | Time |
|------|-------|-------|------|
| 1 | Best Practices | Consistency, Clarity, Extensibility | 45' |
| 2 | Naming Conventions | Naming rules & standards | 1h |
| 3 | API Endpoints | CRUD, HTTP, Status codes | 1.5h |
| 4 | Design Evaluation | Evaluation framework & scoring | 45' |
| 5 | Case Study | Poor API analysis & refactoring | 1h |
| 6 | Peer Review | Review process & techniques | 1h |

**Total**: ~6 giờ học + practice exercises

---

## Questions?

Nếu bạn có câu hỏi:
- Tham khảo các flow chi tiết
- Check external resources
- Hỏi instructor

---

**Happy Learning! 🚀**

---

Index:
- [Flow 1: Best Practices](./1-best-practices/README.md)
- [Flow 2: Naming Conventions](./2-naming-conventions/README.md)
- [Flow 3: API Endpoints](./3-api-endpoints/README.md)
- [Flow 4: Design Evaluation](./4-design-evaluation/README.md)
- [Flow 5: Case Study](./5-case-study-poorly-designed-api/README.md)
- [Flow 6: Peer Review](./6-peer-review/README.md)
