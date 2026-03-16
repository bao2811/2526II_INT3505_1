"""Flask practice server exposing the Book Catalog API."""
from flask import Flask, jsonify, request, url_for
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__, static_folder="static")

SWAGGER_URL = "/docs"
API_URL = "/static/books.yaml"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Book Catalog API"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

BOOKS = [
    {
        "id": 1,
        "title": "Clean Architecture",
        "author": "Robert C. Martin",
        "publishedDate": "2017-09-20",
        "genre": "Professional",
        "summary": "Principles of software architecture",
        "availableCopies": 3,
    },
    {
        "id": 2,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "publishedDate": "1937-09-21",
        "genre": "Fantasy",
        "summary": "The journey of Bilbo Baggins",
        "availableCopies": 5,
    },
]
_next_id = 3
_required_fields = [
    "title",
    "author",
    "publishedDate",
    "genre",
    "summary",
    "availableCopies",
]


def _find_book(book_id: int):
    return next((book for book in BOOKS if book["id"] == book_id), None)


def _validate_payload(payload: dict):
    missing = [field for field in _required_fields if field not in payload]
    if missing:
        return f"Missing fields: {', '.join(missing)}"
    return None


def _filter_books(genre: str | None, author: str | None):
    filtered = BOOKS
    if genre:
        filtered = [book for book in filtered if book["genre"].lower() == genre.lower()]
    if author:
        filtered = [book for book in filtered if author.lower() in book["author"].lower()]
    return filtered


@app.route("/books", methods=["GET"])
def list_books():
    genre = request.args.get("genre")
    author = request.args.get("author")
    return jsonify(_filter_books(genre, author))


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id: int):
    book = _find_book(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book)


@app.route("/books", methods=["POST"])
def create_book():
    payload = request.get_json(force=True)
    error = _validate_payload(payload)
    if error:
        return jsonify({"error": error}), 400

    global _next_id
    book = {"id": _next_id, **payload}
    _next_id += 1
    BOOKS.append(book)
    return (
        jsonify(book),
        201,
        {"Location": url_for("get_book", book_id=book["id"], _external=False)},
    )


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id: int):
    payload = request.get_json(force=True)
    error = _validate_payload(payload)
    if error:
        return jsonify({"error": error}), 400

    book = _find_book(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404

    book.update(payload)
    book["id"] = book_id
    return jsonify(book)


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id: int):
    book = _find_book(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    BOOKS.remove(book)
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
