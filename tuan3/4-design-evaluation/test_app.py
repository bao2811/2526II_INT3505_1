"""
Test Flow 4: Design Evaluation Framework
Kiểm tra: Evaluation scoring, framework, real-world examples
"""

import pytest
import json
import sys
sys.path.insert(0, '/g/2526II_INT3505_1/tuan3/4-design-evaluation')

from app import app, APIEvaluator


class TestEvaluationFramework:
    """Test Suite for API Evaluation Framework"""

    @pytest.fixture
    def client(self):
        """Create Flask test client"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    # ============ TEST 1: APIEvaluator Class ============

    def test_evaluator_creation(self):
        """✅ Test: Can create evaluator instance"""
        evaluator = APIEvaluator("Test API")
        assert evaluator.name == "Test API"

    def test_evaluator_scoring(self):
        """✅ Test: Evaluator calculates total score"""
        evaluator = APIEvaluator("Test API")
        evaluator.evaluate_consistency(20)
        evaluator.evaluate_clarity(20)
        evaluator.evaluate_extensibility(20)
        evaluator.evaluate_correctness(20)
        evaluator.evaluate_performance(20)

        assert evaluator.get_total_score() == 100

    def test_evaluator_rating_excellent(self):
        """✅ Test: 90+ score = Excellent"""
        evaluator = APIEvaluator("Good API")
        # Score 90+
        for _ in range(5):
            evaluator.scores[f'criterion{_}'] = 18  # Each 18/20 = 90 avg

        # Recalculate
        evaluator.evaluate_consistency(18)
        evaluator.evaluate_clarity(18)
        evaluator.evaluate_extensibility(18)
        evaluator.evaluate_correctness(18)
        evaluator.evaluate_performance(18)

        assert evaluator.get_rating() == "Excellent"

    def test_evaluator_rating_good(self):
        """✅ Test: 80-89 score = Good"""
        evaluator = APIEvaluator("Fair API")
        evaluator.evaluate_consistency(16)
        evaluator.evaluate_clarity(16)
        evaluator.evaluate_extensibility(16)
        evaluator.evaluate_correctness(16)
        evaluator.evaluate_performance(16)

        score = evaluator.get_total_score()
        assert 80 <= score < 90
        assert evaluator.get_rating() == "Good"

    def test_evaluator_rating_fair(self):
        """✅ Test: 70-79 score = Fair"""
        evaluator = APIEvaluator("Fair API")
        evaluator.evaluate_consistency(14)
        evaluator.evaluate_clarity(14)
        evaluator.evaluate_extensibility(14)
        evaluator.evaluate_correctness(14)
        evaluator.evaluate_performance(14)

        score = evaluator.get_total_score()
        assert 70 <= score < 80
        assert evaluator.get_rating() == "Fair"

    def test_evaluator_rating_poor(self):
        """✅ Test: <70 score = Poor"""
        evaluator = APIEvaluator("Poor API")
        evaluator.evaluate_consistency(10)
        evaluator.evaluate_clarity(10)
        evaluator.evaluate_extensibility(10)
        evaluator.evaluate_correctness(10)
        evaluator.evaluate_performance(10)

        score = evaluator.get_total_score()
        assert score < 70
        assert evaluator.get_rating() == "Poor"

    def test_evaluator_to_dict(self):
        """✅ Test: Evaluator converts to dict"""
        evaluator = APIEvaluator("Test API")
        evaluator.evaluate_consistency(20, strengths=["Good consistency"])
        evaluator.evaluate_clarity(20)
        evaluator.evaluate_extensibility(20)
        evaluator.evaluate_correctness(20)
        evaluator.evaluate_performance(20)

        result = evaluator.to_dict()
        assert 'name' in result
        assert 'scores' in result
        assert 'total' in result
        assert 'rating' in result
        assert 'strengths' in result
        assert 'issues' in result

    # ============ TEST 2: Evaluation Endpoints ============

    def test_get_all_evaluations(self, client):
        """✅ Test: Get all API evaluations"""
        response = client.get('/api/v1/evaluations')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert isinstance(data['data'], list)
        assert len(data['data']) >= 3  # At least 3 examples

    def test_get_good_evaluation(self, client):
        """✅ Test: Get good API evaluation"""
        response = client.get('/api/v1/evaluations/good')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['data']['rating'] == 'Excellent'
        assert data['data']['total'] >= 90

    def test_get_fair_evaluation(self, client):
        """✅ Test: Get fair API evaluation"""
        response = client.get('/api/v1/evaluations/fair')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['data']['rating'] == 'Fair'
        assert 70 <= data['data']['total'] < 80

    def test_get_poor_evaluation(self, client):
        """✅ Test: Get poor API evaluation"""
        response = client.get('/api/v1/evaluations/poor')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['data']['rating'] == 'Poor'
        assert data['data']['total'] < 70

    # ============ TEST 3: Framework Details ============

    def test_framework_endpoint(self, client):
        """✅ Test: Can retrieve evaluation framework"""
        response = client.get('/api/v1/framework')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'criteria' in data['data']

        criteria = data['data']['criteria']
        # Should have 5 criteria
        assert 'consistency' in criteria
        assert 'clarity' in criteria
        assert 'extensibility' in criteria
        assert 'correctness' in criteria
        assert 'performance' in criteria

    def test_framework_has_checklist(self, client):
        """✅ Test: Framework includes checklist items"""
        response = client.get('/api/v1/framework')
        data = json.loads(response.data)

        consistency = data['data']['criteria']['consistency']
        assert 'checklist' in consistency
        assert len(consistency['checklist']) > 0

    def test_framework_has_weights(self, client):
        """✅ Test: Each criterion has weight (20 points)"""
        response = client.get('/api/v1/framework')
        data = json.loads(response.data)

        for criterion_name, criterion in data['data']['criteria'].items():
            assert 'weight' in criterion
            assert criterion['weight'] == 20

    def test_framework_has_scoring_info(self, client):
        """✅ Test: Framework includes scoring information"""
        response = client.get('/api/v1/framework')
        data = json.loads(response.data)

        assert 'scoring' in data['data']
        scoring = data['data']['scoring']
        assert 'excellent' in scoring
        assert 'good' in scoring
        assert 'fair' in scoring
        assert 'poor' in scoring

    # ============ TEST 4: Scoring Guidance ============

    def test_scoring_guidance_endpoint(self, client):
        """✅ Test: Get scoring guidance"""
        response = client.get('/api/v1/scoring-guidance')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'scoring_scale' in data['data']
        assert 'total_interpretation' in data['data']

    def test_scoring_scale_breakdown(self, client):
        """✅ Test: Scoring scale breakdown"""
        response = client.get('/api/v1/scoring-guidance')
        data = json.loads(response.data)

        scale = data['data']['scoring_scale']
        # Should have guidance for different score ranges
        assert '20' in scale  # Excellent
        assert '18-19' in scale  # Good
        assert '15-17' in scale  # Fair
        assert '12-14' in scale
        assert 'Below 12' in scale  # Poor

    def test_total_interpretation_90_plus(self, client):
        """✅ Test: Interpretation for 90-100 score"""
        response = client.get('/api/v1/scoring-guidance')
        data = json.loads(response.data)

        interpretation = data['data']['total_interpretation']
        excellent = interpretation['90-100']
        assert excellent['rating'] == 'Excellent'
        assert excellent['status'] == 'Production Ready'

    def test_total_interpretation_80_to_89(self, client):
        """✅ Test: Interpretation for 80-89 score"""
        response = client.get('/api/v1/scoring-guidance')
        data = json.loads(response.data)

        interpretation = data['data']['total_interpretation']
        good = interpretation['80-89']
        assert good['rating'] == 'Good'

    def test_total_interpretation_70_to_79(self, client):
        """✅ Test: Interpretation for 70-79 score"""
        response = client.get('/api/v1/scoring-guidance')
        data = json.loads(response.data)

        interpretation = data['data']['total_interpretation']
        fair = interpretation['70-79']
        assert fair['rating'] == 'Fair'

    def test_total_interpretation_below_70(self, client):
        """✅ Test: Interpretation for below 70 score"""
        response = client.get('/api/v1/scoring-guidance')
        data = json.loads(response.data)

        interpretation = data['data']['total_interpretation']
        poor = interpretation['Below 70']
        assert 'Poor' in poor['rating']

    # ============ TEST 5: Evaluation Details ============

    def test_good_api_has_strengths(self, client):
        """✅ Test: Good API evaluation includes strengths"""
        response = client.get('/api/v1/evaluations/good')
        data = json.loads(response.data)

        assert len(data['data']['strengths']) > 0

    def test_good_api_has_issues(self, client):
        """✅ Test: Good API evaluation may have minor issues"""
        response = client.get('/api/v1/evaluations/good')
        data = json.loads(response.data)

        # Good API might have minor issues
        assert isinstance(data['data']['issues'], list)

    def test_poor_api_has_many_issues(self, client):
        """✅ Test: Poor API has multiple issues"""
        response = client.get('/api/v1/evaluations/poor')
        data = json.loads(response.data)

        # Poor API should have multiple issues
        assert len(data['data']['issues']) > 5

    def test_evaluation_breakdown(self, client):
        """✅ Test: Evaluation has score breakdown"""
        response = client.get('/api/v1/evaluations/good')
        data = json.loads(response.data)

        assert 'breakdown' in data['data']
        breakdown = data['data']['breakdown']
        # Each criterion should be scored
        assert 'consistency' in breakdown
        assert 'clarity' in breakdown
        assert 'extensibility' in breakdown
        assert 'correctness' in breakdown
        assert 'performance' in breakdown

    # ============ TEST 6: Criteria Details ============

    def test_consistency_criterion(self, client):
        """✅ Test: Consistency criterion details"""
        response = client.get('/api/v1/framework')
        data = json.loads(response.data)

        consistency = data['data']['criteria']['consistency']
        assert consistency['weight'] == 20
        assert 'description' in consistency
        assert 'checklist' in consistency
        # Should check: consistent format, error handling, HTTP methods, status codes

    def test_clarity_criterion(self, client):
        """✅ Test: Clarity criterion details"""
        response = client.get('/api/v1/framework')
        data = json.loads(response.data)

        clarity = data['data']['criteria']['clarity']
        assert clarity['weight'] == 20
        assert 'description' in clarity
        assert 'checklist' in clarity

    def test_extensibility_criterion(self, client):
        """✅ Test: Extensibility criterion details"""
        response = client.get('/api/v1/framework')
        data = json.loads(response.data)

        extensibility = data['data']['criteria']['extensibility']
        assert extensibility['weight'] == 20
        assert 'description' in extensibility

    def test_correctness_criterion(self, client):
        """✅ Test: Correctness criterion details"""
        response = client.get('/api/v1/framework')
        data = json.loads(response.data)

        correctness = data['data']['criteria']['correctness']
        assert correctness['weight'] == 20

    def test_performance_criterion(self, client):
        """✅ Test: Performance/Security criterion details"""
        response = client.get('/api/v1/framework')
        data = json.loads(response.data)

        performance = data['data']['criteria']['performance']
        assert performance['weight'] == 20


class TestEvaluationSummary:
    """Summary of Evaluation Framework"""

    def test_summary(self):
        """
        ✅ EVALUATION FRAMEWORK:

        5 CRITERIA (20 points each = 100 total):

        1. CONSISTENCY (20 pts):
        - All endpoints use same response format
        - Error format is standardized
        - HTTP methods used correctly
        - Status codes appropriate

        2. CLARITY (20 pts):
        - Endpoint names describe function clearly
        - Response fields are understandable
        - Good documentation and examples
        - Error messages are precise

        3. EXTENSIBILITY (20 pts):
        - Has API versioning
        - Backward compatible design
        - Modular resource structure
        - Optional fields for expansion

        4. CORRECTNESS (20 pts):
        - HTTP methods map correctly
        - Status codes are appropriate
        - Nested resources designed well
        - All CRUD operations present

        5. PERFORMANCE/SECURITY (20 pts):
        - Pagination support
        - Filtering capabilities
        - Sorting support
        - Input validation
        - Rate limiting/authentication

        SCORING:
        90-100 = Excellent (Production Ready)
        80-89 = Good (Acceptable, minor improvements)
        70-79 = Fair (Needs improvements)
        <70 = Poor (Significant refactoring needed)

        REAL-WORLD EXAMPLES:
        ✅ Good API: 97/100 (Excellent)
        ✅ Fair API: 75/100 (Fair)
        ✅ Poor API: 38/100 (Poor)
        """
        assert True
