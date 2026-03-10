"""
Flow 2: Naming Conventions - Proper Endpoint and Parameter Naming
Demo: Demonstrating correct vs incorrect naming conventions
"""

from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# ============ DATABASE MOCK ============
user_profiles_db = [
    {
        "id": 1,
        "user_name": "john_doe",
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": None,
        "created_at": "2024-01-01"
    },
    {
        "id": 2,
        "user_name": "jane_smith",
        "full_name": "Jane Smith",
        "email": "jane@example.com",
        "phone": None,
        "created_at": "2024-01-02"
    },
]

orders_db = [
    {
        "id": 1,
        "user_id": 1,
        "product_name": "Laptop",
        "quantity": 1,
        "total_price": 1000,
        "status": "delivered",
        "created_at": "2024-01-10"
    },
    {
        "id": 2,
        "user_id": 1,
        "product_name": "Mouse",
        "quantity": 2,
        "total_price": 50,
        "status": "pending",
        "created_at": "2024-01-15"
    },
]

payment_methods_db = [
    {"id": 1, "user_id": 1, "type": "credit_card", "last_four": "4242"},
    {"id": 2, "user_id": 2, "type": "debit_card", "last_four": "5555"},
]


# ============ RESPONSE FORMAT ============

def success_response(data, meta=None, status_code=200):
    """Standard response format"""
    response = {
        "status": "success",
        "data": data,
    }
    if meta:
        response["meta"] = meta
    return jsonify(response), status_code


def error_response(code, message, status_code=400):
    """Standard error format"""
    return jsonify({
        "status": "error",
        "error": {
            "code": code,
            "message": message,
        }
    }), status_code


# ============ GOOD: Proper Naming Conventions ============

# ✅ GOOD: Plural nouns, lowercase, versioning
# ✅ GOOD: Multi-word resources use hyphens, not underscores
# ✅ GOOD: Query parameters use hyphens and are descriptive

@app.route('/api/v1/user-profiles', methods=['GET'])
def list_user_profiles():
    """
    List all user profiles

    Query parameters:
      - page: int (default=1)
      - limit: int (default=10)
      - sort-by: str (field name, default="id")
      - order: str ("asc" or "desc", default="asc")
      - search: str (search by full_name or email)
      - status: str (filter by status)
    """

    # ✅ GOOD: Query parameters use lowercase and hyphens
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    sort_by = request.args.get('sort-by', 'id')
    order = request.args.get('order', 'asc')
    search = request.args.get('search', '')

    # Filter
    filtered = user_profiles_db
    if search:
        filtered = [
            u for u in filtered
            if search.lower() in u['full_name'].lower() or search.lower() in u['email'].lower()
        ]

    # Sort
    reverse = order.lower() == 'desc'
    filtered = sorted(filtered, key=lambda x: x.get(sort_by, ''), reverse=reverse)

    # Paginate
    total = len(filtered)
    start = (page - 1) * limit
    end = start + limit

    paginated = filtered[start:end]

    meta = {
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }

    return success_response(paginated, meta=meta)


@app.route('/api/v1/user-profiles/<int:profile_id>', methods=['GET'])
def get_user_profile(profile_id):
    """
    Get specific user profile by ID
    ✅ GOOD: ID in URL path, not query parameter
    """
    profile = next((u for u in user_profiles_db if u["id"] == profile_id), None)

    if not profile:
        return error_response(
            code="USER_PROFILE_NOT_FOUND",
            message=f"User profile with ID {profile_id} not found",
            status_code=404
        )

    return success_response(profile)


@app.route('/api/v1/user-profiles', methods=['POST'])
def create_user_profile():
    """Create new user profile"""
    data = request.get_json()

    # Validation
    errors = []
    if not data.get("user_name"):
        errors.append({"field": "user_name", "message": "Username is required"})
    if not data.get("full_name"):
        errors.append({"field": "full_name", "message": "Full name is required"})
    if not data.get("email"):
        errors.append({"field": "email", "message": "Email is required"})

    if errors:
        return error_response(
            code="VALIDATION_ERROR",
            message="Validation failed",
            status_code=422
        )

    new_profile = {
        "id": max(u["id"] for u in user_profiles_db) + 1,
        "user_name": data["user_name"],
        "full_name": data["full_name"],
        "email": data["email"],
        "phone": data.get("phone"),
        "created_at": datetime.now().isoformat()
    }
    user_profiles_db.append(new_profile)

    return success_response(new_profile, status_code=201)


# ============ NESTED RESOURCES ============

@app.route('/api/v1/user-profiles/<int:profile_id>/orders', methods=['GET'])
def list_user_orders(profile_id):
    """
    List orders for a specific user
    ✅ GOOD: Nested resource pattern /users/{id}/orders
    """
    profile = next((u for u in user_profiles_db if u["id"] == profile_id), None)
    if not profile:
        return error_response(
            code="USER_PROFILE_NOT_FOUND",
            message=f"User profile with ID {profile_id} not found",
            status_code=404
        )

    # ✅ GOOD: Support filtering by status
    status = request.args.get('status')

    user_orders = [o for o in orders_db if o["user_id"] == profile_id]

    if status:
        user_orders = [o for o in user_orders if o["status"] == status]

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    total = len(user_orders)
    start = (page - 1) * limit
    end = start + limit

    meta = {
        "total": total,
        "page": page,
        "limit": limit,
    }

    return success_response(user_orders[start:end], meta=meta)


@app.route('/api/v1/user-profiles/<int:profile_id>/orders/<int:order_id>', methods=['GET'])
def get_user_order(profile_id, order_id):
    """
    Get specific order of a user
    ✅ GOOD: Both parent and child ID in path
    """
    profile = next((u for u in user_profiles_db if u["id"] == profile_id), None)
    if not profile:
        return error_response(
            code="USER_PROFILE_NOT_FOUND",
            message=f"User profile with ID {profile_id} not found",
            status_code=404
        )

    order = next((o for o in orders_db if o["id"] == order_id and o["user_id"] == profile_id), None)
    if not order:
        return error_response(
            code="ORDER_NOT_FOUND",
            message=f"Order with ID {order_id} not found",
            status_code=404
        )

    return success_response(order)


@app.route('/api/v1/user-profiles/<int:profile_id>/payment-methods', methods=['GET'])
def list_payment_methods(profile_id):
    """
    ✅ GOOD: Resource name uses hyphens (payment-methods)
    ✅ GOOD: Consistent naming pattern for multi-word resources
    """
    profile = next((u for u in user_profiles_db if u["id"] == profile_id), None)
    if not profile:
        return error_response(
            code="USER_PROFILE_NOT_FOUND",
            message=f"User profile with ID {profile_id} not found",
            status_code=404
        )

    methods = [m for m in payment_methods_db if m["user_id"] == profile_id]

    return success_response(methods)


# ============ ACTIONS (When verb is needed) ============

@app.route('/api/v1/user-profiles/<int:profile_id>/verify-email', methods=['POST'])
def verify_email(profile_id):
    """
    ✅ GOOD: When action is needed, use lowercase-hyphenated-action after resource
    NOT: /api/v1/user-profiles/verify-email/{id}
    """
    profile = next((u for u in user_profiles_db if u["id"] == profile_id), None)
    if not profile:
        return error_response(
            code="USER_PROFILE_NOT_FOUND",
            message=f"User profile with ID {profile_id} not found",
            status_code=404
        )

    # Simulate email verification
    profile["email_verified"] = True

    return success_response({"message": "Email verified successfully"})


@app.route('/api/v1/user-profiles/<int:profile_id>/reset-password', methods=['POST'])
def reset_password(profile_id):
    """
    ✅ GOOD: Action endpoint with lowercase and hyphens
    """
    profile = next((u for u in user_profiles_db if u["id"] == profile_id), None)
    if not profile:
        return error_response(
            code="USER_PROFILE_NOT_FOUND",
            message=f"User profile with ID {profile_id} not found",
            status_code=404
        )

    return success_response({
        "message": "Password reset link sent to email",
        "email": profile["email"]
    })


# ============ COMPARISON: BAD NAMING ============

# ❌ BAD Examples (Do NOT use these):
# @app.route('/api/getUserProfile')              # ❌ CamelCase, no versioning
# @app.route('/api/get_user_profile')            # ❌ Underscores, no versioning
# @app.route('/api/getuserprofile')              # ❌ No version, hard to read
# @app.route('/api/User-Profiles')               # ❌ Capital letters
# @app.route('/api/v1/UserProfiles')             # ❌ PascalCase
# @app.route('/api/v1/user_profiles')            # ❌ Underscores instead of hyphens
# @app.route('/api/v1/users/123?action=update')  # ❌ Action in query param
# @app.route('/api/v1/getUserOrders/123')        # ❌ Verb in URL
# @app.route('/api/v1/userProfiles/123/UserOrders')  # ❌ Inconsistent casing


# ============ VERSIONING ============

@app.route('/api/v1/healthcheck', methods=['GET'])
def health_check_v1():
    """Version 1 health check - has minimal info"""
    return success_response({
        "status": "healthy",
        "version": "1.0.0"
    })


# Future version (for backward compatibility)
# @app.route('/api/v2/health-check', methods=['GET'])
# def health_check_v2():
#     """Version 2 health check - has more info"""
#     return success_response({
#         "status": "healthy",
#         "version": "2.0.0",
#         "timestamp": datetime.now().isoformat(),
#         "database": "connected",
#         "uptime": "..."
#     })


# ============ TESTING ============

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  Flow 2: Naming Conventions Demo                           ║
    ║  Server running on http://localhost:5001                   ║
    ╚════════════════════════════════════════════════════════════╝

    🧪 Test endpoints:

    ✅ GOOD Naming Examples:
    GET    http://localhost:5001/api/v1/user-profiles
    GET    http://localhost:5001/api/v1/user-profiles/1
    POST   http://localhost:5001/api/v1/user-profiles

    Query with hyphens (lowercase):
    GET    http://localhost:5001/api/v1/user-profiles?sort-by=full_name&order=desc
    GET    http://localhost:5001/api/v1/user-profiles?search=john&limit=5

    Nested resources:
    GET    http://localhost:5001/api/v1/user-profiles/1/orders
    GET    http://localhost:5001/api/v1/user-profiles/1/orders/1
    GET    http://localhost:5001/api/v1/user-profiles/1/payment-methods

    Actions (with hyphens):
    POST   http://localhost:5001/api/v1/user-profiles/1/verify-email
    POST   http://localhost:5001/api/v1/user-profiles/1/reset-password

    📍 Key Naming Rules Demonstrated:
    ✅ Plural nouns: /user-profiles (not /user-profile)
    ✅ Lowercase: /api/v1/ (not /API/V1/)
    ✅ Hyphens for multi-word: /user-profiles (not /user_profiles)
    ✅ Versioning: /v1/ (allows v2 in future)
    ✅ Query params with hyphens: ?sort-by=, ?search=
    ✅ Nested resources: /users/{id}/orders
    ✅ Actions: /resource/{id}/action-name
    """)

    app.run(debug=True, port=5001)
