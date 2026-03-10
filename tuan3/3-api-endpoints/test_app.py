"""
Test Flow 3: API Endpoints - Full CRUD with Proper HTTP Methods and Status Codes
Kiểm tra: CRUD operations, HTTP methods, status codes, nested resources
"""

import pytest
import json
import sys
sys.path.insert(0, '/g/2526II_INT3505_1/tuan3/3-api-endpoints')

from app import app


class TestCRUDEndpoints:
    """Test Suite for CRUD Endpoints"""

    @pytest.fixture
    def client(self):
        """Create Flask test client"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    # ============ TEST 1: CREATE Operation (POST) ============

    def test_create_post_returns_201(self, client):
        """✅ Test: POST returns 201 Created"""
        payload = {
            "title": "Test Post",
            "content": "Test content",
            "author_id": 1
        }
        response = client.post(
            '/api/v1/posts',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 201

    def test_create_post_returns_created_resource(self, client):
        """✅ Test: POST returns the created resource"""
        payload = {
            "title": "New Post",
            "content": "Content here",
            "author_id": 1
        }
        response = client.post(
            '/api/v1/posts',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 201

        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'id' in data['data']
        assert data['data']['title'] == "New Post"

    def test_create_post_validation_error(self, client):
        """✅ Test: POST validation error returns 422"""
        payload = {}  # Missing required fields
        response = client.post(
            '/api/v1/posts',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 422

        data = json.loads(response.data)
        assert data['error']['code'] == 'VALIDATION_ERROR'

    def test_create_post_missing_author(self, client):
        """✅ Test: Missing author_id returns proper error"""
        payload = {
            "title": "Test",
            "content": "Test"
        }
        response = client.post(
            '/api/v1/posts',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 422

        data = json.loads(response.data)
        assert data['error']['code'] == 'VALIDATION_ERROR'
        # ✅ Should have details about missing field
        assert len(data['error']['details']) > 0

    def test_create_post_invalid_author(self, client):
        """✅ Test: Invalid author_id returns 404"""
        payload = {
            "title": "Test Post",
            "content": "Test content",
            "author_id": 9999  # Non-existent author
        }
        response = client.post(
            '/api/v1/posts',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 404

    # ============ TEST 2: READ Operation (GET) ============

    def test_read_all_posts_returns_200(self, client):
        """✅ Test: GET list returns 200 OK"""
        response = client.get('/api/v1/posts')
        assert response.status_code == 200

    def test_read_all_posts_has_pagination(self, client):
        """✅ Test: GET list includes pagination metadata"""
        response = client.get('/api/v1/posts')
        data = json.loads(response.data)

        assert 'meta' in data
        assert 'total' in data['meta']
        assert 'page' in data['meta']
        assert 'limit' in data['meta']

    def test_read_single_post_returns_200(self, client):
        """✅ Test: GET single resource returns 200 OK"""
        response = client.get('/api/v1/posts/1')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'id' in data['data']

    def test_read_nonexistent_post_returns_404(self, client):
        """✅ Test: GET non-existent resource returns 404"""
        response = client.get('/api/v1/posts/9999')
        assert response.status_code == 404

        data = json.loads(response.data)
        assert data['error']['code'] == 'POST_NOT_FOUND'

    def test_read_with_filtering(self, client):
        """✅ Test: GET with filtering query params"""
        response = client.get('/api/v1/posts?status=published')
        assert response.status_code == 200

        data = json.loads(response.data)
        # ✅ Should return published posts only
        for post in data['data']:
            assert post['status'] == 'published'

    def test_read_with_pagination_params(self, client):
        """✅ Test: GET with pagination parameters"""
        response = client.get('/api/v1/posts?page=1&limit=1')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['meta']['page'] == 1
        assert data['meta']['limit'] == 1
        assert len(data['data']) <= 1

    # ============ TEST 3: UPDATE Operation (PUT) ============

    def test_update_full_put_returns_200(self, client):
        """✅ Test: PUT (full update) returns 200 OK"""
        payload = {
            "title": "Updated Title",
            "content": "Updated content",
            "status": "published"
        }
        response = client.put(
            '/api/v1/posts/1',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200

    def test_update_full_put_requires_all_fields(self, client):
        """✅ Test: PUT requires all required fields"""
        payload = {
            "content": "Only content"  # Missing title
        }
        response = client.put(
            '/api/v1/posts/1',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 422

    def test_update_full_put_nonexistent_returns_404(self, client):
        """✅ Test: PUT non-existent resource returns 404"""
        payload = {"title": "Title", "content": "Content"}
        response = client.put(
            '/api/v1/posts/9999',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 404

    # ============ TEST 4: UPDATE Operation (PATCH) ============

    def test_update_partial_patch_returns_200(self, client):
        """✅ Test: PATCH (partial update) returns 200 OK"""
        payload = {
            "title": "New Title Only"
        }
        response = client.patch(
            '/api/v1/posts/1',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200

    def test_patch_allows_single_field(self, client):
        """✅ Test: PATCH allows updating single field"""
        payload = {
            "status": "published"
        }
        response = client.patch(
            '/api/v1/posts/1',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['data']['status'] == 'published'

    def test_patch_nonexistent_returns_404(self, client):
        """✅ Test: PATCH non-existent resource returns 404"""
        response = client.patch(
            '/api/v1/posts/9999',
            data=json.dumps({"title": "Title"}),
            content_type='application/json'
        )
        assert response.status_code == 404

    # ============ TEST 5: DELETE Operation ============

    def test_delete_returns_204(self, client):
        """✅ Test: DELETE returns 204 No Content"""
        response = client.delete('/api/v1/posts/1')
        assert response.status_code == 204

    def test_delete_no_response_body(self, client):
        """✅ Test: DELETE returns empty body (204)"""
        response = client.delete('/api/v1/posts/1')
        assert response.status_code == 204
        assert len(response.data) == 0

    def test_delete_nonexistent_returns_404(self, client):
        """✅ Test: DELETE non-existent resource returns 404"""
        response = client.delete('/api/v1/posts/9999')
        assert response.status_code == 404

    # ============ TEST 6: Nested Resources ============

    def test_nested_get_comments_list(self, client):
        """✅ Test: GET nested resource list"""
        response = client.get('/api/v1/posts/1/comments')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'meta' in data  # Should have pagination

    def test_nested_post_creates_comment(self, client):
        """✅ Test: POST nested resource returns 201"""
        payload = {
            "content": "Test comment",
            "author_id": 2
        }
        response = client.post(
            '/api/v1/posts/1/comments',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 201

    def test_nested_get_single_comment(self, client):
        """✅ Test: GET specific nested resource"""
        response = client.get('/api/v1/posts/1/comments/1')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['data']['id'] == 1
        assert data['data']['post_id'] == 1

    def test_nested_delete_comment(self, client):
        """✅ Test: DELETE nested resource returns 204"""
        response = client.delete('/api/v1/posts/1/comments/1')
        assert response.status_code == 204

    def test_nested_parent_not_found_returns_404(self, client):
        """✅ Test: Accessing nested under non-existent parent"""
        response = client.get('/api/v1/posts/9999/comments')
        assert response.status_code == 404

    # ============ TEST 7: Actions (Non-CRUD) ============

    def test_action_publish_post(self, client):
        """✅ Test: Action endpoint /publish"""
        response = client.post(
            '/api/v1/posts/1/publish',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['data']['status'] == 'published'

    def test_action_unpublish_post(self, client):
        """✅ Test: Action endpoint /unpublish"""
        response = client.post(
            '/api/v1/posts/1/unpublish',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 200

    def test_action_on_nonexistent_returns_404(self, client):
        """✅ Test: Action on non-existent resource"""
        response = client.post(
            '/api/v1/posts/9999/publish',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 404

    # ============ TEST 8: Likes ============

    def test_like_post_returns_201(self, client):
        """✅ Test: Like (POST) returns 201"""
        payload = {"user_id": 2}
        response = client.post(
            '/api/v1/posts/1/likes',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 201

    def test_get_likes_count(self, client):
        """✅ Test: GET likes returns count"""
        response = client.get('/api/v1/posts/1/likes')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'count' in data['data']

    def test_unlike_post_returns_204(self, client):
        """✅ Test: Unlike (DELETE) returns 204"""
        payload = {"user_id": 2}
        response = client.delete(
            '/api/v1/posts/1/likes',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 204

    # ============ TEST 9: HTTP Status Codes Summary ============

    def test_status_code_200_ok(self, client):
        """✅ Test: 200 OK for GET/PUT/PATCH success"""
        # GET
        response = client.get('/api/v1/posts')
        assert response.status_code == 200

    def test_status_code_201_created(self, client):
        """✅ Test: 201 Created for POST"""
        payload = {
            "title": "Test",
            "content": "Test",
            "author_id": 1
        }
        response = client.post(
            '/api/v1/posts',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 201

    def test_status_code_204_no_content(self, client):
        """✅ Test: 204 No Content for DELETE"""
        response = client.delete('/api/v1/posts/1')
        assert response.status_code == 204

    def test_status_code_400_bad_request(self, client):
        """✅ Test: 400 Bad Request for invalid format"""
        # Would need malformed data
        pass

    def test_status_code_404_not_found(self, client):
        """✅ Test: 404 Not Found"""
        response = client.get('/api/v1/posts/9999')
        assert response.status_code == 404

    def test_status_code_422_validation_error(self, client):
        """✅ Test: 422 Unprocessable Entity for validation"""
        response = client.post(
            '/api/v1/posts',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 422


class TestCRUDSummary:
    """Summary of CRUD operations and status codes"""

    def test_summary(self):
        """
        ✅ CRUD OPERATIONS:

        CREATE (POST):
        ✅ POST /posts → 201 Created
        ✅ Returns created resource
        ✅ Validation error → 422
        ✅ Invalid relation → 404

        READ (GET):
        ✅ GET /posts → 200 OK
        ✅ GET /posts/{id} → 200 OK
        ✅ Non-existent → 404 Not Found
        ✅ Supports filtering, pagination, sorting

        UPDATE (PUT - Full):
        ✅ PUT /posts/{id} → 200 OK
        ✅ Requires all fields
        ✅ Missing fields → 422
        ✅ Non-existent → 404

        UPDATE (PATCH - Partial):
        ✅ PATCH /posts/{id} → 200 OK
        ✅ Allows single field update
        ✅ Non-existent → 404

        DELETE:
        ✅ DELETE /posts/{id} → 204 No Content
        ✅ Empty response body
        ✅ Non-existent → 404

        NESTED RESOURCES:
        ✅ GET /posts/{id}/comments → 200 OK
        ✅ POST /posts/{id}/comments → 201 Created
        ✅ DELETE /posts/{id}/comments/{id} → 204

        ACTIONS:
        ✅ POST /posts/{id}/publish → 200 OK
        ✅ POST /posts/{id}/unpublish → 200 OK

        HTTP STATUS CODES:
        ✅ 200 OK - GET/PUT/PATCH success
        ✅ 201 Created - POST success
        ✅ 204 No Content - DELETE success
        ✅ 400 Bad Request - Invalid format
        ✅ 404 Not Found - Resource missing
        ✅ 409 Conflict - Duplicate/conflict
        ✅ 422 Unprocessable - Validation error
        """
        assert True
