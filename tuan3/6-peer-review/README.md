# Flow 6: Peer Review - Đánh giá Thiết kế API của Nhóm Bạn

## Mục tiêu
Học cách review API design của đồng nghiệp/nhóm khác, đưa feedback xây dựng, và cải thiện chất lượng chung.

## Peer Review Process

### 1. Preparation Phase

Trước khi review, chuẩn bị:

- [ ] Đọc API documentation nếu có
- [ ] Hiểu use case của API
- [ ] Chuẩn bị checklist
- [ ] Có mindset constructive (not judgmental)
- [ ] Prepare examples từ best practices

### 2. Review Checklist

#### A. Naming Conventions (5 min)

```
□ Endpoints sử dụng plural nouns?
  ✅ /api/users (good)
  ❌ /api/user (bad)

□ Tất cả lowercase?
  ✅ /api/user-profiles (good)
  ❌ /api/UserProfiles (bad)

□ Multi-word sử dụng hyphens?
  ✅ /api/order-items (good)
  ❌ /api/order_items (bad)

□ Có API versioning?
  ✅ /api/v1/users (good)
  ❌ /api/users (bad)

□ Query params cũng lowercase?
  ✅ ?sort-by=created-date (good)
  ❌ ?sortBy=createdDate (bad)
```

#### B. HTTP Methods (5 min)

```
□ GET cho retrieval?
  GET /api/users        ✅
  GET /api/users/{id}   ✅

□ POST cho creation?
  POST /api/users       ✅

□ PUT/PATCH cho update?
  PUT /api/users/{id}   ✅
  PATCH /api/users/{id} ✅

□ DELETE cho deletion?
  DELETE /api/users/{id} ✅

□ Không có verbs trong URL?
  ✅ DELETE /api/users/{id}        (good)
  ❌ GET /api/deleteUser/{id}      (bad)
  ❌ POST /api/users/delete/{id}   (bad)
```

#### C. Response Format (5 min)

```
□ Response format consistent?

  ✅ {
       "status": "success",
       "data": { ... },
       "meta": { ... }
     }

  ❌ {
       "code": 200,
       "result": { ... }
     }
     (Different format for different endpoints)

□ Error format consistent?

  ✅ {
       "status": "error",
       "error": {
         "code": "VALIDATION_ERROR",
         "message": "...",
         "details": [ ... ]
       }
     }

  ❌ {
       "error": "Invalid input"
     }
     (Not detailed, inconsistent)

□ Có pagination metadata?

  ✅ {
       "meta": {
         "total": 100,
         "page": 1,
         "limit": 20
       }
     }

  ❌ No pagination info
```

#### D. Status Codes (5 min)

```
□ 201 Created cho POST?
  POST /api/users → 201 Created ✅

□ 200 OK cho successful GET/PUT/PATCH?
  GET /api/users/1 → 200 OK ✅
  PUT /api/users/1 → 200 OK ✅

□ 204 No Content cho DELETE (optional)?
  DELETE /api/users/1 → 204 No Content ✅

□ 400 Bad Request cho invalid input?
  POST /api/users {"name": ""} → 400 Bad Request ✅

□ 422 Unprocessable Entity cho validation errors?
  POST /api/users {"email": "invalid"} → 422 ✅

□ 401 Unauthorized cho missing auth?
  GET /api/users (no token) → 401 ✅

□ 403 Forbidden cho insufficient permission?
  DELETE /api/users/1 (not admin) → 403 ✅

□ 404 Not Found cho resource not found?
  GET /api/users/999 → 404 ✅

□ 500 Internal Server Error cho server issues?
  Any server error → 500 ✅
```

#### E. Features & Functionality (10 min)

```
□ Pagination support?
  GET /api/users?page=1&limit=20 ✅

□ Filtering support?
  GET /api/users?status=active ✅

□ Sorting support?
  GET /api/users?sort-by=name&order=asc ✅

□ Search support (if needed)?
  GET /api/users?search=john ✅

□ Include/expand related resources?
  GET /api/users/1?include=orders ✅

□ Nested resources designed well?
  GET /api/users/1/orders ✅
  GET /api/users/1/orders/100 ✅

□ CRUD operations complete?
  CREATE: POST /api/resource ✅
  READ:   GET /api/resource(s) ✅
  UPDATE: PUT/PATCH /api/resource/id ✅
  DELETE: DELETE /api/resource/id ✅

□ Documentation adequate?
  - Examples provided? ✅
  - Error cases documented? ✅
  - Authentication explained? ✅
```

---

## Review Template

```markdown
# Peer Review: [Project Name] API

## Reviewer: [Your Name]
## Date: [Date]
## API: [API Name/URL]

### Overall Assessment
- **Score**: ___ / 100
- **Status**: ☐ Excellent ☐ Good ☐ Acceptable ☐ Needs Work

---

### 1. Naming Conventions
**Score**: ___ / 10

**ὶssues:**
- [ ] Issue 1: _______________
- [ ] Issue 2: _______________

**Positive:**
- ✅ Good 1: _______________
- ✅ Good 2: _______________

---

### 2. HTTP Methods
**Score**: ___ / 10

**Issues:**
- [ ] _______________

**Positive:**
- ✅ _______________

---

### 3. Response Format
**Score**: ___ / 15

**Issues:**
- [ ] _______________

**Examples:**

Inconsistency found in:
\`\`\`
GET /api/users    → {"data": [...]}
GET /api/products → {"items": [...]}
\`\`\`

Should be:
\`\`\`
GET /api/users    → {"status": "success", "data": [...]}
GET /api/products → {"status": "success", "data": [...]}
\`\`\`

---

### 4. Status Codes
**Score**: ___ / 15

**Issues:**
- [ ] _______________

**Documentation:**
- Response codes documented? Yes / No
- All error cases covered? Yes / No

---

### 5. Features & Functionality
**Score**: ___ / 25

**Missing Features:**
- [ ] Pagination
- [ ] Filtering
- [ ] Sorting
- [ ] Search
- [ ] _______________

**Functionality Assessment:**
- CRUD complete? Yes / No
- Nested resources? Yes / No
- Related resources linked? Yes / No

---

### 6. Security
**Score**: ___ / 10

**Concerns:**
- Authentication required? Yes / No
- Authorization checks? Yes / No
- Input validation? Yes / No

---

### 7. Documentation
**Score**: ___ / 10

**Present:**
- [ ] Endpoints listed
- [ ] Examples provided
- [ ] Error cases documented
- [ ] Authentication explained
- [ ] Rate limiting documented

---

### 8. Performance
**Score**: ___ / 5

**Concerns:**
- Need pagination? _______________
- Response size acceptable? _______________
- Caching strategy? _______________

---

## Detailed Feedback

### Strengths
1. _______________
2. _______________

### Areas for Improvement
1. _______________
   - **Priority**: High / Medium / Low
   - **Suggestion**: _______________

2. _______________
   - **Priority**: High / Medium / Low
   - **Suggestion**: _______________

### Suggestions for Next Steps
1. _______________
2. _______________

---

## Questions for Discussion
1. Q: _______________
   A: _______________

2. Q: _______________
   A: _______________

---

## Follow-up
- [ ] Schedule follow-up review
- [ ] Check improvements made
- [ ] Update documentation
```

---

## Real-world Peer Review Example

### Review Scenario: Social Media API

**Reviewer's Comments:**

#### ✅ What's Good

```
1. Consistent naming convention
   - All endpoints use lowercase, hyphens, plural nouns ✅
   - Query params also follow same convention ✅

2. Proper HTTP methods
   - No verbs in URLs ✅
   - Correct CRUD mapping ✅

3. Good documentation
   - Examples provided ✅
   - Error cases explained ✅

4. RESTful design
   - Nested resources make sense ✅
   - Hierarchily clear ✅
```

#### ⚠️ Issues Found

```
1. Missing versioning
   GET /api/users (should be /api/v1/users)

   Suggestion: Add versioning to support future changes

   /api/v1/posts
   /api/v2/posts (if breaking changes)

2. No pagination example in docs

   Suggestion: Add example:
   GET /api/v1/posts?page=1&limit=20

   Response:
   {
     "data": [...],
     "meta": {
       "total": 1000,
       "page": 1,
       "limit": 20
     }
   }

3. Links endpoints need documentation

   Suggestion: Document clearly:
   POST   /api/v1/posts/{id}/likes       # Like a post
   DELETE /api/v1/posts/{id}/likes       # Unlike a post
   GET    /api/v1/posts/{id}/likes/count # Get like count

4. No rate limiting mentioned

   Suggestion: Add rate limiting headers:
   X-RateLimit-Limit: 1000
   X-RateLimit-Remaining: 999
   X-RateLimit-Reset: 1635432000

5. Search endpoint design

   Current: GET /api/search?q=text
   Better: GET /api/v1/posts?search=text

   Reason: Consistent with resource-based design
```

#### 📊 Score Breakdown

```
Naming Conventions:        9/10
HTTP Methods:             10/10
Response Format:           9/10
Status Codes:              8/10
Features:                  7/10 (missing pagination docs, limited filtering)
Security:                  8/10 (rate limiting not documented)
Documentation:             8/10 (good overall, minor gaps)
Performance:               7/10 (needs pagination defaults)

TOTAL:                    66/70 = 94/100 ✅ EXCELLENT
```

---

## Peer Review Best Practices

### ✅ DO's

1. **Be Constructive**
   - Focus on improving design
   - Suggest solutions, not just problems
   - Use "I suggest" not "You did wrong"

2. **Be Specific**
   - Point to exact endpoints
   - Provide examples
   - Show before/after comparisons

3. **Ask Questions**
   - "Why did you choose this approach?"
   - "Have you considered...?"
   - "What about this use case?"

4. **Give Credit**
   - Acknowledge good design decisions
   - Highlight strengths
   - Be balanced in feedback

5. **Reference Standards**
   - Cite REST principles
   - Reference best practices
   - Provide documentation links

### ❌ DON'Ts

1. **Don't be judgmental**
   - ❌ "This is terrible"
   - ✅ "Let's consider a better approach"

2. **Don't be vague**
   - ❌ "This doesn't look good"
   - ✅ "GET /getUser violates REST; use GET /users/{id} instead"

3. **Don't dominate**
   - Listen to explanations
   - Ask why before criticizing
   - Accept different valid approaches

4. **Don't ignore context**
   - Legacy systems may have constraints
   - Business requirements matter
   - Sometimes pragmatism > perfection

5. **Don't create friction**
   - Keep tone professional
   - Respect the author's work
   - Collaborate, not criticize

---

## Conducting a Live Review

### Meeting Agenda (30-45 min)

```
1. Introduction (2 min)
   - Thank presenter
   - Explain review process
   - Set collaborative tone

2. Presentation (10 min)
   - Present API design
   - Explain use cases
   - Share design decisions

3. Questions (5 min)
   - Reviewers ask clarifying questions
   - No judgment, just understanding

4. Feedback (15-20 min)
   - Positive feedback first
   - Issues and suggestions
   - Prioritize by impact

5. Discussion (5-10 min)
   - Address concerns
   - Agree on next steps
   - Schedule follow-up if needed
```

### Sample Script

```
"Thank you for sharing your API design. The overall structure is solid,
with clear resource hierarchy and consistent naming. I have a few
suggestions to strengthen it further.

First, I noticed the API doesn't have versioning. I suggest adding /v1/
to your base URL. This allows you to evolve the API in the future without
breaking clients. Here's an example...

Second, pagination isn't documented. For endpoints returning lists, I
recommend supporting page/limit parameters...

What are your thoughts on these suggestions?"
```

---

## Follow-up Actions

After review, ensure:

- [ ] Notes documented
- [ ] Issues prioritized
- [ ] Improvements planned
- [ ] Follow-up date set
- [ ] Changes communicated
- [ ] Second review scheduled (if needed)

---

## Bài tập thực hành

1. **Review một API**
   - Choose a team project API
   - Use review checklist
   - Document findings
   - Total time: 30 min

2. **Conduct Live Review**
   - Schedule with team
   - Follow meeting agenda
   - Take notes
   - Give constructive feedback

3. **Review & Counter-Review**
   - Your API reviewed by 2 peers
   - Take their feedback
   - Improve design
   - Document changes

4. **Create Review Guidelines**
   - For your team/project
   - Based on best practices
   - Shared checklist
   - Standard format

---

## Review Checklist Summary

```
QUICK CHECKLIST (5 min)

Naming:     ☐ Plural  ☐ Lowercase  ☐ Hyphens  ☐ Versioned
Methods:    ☐ GET/POST/PUT/DELETE correct  ☐ No verbs
Response:   ☐ Consistent format  ☐ Has status field
Codes:      ☐ 201 for POST  ☐ 4xx for errors
Docs:       ☐ Examples  ☐ Error cases  ☐ Auth explained
Features:   ☐ Pagination  ☐ Filtering  ☐ Sorting

ISSUES FOUND: ___
SCORE: ___ / 100
```

---
**Hoàn tất**: [Quay lại Index](../README.md)
