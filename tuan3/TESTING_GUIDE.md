# Testing Guide - Tuan 3 - API Design Principles

## 📋 Overview

Toàn bộ 6 flows có test files với pytest. Tổng cộng hơn **150+ test cases** để kiểm tra từng khía cạnh của thiết kế API.

## 📁 Test Files Created

```
tuan3/
├── 1-best-practices/test_app.py
├── 2-naming-conventions/test_app.py
├── 3-api-endpoints/test_app.py
├── 4-design-evaluation/test_app.py
├── 5-case-study-poorly-designed-api/test_app.py
├── 6-peer-review/test_app.py
└── requirements.txt (updated)
```

## 🚀 Installation

```bash
cd /g/2526II_INT3505_1/tuan3
pip install -r requirements.txt
```

## 🧪 Running Tests

### Run All Tests
```bash
pytest                          # Run all tests
pytest -v                       # Verbose output
pytest -v --tb=short          # Short traceback
pytest --cov=. --cov-report=html  # With coverage report
```

### Run Tests for Specific Flow
```bash
# Flow 1
pytest 1-best-practices/test_app.py -v

# Flow 2
pytest 2-naming-conventions/test_app.py -v

# Flow 3
pytest 3-api-endpoints/test_app.py -v

# Flow 4
pytest 4-design-evaluation/test_app.py -v

# Flow 5
pytest 5-case-study-poorly-designed-api/test_app.py -v

# Flow 6
pytest 6-peer-review/test_app.py -v
```

### Run Specific Test
```bash
pytest 1-best-practices/test_app.py::TestBestPracticesAPI::test_consistency -v
```

### Run with Pattern Matching
```bash
pytest -k "consistency" -v     # Run tests with 'consistency' in name
pytest -k "status_code" -v     # Run all status code tests
```

---

## 📊 Test Coverage by Flow

### Flow 1: Best Practices (12 test cases)

**File**: `1-best-practices/test_app.py`

**Tests cover:**
- ✅ Consistency: response format, error format, HTTP methods, status codes
- ✅ Clarity: endpoint names, error messages
- ✅ Extensibility: versioning, pagination

**Key tests:**
```python
test_list_users_response_format()         # Check response structure
test_create_user_response_format()        # Check 201 Created
test_error_response_format()              # Check error format
test_endpoints_are_clear()                # Check naming
test_health_check_endpoint()              # Check health endpoint
```

---

### Flow 2: Naming Conventions (20 test cases)

**File**: `2-naming-conventions/test_app.py`

**Tests cover:**
- ✅ Plural nouns: /user-profiles (not /user-profile)
- ✅ Lowercase: /api/v1/ (not /API/V1/)
- ✅ Hyphens: /payment-methods (not /payment_methods)
- ✅ Versioning: /v1/ allows future /v2/
- ✅ Query parameters: sort-by, search, page, limit
- ✅ Nested resources: /users/{id}/orders
- ✅ Actions: /users/{id}/verify-email

**Key tests:**
```python
test_plural_nouns_user_profiles()         # Check plural
test_lowercase_api_version()              # Check lowercase
test_hyphens_for_multi_word_resources()   # Check hyphens
test_query_params_use_hyphens()           # Check query params
test_nested_resource_pattern()            # Check nested
test_action_endpoint_uses_hyphens()       # Check actions
```

---

### Flow 3: CRUD Endpoints (45+ test cases)

**File**: `3-api-endpoints/test_app.py`

**Tests cover:**
- ✅ CREATE: POST returns 201, validation (422)
- ✅ READ: GET returns 200, 404 for not found
- ✅ UPDATE: PUT (full), PATCH (partial)
- ✅ DELETE: returns 204 No Content
- ✅ Nested resources: /posts/{id}/comments
- ✅ Actions: /posts/{id}/publish
- ✅ Status codes: 200, 201, 204, 404, 422
- ✅ Pagination, filtering, sorting

**Key tests:**
```python
test_create_post_returns_201()            # POST -> 201
test_read_single_post_returns_200()       # GET single -> 200
test_update_full_put_returns_200()        # PUT -> 200
test_update_partial_patch_returns_200()   # PATCH -> 200
test_delete_returns_204()                 # DELETE -> 204
test_read_nonexistent_post_returns_404()  # 404 handling
test_nested_post_creates_comment()        # Nested POST -> 201
test_action_publish_post()                # Action endpoint
```

---

### Flow 4: Design Evaluation (20+ test cases)

**File**: `4-design-evaluation/test_app.py`

**Tests cover:**
- ✅ APIEvaluator class
- ✅ Scoring system (0-100)
- ✅ Ratings: Excellent (90+), Good (80+), Fair (70+), Poor (<70)
- ✅ Evaluation framework with 5 criteria
- ✅ Real-world examples (good, fair, poor APIs)
- ✅ Framework details and checklist
- ✅ Scoring guidance

**Key tests:**
```python
test_evaluator_creation()                 # Create evaluator
test_evaluator_scoring()                  # Calculate score
test_evaluator_rating_excellent()         # Rate as Excellent
test_framework_endpoint()                 # Get framework
test_framework_has_checklist()            # Check framework
test_get_good_evaluation()                # Good API (97/100)
test_get_fair_evaluation()                # Fair API (75/100)
test_get_poor_evaluation()                # Poor API (38/100)
```

---

### Flow 5: Poorly Designed API (25+ test cases)

**File**: `5-case-study-poorly-designed-api/test_app.py`

**Tests cover – Anti-patterns Identified:**
1. ❌ Verb-based endpoints: /getallproducts, /getproduct
2. ❌ Inconsistent response format: {code} vs {status}
3. ❌ Wrong HTTP methods: GET /logout
4. ❌ Inconsistent parameter names: prod_id, OrderID, orderid
5. ❌ No API versioning
6. ❌ No pagination support
7. ❌ No filtering/sorting
8. ❌ Wrong status codes: 200 instead of 201
9. ❌ No nested resources
10. ❌ Security issues: CSRF vulnerability

**Key tests:**
```python
test_verb_based_getallproducts()          # Identify verb issue
test_inconsistent_response_getallproducts() # Response format issue
test_get_logout_issue()                   # HTTP method issue
test_parameter_prod_id()                  # Parameter naming
test_no_pagination_support()              # Pagination issue
test_create_product_returns_200()         # Status code issue
test_wrong_http_methods_issue_identified() # Issue identification
test_total_issues_count()                 # Should find 10 issues
test_refactoring_endpoints_provided()     # Refactored solutions
```

---

### Flow 6: Well-Designed API (35+ test cases)

**File**: `6-peer-review/test_app.py`

**Tests cover – Production-Ready Checklist:**
- ✅ Naming conventions: plural, lowercase, hyphens, versioning
- ✅ HTTP methods: GET, POST, PUT, PATCH, DELETE
- ✅ Response format: {status, data, meta}
- ✅ Status codes: 200, 201, 204, 404, 422
- ✅ Pagination with metadata
- ✅ Filtering & sorting
- ✅ Nested resources
- ✅ Validation
- ✅ Error handling
- ✅ Self-documentation

**Key tests:**
```python
test_plural_resource_names()              # Check naming
test_post_for_creation()                  # POST -> 201
test_delete_for_deletion()                # DELETE -> 204
test_consistent_success_response_format() # Response format
test_pagination_support()                 # Pagination works
test_nested_resource_pattern()            # Nested resources
test_required_field_validation()          # Validation
test_review_checklist_endpoint()          # Self-docs
test_peer_review_score_excellent()        # Score 97/100
```

---

## 📈 Test Execution Example

```bash
$ cd /g/2526II_INT3505_1/tuan3

# Install dependencies
$ pip install -r requirements.txt

# Run all tests
$ pytest -v

# Output:
# 1-best-practices/test_app.py::TestBestPracticesAPI::test_list_users_response_format PASSED
# 1-best-practices/test_app.py::TestBestPracticesAPI::test_create_user_response_format PASSED
# 2-naming-conventions/test_app.py::TestNamingConventionsAPI::test_plural_nouns_user_profiles PASSED
# ...
# ======================= 150+ passed in 2.45s =======================
```

---

## ✅ Test Checklist

After running tests, verify:

- [ ] Flow 1: Best Practices - 12 tests pass
- [ ] Flow 2: Naming Conventions - 20 tests pass
- [ ] Flow 3: CRUD Endpoints - 45+ tests pass
- [ ] Flow 4: Design Evaluation - 20+ tests pass
- [ ] Flow 5: Case Study - 25+ tests pass
- [ ] Flow 6: Peer Review - 35+ tests pass
- [ ] Total: 150+ tests pass
- [ ] No errors or failures
- [ ] Coverage > 90%

---

## 🎓 Learning from Tests

Each test demonstrates:

1. **What to test**: API design principles
2. **How to test**: Using pytest assertions
3. **What should pass**: Good API practices
4. **What should fail**: Anti-patterns and bad practices
5. **Expected behavior**: Status codes, response formats, error handling

## 💡 Using Tests for Learning

```python
# Example: Understanding status codes
def test_status_201_for_post(self, client):
    """✅ Test: 201 Created for POST"""
    payload = {"name": "Test", "description": "Test"}
    response = client.post(
        '/api/v1/projects',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert response.status_code == 201
```

This test shows:
- POST requests should return **201 Created**
- Not 200 OK
- Not any other status code

## 🔍 Test Organization

Each test file has:

1. **Main test class**: `TestXxxAPI`
   - Multiple test methods
   - Using pytest fixtures
   - Clear naming

2. **Summary test class**: `TestXxxSummary`
   - Documents what was tested
   - Shows expected behavior
   - Lists anti-patterns

---

## 🚀 Next Steps

1. **Run the tests**: `pytest -v`
2. **Study failing tests**: Understand why they fail
3. **Study passing tests**: Learn what's correct
4. **Modify and experiment**: Add your own tests
5. **Build your API**: Apply what you learned

---

## 📚 Test Command Reference

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# Stop after first failure
pytest -x

# Show print statements
pytest -s

# Run specific file
pytest 1-best-practices/test_app.py

# Run specific test class
pytest 1-best-practices/test_app.py::TestBestPracticesAPI

# Run specific test method
pytest 1-best-practices/test_app.py::TestBestPracticesAPI::test_consistency

# Run tests matching pattern
pytest -k "consistency"

# Generate coverage report
pytest --cov=. --cov-report=html

# Show slowest tests
pytest --durations=10

# Run with markers
pytest -m "slow"
```

---

## 🎯 Success Criteria

- ✅ All 150+ tests pass
- ✅ No errors or warnings
- ✅ Code coverage > 90%
- ✅ Tests are reproducible
- ✅ Tests document API design

---

**Happy Testing! 🚀**
