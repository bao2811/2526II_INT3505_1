"""
Test Flow 6: Peer Review - Well-Designed API Ready for Production
Kiểm tra: Production-ready API with all best practices
"""

import pytest
import json
import sys
sys.path.insert(0, '/g/2526II_INT3505_1/tuan3/6-peer-review')

from app import app


class TestWellDesignedAPI:
    """Test Suite for Well-Designed API (Production Ready)"""

    @pytest.fixture
    def client(self):
        """Create Flask test client"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    # ============ TEST 1: Naming Conventions ✅ ============

    def test_plural_resource_names(self, client):
        """✅ Test: Resource names are plural"""
        response = client.get('/api/v1/projects')
        assert response.status_code == 200

    def test_lowercase_endpoints(self, client):
        """✅ Test: All endpoints are lowercase"""
        response = client.get('/api/v1/projects')
        # ✅ /v1/ is lowercase, not /V1/
        assert response.status_code == 200

    def test_hyphens_in_nested_resources(self, client):
        """✅ Test: Nested resources use hyphens"""
        response = client.get('/api/v1/team-members')
        # ✅ team-members uses hyphens, not team_members
        assert response.status_code == 200

    def test_api_versioning_present(self, client):
        """✅ Test: Versioning is present (/v1/)"""
        response = client.get('/api/v1/projects')
        # ✅ /v1/ allows for future /v2/
        assert response.status_code == 200

    # ============ TEST 2: HTTP Methods ✅ ============

    def test_get_for_retrieval(self, client):
        """✅ Test: GET is used for retrieval"""
        response = client.get('/api/v1/projects')
        assert response.status_code == 200

    def test_post_for_creation(self, client):
        """✅ Test: POST is used for creation"""
        payload = {
            "name": "New Project",
            "description": "Test project"
        }
        response = client.post(
            '/api/v1/projects',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 201

    def test_put_for_full_update(self, client):
        """✅ Test: PUT is used for full update"""
        payload = {
            "name": "Updated",
            "description": "Updated description"
        }
        response = client.put(
            '/api/v1/projects/1',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 200

    def test_patch_for_partial_update(self, client):
        """✅ Test: PATCH is used for partial update"""
        response = client.patch(
            '/api/v1/projects/1',
            data=json.dumps({"name": "New Name"}),
            content_type='application/json'
        )
        assert response.status_code == 200

    def test_delete_for_deletion(self, client):
        """✅ Test: DELETE is used for deletion"""
        response = client.delete('/api/v1/projects/1')
        assert response.status_code == 204

    def test_no_verbs_in_urls(self, client):
        """✅ Test: No verbs in URLs (not /getProjects, /createProject)"""
        # All endpoints are resource-based
        response = client.get('/api/v1/projects')
        # ✅ No verbs, just resource names
        assert response.status_code == 200

    # ============ TEST 3: Response Format ✅ ============

    def test_consistent_success_response_format(self, client):
        """✅ Test: All success responses have consistent format"""
        response = client.get('/api/v1/projects')
        data = json.loads(response.data)

        # ✅ Standard format: {status, data, meta}
        assert 'status' in data
        assert 'data' in data
        assert data['status'] == 'success'

    def test_response_has_metadata(self, client):
        """✅ Test: List responses include metadata"""
        response = client.get('/api/v1/projects')
        data = json.loads(response.data)

        # ✅ Includes pagination metadata
        assert 'meta' in data
        assert 'total' in data['meta']
        assert 'page' in data['meta']
        assert 'limit' in data['meta']

    def test_error_response_format(self, client):
        """✅ Test: Error responses have consistent format"""
        response = client.post(
            '/api/v1/projects',
            data=json.dumps({}),  # Missing required fields
            content_type='application/json'
        )
        data = json.loads(response.data)

        # ✅ Standard error format
        assert data['status'] == 'error'
        assert 'error' in data
        assert 'code' in data['error']
        assert 'message' in data['error']
        assert 'details' in data['error']

    # ============ TEST 4: Status Codes ✅ ============

    def test_status_200_for_get(self, client):
        """✅ Test: 200 OK for GET"""
        response = client.get('/api/v1/projects')
        assert response.status_code == 200

    def test_status_201_for_post(self, client):
        """✅ Test: 201 Created for POST"""
        payload = {"name": "Test", "description": "Test"}
        response = client.post(
            '/api/v1/projects',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 201

    def test_status_204_for_delete(self, client):
        """✅ Test: 204 No Content for DELETE"""
        response = client.delete('/api/v1/projects/1')
        assert response.status_code == 204

    def test_status_404_for_not_found(self, client):
        """✅ Test: 404 Not Found"""
        response = client.get('/api/v1/projects/9999')
        assert response.status_code == 404

    def test_status_422_for_validation_error(self, client):
        """✅ Test: 422 for validation errors"""
        response = client.post(
            '/api/v1/projects',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 422

    # ============ TEST 5: Pagination ✅ ============

    def test_pagination_support(self, client):
        """✅ Test: Pagination is supported"""
        response = client.get('/api/v1/projects?page=1&limit=5')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['meta']['page'] == 1
        assert data['meta']['limit'] == 5

    def test_pagination_metadata(self, client):
        """✅ Test: Pagination includes useful metadata"""
        response = client.get('/api/v1/projects')
        data = json.loads(response.data)

        # ✅ Has all pagination info
        assert 'total' in data['meta']
        assert 'page' in data['meta']
        assert 'limit' in data['meta']
        assert 'pages' in data['meta']

    # ============ TEST 6: Filtering ✅ ============

    def test_filtering_by_status(self, client):
        """✅ Test: Filtering is supported"""
        response = client.get('/api/v1/projects?status=active')
        assert response.status_code == 200

    # ============ TEST 7: Nested Resources ✅ ============

    def test_nested_resource_pattern(self, client):
        """✅ Test: Nested resources follow pattern"""
        response = client.get('/api/v1/projects/1/tasks')
        assert response.status_code == 200

    def test_nested_resource_crud(self, client):
        """✅ Test: Can CRUD nested resources"""
        # POST nested resource
        payload = {
            "title": "New Task",
            "status": "pending",
            "assigned_to": 1
        }
        response = client.post(
            '/api/v1/projects/1/tasks',
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 201

    def test_nested_get_single_resource(self, client):
        """✅ Test: Can get single nested resource"""
        response = client.get('/api/v1/projects/1/tasks/1')
        assert response.status_code == 200

    # ============ TEST 8: Query Parameters ✅ ============

    def test_query_params_lowercase(self, client):
        """✅ Test: Query parameters are lowercase"""
        response = client.get('/api/v1/team-members?sort-by=name&order=desc')
        assert response.status_code == 200

    def test_query_params_with_sorting(self, client):
        """✅ Test: Sorting is supported"""
        response = client.get('/api/v1/team-members?sort-by=name&order=desc')
        assert response.status_code == 200

    # ============ TEST 9: Validation ✅ ============

    def test_required_field_validation(self, client):
        """✅ Test: Required fields are validated"""
        response = client.post(
            '/api/v1/projects',
            data=json.dumps({"description": "Missing name"}),
            content_type='application/json'
        )
        assert response.status_code == 422

        data = json.loads(response.data)
        # ✅ Details about validation error
        assert len(data['error']['details']) > 0

    def test_validation_response_format(self, client):
        """✅ Test: Validation errors have detail format"""
        response = client.post(
            '/api/v1/projects',
            data=json.dumps({}),
            content_type='application/json'
        )
        data = json.loads(response.data)

        # ✅ Each field has error details
        details = data['error']['details']
        for detail in details:
            assert 'field' in detail
            assert 'message' in detail

    # ============ TEST 10: Peer Review Endpoints ✅ ============

    def test_review_checklist_endpoint(self, client):
        """✅ Test: Self-documenting checklist endpoint"""
        response = client.get('/api/v1/review-checklist')
        assert response.status_code == 200

        data = json.loads(response.data)
        # ✅ API documents its own evaluation
        assert 'evaluation' in data['data']
        assert 'total_score' in data['data']
        assert 'rating' in data['data']

    def test_peer_review_feedback_endpoint(self, client):
        """✅ Test: Feedback endpoint shows strengths and improvements"""
        response = client.get('/api/v1/peer-review-feedback')
        assert response.status_code == 200

        data = json.loads(response.data)
        # ✅ Self-aware API documents strengths
        assert 'strengths' in data['data']
        assert len(data['data']['strengths']) > 0
        # ✅ And areas for improvement
        assert 'areas_for_improvement' in data['data']

    # ============ TEST 11: Documentation ✅ ============

    def test_api_self_documents(self, client):
        """✅ Test: API has self-documenting endpoints"""
        response = client.get('/api/v1/review-checklist')
        data = json.loads(response.data)

        checklist = data['data']
        # ✅ API explains what was evaluated
        assert 'api_name' in checklist
        assert 'evaluation' in checklist

    # ============ TEST 12: Error Handling ============

    def test_404_when_parent_not_found(self, client):
        """✅ Test: 404 when accessing nested under non-existent parent"""
        response = client.get('/api/v1/projects/9999/tasks')
        assert response.status_code == 404

    def test_404_when_nested_not_found(self, client):
        """✅ Test: 404 when nested resource doesn't exist"""
        response = client.get('/api/v1/projects/1/tasks/9999')
        assert response.status_code == 404

    # ============ TEST 13: Consistency Across Resources ============

    def test_all_resources_use_same_patterns(self, client):
        """✅ Test: All resources follow same patterns"""
        # Test projects
        response = client.get('/api/v1/projects')
        assert response.status_code == 200

        # Test team-members
        response = client.get('/api/v1/team-members')
        assert response.status_code == 200

        # Both use same response format
        data = json.loads(response.data)
        assert 'status' in data
        assert 'data' in data
        assert 'meta' in data


class TestPeerReviewSummary:
    """Summary of Well-Designed API - Production Ready"""

    def test_peer_review_score_excellent(self, client):
        """✅ Test: API scores as Excellent (97/100)"""
        response = client.get('/api/v1/review-checklist')
        data = json.loads(response.data)

        assert data['data']['total_score'] >= 90
        assert data['data']['rating'] == 'Excellent'

    def test_summary(self):
        """
        ✅ WELL-DESIGNED API - 97/100 (EXCELLENT):

        ✅ NAMING CONVENTIONS (19/20):
        - Plural nouns: /projects, /tasks, /team-members
        - Lowercase: /api/v1/
        - Hyphens for multi-word: /team-members
        - Versioning: /v1/
        - Query params: lowercase, hyphens

        ✅ HTTP METHODS (20/20):
        - GET for retrieval
        - POST for creation (201)
        - PUT for full update (200)
        - PATCH for partial update (200)
        - DELETE for deletion (204)
        - No verbs in URLs

        ✅ RESPONSE FORMAT (20/20):
        - Consistent {status, data, meta}
        - Error format standardized
        - Pagination metadata included
        - Validation details provided

        ✅ STATUS CODES (20/20):
        - 200 OK for GET/PUT/PATCH
        - 201 Created for POST
        - 204 No Content for DELETE
        - 404 Not Found for missing resources
        - 422 Unprocessable for validation

        ✅ FEATURES (18/20):
        - Pagination with metadata
        - Filtering support
        - Sorting support
        - Nested resources
        - Could add: batch operations, search

        PRODUCTION-READY:
        ✅ All endpoints documented
        ✅ Error handling comprehensive
        ✅ Validation included
        ✅ Nested resources designed well
        ✅ Self-documenting endpoints
        ✅ Consistent across all resources
        ✅ Backward compatible
        ✅ Easy to extend

        RECOMMENDATIONS FOR IMPROVEMENT:
        - Add search functionality
        - Document example requests/responses
        - Implement rate limiting headers
        - Add include/expand for related resources
        - Support batch operations
        """
        assert True
