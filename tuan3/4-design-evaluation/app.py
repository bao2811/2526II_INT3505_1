"""
Flow 4: API Design Evaluation - Example APIs with Quality Scoring
Demo: Evaluate API design quality with the framework
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# ============ API QUALITY EVALUATION FRAMEWORK ============

class APIEvaluator:
    """
    Evaluates API design quality based on 5 criteria:
    1. Consistency (20 points)
    2. Clarity (20 points)
    3. Extensibility (20 points)
    4. Correctness (20 points)
    5. Performance/Security (20 points)
    Total: 100 points
    """

    def __init__(self, name):
        self.name = name
        self.scores = {}
        self.issues = []
        self.strengths = []

    def evaluate_consistency(self, score, issues=None, strengths=None):
        """Evaluate consistency (naming, response format, HTTP methods)"""
        self.scores['consistency'] = score
        if issues:
            self.issues.extend(issues)
        if strengths:
            self.strengths.extend(strengths)

    def evaluate_clarity(self, score, issues=None, strengths=None):
        """Evaluate clarity (documentation, error messages)"""
        self.scores['clarity'] = score
        if issues:
            self.issues.extend(issues)
        if strengths:
            self.strengths.extend(strengths)

    def evaluate_extensibility(self, score, issues=None, strengths=None):
        """Evaluate extensibility (versioning, backward compatibility)"""
        self.scores['extensibility'] = score
        if issues:
            self.issues.extend(issues)
        if strengths:
            self.strengths.extend(strengths)

    def evaluate_correctness(self, score, issues=None, strengths=None):
        """Evaluate correctness (HTTP methods, status codes, nested resources)"""
        self.scores['correctness'] = score
        if issues:
            self.issues.extend(issues)
        if strengths:
            self.strengths.extend(strengths)

    def evaluate_performance(self, score, issues=None, strengths=None):
        """Evaluate performance/security (pagination, filtering, auth)"""
        self.scores['performance'] = score
        if issues:
            self.issues.extend(issues)
        if strengths:
            self.strengths.extend(strengths)

    def get_total_score(self):
        """Calculate total score (0-100)"""
        if not self.scores:
            return 0
        return sum(self.scores.values()) // 5  # Average of 5 categories

    def get_rating(self):
        """Get qualitative rating"""
        score = self.get_total_score()
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Good"
        elif score >= 70:
            return "Fair"
        else:
            return "Poor"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "name": self.name,
            "scores": self.scores,
            "total": self.get_total_score(),
            "rating": self.get_rating(),
            "strengths": self.strengths,
            "issues": self.issues,
            "breakdown": {
                "consistency": f"{self.scores.get('consistency', 0)}/20",
                "clarity": f"{self.scores.get('clarity', 0)}/20",
                "extensibility": f"{self.scores.get('extensibility', 0)}/20",
                "correctness": f"{self.scores.get('correctness', 0)}/20",
                "performance": f"{self.scores.get('performance', 0)}/20"
            }
        }


# ============ EXAMPLE 1: Good API Design (90+ score) ============

good_api = APIEvaluator("E-commerce API (Good)")

good_api.evaluate_consistency(
    score=19,
    issues=["Minor: timestamp format could be documented"],
    strengths=[
        "All endpoints use consistent response format",
        "Error format is standardized",
        "HTTP methods used correctly",
        "Status codes appropriate"
    ]
)

good_api.evaluate_clarity(
    score=19,
    issues=["Could provide more detailed error messages"],
    strengths=[
        "Endpoint names are clear and descriptive",
        "Response fields are self-explanatory",
        "Good API documentation",
        "Examples provided"
    ]
)

good_api.evaluate_extensibility(
    score=19,
    issues=["Could support more query parameters"],
    strengths=[
        "Has API versioning (/v1/)",
        "Backward compatible design",
        "Modular resource structure",
        "Optional fields for future expansion"
    ]
)

good_api.evaluate_correctness(
    score=19,
    issues=["Some edge cases not documented"],
    strengths=[
        "Correct HTTP method mapping",
        "Proper status codes (201, 204, 400, 404)",
        "Good nested resource design",
        "Complete CRUD operations"
    ]
)

good_api.evaluate_performance(
    score=18,
    issues=["Rate limiting not documented"],
    strengths=[
        "Pagination support",
        "Filtering capabilities",
        "Sorting support",
        "Input validation (422)"
    ]
)


# ============ EXAMPLE 2: Fair API Design (70-79 score) ============

fair_api = APIEvaluator("Social Media API (Fair)")

fair_api.evaluate_consistency(
    score=14,
    issues=[
        "Inconsistent parameter naming (userId vs user_id)",
        "Some endpoints return 'data', others return 'items'",
        "Status code usage inconsistent"
    ],
    strengths=[
        "Most endpoints use plural nouns",
        "Mostly lowercase",
        "Response format generally consistent"
    ]
)

fair_api.evaluate_clarity(
    score=15,
    issues=[
        "Some endpoints lack documentation",
        "Error messages not detailed",
        "Missing endpoint descriptions"
    ],
    strengths=[
        "Most endpoint names are clear",
        "Basic example provided",
        "Endpoints are searchable"
    ]
)

fair_api.evaluate_extensibility(
    score=12,
    issues=[
        "No API versioning currently",
        "Tightly coupled endpoints",
        "Hard to add new features without breaking old ones"
    ],
    strengths=[
        "Modular design attempted",
        "Some separation of concerns"
    ]
)

fair_api.evaluate_correctness(
    score=13,
    issues=[
        "Some GET requests modify data",
        "Nested resources not well designed",
        "Status codes not always appropriate"
    ],
    strengths=[
        "Most HTTP methods are correct",
        "DELETE is properly implemented",
        "POST for creating new records"
    ]
)

fair_api.evaluate_performance(
    score=12,
    issues=[
        "No pagination mentioned",
        "Filtering is limited",
        "No sorting support",
        "Performance implications not addressed"
    ],
    strengths=[
        "Basic filtering available",
        "Attempts at search functionality",
        "Basic authentication"
    ]
)


# ============ EXAMPLE 3: Poor API Design (<70 score) ============

poor_api = APIEvaluator("Legacy API (Poor)")

poor_api.evaluate_consistency(
    score=8,
    issues=[
        "Inconsistent endpoint naming (getUser, createProduct, deleteOrder)",
        "Response format varies by endpoint",
        "Status codes are always 200 or 500",
        "Mix of singular and plural nouns"
    ],
    strengths=[
        "At least some attempt at organizing endpoints"
    ]
)

poor_api.evaluate_clarity(
    score=7,
    issues=[
        "Endpoint names use verbs (bad practice)",
        "Response fields inconsistent",
        "Error messages are vague",
        "No documentation or examples"
    ],
    strengths=[
        "Endpoint names somewhat descriptive"
    ]
)

poor_api.evaluate_extensibility(
    score=5,
    issues=[
        "No API versioning",
        "Breaking changes would affect all clients",
        "Tightly coupled design",
        "Cannot evolve without client refactoring"
    ],
    strengths=[]
)

poor_api.evaluate_correctness(
    score=6,
    issues=[
        "GET requests modify data (security issue)",
        "DELETE via query parameters",
        "Wrong status codes (always 200)",
        "No proper error handling"
    ],
    strengths=[
        "Some attempt at REST principles"
    ]
)

poor_api.evaluate_performance(
    score=5,
    issues=[
        "No pagination (returns all data)",
        "No filtering",
        "No sorting",
        "No input validation",
        "Security vulnerabilities (CSRF with GET)"
    ],
    strengths=[]
)


# ============ ENDPOINTS ============

@app.route('/api/v1/evaluations', methods=['GET'])
def get_all_evaluations():
    """Get all API evaluations"""
    evaluations = [
        good_api.to_dict(),
        fair_api.to_dict(),
        poor_api.to_dict()
    ]
    return jsonify({
        "status": "success",
        "data": evaluations
    })


@app.route('/api/v1/evaluations/good', methods=['GET'])
def get_good_evaluation():
    """Get good API evaluation"""
    return jsonify({
        "status": "success",
        "data": good_api.to_dict()
    })


@app.route('/api/v1/evaluations/fair', methods=['GET'])
def get_fair_evaluation():
    """Get fair API evaluation"""
    return jsonify({
        "status": "success",
        "data": fair_api.to_dict()
    })


@app.route('/api/v1/evaluations/poor', methods=['GET'])
def get_poor_evaluation():
    """Get poor API evaluation"""
    return jsonify({
        "status": "success",
        "data": poor_api.to_dict()
    })


@app.route('/api/v1/framework', methods=['GET'])
def get_evaluation_framework():
    """Get evaluation framework details"""
    framework = {
        "criteria": {
            "consistency": {
                "weight": 20,
                "description": "Consistent naming, response format, HTTP methods, status codes",
                "checklist": [
                    "All endpoints use same response format",
                    "Error format is standardized",
                    "HTTP methods used correctly",
                    "Status codes appropriate",
                    "Naming conventions applied consistently"
                ]
            },
            "clarity": {
                "weight": 20,
                "description": "Clear names, good documentation, helpful error messages",
                "checklist": [
                    "Endpoint names describe function clearly",
                    "Response fields are understandable",
                    "Good documentation and examples",
                    "Error messages are precise",
                    "Purpose of each endpoint is obvious"
                ]
            },
            "extensibility": {
                "weight": 20,
                "description": "Versioning, backward compatibility, modular design",
                "checklist": [
                    "Has API versioning",
                    "Backward compatible",
                    "Modular resource structure",
                    "Optional fields for expansion",
                    "Can add features without breaking old ones"
                ]
            },
            "correctness": {
                "weight": 20,
                "description": "HTTP methods, status codes, nested resources, CRUD",
                "checklist": [
                    "HTTP methods map correctly to operations",
                    "Status codes are appropriate",
                    "Nested resources designed well",
                    "All CRUD operations present",
                    "Error handling comprehensive"
                ]
            },
            "performance": {
                "weight": 20,
                "description": "Pagination, filtering, sorting, security, validation",
                "checklist": [
                    "Pagination support",
                    "Filtering capabilities",
                    "Sorting support",
                    "Input validation",
                    "Rate limiting/authentication"
                ]
            }
        },
        "scoring": {
            "excellent": "90-100",
            "good": "80-89",
            "fair": "70-79",
            "poor": "Below 70"
        }
    }
    return jsonify({
        "status": "success",
        "data": framework
    })


@app.route('/api/v1/scoring-guidance', methods=['GET'])
def get_scoring_guidance():
    """Get guidance on scoring"""
    guidance = {
        "scoring_scale": {
            "20": "Excellent - No issues, follows all best practices",
            "18-19": "Good - Minor issues, mostly follows best practices",
            "15-17": "Fair - Some issues that should be addressed",
            "12-14": "Needs Improvement - Multiple issues, some best practices missing",
            "Below 12": "Poor - Significant issues, major best practices missing"
        },
        "total_interpretation": {
            "90-100": {
                "rating": "Excellent",
                "status": "Production Ready",
                "action": "No action needed, maintain quality"
            },
            "80-89": {
                "rating": "Good",
                "status": "Acceptable",
                "action": "Minor improvements recommended"
            },
            "70-79": {
                "rating": "Fair",
                "status": "Needs Improvements",
                "action": "Address issues before production"
            },
            "Below 70": {
                "rating": "Poor",
                "status": "Significant Refactoring Needed",
                "action": "Major redesign required"
            }
        },
        "evaluation_process": [
            "1. Read API documentation",
            "2. Analyze endpoint naming/design",
            "3. Check response formats",
            "4. Check HTTP methods and status codes",
            "5. Score each of 5 criteria",
            "6. Calculate total (average of 5 criteria)",
            "7. Write report with findings"
        ]
    }
    return jsonify({
        "status": "success",
        "data": guidance
    })


# ============ TESTING ============

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  Flow 4: API Design Evaluation Demo                        ║
    ║  Server running on http://localhost:5003                   ║
    ╚════════════════════════════════════════════════════════════╝

    🧪 Test endpoints:

    Get all evaluations:
    GET    http://localhost:5003/api/v1/evaluations

    Get specific evaluation:
    GET    http://localhost:5003/api/v1/evaluations/good
    GET    http://localhost:5003/api/v1/evaluations/fair
    GET    http://localhost:5003/api/v1/evaluations/poor

    Get evaluation framework:
    GET    http://localhost:5003/api/v1/framework

    Get scoring guidance:
    GET    http://localhost:5003/api/v1/scoring-guidance

    📍 Key Concepts Demonstrated:
    ✅ Framework: 5 criteria with 20 points each = 100 total
    ✅ Scoring: Excellent (90+), Good (80+), Fair (70+), Poor (<70)
    ✅ Examples: Good, Fair, and Poor API designs with scores
    ✅ Evaluation: Issues and strengths identified for each API
    """)

    app.run(debug=True, port=5003)
