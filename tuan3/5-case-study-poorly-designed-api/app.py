"""
Flow 5: Case Study - Poorly Designed API
Demo: Real-world example of API design anti-patterns
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# ============ DATABASE MOCK ============
products_db = [
    {"prod_id": 1, "prod_name": "Laptop", "price": 1000},
    {"prod_id": 2, "prod_name": "Mouse", "price": 25},
]

orders_db = [
    {"OrderID": "ORD001", "prod_id": 1, "quantity": 1, "total": 1000},
    {"OrderID": "ORD002", "prod_id": 2, "quantity": 2, "total": 50},
]


# ============ ISSUE 1 & 2: Verb-based, Inconsistent Response Format ============

# ❌ BAD: Verb-based endpoint, inconsistent response
@app.route('/api/getallproducts', methods=['GET'])
def getallproducts():
    """
    ❌ ISSUES:
    - Verb in URL (getallproducts)
    - No versioning
    - Bad practice endpoint name
    """
    return jsonify({
        "code": 200,
        "response": products_db
    })


# ❌ BAD: getproduct - inconsistent
@app.route('/api/getproduct', methods=['GET'])
def getproduct():
    """
    ❌ ISSUES:
    - Verb-based (getproduct)
    - Uses query param for ID (inconsistent with pagination)
    - Response format different from getallproducts
    """
    prod_id = request.args.get('prod_id')
    product = next((p for p in products_db if p['prod_id'] == int(prod_id)), None)

    if not product:
        return jsonify({
            "error": "Product not found"  # ❌ Different error format!
        }), 404

    return jsonify({
        "status": "ok",  # ❌ Different status field!
        "data": product
    })


# ============ ISSUE 3: Wrong HTTP Methods ============

# ❌ BAD: GET for logout (should be POST)
@app.route('/api/logout', methods=['GET'])
def logout():
    """
    ❌ ISSUE: GET for logout
    - Logout modifies state (should be POST/DELETE)
    - CSRF vulnerability
    - Cached logout is dangerous
    """
    return jsonify({"message": "Logged out"})


# ❌ BAD: POST for searching (GET is more appropriate)
@app.route('/api/searchItems', methods=['POST'])
def searchItems():
    """
    ❌ ISSUE: POST for search (should be GET)
    - Search is a query operation (use GET)
    - Query parameters more appropriate
    """
    keyword = request.form.get('keyword')
    results = [p for p in products_db if keyword.lower() in p['prod_name'].lower()]
    return jsonify({"items": results})


# ============ ISSUE 4: Inconsistent Parameter Names ============

# ❌ BAD: Different parameter names
@app.route('/api/getOrder', methods=['GET'])
def getOrder():
    """
    ❌ ISSUES:
    - Different parameter name: OrderID (not orderid or order_id)
    - Verb-based endpoint
    - No versioning
    """
    order_id = request.args.get('OrderID')  # ❌ Mixed case parameter!
    order = next((o for o in orders_db if o['OrderID'] == order_id), None)

    if not order:
        return jsonify({"message": "Not found"})  # ❌ Inconsistent error!

    return jsonify(order)


@app.route('/api/cancelorder', methods=['POST'])
def cancelorder():
    """
    ❌ ISSUES:
    - Verb in URL with action (cancelorder)
    - Query parameter for ID
    - Should be DELETE /api/orders/{id}
    - Parameter name inconsistency: orderid (different from OrderID)
    """
    order_id = request.args.get('orderid')  # ❌ lowercase, but getOrder uses OrderID!

    order = next((o for o in orders_db if o['OrderID'] == order_id), None)

    if not order:
        return jsonify({"success": False})  # ❌ Different error format!

    # Cancel order
    orders_db.remove(order)

    return jsonify({"success": True})


# ============ ISSUE 5: No versioning, ISSUE 6: No Pagination ============

# ❌ BAD: Returns all products
@app.route('/api/products', methods=['GET'])
def products():
    """
    ❌ ISSUES:
    - No versioning
    - Returns ALL products (no pagination)
    - With 1 million products, it's extremely slow
    """
    return jsonify(products_db)


# ============ ISSUE 7: No Filtering/Sorting ============

# ❌ BAD: Limited end (no filtering, sorting, searching)
@app.route('/api/Admin/Reports', methods=['GET'])
def admin_reports():
    """
    ❌ ISSUES:
    - Inconsistent casing (Admin)
    - No filtering/sorting
    - Probably should be protected (no auth check visible)
    - Verb in description, not clear what this returns
    """
    return jsonify({
        "all_products": products_db,
        "all_orders": orders_db
    })


# ============ ISSUE 8: Inconsistent Status Codes ============

# ❌ BAD: All endpoints return 200 or 500
@app.route('/api/createProduct', methods=['POST'])
def createProduct():
    """
    ❌ ISSUES:
    - Verb in URL (createProduct)
    - Uses POST (correct, but inconsistent with other endpoints)
    - Returns 200 for success (should be 201)
    - CamelCase endpoint
    """
    data = request.get_json()

    if not data.get('name'):
        return jsonify({"error": "Missing name"}), 200  # ❌ Should be 400!

    new_product = {
        "prod_id": max(p['prod_id'] for p in products_db) + 1,
        "prod_name": data['name'],
        "price": data.get('price', 0)
    }

    products_db.append(new_product)

    # ❌ Should return 201, not 200
    return jsonify(new_product), 200


# ============ ISSUE 9: No Response Format Standard ============

# ❌ BAD: User endpoint with different format
@app.route('/api/user/profile', methods=['GET'])
def user_profile():
    """
    ❌ ISSUES:
    - Different response format from products
    - Mixed singular/plural (user/users)
    - No versioning
    """
    return jsonify({
        "id": 1,
        "name": "John",
        "email": "john@example.com"
        # ❌ No 'status' field like other endpoints
    })


@app.route('/api/user/update', methods=['POST'])
def user_update():
    """
    ❌ ISSUES:
    - Uses POST for update (should be PUT/PATCH)
    - Verb in URL (update)
    - Different error format
    """
    data = request.get_json()

    if not data.get('id'):
        return jsonify({
            "error_code": "MISSING_ID",
            "message": "ID is required"
        }), 400

    # Update user
    return jsonify({
        "success": True,
        "modified": 1
    })


# ============ SUMMARY: Issues Found ============

@app.route('/api/issues-summary', methods=['GET'])
def issues_summary():
    """Summary of all issues in this poorly designed API"""
    issues = [
        {
            "priority": "CRITICAL",
            "issue": "Verb-based endpoints",
            "examples": [
                "/api/getallproducts",
                "/api/getproduct",
                "/api/getOrder",
                "/api/cancelorder",
                "/api/createProduct"
            ],
            "fix": "Use resource-based: /api/v1/products, /api/v1/orders, etc"
        },
        {
            "priority": "CRITICAL",
            "issue": "Inconsistent response format",
            "examples": [
                "getallproducts: {code, response}",
                "getproduct: {status, data}",
                "user_profile: {id, name, email}"
            ],
            "fix": "Standardize to: {status, data, meta}"
        },
        {
            "priority": "CRITICAL",
            "issue": "Wrong HTTP methods",
            "examples": [
                "GET /logout (should be DELETE or POST)",
                "POST /searchItems (should be GET)",
                "POST /user/update (should be PUT/PATCH)"
            ],
            "fix": "Use correct methods: GET for query, POST for create, PUT/PATCH for update, DELETE for delete"
        },
        {
            "priority": "HIGH",
            "issue": "Inconsistent parameter naming",
            "examples": [
                "prod_id vs OrderID vs orderid",
                "Mixed case: OrderID vs orderid"
            ],
            "fix": "Use consistent lowercase with hyphens or underscores"
        },
        {
            "priority": "HIGH",
            "issue": "No API versioning",
            "examples": [
                "All endpoints are /api/* without /v1/, /v2/"
            ],
            "fix": "Add versioning: /api/v1/, /api/v2/"
        },
        {
            "priority": "HIGH",
            "issue": "No pagination support",
            "examples": [
                "/api/getallproducts returns all products",
                "No page/limit parameters"
            ],
            "fix": "Add pagination: ?page=1&limit=10 with metadata"
        },
        {
            "priority": "MEDIUM",
            "issue": "No filtering/sorting",
            "examples": [
                "Can't filter by status",
                "Can't sort by price",
                "Limited search capability"
            ],
            "fix": "Add: ?filter=, ?sort-by=, ?order="
        },
        {
            "priority": "CRITICAL",
            "issue": "Incorrect status codes",
            "examples": [
                "createProduct returns 200 for success (should be 201)",
                "Missing validation errors (should be 422)",
                "Missing proper 404 handling"
            ],
            "fix": "Use: 201 Created, 204 No Content, 400 Bad Request, 422 Validation Error, 404 Not Found"
        },
        {
            "priority": "HIGH",
            "issue": "No nested resources",
            "examples": [
                "No /api/users/{id}/orders",
                "Flat structure makes relationships unclear"
            ],
            "fix": "Design nested resources: /resources/{id}/sub-resources"
        },
        {
            "priority": "HIGH",
            "issue": "Security issues",
            "examples": [
                "GET /logout (CSRF vulnerable)",
                "No auth checking visible",
                "Admin endpoint not protected"
            ],
            "fix": "Use POST/DELETE for state changes, add auth headers, secure endpoints"
        }
    ]

    return jsonify({
        "status": "success",
        "data": {
            "total_issues": len(issues),
            "critical": sum(1 for i in issues if i['priority'] == 'CRITICAL'),
            "high": sum(1 for i in issues if i['priority'] == 'HIGH'),
            "medium": sum(1 for i in issues if i['priority'] == 'MEDIUM'),
            "issues": issues
        }
    })


@app.route('/api/refactored-comparison', methods=['GET'])
def refactored_comparison():
    """Show how to refactor this API"""
    comparison = {
        "before_after": [
            {
                "bad": "GET /api/getallproducts",
                "good": "GET /api/v1/products"
            },
            {
                "bad": "GET /api/getproduct?prod_id=1",
                "good": "GET /api/v1/products/1"
            },
            {
                "bad": "GET /api/logout",
                "good": "POST /api/v1/auth/logout"
            },
            {
                "bad": "POST /api/searchItems",
                "good": "GET /api/v1/products?search=keyword"
            },
            {
                "bad": "GET /api/getOrder?OrderID=ORD001",
                "good": "GET /api/v1/orders/1"
            },
            {
                "bad": "POST /api/cancelorder?orderid=ORD001",
                "good": "DELETE /api/v1/orders/1"
            },
            {
                "bad": "GET /api/products (no pagination)",
                "good": "GET /api/v1/products?page=1&limit=10"
            },
            {
                "bad": "POST /api/createProduct returns 200",
                "good": "POST /api/v1/products returns 201 Created"
            },
            {
                "bad": "POST /api/user/update",
                "good": "PUT /api/v1/users/{id} or PATCH /api/v1/users/{id}"
            },
            {
                "bad": "Different response formats",
                "good": "{status, data, meta} everywhere"
            }
        ]
    }

    return jsonify({
        "status": "success",
        "data": comparison
    })


# ============ TESTING ============

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  Flow 5: Case Study - Poorly Designed API                  ║
    ║  Server running on http://localhost:5004                   ║
    ╚════════════════════════════════════════════════════════════╝

    🧪 Test endpoints:

    Poorly designed endpoints:
    GET    http://localhost:5004/api/getallproducts
    GET    http://localhost:5004/api/getproduct?prod_id=1
    GET    http://localhost:5004/api/logout
    GET    http://localhost:5004/api/getOrder?OrderID=ORD001
    POST   http://localhost:5004/api/cancelorder?orderid=ORD001
    POST   http://localhost:5004/api/createProduct
    GET    http://localhost:5004/api/products
    GET    http://localhost:5004/api/user/profile

    Analysis:
    GET    http://localhost:5004/api/issues-summary
    GET    http://localhost:5004/api/refactored-comparison

    📍 Issues Demonstrated:
    ❌ Verb-based endpoints (getall, get, cancel, create)
    ❌ Inconsistent response formats (code/response vs status/data)
    ❌ Wrong HTTP methods (GET for logout, POST for search)
    ❌ Inconsistent parameter naming (prod_id vs OrderID vs orderid)
    ❌ No API versioning
    ❌ No pagination (returns all data)
    ❌ No filtering/sorting
    ❌ Wrong status codes (200 instead of 201)
    ❌ No nested resources
    ❌ Security issues (GET logout has CSRF vulnerability)

    💡 Total Issues Found: 10
    ⚠️  Estimated Score: ~40/100 (POOR)
    """)

    app.run(debug=True, port=5004)
