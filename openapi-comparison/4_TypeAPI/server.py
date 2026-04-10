"""Flask server for the TypeAPI library spec."""

from flask import Flask, jsonify


app = Flask(__name__)


BOOKS = [
    {"id": 1, "title": "Số Đỏ"},
    {"id": 2, "title": "Lão Hạc"},
]


@app.get("/api/books")
def list_books():
    return jsonify(BOOKS)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)