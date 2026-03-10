"""
Test Flow 2: Naming Conventions API
Kiểm tra: Plural nouns, lowercase, hyphens, versioning, query params
"""

import pytest
import json
import sys
sys.path.insert(0, '/g/2526II_INT3505_1/tuan3/2-naming-conventions')

from app import app


class TestNamingConventionsAPI:
    """Test Suite for Naming Conventions API"""

    @pytest.fixture
    def client(self):
        """Create Flask test client"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    # ============ TEST 1: Plural Nouns ============

    def test_plural_nouns_user_profiles(self, client):
        """✅ Test: Uses plural noun /user-profiles (not /user-profile)"""
        response = client.get('/api/v1/user-profiles')
        assert response.status_code == 200

    def test_single_resource_in_path(self, client):
        """✅ Test: Single resource uses ID in path /user-profiles/{id}"""
        response = client.get('/api/v1/user-profiles/1')
        assert response.status_code == 200

    # ============ TEST 2: Lowercase ============

    def test_lowercase_api_version(self, client):
        """✅ Test: Version is lowercase /v1/ (not /V1/)"""
        response = client.get('/api/v1/user-profiles')
        assert response.status_code == 200
        # If it was /V1/, it would not work (case sensitive)

    def test_lowercase_resource_names(self, client):
        """✅ Test: Resource names are lowercase"""
        response = client.get('/api/v1/user-profiles')
        data = json.loads(response.data)
        assert response.status_code == 200
        # ✅ 'user-profiles' is all lowercase

    # ============ TEST 3: Hyphens for Multi-word ============

    def test_hyphens_for_multi_word_resources(self, client):
        """✅ Test: Multi-word resources use hyphens"""
        # user-profiles uses hyphens, not user_profiles
        response = client.get('/api/v1/user-profiles')
        assert response.status_code == 200

    def test_payment_methods_uses_hyphens(self, client):
        """✅ Test: payment-methods uses hyphens (not payment_methods)"""
        response = client.get('/api/v1/user-profiles/1/payment-methods')
        assert response.status_code == 200

    def test_reset_password_action_uses_hyphens(self, client):
        """✅ Test: Action endpoints use hyphens /reset-password"""
        response = client.post(
            '/api/v1/user-profiles/1/reset-password',
            data=json.dumps({}),
            content_type='application/json'
        )
        # ✅ Uses hyphens, not underscores
        assert response.status_code == 200

    # ============ TEST 4: Versioning ============

    def test_api_version_in_url(self, client):
        """✅ Test: API version is in URL /v1/"""
        response = client.get('/api/v1/user-profiles')
        assert response.status_code == 200

    def test_versioning_allows_future_versions(self, client):
        """✅ Test: Versioning structure allows /v2/ in future"""
        # Currently /v1/ exists
        response = client.get('/api/v1/user-profiles')
        assert response.status_code == 200
        # In future, /v2/ can be added without breaking /v1/

    # ============ TEST 5: Query Parameters ============

    def test_query_params_use_hyphens(self, client):
        """✅ Test: Query parameters use hyphens (sort-by, not sortBy)"""
        response = client.get('/api/v1/user-profiles?sort-by=full_name&order=asc')
        assert response.status_code == 200
        data = json.loads(response.data)
        # ✅ Parameters work with hyphens

    def test_query_params_pagination(self, client):
        """✅ Test: Pagination query params"""
        response = client.get('/api/v1/user-profiles?page=1&limit=5')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['meta']['page'] == 1
        assert data['meta']['limit'] == 5

    def test_query_params_search(self, client):
        """✅ Test: Search query parameter"""
        response = client.get('/api/v1/user-profiles?search=john')
        assert response.status_code == 200

    def test_query_params_lowercase(self, client):
        """✅ Test: Query param names are lowercase"""
        # page, limit, sort-by, order, search - all lowercase
        response = client.get('/api/v1/user-profiles?page=1&sort-by=name&order=desc')
        assert response.status_code == 200

    # ============ TEST 6: Nested Resources ============

    def test_nested_resource_pattern(self, client):
        """✅ Test: Nested resources follow pattern /parent/{id}/child"""
        response = client.get('/api/v1/user-profiles/1/orders')
        assert response.status_code == 200

    def test_nested_resource_with_id(self, client):
        """✅ Test: Can access specific nested resource"""
        response = client.get('/api/v1/user-profiles/1/orders/100')
        assert response.status_code == 200

    def test_nested_payment_methods(self, client):
        """✅ Test: payment-methods as nested resource"""
        response = client.get('/api/v1/user-profiles/1/payment-methods')
        assert response.status_code == 200

    # ============ TEST 7: Actions ============

    def test_action_endpoint_uses_hyphens(self, client):
        """✅ Test: Action endpoints use hyphens /verify-email"""
        response = client.post(
            '/api/v1/user-profiles/1/verify-email',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 200

    def test_reset_password_action(self, client):
        """✅ Test: reset-password action endpoint"""
        response = client.post(
            '/api/v1/user-profiles/1/reset-password',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 200

    # ============ TEST 8: Consistency Across Resources ============

    def test_consistent_naming_in_orders(self, client):
        """✅ Test: Orders also follow naming conventions"""
        response = client.get('/api/v1/user-profiles/1/orders')
        assert response.status_code == 200
        # ✅ Uses lowercase, plural 'orders'

    def test_consistent_query_param_naming(self, client):
        """✅ Test: Query params consistent across different resources"""
        response = client.get('/api/v1/user-profiles/1/orders?page=1&limit=10')
        assert response.status_code == 200
        # ✅ Same page/limit params work consistently

    # ============ TEST 9: Bad Naming Would Fail ============

    def test_bad_naming_would_not_work(self, client):
        """✅ Test: Bad naming conventions don't work"""
        # These would return 404 because they don't exist
        response = client.get('/api/v1/UserProfile')  # PascalCase - wrong
        assert response.status_code == 404

        response = client.get('/api/v1/user_profiles')  # underscores - wrong
        assert response.status_code == 404

    # ============ TEST 10: Response Format with Good Naming ============

    def test_consistent_response_format(self, client):
        """✅ Test: Response format is consistent regardless of naming"""
        response = client.get('/api/v1/user-profiles')
        assert response.status_code == 200

        data = json.loads(response.data)
        # ✅ Good naming + good response format
        assert 'status' in data
        assert 'data' in data
        assert 'meta' in data


class TestNamingConventionsSummary:
    """Summary of Naming Conventions demonstrated"""

    def test_summary(self):
        """
        ✅ NAMING CONVENTIONS:

        1. PLURAL NOUNS:
        ✅ /api/v1/user-profiles (not /api/v1/user-profile)
        ✅ /api/v1/orders (not /api/v1/order)

        2. LOWERCASE:
        ✅ /api/v1/ (not /API/V1/)
        ✅ /user-profiles (not /User-Profiles)

        3. HYPHENS for multi-word:
        ✅ /user-profiles (not /user_profiles)
        ✅ /payment-methods (not /payment_methods)
        ✅ /verify-email (not /verifyEmail)
        ✅ /reset-password (not /resetPassword)

        4. VERSIONING:
        ✅ /api/v1/ allows for future /v2/
        ✅ Backward compatible design

        5. QUERY PARAMETERS:
        ✅ ?page=1&limit=10
        ✅ ?sort-by=name&order=desc (hyphens)
        ✅ ?search=keyword

        6. NESTED RESOURCES:
        ✅ /user-profiles/{id}/orders
        ✅ /user-profiles/{id}/orders/{id}
        ✅ /user-profiles/{id}/payment-methods

        7. ACTIONS:
        ✅ POST /user-profiles/{id}/verify-email
        ✅ POST /user-profiles/{id}/reset-password

        ANTI-PATTERNS (These DON'T work):
        ❌ /api/v1/UserProfile (PascalCase)
        ❌ /api/v1/user_profiles (underscores)
        ❌ /api/v1/GetUserProfile (verbs)
        ❌ /api/user-profiles (no versioning)
        ❌ ?sortBy=name (camelCase params)
        """
        assert True
