import os
import time
import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'bao12345'),
    'database': os.getenv('DB_NAME', 'pagination_demo'),
    'port': int(os.getenv('DB_PORT', 3306))
}

CORS(app)

def get_db_connection():
    """Get database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def test_db_connection():
    """Test database connection"""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        cursor.fetchone()
        cursor.close()
        conn.close()
        return True
    except:
        return False

# ============================================
# 1️⃣ OFFSET PAGINATION
# ============================================
@app.route('/api/pagination/offset', methods=['GET'])
def offset_pagination():
    try:
        offset = max(0, int(request.args.get('offset', 0)))
        limit = min(100, max(1, int(request.args.get('limit', 10))))

        start_time = time.time()

        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = conn.cursor(dictionary=True)

        # Get total count
        cursor.execute('SELECT COUNT(*) as total FROM users')
        total = cursor.fetchone()['total']

        # Get paginated data
        cursor.execute(
            'SELECT id, username, email, full_name, age, city, country, phone, created_at FROM users ORDER BY id LIMIT %s OFFSET %s',
            (limit, offset)
        )
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        end_time = time.time()

        # Convert datetime objects to strings
        for user in users:
            if user['created_at']:
                user['created_at'] = user['created_at'].isoformat()

        return jsonify({
            'data': users,
            'pagination': {
                'limit': limit,
                'total': total,
                'offset': offset,
                'has_next': offset + limit < total,
                'has_previous': offset > 0
            },
            'performance': {
                'duration_ms': int((end_time - start_time) * 1000),
                'method': 'OFFSET PAGINATION'
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================
# 2️⃣ CURSOR PAGINATION
# ============================================
@app.route('/api/pagination/cursor', methods=['GET'])
def cursor_pagination():
    try:
        limit = min(100, max(1, int(request.args.get('limit', 10))))
        last_id = max(0, int(request.args.get('last_id', 0)))

        start_time = time.time()

        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            'SELECT id, username, email, full_name, age, city, country, phone, created_at FROM users WHERE id > %s ORDER BY id LIMIT %s',
            (last_id, limit + 1)
        )
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        end_time = time.time()

        # Convert datetime objects to strings
        for user in users:
            if user['created_at']:
                user['created_at'] = user['created_at'].isoformat()

        # Check if there's a next page
        has_next = len(users) > limit
        data = users[:limit] if has_next else users

        return jsonify({
            'data': data,
            'pagination': {
                'limit': limit,
                'last_id': last_id,
                'has_next': has_next,
                'next_last_id': data[-1]['id'] if len(data) > 0 else None,
                'records_returned': len(data)
            },
            'performance': {
                'duration_ms': int((end_time - start_time) * 1000),
                'method': 'CURSOR PAGINATION'
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================
# 3️⃣ PAGE-BASED PAGINATION
# ============================================
@app.route('/api/pagination/page-based', methods=['GET'])
def page_based_pagination():
    try:
        page = max(1, int(request.args.get('page', 1)))
        per_page = min(100, max(1, int(request.args.get('per_page', 10))))

        start_time = time.time()

        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = conn.cursor(dictionary=True)

        # Get total count
        cursor.execute('SELECT COUNT(*) as total FROM users')
        total = cursor.fetchone()['total']

        # Calculate offset
        offset = (page - 1) * per_page

        # Get paginated data
        cursor.execute(
            'SELECT id, username, email, full_name, age, city, country, phone, created_at FROM users ORDER BY id LIMIT %s OFFSET %s',
            (per_page, offset)
        )
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        end_time = time.time()

        # Convert datetime objects to strings
        for user in users:
            if user['created_at']:
                user['created_at'] = user['created_at'].isoformat()

        total_pages = (total + per_page - 1) // per_page

        return jsonify({
            'data': users,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_previous': page > 1
            },
            'performance': {
                'duration_ms': int((end_time - start_time) * 1000),
                'method': 'PAGE-BASED PAGINATION'
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================
# UTILITY ENDPOINTS
# ============================================

# Get database stats
@app.route('/api/pagination/stats', methods=['GET'])
def get_stats():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = conn.cursor(dictionary=True)

        # Get statistics
        cursor.execute('''
            SELECT
                COUNT(*) as total_records,
                MIN(id) as min_id,
                MAX(id) as max_id,
                MIN(created_at) as oldest_record,
                MAX(created_at) as newest_record
            FROM users
        ''')
        stats = cursor.fetchone()

        # Get size
        cursor.execute('''
            SELECT
                ROUND(((data_length + index_length) / 1024 / 1024), 2) as size_mb
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'users'
        ''', (os.getenv('DB_NAME'),))
        size_info = cursor.fetchone()

        cursor.close()
        conn.close()

        # Convert datetime to string
        if stats['oldest_record']:
            stats['oldest_record'] = stats['oldest_record'].isoformat()
        if stats['newest_record']:
            stats['newest_record'] = stats['newest_record'].isoformat()

        return jsonify({
            'database_stats': {
                **stats,
                'size_mb': size_info['size_mb'] if size_info else 0
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Search users
@app.route('/api/pagination/search', methods=['GET'])
def search_users():
    try:
        keyword = request.args.get('q', '')
        limit = min(50, int(request.args.get('limit', 10)))

        if len(keyword) < 2:
            return jsonify({'data': [], 'message': 'Query must be at least 2 characters'})

        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            'SELECT id, username, email, full_name FROM users WHERE username LIKE %s OR email LIKE %s LIMIT %s',
            (f'%{keyword}%', f'%{keyword}%', limit)
        )
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify({
            'data': users,
            'search_query': keyword,
            'results_count': len(users)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Filter by city
@app.route('/api/pagination/filter/city/<city>', methods=['GET'])
def filter_by_city(city):
    try:
        page = max(1, int(request.args.get('page', 1)))
        limit = min(100, int(request.args.get('limit', 10)))
        offset = (page - 1) * limit

        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = conn.cursor(dictionary=True)

        # Get total
        cursor.execute('SELECT COUNT(*) as total FROM users WHERE city = %s', (city,))
        total = cursor.fetchone()['total']

        # Get data
        cursor.execute(
            'SELECT * FROM users WHERE city = %s ORDER BY id LIMIT %s OFFSET %s',
            (city, limit, offset)
        )
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convert datetime to strings
        for user in users:
            if user['created_at']:
                user['created_at'] = user['created_at'].isoformat()
            if user['updated_at']:
                user['updated_at'] = user['updated_at'].isoformat()

        return jsonify({
            'data': users,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'total_pages': (total + limit - 1) // limit,
                'city': city
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Get random users
@app.route('/api/pagination/random', methods=['GET'])
def get_random_users():
    try:
        limit = min(100, int(request.args.get('limit', 10)))

        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users ORDER BY RAND() LIMIT %s', (limit,))
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convert datetime to strings
        for user in users:
            if user['created_at']:
                user['created_at'] = user['created_at'].isoformat()
            if user['updated_at']:
                user['updated_at'] = user['updated_at'].isoformat()

        return jsonify({
            'data': users,
            'method': 'RANDOM SELECTION'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================
# HOME ROUTES
# ============================================

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': '📄 Pagination Demo API (Flask)',
        'version': '1.0.0',
        'endpoints': {
            'offset': '/api/pagination/offset?offset=0&limit=10',
            'cursor': '/api/pagination/cursor?limit=10&last_id=0',
            'pageBased': '/api/pagination/page-based?page=1&per_page=10'
        },
        'docs': '/api/pagination/docs'
    })


@app.route('/api/pagination/docs', methods=['GET'])
def docs():
    return jsonify({
        'message': 'Pagination Endpoints Documentation',
        'endpoints': [
            {
                'name': 'Offset Pagination',
                'url': '/api/pagination/offset',
                'method': 'GET',
                'params': 'offset (int), limit (int)',
                'example': '/api/pagination/offset?offset=0&limit=20'
            },
            {
                'name': 'Cursor Pagination',
                'url': '/api/pagination/cursor',
                'method': 'GET',
                'params': 'limit (int), last_id (int)',
                'example': '/api/pagination/cursor?limit=20&last_id=0'
            },
            {
                'name': 'Page-Based Pagination',
                'url': '/api/pagination/page-based',
                'method': 'GET',
                'params': 'page (int), per_page (int)',
                'example': '/api/pagination/page-based?page=1&per_page=20'
            }
        ]
    })


# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Pagination Demo API - Flask")
    print("="*60)

    # Test database connection
    print("🔍 Testing database connection...")
    if test_db_connection():
        print("✅ Database connected successfully")
    else:
        print("❌ Database connection failed!")
        print("   Make sure:")
        print("   1. MySQL is running")
        print("   2. Database 'pagination_demo' exists")
        print("   3. Credentials are correct in .env")
        print("\n   To generate data, run: python generate_data.py")
        exit(1)

    port = int(os.getenv('PORT', 3000))
    print(f"\n✅ Server starting on http://localhost:{port}")
    print(f"📚 API Documentation: http://localhost:{port}/api/pagination/docs")
    print("="*60 + "\n")

    app.run(debug=True, host='localhost', port=port)
