import os
import uuid
from threading import Lock

from flask import Flask, jsonify, request


def create_app() -> Flask:
    app = Flask(__name__)
    storage_lock = Lock()
    products: dict[str, dict] = {}

    # Seed dữ liệu mẫu để test nhanh GET/GET by id
    seed_id = str(uuid.uuid4())
    products[seed_id] = {
        "id": seed_id,
        "name": "Keyboard",
        "description": "Mechanical keyboard",
        "price": 35.5,
        "inStock": True,
    }

    def validate_product_payload(payload: dict, partial: bool = False):
        if not isinstance(payload, dict):
            return "Request body phải là JSON object."

        allowed_fields = {"name", "description", "price", "inStock"}
        unknown_fields = set(payload.keys()) - allowed_fields
        if unknown_fields:
            return f"Field không hợp lệ: {', '.join(sorted(unknown_fields))}"

        required_fields = {"name", "price"}
        if not partial:
            missing = required_fields - set(payload.keys())
            if missing:
                return f"Thiếu field bắt buộc: {', '.join(sorted(missing))}"

        if "name" in payload and (not isinstance(payload["name"], str) or not payload["name"].strip()):
            return "Field 'name' phải là chuỗi không rỗng."

        if "description" in payload and not isinstance(payload["description"], str):
            return "Field 'description' phải là chuỗi."

        if "price" in payload:
            price = payload["price"]
            if not isinstance(price, (int, float)):
                return "Field 'price' phải là số."
            if price < 0:
                return "Field 'price' phải >= 0."

        if "inStock" in payload and not isinstance(payload["inStock"], bool):
            return "Field 'inStock' phải là boolean."

        return None

    @app.get("/products")
    def get_products():
        with storage_lock:
            return jsonify({"count": len(products), "data": list(products.values())}), 200

    @app.get("/products/<product_id>")
    def get_product_by_id(product_id: str):
        with storage_lock:
            product = products.get(product_id)
            if not product:
                return jsonify({"error": "Product not found"}), 404
            return jsonify(product), 200

    @app.post("/products")
    def create_product():
        payload = request.get_json(silent=True)
        error = validate_product_payload(payload, partial=False)
        if error:
            return jsonify({"error": error}), 400

        product_id = str(uuid.uuid4())
        new_product = {
            "id": product_id,
            "name": payload["name"].strip(),
            "description": payload.get("description", ""),
            "price": float(payload["price"]),
            "inStock": payload.get("inStock", True),
        }

        with storage_lock:
            products[product_id] = new_product

        return jsonify(new_product), 201

    @app.put("/products/<product_id>")
    def update_product(product_id: str):
        payload = request.get_json(silent=True)
        error = validate_product_payload(payload, partial=False)
        if error:
            return jsonify({"error": error}), 400

        with storage_lock:
            if product_id not in products:
                return jsonify({"error": "Product not found"}), 404

            updated = {
                "id": product_id,
                "name": payload["name"].strip(),
                "description": payload.get("description", ""),
                "price": float(payload["price"]),
                "inStock": payload.get("inStock", True),
            }
            products[product_id] = updated
            return jsonify(updated), 200

    @app.delete("/products/<product_id>")
    def delete_product(product_id: str):
        with storage_lock:
            if product_id not in products:
                return jsonify({"error": "Product not found"}), 404
            deleted = products.pop(product_id)
            return jsonify({"message": "Deleted successfully", "deleted": deleted}), 200

    return app


if __name__ == "__main__":
    flask_app = create_app()
    port = int(os.getenv("PORT", "5000"))
    flask_app.run(host="0.0.0.0", port=port, debug=True)
