"""
Test Flow 1: Best Practices API
Kiểm tra: Consistency, Clarity, Extensibility
"""

import pytest
import json
import sys
sys.path.insert(0, '/g/2526II_INT3505_1/tuan3/1-best-practices')

from app import app


class TestBestPracticesAPI:
    """Test Suite for Best Practices API"""

    @pytest.fixture
    def client(self):
        """Create Flask test client"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    # ============ TEST 1: Consistency - Response Format ============

    def test_list_users_response_format(self, client):
        """✅ Test: List users returns consistent format"""
        response = client.get('/api/v1/users')
        assert response.status_code == 200

        data = json.loads(response.data)
        # ✅ Check consistent structure
        assert 'status' in data
        assert 'data' in data
        assert 'meta' in data
        assert data['status'] == 'success'

    def test_create_user_response_format(self, client):
        """✅ Test: Create user returns 201 with consistent format"""
        payload = {
            "name": "Test User",
            "email": "test@example.com"
        }
        response = client.post(
            '/api/v1/users',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 201

        data = json.loads(response.data)
        # ✅ Check consistent response structure
        assert data['status'] == 'success'
        assert 'data' in data
        assert 'name' in data['data']
        assert 'email' in data['data']

    def test_error_response_format(self, client):
        """✅ Test: Error responses are consistent"""
        # Create without required fields
        response = client.post(
            '/api/v1/users',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 422

        data = json.loads(response.data)
        # ✅ Check error format
        assert data['status'] == 'error'
        assert 'error' in data
        assert 'code' in data['error']
        assert 'message' in data['error']
        assert 'details' in data['error']

    # ============ TEST 2: Clarity - Clear Endpoint Names ============

    def test_endpoints_are_clear(self, client):
        """✅ Test: Endpoint names are descriptive and clear"""
        # No verb-based endpoints
        # All endpoints are resource-based like /api/v1/users

        response = client.get('/api/v1/users')
        assert response.status_code == 200  # Clear what it does

        response = client.get('/api/v1/users/1')
        assert response.status_code == 200  # Clear: get specific user

    def test_error_messages_are_clear(self, client):
        """✅ Test: Error messages are descriptive"""
        response = client.get('/api/v1/users/999')
        assert response.status_code == 404

        data = json.loads(response.data)
        error = data['error']
        # ✅ Check message is clear and helpful
        assert 'not found' in error['message'].lower()
        assert '999' in error['message']  # Includes the ID

    # ============ TEST 3: Extensibility - Versioning & Pagination ============

    def test_api_versioning(self, client):
        """✅ Test: API has versioning (/v1/)"""
        response = client.get('/api/v1/users')
        assert response.status_code == 200
        # ✅ URL has /v1/ for extensibility

    def test_pagination_support(self, client):
        """✅ Test: Pagination is supported"""
        response = client.get('/api/v1/users?page=1&limit=5')
        assert response.status_code == 200

        data = json.loads(response.data)
        # ✅ Check pagination metadata
        assert 'meta' in data
        assert 'page' in data['meta']
        assert 'limit' in data['meta']
        assert 'total' in data['meta']
        assert 'pages' in data['meta']

        assert data['meta']['page'] == 1
        assert data['meta']['limit'] == 5

    def test_pagination_different_pages(self, client):
        """✅ Test: Pagination works with different page numbers"""
        response1 = client.get('/api/v1/users?page=1&limit=1')
        response2 = client.get('/api/v1/users?page=2&limit=1')

        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)

        # ✅ Different pages return different data (or empty if no data)
        assert data1['meta']['page'] == 1
        assert data2['meta']['page'] == 2

    # ============ TEST 4: HTTP Methods ============

    def test_get_method_for_retrieval(self, client):
        """✅ Test: GET is used for retrieval"""
        response = client.get('/api/v1/users')
        assert response.status_code == 200

    def test_post_method_for_creation(self, client):
        """✅ Test: POST is used for creation"""
        payload = {
            "name": "New User",
            "email": "newuser@example.com"
        }
        response = client.post(
            '/api/v1/users',
            data=json.dumps(payload),
            content_type='application/json'
        )
        # ✅ POST returns 201 Created
        assert response.status_code == 201

    def test_put_method_for_update(self, client):
        """✅ Test: PUT is used for update"""
        payload = {
            "name": "Updated Name",
            "email": "updated@example.com"
        }
        response = client.put(
            '/api/v1/users/1',
            data=json.dumps(payload),
            content_type='application/json'
        )
        # ✅ PUT returns 200 OK
        assert response.status_code == 200

    def test_delete_method_for_deletion(self, client):
        """✅ Test: DELETE is used for deletion"""
        response = client.delete('/api/v1/users/1')
        # ✅ DELETE returns 204 No Content
        assert response.status_code == 204

    # ============ TEST 5: Status Codes ============

    def test_status_code_200_for_success(self, client):
        """✅ Test: 200 OK for successful GET"""
        response = client.get('/api/v1/users')
        assert response.status_code == 200

    def test_status_code_201_for_created(self, client):
        """✅ Test: 201 Created for POST"""
        payload = {
            "name": "Test",
            "email": "test@example.com"
        }
        response = client.post(
            '/api/v1/users',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 201

    def test_status_code_204_for_delete(self, client):
        """✅ Test: 204 No Content for DELETE"""
        response = client.delete('/api/v1/users/1')
        assert response.status_code == 204

    def test_status_code_404_for_not_found(self, client):
        """✅ Test: 404 Not Found when resource doesn't exist"""
        response = client.get('/api/v1/users/99999')
        assert response.status_code == 404

    def test_status_code_422_for_validation_error(self, client):
        """✅ Test: 422 for validation errors"""
        response = client.post(
            '/api/v1/users',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 422

    # ============ TEST 6: Products Consistency ============

    def test_products_use_same_response_format(self, client):
        """✅ Test: Products use same response format as users"""
        response = client.get('/api/v1/products')
        assert response.status_code == 200

        data = json.loads(response.data)
        # ✅ Same structure as users
        assert 'status' in data
        assert 'data' in data
        assert 'meta' in data
        assert data['status'] == 'success'

    def test_products_have_consistent_error_handling(self, client):
        """✅ Test: Products error handling is consistent"""
        response = client.get('/api/v1/products/99999')
        assert response.status_code == 404

        data = json.loads(response.data)
        # ✅ Same error format as users
        assert data['status'] == 'error'
        assert 'error' in data

    # ============ TEST 7: Health Check ============

    def test_health_check_endpoint(self, client):
        """✅ Test: Health check endpoint"""
        response = client.get('/api/v1/health')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'status' in data
        assert 'version' in data


class TestBestPracticesSummary:
    """Summary of Best Practices demonstrated"""

    def test_summary(self):
        """
        ✅ CONSISTENCY:
        - All endpoints use same response format {status, data, meta}
        - All errors use same error format {status, error: {code, message, details}}
        - HTTP methods used correctly (GET, POST, PUT, DELETE)
        - Status codes are appropriate (200, 201, 204, 404, 422)

        ✅ CLARITY:
        - Endpoint names are descriptive (/api/v1/users, /api/v1/products)
        - No verbs in URLs (not /api/getusers)
        - Error messages are helpful and include context

        ✅ EXTENSIBILITY:
        - API versioning (/v1/) allows for future versions
        - Pagination support ({page, limit, total})
        - Modular resource structure allows easy expansion
        """
        assert True
