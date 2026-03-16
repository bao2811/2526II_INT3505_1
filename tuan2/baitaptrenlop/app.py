from flask import Flask, jsonify, request, url_for, session, make_response
import secrets
import hashlib
import time
import jwt
from flask_jwt_extended import jwt_required

app = Flask(__name__)

secret_key = "bao12345"

def generate_jwt(payload):
    """Tạo JWT token (Minh họa Stateless Authentication)"""
    return jwt.encode(payload, secret_key, algorithm='HS256', headers={"typ": "JWT", "alg": "HS256", "by": "Bao Hoang"})

def verify_jwt(token):
    """Xác thực JWT token"""
    try:
        decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        return None  # Token đã hết hạn
    except jwt.InvalidTokenError:
        return None  # Token không hợp lệ
    
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Giả lập xác thực người dùng (Thực tế nên kiểm tra database)
    if username == 'admin' and password == 'password':
        token = generate_jwt({"username": username, "role": "admin", "exp": time.time() + 3600})  # Token có thời hạn 1 giờ
        return jsonify({"token": token})
    else:
        return jsonify({"error": "Invalid credentials"}), 401
    
@app.route('/api/products', methods=['GET'])
@jwt_required
def get_products():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Unauthorized"}), 401
    
    token = auth_header.split(" ")[1]
    user_info = verify_jwt(token)
    
    if not user_info:
        return jsonify({"error": "Invalid or expired token"}), 401
    
    # Trả về danh sách sản phẩm (Minh họa Resource Representation)
    products = [
        {"username": user_info["username"], "role": user_info["role"]},
        {"id": 1, "name": "Laptop", "price": 1200},
        {"id": 2, "name": "Phone", "price": 800},
        {"id": 3, "name": "Tablet", "price": 500}
    ]
    
    return jsonify({"products": products})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

def require_auth():
    """Decorator để yêu cầu xác thực JWT cho các endpoint"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"error": "Unauthorized"}), 401
            
            token = auth_header.split(" ")[1]
            user_info = verify_jwt(token)
            
            if not user_info:
                return jsonify({"error": "Invalid or expired token"}), 401
            
            # Có thể thêm thông tin người dùng vào context nếu cần
            return f(*args, **kwargs)
        return wrapper
    return decorator