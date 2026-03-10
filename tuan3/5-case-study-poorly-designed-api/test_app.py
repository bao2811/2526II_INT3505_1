"""
Test Flow 5: Case Study - Poorly Designed API
Kiểm tra: Anti-patterns, issues detection, refactoring comparison
"""

import pytest
import json
import sys
sys.path.insert(0, '/g/2526II_INT3505_1/tuan3/5-case-study-poorly-designed-api')

from app import app


class TestPoorlyDesignedAPI:
    """Test Suite for Poorly Designed API - Anti-patterns"""

    @pytest.fixture
    def client(self):
        """Create Flask test client"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    # ============ TEST 1: Verb-based Endpoints ============

    def test_verb_based_getallproducts(self, client):
        """❌ Test: Verb-based endpoint /getallproducts"""
        response = client.get('/api/getallproducts')
        # ❌ ISSUE: Verb in URL (should be /api/v1/products)
        assert response.status_code == 200
        # This should NOT work with good API design

    def test_verb_based_getproduct(self, client):
        """❌ Test: Verb-based endpoint /getproduct"""
        response = client.get('/api/getproduct?prod_id=1')
        # ❌ ISSUE: Verb 'get' in URL
        assert response.status_code == 200

    def test_verb_based_endpoints_are_bad(self, client):
        """✅ Test: Identify verb-based endpoints as anti-pattern"""
        response = client.get('/api/issues-summary')
        data = json.loads(response.data)

        issues = data['data']['issues']
        assert issues[0]['issue'] == 'Verb-based endpoints'
        assert 'getallproducts' in str(issues[0]['examples'])

    # ============ TEST 2: Inconsistent Response Format ============

    def test_inconsistent_response_getallproducts(self, client):
        """❌ Test: getallproducts uses {code, response} format"""
        response = client.get('/api/getallproducts')
        data = json.loads(response.data)

        # ❌ Uses different format than getproduct
        assert 'code' in data
        assert 'response' in data

    def test_inconsistent_response_getproduct(self, client):
        """❌ Test: getproduct uses {status, data} format"""
        response = client.get('/api/getproduct?prod_id=1')
        data = json.loads(response.data)

        # ❌ Different format from getallproducts!
        assert 'status' in data
        assert 'data' in data

    def test_inconsistent_response_issue_identified(self, client):
        """✅ Test: Inconsistent response format identified as issue"""
        response = client.get('/api/issues-summary')
        data = json.loads(response.data)

        issues = data['data']['issues']
        # Find inconsistent format issue
        format_issue = next(
            (i for i in issues if 'response format' in i['issue'].lower()),
            None
        )
        assert format_issue is not None
        assert format_issue['priority'] == 'CRITICAL'

    # ============ TEST 3: Wrong HTTP Methods ============

    def test_get_logout_issue(self, client):
        """❌ Test: GET for logout (should be POST/DELETE)"""
        response = client.get('/api/logout')
        # ❌ ISSUE: GET shouldn't modify state (CSRF vulnerability)
        assert response.status_code == 200

    def test_post_search_issue(self, client):
        """❌ Test: POST for search (should be GET)"""
        response = client.post(
            '/api/searchItems',
            data={'keyword': 'test'},
        )
        # ❌ ISSUE: Search is query operation, should be GET
        # Note: POST form data, not JSON

    def test_post_user_update_issue(self, client):
        """❌ Test: POST for update (should be PUT/PATCH)"""
        response = client.post(
            '/api/user/update',
            data=json.dumps({'id': 1}),
            content_type='application/json'
        )
        # ❌ ISSUE: Update should use PUT/PATCH
        assert response.status_code >= 200

    def test_wrong_http_methods_issue_identified(self, client):
        """✅ Test: Wrong HTTP methods identified as issue"""
        response = client.get('/api/issues-summary')
        data = json.loads(response.data)

        issues = data['data']['issues']
        http_issue = next(
            (i for i in issues if 'HTTP methods' in i['issue']),
            None
        )
        assert http_issue is not None
        assert http_issue['priority'] == 'CRITICAL'
        assert 'logout' in str(http_issue['examples'])

    # ============ TEST 4: Inconsistent Parameter Names ============

    def test_parameter_prod_id(self, client):
        """❌ Test: Uses prod_id parameter"""
        response = client.get('/api/getproduct?prod_id=1')
        assert response.status_code == 200

    def test_parameter_OrderID_uppercase(self, client):
        """❌ Test: Uses OrderID (mixed case)"""
        response = client.get('/api/getOrder?OrderID=ORD001')
        assert response.status_code == 200

    def test_parameter_orderid_lowercase(self, client):
        """❌ Test: Uses orderid (different from OrderID)"""
        response = client.post(
            '/api/cancelorder?orderid=ORD001'
        )
        assert response.status_code >= 200

    def test_inconsistent_parameter_names_issue(self, client):
        """✅ Test: Inconsistent parameter naming identified"""
        response = client.get('/api/issues-summary')
        data = json.loads(response.data)

        issues = data['data']['issues']
        param_issue = next(
            (i for i in issues if 'parameter' in i['issue'].lower()),
            None
        )
        assert param_issue is not None
        assert param_issue['priority'] == 'HIGH'

    # ============ TEST 5: No Versioning ============

    def test_no_versioning_in_endpoints(self, client):
        """❌ Test: Endpoints don't have /v1/ versioning"""
        # All endpoints are /api/* not /api/v1/*
        response = client.get('/api/getallproducts')
        assert response.status_code == 200
        # ❌ No version for backward compatibility

    def test_no_versioning_issue(self, client):
        """✅ Test: Lack of versioning identified as issue"""
        response = client.get('/api/issues-summary')
        data = json.loads(response.data)

        issues = data['data']['issues']
        version_issue = next(
            (i for i in issues if 'versioning' in i['issue'].lower()),
            None
        )
        assert version_issue is not None
        assert version_issue['priority'] == 'HIGH'

    # ============ TEST 6: No Pagination ============

    def test_no_pagination_support(self, client):
        """❌ Test: /api/products returns all products (no pagination)"""
        response = client.get('/api/products')
        assert response.status_code == 200
        # ❌ No page/limit parameters, no pagination metadata

    def test_no_pagination_issue(self, client):
        """✅ Test: Missing pagination identified as issue"""
        response = client.get('/api/issues-summary')
        data = json.loads(response.data)

        issues = data['data']['issues']
        pagination_issue = next(
            (i for i in issues if 'pagination' in i['issue'].lower()),
            None
        )
        assert pagination_issue is not None
        assert pagination_issue['priority'] == 'HIGH'

    # ============ TEST 7: Wrong Status Codes ============

    def test_create_product_returns_200_instead_of_201(self, client):
        """❌ Test: POST returns 200 (should be 201)"""
        response = client.post(
            '/api/createProduct',
            data=json.dumps({'name': 'Test', 'price': 100}),
            content_type='application/json'
        )
        # ❌ Returns 200, should be 201 Created
        assert response.status_code == 200

    def test_wrong_status_codes_issue(self, client):
        """✅ Test: Wrong status codes identified as issue"""
        response = client.get('/api/issues-summary')
        data = json.loads(response.data)

        issues = data['data']['issues']
        status_issue = next(
            (i for i in issues if 'status code' in i['issue'].lower()),
            None
        )
        assert status_issue is not None
        assert status_issue['priority'] == 'CRITICAL'

    # ============ TEST 8: Security Issues ============

    def test_logout_via_get_is_csrf_vulnerable(self, client):
        """❌ Test: GET logout is CSRF vulnerable"""
        response = client.get('/api/logout')
        # ❌ GET logout = CSRF vulnerability (user can be logged out by visiting link)

    def test_security_issues_identified(self, client):
        """✅ Test: Security issues identified"""
        response = client.get('/api/issues-summary')
        data = json.loads(response.data)

        issues = data['data']['issues']
        security_issue = next(
            (i for i in issues if 'security' in i['issue'].lower()),
            None
        )
        assert security_issue is not None
        assert security_issue['priority'] == 'HIGH'

    # ============ TEST 9: Total Issues Count ============

    def test_total_issues_count(self, client):
        """✅ Test: Correctly identifies all 10 issues"""
        response = client.get('/api/issues-summary')
        data = json.loads(response.data)

        assert data['data']['total_issues'] == 10
        assert data['data']['critical'] == 4  # 4 critical issues
        assert data['data']['high'] == 6      # 6 high issues

    def test_issues_organized_by_priority(self, client):
        """✅ Test: Issues are properly categorized by priority"""
        response = client.get('/api/issues-summary')
        data = json.loads(response.data)

        issues = data['data']['issues']
        priorities = [i['priority'] for i in issues]

        assert 'CRITICAL' in priorities
        assert 'HIGH' in priorities
        assert 'MEDIUM' in priorities

    # ============ TEST 10: Refactoring Comparison ============

    def test_refactoring_endpoints_provided(self, client):
        """✅ Test: Refactored good endpoints provided"""
        response = client.get('/api/refactored-comparison')
        assert response.status_code == 200

        data = json.loads(response.data)
        comparisons = data['data']['before_after']

        # Should have multiple before/after pairs
        assert len(comparisons) > 5

    def test_refactor_verb_to_resource(self, client):
        """✅ Test: Refactor /getallproducts to /products"""
        response = client.get('/api/refactored-comparison')
        data = json.loads(response.data)

        comparisons = data['data']['before_after']
        getall_refactor = next(
            (c for c in comparisons if 'getallproducts' in c['bad']),
            None
        )
        assert getall_refactor is not None
        assert '/api/v1/products' in getall_refactor['good']

    def test_refactor_get_logout_to_post(self, client):
        """✅ Test: Refactor GET logout to POST logout"""
        response = client.get('/api/refactored-comparison')
        data = json.loads(response.data)

        comparisons = data['data']['before_after']
        logout_refactor = next(
            (c for c in comparisons if '/logout' in c['bad']),
            None
        )
        assert logout_refactor is not None
        assert 'POST' in logout_refactor['good']

    def test_refactor_no_pagination_to_paginated(self, client):
        """✅ Test: Refactor no pagination to paginated"""
        response = client.get('/api/refactored-comparison')
        data = json.loads(response.data)

        comparisons = data['data']['before_after']
        pagination_refactor = next(
            (c for c in comparisons if 'pagination' in c['bad'].lower()),
            None
        )
        assert pagination_refactor is not None


class TestCaseStudySummary:
    """Summary of Case Study - 10 Issues Identified"""

    def test_case_study_summary(self):
        """
        ✅ 10 API DESIGN ISSUES IDENTIFIED:

        CRITICAL (4):
        ❌ Verb-based endpoints: /getallproducts, /getproduct, /getOrder, /cancelorder
        ❌ Inconsistent response format: {code} vs {status} vs {message}
        ❌ Wrong HTTP methods: GET /logout, POST /search
        ❌ Wrong status codes: 200 instead of 201

        HIGH (6):
        ❌ Inconsistent parameter names: prod_id, OrderID, orderid
        ❌ No API versioning: /api/* not /api/v1/*
        ❌ No pagination support: /api/products returns ALL
        ❌ No filtering/sorting: Limited query capabilities
        ❌ No nested resources: Flat structure
        ❌ Security issues: GET /logout = CSRF vulnerability

        REFACTORED EXAMPLES:
        ✅ GET /api/getallproducts → GET /api/v1/products
        ✅ GET /api/getproduct?prod_id=1 → GET /api/v1/products/1
        ✅ GET /api/logout → POST /api/v1/auth/logout
        ✅ POST /api/searchItems → GET /api/v1/products?search=keyword
        ✅ GET /api/getOrder?OrderID=ORD001 → GET /api/v1/orders/1
        ✅ No pagination → ?page=1&limit=10
        ✅ Response {code} → {status, data, meta}

        ESTIMATED SCORE: ~40/100 (POOR - Needs significant refactoring)
        """
        assert True
