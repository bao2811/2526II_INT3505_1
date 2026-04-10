"""Flask server for the API Blueprint library spec."""

from flask import Flask, jsonify, request, url_for


app = Flask(__name__)


BOOKS = [
    {"id": 1, "title": "Lập trình Python", "author": "Nguyễn Văn A"},
    {"id": 2, "title": "Clean Code", "author": "Robert C. Martin"},
]
NEXT_ID = 3


def find_book(book_id: int):
    return next((book for book in BOOKS if book["id"] == book_id), None)


@app.get("/api/books")
def list_books():
    return jsonify(BOOKS)


@app.post("/api/books")
def create_book():
    payload = request.get_json(silent=True) or {}
    title = payload.get("title")
    author = payload.get("author")

    if not isinstance(title, str) or not isinstance(author, str):
        return jsonify({"error": "title and author are required"}), 400

    global NEXT_ID
    book = {"id": NEXT_ID, "title": title, "author": author}
    NEXT_ID += 1
    BOOKS.append(book)

    return jsonify(book), 201, {"Location": url_for("get_book", book_id=book["id"], _external=False)}


@app.get("/api/books/<int:book_id>")
def get_book(book_id: int):
    book = find_book(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book)


@app.put("/api/books/<int:book_id>")
def update_book(book_id: int):
    payload = request.get_json(silent=True) or {}
    title = payload.get("title")
    author = payload.get("author")

    if not isinstance(title, str) or not isinstance(author, str):
        return jsonify({"error": "title and author are required"}), 400

    book = find_book(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404

    book.update({"title": title, "author": author})
    return jsonify(book)


@app.delete("/api/books/<int:book_id>")
def delete_book(book_id: int):
    book = find_book(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404

    BOOKS.remove(book)
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)