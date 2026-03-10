"""
Flow 3: API Endpoints - Full CRUD Design with Proper HTTP Methods and Status Codes
Demo: Complete REST API implementation
"""

from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# ============ DATABASE MOCK ============
posts_db = [
    {
        "id": 1,
        "title": "Getting Started with REST APIs",
        "content": "Learn the basics of REST API design...",
        "author_id": 1,
        "status": "published",
        "created_at": "2024-01-01",
        "updated_at": "2024-01-01"
    },
    {
        "id": 2,
        "title": "API Best Practices",
        "content": "Best practices for designing scalable APIs...",
        "author_id": 1,
        "status": "draft",
        "created_at": "2024-01-02",
        "updated_at": "2024-01-02"
    },
]

comments_db = [
    {
        "id": 1,
        "post_id": 1,
        "author_id": 2,
        "content": "Great article!",
        "created_at": "2024-01-01",
        "updated_at": "2024-01-01"
    },
]

likes_db = [
    {"id": 1, "post_id": 1, "user_id": 2, "created_at": "2024-01-01"},
    {"id": 2, "post_id": 1, "user_id": 3, "created_at": "2024-01-01"},
]

authors_db = [
    {"id": 1, "name": "John Admin", "email": "john@blog.com"},
    {"id": 2, "name": "Jane Reader", "email": "jane@blog.com"},
    {"id": 3, "name": "Bob Developer", "email": "bob@blog.com"},
]


# ============ RESPONSE UTILITIES ============

def success(data=None, meta=None, status_code=200):
    """Standard success response"""
    response = {
        "status": "success",
        "data": data,
    }
    if meta:
        response["meta"] = meta
    return jsonify(response), status_code


def error(code, message, details=None, status_code=400):
    """Standard error response"""
    error_obj = {
        "code": code,
        "message": message,
    }
    if details:
        error_obj["details"] = details
    return jsonify({
        "status": "error",
        "error": error_obj
    }), status_code


# ============ POSTS - FULL CRUD ============

@app.route('/api/v1/posts', methods=['GET'])
def list_posts():
    """
    📖 READ (List) - GET /posts
    Returns: 200 OK with list of posts
    """
    # Filtering
    status = request.args.get('status')
    author_id = request.args.get('author-id', type=int)

    filtered = posts_db
    if status:
        filtered = [p for p in filtered if p['status'] == status]
    if author_id:
        filtered = [p for p in filtered if p['author_id'] == author_id]

    # Pagination
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    total = len(filtered)
    start = (page - 1) * limit
    end = start + limit

    meta = {
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }

    return success(filtered[start:end], meta=meta)


@app.route('/api/v1/posts', methods=['POST'])
def create_post():
    """
    📝 CREATE - POST /posts
    Returns: 201 Created with new post
    """
    data = request.get_json()

    # Validation
    errors = []
    if not data.get("title"):
        errors.append({"field": "title", "message": "Title is required"})
    if not data.get("content"):
        errors.append({"field": "content", "message": "Content is required"})
    if not data.get("author_id"):
        errors.append({"field": "author_id", "message": "Author ID is required"})

    if errors:
        return error(
            code="VALIDATION_ERROR",
            message="Validation failed",
            details=errors,
            status_code=422
        )

    # Check author exists
    author = next((a for a in authors_db if a["id"] == data["author_id"]), None)
    if not author:
        return error(
            code="AUTHOR_NOT_FOUND",
            message=f"Author with ID {data['author_id']} not found",
            status_code=404
        )

    # Create post
    new_post = {
        "id": max(p["id"] for p in posts_db) + 1,
        "title": data["title"],
        "content": data["content"],
        "author_id": data["author_id"],
        "status": data.get("status", "draft"),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    posts_db.append(new_post)

    # Return 201 Created
    return success(new_post, status_code=201)


@app.route('/api/v1/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """
    📖 READ (Single) - GET /posts/{id}
    Returns: 200 OK (if exists) or 404 Not Found
    """
    post = next((p for p in posts_db if p["id"] == post_id), None)

    if not post:
        return error(
            code="POST_NOT_FOUND",
            message=f"Post with ID {post_id} not found",
            status_code=404
        )

    return success(post)


@app.route('/api/v1/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    ✏️ UPDATE (Full) - PUT /posts/{id}
    Returns: 200 OK (updated resource) or 404 Not Found
    """
    post = next((p for p in posts_db if p["id"] == post_id), None)

    if not post:
        return error(
            code="POST_NOT_FOUND",
            message=f"Post with ID {post_id} not found",
            status_code=404
        )

    data = request.get_json()

    # Update all fields (or fail if missing)
    if "title" not in data:
        return error(
            code="VALIDATION_ERROR",
            message="Title is required for PUT",
            status_code=422
        )

    post["title"] = data["title"]
    post["content"] = data.get("content", post["content"])
    post["status"] = data.get("status", post["status"])
    post["updated_at"] = datetime.now().isoformat()

    return success(post)


@app.route('/api/v1/posts/<int:post_id>', methods=['PATCH'])
def partial_update_post(post_id):
    """
    ✏️ UPDATE (Partial) - PATCH /posts/{id}
    Returns: 200 OK (updated resource) or 404 Not Found
    """
    post = next((p for p in posts_db if p["id"] == post_id), None)

    if not post:
        return error(
            code="POST_NOT_FOUND",
            message=f"Post with ID {post_id} not found",
            status_code=404
        )

    data = request.get_json()

    # Update only provided fields
    if "title" in data:
        post["title"] = data["title"]
    if "content" in data:
        post["content"] = data["content"]
    if "status" in data:
        post["status"] = data["status"]

    post["updated_at"] = datetime.now().isoformat()

    return success(post)


@app.route('/api/v1/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    🗑️ DELETE - DELETE /posts/{id}
    Returns: 204 No Content (on success) or 404 Not Found
    """
    global posts_db

    post = next((p for p in posts_db if p["id"] == post_id), None)

    if not post:
        return error(
            code="POST_NOT_FOUND",
            message=f"Post with ID {post_id} not found",
            status_code=404
        )

    posts_db = [p for p in posts_db if p["id"] != post_id]

    # Return 204 No Content
    return '', 204


# ============ NESTED RESOURCES: Comments ============

@app.route('/api/v1/posts/<int:post_id>/comments', methods=['GET'])
def list_post_comments(post_id):
    """
    📖 READ (List) Nested - GET /posts/{id}/comments
    """
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post:
        return error(
            code="POST_NOT_FOUND",
            message=f"Post with ID {post_id} not found",
            status_code=404
        )

    post_comments = [c for c in comments_db if c["post_id"] == post_id]

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    total = len(post_comments)
    start = (page - 1) * limit
    end = start + limit

    meta = {"total": total, "page": page, "limit": limit}

    return success(post_comments[start:end], meta=meta)


@app.route('/api/v1/posts/<int:post_id>/comments', methods=['POST'])
def create_post_comment(post_id):
    """
    📝 CREATE Nested - POST /posts/{id}/comments
    Returns: 201 Created with new comment
    """
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post:
        return error(
            code="POST_NOT_FOUND",
            message=f"Post with ID {post_id} not found",
            status_code=404
        )

    data = request.get_json()

    # Validation
    if not data.get("content"):
        return error(
            code="VALIDATION_ERROR",
            message="Content is required",
            status_code=422
        )

    if not data.get("author_id"):
        return error(
            code="VALIDATION_ERROR",
            message="Author ID is required",
            status_code=422
        )

    new_comment = {
        "id": max(c["id"] for c in comments_db) + 1 if comments_db else 1,
        "post_id": post_id,
        "author_id": data["author_id"],
        "content": data["content"],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    comments_db.append(new_comment)

    return success(new_comment, status_code=201)


@app.route('/api/v1/posts/<int:post_id>/comments/<int:comment_id>', methods=['GET'])
def get_post_comment(post_id, comment_id):
    """
    📖 READ (Single) Nested - GET /posts/{id}/comments/{comment_id}
    """
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post:
        return error(
            code="POST_NOT_FOUND",
            message=f"Post with ID {post_id} not found",
            status_code=404
        )

    comment = next(
        (c for c in comments_db if c["id"] == comment_id and c["post_id"] == post_id),
        None
    )

    if not comment:
        return error(
            code="COMMENT_NOT_FOUND",
            message=f"Comment with ID {comment_id} not found",
            status_code=404
        )

    return success(comment)


@app.route('/api/v1/posts/<int:post_id>/comments/<int:comment_id>', methods=['DELETE'])
def delete_post_comment(post_id, comment_id):
    """
    🗑️ DELETE Nested - DELETE /posts/{id}/comments/{comment_id}
    Returns: 204 No Content
    """
    global comments_db

    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post:
        return error(
            code="POST_NOT_FOUND",
            message=f"Post with ID {post_id} not found",
            status_code=404
        )

    comment = next(
        (c for c in comments_db if c["id"] == comment_id and c["post_id"] == post_id),
        None
    )

    if not comment:
        return error(
            code="COMMENT_NOT_FOUND",
            message=f"Comment with ID {comment_id} not found",
            status_code=404
        )

    comments_db = [c for c in comments_db if not (c["id"] == comment_id and c["post_id"] == post_id)]

    return '', 204


# ============ ACTIONS ============

@app.route('/api/v1/posts/<int:post_id>/publish', methods=['POST'])
def publish_post(post_id):
    """
    ✅ ACTION - POST /posts/{id}/publish
    For non-CRUD actions, use POST with action name
    """
    post = next((p for p in posts_db if p["id"] == post_id), None)

    if not post:
        return error(
            code="POST_NOT_FOUND",
            message=f"Post with ID {post_id} not found",
            status_code=404
        )

    if post["status"] == "published":
        return error(
            code="INVALID_STATE",
            message="Post is already published",
            status_code=409
        )

    post["status"] = "published"
    post["updated_at"] = datetime.now().isoformat()

    return success(post)


@app.route('/api/v1/posts/<int:post_id>/unpublish', methods=['POST'])
def unpublish_post(post_id):
    """ACTION - POST /posts/{id}/unpublish"""
    post = next((p for p in posts_db if p["id"] == post_id), None)

    if not post:
        return error(
            code="POST_NOT_FOUND",
            message=f"Post with ID {post_id} not found",
            status_code=404
        )

    post["status"] = "draft"
    post["updated_at"] = datetime.now().isoformat()

    return success(post)


# ============ LIKES ============

@app.route('/api/v1/posts/<int:post_id>/likes', methods=['GET'])
def get_post_likes(post_id):
    """GET likes for a post (with count)"""
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post:
        return error(
            code="POST_NOT_FOUND",
            message=f"Post with ID {post_id} not found",
            status_code=404
        )

    post_likes = [l for l in likes_db if l["post_id"] == post_id]

    return success({
        "count": len(post_likes),
        "likes": post_likes
    })


@app.route('/api/v1/posts/<int:post_id>/likes', methods=['POST'])
def like_post(post_id):
    """Like a post"""
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post:
        return error(
            code="POST_NOT_FOUND",
            message=f"Post with ID {post_id} not found",
            status_code=404
        )

    data = request.get_json()
    user_id = data.get("user_id")

    # Check if already liked
    existing_like = next(
        (l for l in likes_db if l["post_id"] == post_id and l["user_id"] == user_id),
        None
    )

    if existing_like:
        return error(
            code="ALREADY_LIKED",
            message="User already liked this post",
            status_code=409
        )

    new_like = {
        "id": max(l["id"] for l in likes_db) + 1 if likes_db else 1,
        "post_id": post_id,
        "user_id": user_id,
        "created_at": datetime.now().isoformat()
    }
    likes_db.append(new_like)

    return success(new_like, status_code=201)


@app.route('/api/v1/posts/<int:post_id>/likes', methods=['DELETE'])
def unlike_post(post_id):
    """Unlike a post"""
    global likes_db

    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post:
        return error(
            code="POST_NOT_FOUND",
            message=f"Post with ID {post_id} not found",
            status_code=404
        )

    data = request.get_json()
    user_id = data.get("user_id")

    like = next(
        (l for l in likes_db if l["post_id"] == post_id and l["user_id"] == user_id),
        None
    )

    if not like:
        return error(
            code="LIKE_NOT_FOUND",
            message="User hasn't liked this post",
            status_code=404
        )

    likes_db = [l for l in likes_db if not (l["post_id"] == post_id and l["user_id"] == user_id)]

    return '', 204


# ============ STATUS CODE REFERENCE ============

@app.route('/api/v1/status-codes-reference', methods=['GET'])
def status_codes_reference():
    """Reference for HTTP status codes"""
    reference = {
        "2xx_Success": {
            "200": "OK - Request succeeded with response body",
            "201": "Created - Resource created successfully",
            "204": "No Content - Request succeeded, no response body (DELETE)"
        },
        "4xx_Client_Error": {
            "400": "Bad Request - Invalid request format",
            "401": "Unauthorized - Not authenticated",
            "403": "Forbidden - Authenticated but not authorized",
            "404": "Not Found - Resource not found",
            "409": "Conflict - Conflict (e.g., duplicate resource)",
            "422": "Unprocessable Entity - Validation error"
        },
        "5xx_Server_Error": {
            "500": "Internal Server Error - Server error",
            "503": "Service Unavailable - Server unavailable"
        }
    }
    return jsonify(reference)


# ============ TESTING ============

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  Flow 3: API Endpoints - Full CRUD Demo                    ║
    ║  Server running on http://localhost:5002                   ║
    ╚════════════════════════════════════════════════════════════╝

    🧪 Test endpoints:

    CREATE (POST):
    POST   http://localhost:5002/api/v1/posts
    Body: {"title": "...", "content": "...", "author_id": 1}
    Response: 201 Created ✅

    READ (GET):
    GET    http://localhost:5002/api/v1/posts
    GET    http://localhost:5002/api/v1/posts/1
    Response: 200 OK ✅

    UPDATE (PUT - Full):
    PUT    http://localhost:5002/api/v1/posts/1
    Body: {"title": "Updated", "content": "..."}
    Response: 200 OK ✅

    UPDATE (PATCH - Partial):
    PATCH  http://localhost:5002/api/v1/posts/1
    Body: {"title": "New Title"}
    Response: 200 OK ✅

    DELETE:
    DELETE http://localhost:5002/api/v1/posts/1
    Response: 204 No Content ✅

    NESTED RESOURCES:
    GET    http://localhost:5002/api/v1/posts/1/comments
    POST   http://localhost:5002/api/v1/posts/1/comments
    GET    http://localhost:5002/api/v1/posts/1/comments/1
    DELETE http://localhost:5002/api/v1/posts/1/comments/1

    ACTIONS (Non-CRUD):
    POST   http://localhost:5002/api/v1/posts/1/publish
    POST   http://localhost:5002/api/v1/posts/1/unpublish

    LIKES:
    GET    http://localhost:5002/api/v1/posts/1/likes
    POST   http://localhost:5002/api/v1/posts/1/likes
    DELETE http://localhost:5002/api/v1/posts/1/likes

    📍 Key Concepts Demonstrated:
    ✅ CRUD: Create (POST), Read (GET), Update (PUT/PATCH), Delete (DELETE)
    ✅ Status Codes: 201, 200, 204, 400, 404, 409, 422
    ✅ Nested Resources: /posts/{id}/comments
    ✅ Actions: /posts/{id}/publish
    ✅ Pagination: ?page=1&limit=10
    ✅ Filtering: ?status=published&author-id=1
    ✅ Error Handling: Consistent error format
    """)

    app.run(debug=True, port=5002)
