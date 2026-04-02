"""Flask backend for Week 6: Authentication and Authorization."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Any, Callable
from uuid import uuid4

import jwt
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


ACCESS_TOKEN_EXPIRES_MINUTES = _env_int("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", 15)
REFRESH_TOKEN_EXPIRES_DAYS = _env_int("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 7)
ACCESS_SECRET = os.getenv("JWT_SECRET_KEY", "dev-access-secret")
REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET_KEY", "dev-refresh-secret")

OAUTH_CLIENT_ID = os.getenv("OAUTH_CLIENT_ID", "demo-client")
OAUTH_CLIENT_SECRET = os.getenv("OAUTH_CLIENT_SECRET", "demo-secret")


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _hash_password(raw_password: str) -> str:
    return generate_password_hash(raw_password)


def _verify_password(raw_password: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, raw_password)


def _create_token(
    *,
    user: dict[str, Any],
    secret: str,
    expires_delta: timedelta,
    token_type: str,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    now = _utcnow()
    payload: dict[str, Any] = {
        "jti": str(uuid4()),
        "sub": user["id"],
        "name": user["name"],
        "role": user["role"],
        "scopes": user["scopes"],
        "typ": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, secret, algorithm="HS256")


def _decode_token(token: str, *, token_type: str) -> dict[str, Any]:
    secret = ACCESS_SECRET if token_type == "access" else REFRESH_SECRET
    payload = jwt.decode(token, secret, algorithms=["HS256"])
    if payload.get("typ") != token_type:
        raise jwt.InvalidTokenError("Invalid token type")
    return payload


def _make_public_user(user: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "scopes": user["scopes"],
    }


app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
CORS(app)


_users: list[dict[str, Any]] = [
    {
        "id": "usr_001",
        "name": "Nguyen Van An",
        "email": "admin@example.com",
        "password_hash": _hash_password("admin123"),
        "role": "admin",
        "scopes": ["read:books", "write:books", "delete:books"],
    },
    {
        "id": "usr_002",
        "name": "Tran Thi Bich",
        "email": "user@example.com",
        "password_hash": _hash_password("user123"),
        "role": "user",
        "scopes": ["read:books"],
    },
]

_refresh_tokens: dict[str, dict[str, Any]] = {}
_oauth_codes: dict[str, dict[str, Any]] = {}

_books: list[dict[str, Any]] = [
    {
        "id": 1,
        "title": "Clean Architecture",
        "author": "Robert C. Martin",
        "genre": "Professional",
        "publishedDate": "2017-09-20",
        "summary": "Principles of software architecture",
        "availableCopies": 3,
        "createdBy": "usr_001",
    },
    {
        "id": 2,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "genre": "Fantasy",
        "publishedDate": "1937-09-21",
        "summary": "The journey of Bilbo Baggins",
        "availableCopies": 5,
        "createdBy": "usr_001",
    },
]

_book_next_id = 3

_book_required_fields = [
    "title",
    "author",
    "genre",
    "publishedDate",
    "summary",
    "availableCopies",
]


def _find_user_by_email(email: str) -> dict[str, Any] | None:
    return next((user for user in _users if user["email"].lower() == email.lower()), None)


def _find_user_by_id(user_id: str) -> dict[str, Any] | None:
    return next((user for user in _users if user["id"] == user_id), None)


def _find_book(book_id: int) -> dict[str, Any] | None:
    return next((book for book in _books if book["id"] == book_id), None)


def _require_json_payload() -> dict[str, Any] | None:
    payload = request.get_json(silent=True)
    if payload is None:
        return None
    if not isinstance(payload, dict):
        return None
    return payload


def _extract_bearer_token() -> str | None:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    return auth_header[7:].strip() or None


def require_auth(view_func: Callable[..., Any]):
    @wraps(view_func)
    def wrapper(*args: Any, **kwargs: Any):
        token = _extract_bearer_token()
        if token is None:
            return (
                jsonify(
                    {
                        "error": "UNAUTHORIZED",
                        "message": 'Authentication required. Include "Authorization: Bearer <token>" header.',
                    }
                ),
                401,
            )

        try:
            payload = _decode_token(token, token_type="access")
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "TOKEN_EXPIRED", "message": "Access token has expired."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "INVALID_TOKEN", "message": "The provided token is invalid."}), 401

        user = _find_user_by_id(payload["sub"])
        if user is None:
            return jsonify({"error": "INVALID_TOKEN", "message": "User not found for this token."}), 401

        request.user = user  # type: ignore[attr-defined]
        request.token_payload = payload  # type: ignore[attr-defined]
        return view_func(*args, **kwargs)

    return wrapper


def require_roles(*allowed_roles: str):
    def decorator(view_func: Callable[..., Any]):
        @wraps(view_func)
        def wrapper(*args: Any, **kwargs: Any):
            user = getattr(request, "user", None)
            if user is None:
                return jsonify({"error": "UNAUTHORIZED", "message": "Authentication required."}), 401

            if user["role"] not in allowed_roles:
                return (
                    jsonify(
                        {
                            "error": "FORBIDDEN",
                            "message": "Insufficient permissions.",
                            "requiredRoles": list(allowed_roles),
                            "yourRole": user["role"],
                        }
                    ),
                    403,
                )

            return view_func(*args, **kwargs)

        return wrapper

    return decorator


def require_scopes(*required_scopes: str):
    def decorator(view_func: Callable[..., Any]):
        @wraps(view_func)
        def wrapper(*args: Any, **kwargs: Any):
            user = getattr(request, "user", None)
            if user is None:
                return jsonify({"error": "UNAUTHORIZED", "message": "Authentication required."}), 401

            user_scopes = set(user.get("scopes", []))
            missing = [scope for scope in required_scopes if scope not in user_scopes]
            if missing:
                return (
                    jsonify(
                        {
                            "error": "FORBIDDEN",
                            "message": "Missing required scope.",
                            "requiredScopes": list(required_scopes),
                            "missingScopes": missing,
                        }
                    ),
                    403,
                )

            return view_func(*args, **kwargs)

        return wrapper

    return decorator


def _validate_book_payload(payload: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    for field in _book_required_fields:
        if field not in payload:
            errors.append({"field": field, "message": "This field is required."})

    if "title" in payload and (not isinstance(payload["title"], str) or len(payload["title"].strip()) < 3):
        errors.append({"field": "title", "message": "Title must be at least 3 characters."})

    if "author" in payload and (not isinstance(payload["author"], str) or len(payload["author"].strip()) < 2):
        errors.append({"field": "author", "message": "Author must be at least 2 characters."})

    if "availableCopies" in payload:
        try:
            available_copies = int(payload["availableCopies"])
            if available_copies < 0:
                raise ValueError
        except (TypeError, ValueError):
            errors.append({"field": "availableCopies", "message": "availableCopies must be a non-negative integer."})

    return errors


@app.get("/")
def home():
    return jsonify(
        {
            "name": "Week 6 Flask API",
            "description": "Authentication and Authorization with JWT",
            "endpoints": {
                "login": "/auth/login",
                "refresh": "/auth/refresh",
                "logout": "/auth/logout",
                "me": "/auth/me",
                "oauth_authorize": "/oauth/authorize",
                "oauth_token": "/oauth/token",
                "books": "/books",
            },
            "testAccounts": [
                {"email": "admin@example.com", "password": "admin123", "role": "admin"},
                {"email": "user@example.com", "password": "user123", "role": "user"},
            ],
        }
    )


@app.get("/health")
def health():
    return jsonify({"status": "ok", "time": _utcnow().isoformat()})


@app.post("/auth/login")
def login():
    payload = _require_json_payload()
    if payload is None:
        return jsonify({"error": "INVALID_BODY", "message": "JSON body is required."}), 400

    email = payload.get("email")
    password = payload.get("password")
    if not isinstance(email, str) or not isinstance(password, str):
        return jsonify({"error": "INVALID_BODY", "message": "email and password are required."}), 400

    user = _find_user_by_email(email)
    if user is None or not _verify_password(password, user["password_hash"]):
        return jsonify({"error": "INVALID_CREDENTIALS", "message": "Email or password is incorrect."}), 401

    access_token = _create_token(
        user=user,
        secret=ACCESS_SECRET,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES),
        token_type="access",
    )
    refresh_token = _create_token(
        user=user,
        secret=REFRESH_SECRET,
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRES_DAYS),
        token_type="refresh",
    )

    refresh_payload = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=["HS256"])
    _refresh_tokens[refresh_payload["jti"]] = {
        "userId": user["id"],
        "tokenId": refresh_payload["jti"],
        "expiresAt": refresh_payload["exp"],
        "revoked": False,
    }

    return jsonify(
        {
            "tokenType": "Bearer",
            "accessToken": access_token,
            "expiresIn": ACCESS_TOKEN_EXPIRES_MINUTES * 60,
            "refreshToken": refresh_token,
            "user": _make_public_user(user),
        }
    )


@app.post("/auth/refresh")
def refresh_token():
    payload = _require_json_payload()
    if payload is None:
        return jsonify({"error": "INVALID_BODY", "message": "JSON body is required."}), 400

    token = payload.get("refreshToken")
    if not isinstance(token, str) or not token.strip():
        return jsonify({"error": "INVALID_BODY", "message": "refreshToken is required."}), 400

    try:
        refresh_payload = _decode_token(token, token_type="refresh")
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "TOKEN_EXPIRED", "message": "Refresh token has expired."}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "INVALID_TOKEN", "message": "The provided refresh token is invalid."}), 401

    token_record = _refresh_tokens.get(refresh_payload["jti"])
    if token_record is None or token_record["revoked"]:
        return jsonify({"error": "TOKEN_REVOKED", "message": "Refresh token is revoked or unknown."}), 401

    user = _find_user_by_id(refresh_payload["sub"])
    if user is None:
        return jsonify({"error": "INVALID_TOKEN", "message": "User not found for this token."}), 401

    access_token = _create_token(
        user=user,
        secret=ACCESS_SECRET,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES),
        token_type="access",
    )

    return jsonify(
        {
            "tokenType": "Bearer",
            "accessToken": access_token,
            "expiresIn": ACCESS_TOKEN_EXPIRES_MINUTES * 60,
        }
    )


@app.post("/oauth/authorize")
def oauth_authorize():
    payload = _require_json_payload()
    if payload is None:
        return jsonify({"error": "INVALID_BODY", "message": "JSON body is required."}), 400

    client_id = payload.get("client_id")
    email = payload.get("email")
    password = payload.get("password")
    scope = payload.get("scope", "read:books")

    if client_id != OAUTH_CLIENT_ID:
        return jsonify({"error": "INVALID_CLIENT", "message": "Unknown client_id."}), 401
    if not isinstance(email, str) or not isinstance(password, str):
        return jsonify({"error": "INVALID_BODY", "message": "email and password are required."}), 400

    user = _find_user_by_email(email)
    if user is None or not _verify_password(password, user["password_hash"]):
        return jsonify({"error": "ACCESS_DENIED", "message": "Invalid user credentials."}), 401

    code = str(uuid4())
    _oauth_codes[code] = {
        "userId": user["id"],
        "clientId": client_id,
        "scope": scope,
        "expiresAt": int((_utcnow() + timedelta(minutes=5)).timestamp()),
    }

    return jsonify({"authorizationCode": code, "tokenEndpoint": "/oauth/token"})


@app.post("/oauth/token")
def oauth_token():
    payload = _require_json_payload()
    if payload is None:
        return jsonify({"error": "INVALID_BODY", "message": "JSON body is required."}), 400

    client_id = payload.get("client_id")
    client_secret = payload.get("client_secret")
    code = payload.get("code")

    if client_id != OAUTH_CLIENT_ID or client_secret != OAUTH_CLIENT_SECRET:
        return jsonify({"error": "INVALID_CLIENT", "message": "Client authentication failed."}), 401
    if not isinstance(code, str) or not code.strip():
        return jsonify({"error": "INVALID_BODY", "message": "code is required."}), 400

    auth_code = _oauth_codes.pop(code, None)
    if auth_code is None:
        return jsonify({"error": "INVALID_CODE", "message": "Authorization code is invalid or already used."}), 401
    if auth_code["expiresAt"] < int(_utcnow().timestamp()):
        return jsonify({"error": "CODE_EXPIRED", "message": "Authorization code expired."}), 401

    user = _find_user_by_id(auth_code["userId"])
    if user is None:
        return jsonify({"error": "INVALID_CODE", "message": "User not found."}), 401

    access_token = _create_token(
        user=user,
        secret=ACCESS_SECRET,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES),
        token_type="access",
        extra_claims={"scope": auth_code["scope"]},
    )

    return jsonify(
        {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": ACCESS_TOKEN_EXPIRES_MINUTES * 60,
            "scope": auth_code["scope"],
            "user": _make_public_user(user),
        }
    )


@app.post("/auth/logout")
@require_auth
def logout():
    refresh_token_value = request.headers.get("X-Refresh-Token")
    revoked_refresh_token_id = None

    if isinstance(refresh_token_value, str) and refresh_token_value.strip():
        try:
            refresh_payload = _decode_token(refresh_token_value, token_type="refresh")
            record = _refresh_tokens.get(refresh_payload["jti"])
            if record is not None:
                record["revoked"] = True
                revoked_refresh_token_id = refresh_payload["jti"]
        except jwt.InvalidTokenError:
            pass

    return jsonify(
        {
            "message": "Logged out successfully.",
            "revokedRefreshTokenId": revoked_refresh_token_id,
        }
    )


@app.get("/auth/me")
@require_auth
def me():
    return jsonify(
        {
            "user": _make_public_user(request.user),  # type: ignore[attr-defined]
            "token": request.token_payload,  # type: ignore[attr-defined]
        }
    )


@app.get("/oauth/me")
@require_auth
def oauth_me():
    return jsonify({"user": _make_public_user(request.user)})


@app.get("/books")
@require_auth
@require_scopes("read:books")
def list_books():
    genre = request.args.get("genre")
    author = request.args.get("author")

    books = _books
    if genre:
        books = [book for book in books if book["genre"].lower() == genre.lower()]
    if author:
        books = [book for book in books if author.lower() in book["author"].lower()]

    return jsonify({"data": books, "total": len(books)})


@app.get("/books/<int:book_id>")
@require_auth
@require_scopes("read:books")
def get_book(book_id: int):
    book = _find_book(book_id)
    if book is None:
        return jsonify({"error": "BOOK_NOT_FOUND", "message": "Book not found."}), 404
    return jsonify(book)


@app.post("/books")
@require_auth
@require_scopes("write:books")
def create_book():
    payload = _require_json_payload()
    if payload is None:
        return jsonify({"error": "INVALID_BODY", "message": "JSON body is required."}), 400

    errors = _validate_book_payload(payload)
    if errors:
        return jsonify({"error": "VALIDATION_ERROR", "details": errors}), 422

    global _book_next_id
    book = {
        "id": _book_next_id,
        "title": str(payload["title"]).strip(),
        "author": str(payload["author"]).strip(),
        "genre": str(payload["genre"]).strip(),
        "publishedDate": str(payload["publishedDate"]).strip(),
        "summary": str(payload["summary"]).strip(),
        "availableCopies": int(payload["availableCopies"]),
        "createdBy": request.user["id"],  # type: ignore[attr-defined]
    }
    _book_next_id += 1
    _books.append(book)

    return jsonify(book), 201


@app.put("/books/<int:book_id>")
@require_auth
@require_roles("admin")
def update_book(book_id: int):
    payload = _require_json_payload()
    if payload is None:
        return jsonify({"error": "INVALID_BODY", "message": "JSON body is required."}), 400

    errors = _validate_book_payload(payload)
    if errors:
        return jsonify({"error": "VALIDATION_ERROR", "details": errors}), 422

    book = _find_book(book_id)
    if book is None:
        return jsonify({"error": "BOOK_NOT_FOUND", "message": "Book not found."}), 404

    book.update(
        {
            "title": str(payload["title"]).strip(),
            "author": str(payload["author"]).strip(),
            "genre": str(payload["genre"]).strip(),
            "publishedDate": str(payload["publishedDate"]).strip(),
            "summary": str(payload["summary"]).strip(),
            "availableCopies": int(payload["availableCopies"]),
        }
    )
    return jsonify(book)


@app.delete("/books/<int:book_id>")
@require_auth
@require_roles("admin")
def delete_book(book_id: int):
    book = _find_book(book_id)
    if book is None:
        return jsonify({"error": "BOOK_NOT_FOUND", "message": "Book not found."}), 404

    _books.remove(book)
    return "", 204


@app.get("/security/audit")
def security_audit():
    findings: list[dict[str, str]] = []

    findings.append(
        {
            "issue": "Token leakage via logs",
            "status": "checked",
            "recommendation": "Do not log Authorization headers or raw tokens.",
        }
    )
    findings.append(
        {
            "issue": "Replay attack risk",
            "status": "checked",
            "recommendation": "Use short-lived access tokens, HTTPS, and refresh token revocation.",
        }
    )
    findings.append(
        {
            "issue": "Secret management",
            "status": "checked",
            "recommendation": "Keep JWT secrets in environment variables and do not commit them.",
        }
    )

    return jsonify({"findings": findings, "count": len(findings)})


@app.errorhandler(404)
def not_found(_error: Any):
    return jsonify({"error": "NOT_FOUND", "message": "Route not found."}), 404


@app.errorhandler(500)
def internal_error(_error: Any):
    return jsonify({"error": "INTERNAL_SERVER_ERROR", "message": "Unexpected server error."}), 500


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=debug)