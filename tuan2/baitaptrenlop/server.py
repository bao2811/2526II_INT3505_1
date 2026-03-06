from flask import Flask, jsonify, request

app = Flask(__name__)

# Giả lập database
products = [
    {"id": 1, "name": "Laptop", "price": 1200},
    {"id": 2, "name": "Phone", "price": 800},
    {"id": 3, "name": "Tablet", "price": 500}
]

# Tính chất Client-Server: Tách rời giao diện người dùng (Client) khỏi lưu trữ dữ liệu và xử lý nghiệp vụ (Server).
# Client không cần biết cách dữ liệu được lưu trữ, chỉ cần biết cách giao tiếp qua các API endpoints.

@app.route('/api/products', methods=['GET'])
def get_products():
    """
    Client yêu cầu danh sách sản phẩm.
    Server trả về dữ liệu dưới định dạng JSON.
    """
    return jsonify(products), 200

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Client yêu cầu chi tiết của một sản phẩm cụ thể.
    """
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product), 200
    return jsonify({"message": "Product not found"}), 404

@app.route('/api/products', methods=['POST'])
def add_product():
    """
    Client gửi dữ liệu để tạo sản phẩm mới.
    """
    data = request.get_json()
    if not data or not 'name' in data or not 'price' in data:
        return jsonify({"message": "Invalid input"}), 400
    
    new_product = {
        "id": len(products) + 1,
        "name": data['name'],
        "price": data['price']
    }
    products.append(new_product)
    return jsonify(new_product), 201

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """
    Client yêu cầu cập nhật thông tin sản phẩm.
    """
    data = request.get_json()
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    product['name'] = data.get('name', product['name'])
    product['price'] = data.get('price', product['price'])
    return jsonify(product), 200

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """
    Client yêu cầu xóa sản phẩm.
    """
    global products
    products = [p for p in products if p['id'] != product_id]
    return jsonify({"message": "Product deleted"}), 200

if __name__ == '__main__':
    # Chạy server ở port 5000
    app.run(debug=True, port=5000)
