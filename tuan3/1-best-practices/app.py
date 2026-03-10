"""
Flow 1: Best Practices - Consistency, Clarity, Extensibility
Demo: Xây dựng API theo best practices
"""

from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# ============ DATABASE MOCK ============
users_db = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "created_at": "2024-01-01"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "created_at": "2024-01-02"},
]

products_db = [
    {"id": 1, "name": "Laptop", "price": 1000, "created_at": "2024-01-01"},
    {"id": 2, "name": "Mouse", "price": 25, "created_at": "2024-01-01"},
]


# ============ CONSISTENCY: Unified Response Format ============

class APIResponse:
    """
    Consistent response format cho tất cả endpoints
    Tất cả response theo cùng một schema
    """

    @staticmethod
    def success(data, meta=None, status_code=200):
        """Success response - consistent format"""
        response = {
            "status": "success",
            "data": data,
        }
        if meta:
            response["meta"] = meta
        return jsonify(response), status_code

    @staticmethod
    def error(code, message, details=None, status_code=400):
        """Error response - consistent format"""
        response = {
            "status": "error",
            "error": {
                "code": code,
                "message": message,
            }
        }
        if details:
            response["error"]["details"] = details
        return jsonify(response), status_code


# ============ CLARITY: Clear Endpoint Names and Descriptions ============

# ❌ BAD - Không rõ ràng, verb-based
# @app.route('/api/getusr')
# @app.route('/api/getuserbyid')
# @app.route('/api/addusr')

# ✅ GOOD - Rõ ràng, resource-based
@app.route('/api/v1/users', methods=['GET'])
def get_users():
    """
    Lấy danh sách users
    Query params:
      - page: int (default=1)
      - limit: int (default=10)
    """
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    # Calculate pagination
    total = len(users_db)
    start = (page - 1) * limit
    end = start + limit

    paginated_users = users_db[start:end]

    meta = {
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }

    return APIResponse.success(paginated_users, meta=meta)


@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Lấy user theo ID"""
    user = next((u for u in users_db if u["id"] == user_id), None)

    if not user:
        return APIResponse.error(
            code="USER_NOT_FOUND",
            message=f"User with ID {user_id} not found",
            status_code=404
        )

    return APIResponse.success(user)


@app.route('/api/v1/users', methods=['POST'])
def create_user():
    """Tạo user mới"""
    data = request.get_json()

    # Validation
    errors = []
    if not data.get("name"):
        errors.append({"field": "name", "message": "Name is required"})
    if not data.get("email"):
        errors.append({"field": "email", "message": "Email is required"})

    if errors:
        return APIResponse.error(
            code="VALIDATION_ERROR",
            message="Validation failed",
            details=errors,
            status_code=422
        )

    # Create user
    new_user = {
        "id": max(u["id"] for u in users_db) + 1,
        "name": data["name"],
        "email": data["email"],
        "created_at": datetime.now().isoformat()
    }
    users_db.append(new_user)

    return APIResponse.success(new_user, status_code=201)


@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Cập nhật user"""
    user = next((u for u in users_db if u["id"] == user_id), None)

    if not user:
        return APIResponse.error(
            code="USER_NOT_FOUND",
            message=f"User with ID {user_id} not found",
            status_code=404
        )

    data = request.get_json()

    # Update
    if "name" in data:
        user["name"] = data["name"]
    if "email" in data:
        user["email"] = data["email"]

    return APIResponse.success(user)


@app.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Xóa user"""
    global users_db
    user = next((u for u in users_db if u["id"] == user_id), None)

    if not user:
        return APIResponse.error(
            code="USER_NOT_FOUND",
            message=f"User with ID {user_id} not found",
            status_code=404
        )

    users_db = [u for u in users_db if u["id"] != user_id]

    return APIResponse.success(None, status_code=204)


# ============ CONSISTENCY: Tương tự cho Products ============

@app.route('/api/v1/products', methods=['GET'])
def get_products():
    """Lấy danh sách products - consistent format như users"""
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    total = len(products_db)
    start = (page - 1) * limit
    end = start + limit

    paginated_products = products_db[start:end]

    meta = {
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }

    return APIResponse.success(paginated_products, meta=meta)


@app.route('/api/v1/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Lấy product - consistent error handling"""
    product = next((p for p in products_db if p["id"] == product_id), None)

    if not product:
        return APIResponse.error(
            code="PRODUCT_NOT_FOUND",
            message=f"Product with ID {product_id} not found",
            status_code=404
        )

    return APIResponse.success(product)


# ============ EXTENSIBILITY: Optional Fields for Version Compatibility ============

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """API health check"""
    response = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
    return jsonify(response)


# ============ Error Handlers ============

@app.errorhandler(400)
def bad_request(error):
    return APIResponse.error(
        code="BAD_REQUEST",
        message="Bad request",
        status_code=400
    )


@app.errorhandler(404)
def not_found(error):
    return APIResponse.error(
        code="ENDPOINT_NOT_FOUND",
        message="Endpoint not found",
        status_code=404
    )


@app.errorhandler(500)
def server_error(error):
    return APIResponse.error(
        code="INTERNAL_SERVER_ERROR",
        message="Internal server error",
        status_code=500
    )


# ============ TESTING ============

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  Flow 1: Best Practices API Demo                           ║
    ║  Server running on http://localhost:5000                   ║
    ╚════════════════════════════════════════════════════════════╝

    🧪 Test endpoints:

    GET    http://localhost:5000/api/v1/users
    GET    http://localhost:5000/api/v1/users/1
    POST   http://localhost:5000/api/v1/users
    PUT    http://localhost:5000/api/v1/users/1
    DELETE http://localhost:5000/api/v1/users/1

    GET    http://localhost:5000/api/v1/products
    GET    http://localhost:5000/api/v1/products/1

    GET    http://localhost:5000/api/v1/health

    📍 Key Concepts Demonstrated:
    ✅ Consistency: All endpoints use same response format
    ✅ Clarity: Clear endpoint names and descriptions
    ✅ Extensibility: Versioning (/v1/) and pagination support
    """)

    app.run(debug=True, port=5000)
