from flask import Flask, jsonify, request, url_for, session, make_response
import secrets
import hashlib
import time

app = Flask(__name__)
# Key bí mật cho việc sử dụng session (Minh họa tính Stateful)
app.secret_key = secrets.token_hex(16)

# --- Resource Representation ---
products = [
    {"id": 1, "name": "Laptop", "price": 1200},
    {"id": 2, "name": "Phone", "price": 800},
    {"id": 3, "name": "Tablet", "price": 500}
]

# Biến để theo dõi thời điểm cập nhật cuối cùng (Minh họa Cacheable)
last_modified_time = time.time()

def generate_etag(data):
    """Tạo ETag dựa trên nội dung dữ liệu (Property: Cacheable)"""
    return hashlib.md5(str(data).encode()).hexdigest()

# Giả lập database danh sách token (Stateless Auth)
VALID_API_KEYS = ["admin-token-123", "user-token-456"]

def check_stateless_auth():
    api_key = request.headers.get('X-API-KEY')
    return api_key in VALID_API_KEYS

def add_links(product):
    return {
        **product,
        "links": [
            {"rel": "self", "href": url_for('get_product', product_id=product['id'], _external=True), "method": "GET"},
            {"rel": "update", "href": url_for('update_product', product_id=product['id'], _external=True), "method": "PUT"},
            {"rel": "delete", "href": url_for('delete_product', product_id=product['id'], _external=True), "method": "DELETE"}
        ]
    }

# --- 1. STATELESS & CACHEABLE API ENDPOINTS ---
@app.route('/api/products', methods=['GET'])
def get_products():
    if not check_stateless_auth():
        return jsonify({"error": "Unauthorized"}), 401
    
    data_to_return = {
        "count": len(products),
        "products": [add_links(p) for p in products],
        "links": [{"rel": "create", "href": url_for('add_product', _external=True), "method": "POST"}]
    }
    
    # --- Cacheable: ETag & Cache-Control ---
    etag = generate_etag(data_to_return)
    
    # Kiểm tra Conditional Request (If-None-Match)
    if request.headers.get('If-None-Match') == etag:
        return '', 304  # Not Modified (Tiết kiệm băng thông)

    response = make_response(jsonify(data_to_return))
    response.headers['ETag'] = etag
    # Cache trong 60 giây (public cho phép proxy cache)
    response.headers['Cache-Control'] = 'public, max-age=60'
    return response, 200

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    if not check_stateless_auth():
        return jsonify({"error": "Unauthorized"}), 401
    
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({"error": "Not Found"}), 404
    
    data_to_return = add_links(product)
    etag = generate_etag(data_to_return)
    
    if request.headers.get('If-None-Match') == etag:
        return '', 304

    response = make_response(jsonify(data_to_return))
    response.headers['ETag'] = etag
    response.headers['Cache-Control'] = 'private, max-age=120' # Cache cá nhân trong 2 phút
    return response, 200

# --- 2. STATEFUL EXAMPLE ---
@app.route('/api/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart_stateful(product_id):
    if 'cart' not in session:
        session['cart'] = []
    
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        session['cart'].append(product)
        # Thông tin nhạy cảm (Giỏ hàng) THƯỜNG KHÔNG NÊN CACHE hoặc đặt no-store
        response = make_response(jsonify({
            "message": "Added to cart",
            "current_cart": session['cart']
        }))
        response.headers['Cache-Control'] = 'no-store' 
        return response, 200
    return jsonify({"error": "Product not found"}), 404

@app.route('/api/cart', methods=['GET'])
def get_cart_stateful():
    cart = session.get('cart', [])
    response = make_response(jsonify({"cart": cart}))
    response.headers['Cache-Control'] = 'no-cache, must-revalidate'
    return response, 200

@app.route('/api/products', methods=['POST'])
def add_product():
    if not check_stateless_auth():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    new_product = {
        "id": products[-1]['id'] + 1 if products else 1,
        "name": data['name'],
        "price": data['price']
    }
    products.append(new_product)
    # Vô hiệu hóa cache bằng cách thay đổi dữ liệu (Response mới sẽ có ETag mới)
    return jsonify(add_links(new_product)), 201

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if not check_stateless_auth():
        return jsonify({"error": "Unauthorized"}), 401
    global products
    products = [p for p in products if p['id'] != product_id]
    return jsonify({"message": "Product deleted"}), 200

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    if not check_stateless_auth():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({"error": "Not Found"}), 404
    product['name'] = data.get('name', product['name'])
    product['price'] = data.get('price', product['price'])
    return jsonify(add_links(product)), 200



if __name__ == '__main__':
    app.run(debug=True, port=5000)
