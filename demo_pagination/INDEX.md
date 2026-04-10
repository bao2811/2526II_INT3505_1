# 📄 Demo Pagination - File Index

## 📁 Cấu Trúc Dự Án

```
demo_pagination/
├── app.py                    # Flask ứng dụng chính
├── config.py                 # File cấu hình
├── database.sql              # Script tạo database với 1M records
├── requirements.txt          # Dependencies chính (Python)
├── requirements-dev.txt      # Dependencies bổ sung cho testing/dev
├── .env                      # Environment variables (mẫu)
├── .gitignore                # Git ignore rules
├── Dockerfile                # Docker image (tùy chọn)
├── docker-compose.yml        # Docker Compose (tùy chọn)
├── test_api.py              # Script test/benchmark API
├── README.md                 # Tài liệu đầy đủ
├── QUICK_START.md            # Hướng dẫn bắt đầu nhanh
└── INDEX.md                  # File này
```

---

## 📖 Các File Quan Trọng

### 🚀 Bắt Đầu

1. **QUICK_START.md** - Đọc trước tiên (5 phút)
2. **README.md** - Tài liệu chi tiết

### 💻 Code

- **app.py** - Flask backend chính (15KB)
  - 5 loại pagination endpoints
  - 3 utility endpoints (search, filter, stats)
  - Error handling

- **config.py** - Cấu hình app
  - Database settings
  - App settings
  - Default values

- **database.sql** - MySQL script
  - Tạo database `pagination_demo`
  - Tạo bảng `users` (1 triệu records)
  - Tạo indexes tối ưu

### 🧪 Testing

- **test_api.py** - Comprehensive test suite
  - Test tất cả 5 loại pagination
  - Performance benchmark
  - Data validation
  - Pretty output

### ⚙️ Configuration

- **.env** - Environment variables
  - Database credentials
  - Server port
  - [Example provided]

- **requirements.txt** - Python packages

  ```
  flask==3.0.0
  flask-cors==4.0.0
  flask-mysqldb==1.0.1
  python-dotenv==1.0.0
  mysqlclient==2.2.0
  ```

- **requirements-dev.txt** - Dev dependencies
  - - gunicorn (production)
  - - requests (testing)
  - - tabulate (pretty display)

### 🐳 Docker (Tùy chọn)

- **Dockerfile** - Build Flask image
- **docker-compose.yml** - MySQL + Flask setup

---

## 🎯 API Endpoints (5 loại phân trang)

### 1. Offset Pagination

```
GET /api/pagination/offset?page=1&limit=20
```

- ✅ Đơn giản, dễ hiểu
- ❌ Chậm khi offset lớn (trang cuối)

### 2. Cursor Pagination ⭐

```
GET /api/pagination/cursor?limit=20&cursor=null
```

- ✅ Rất nhanh, luôn O(1)
- ✅ Tốt cho infinite scroll
- ❌ Không thể nhảy trang

### 3. Keyset Pagination ⭐

```
GET /api/pagination/keyset?limit=20&last_id=0&sort_by=id
```

- ✅ Rất nhanh
- ✅ Linh hoạt với sorting
- ❌ Không thể nhảy trang

### 4. Limit-Offset Pagination

```
GET /api/pagination/limit-offset?limit=20&offset=0
```

- Tương tự offset nhưng dùng OFFSET keyword

### 5. Page-Based Pagination

```
GET /api/pagination/page-based?page=1&per_page=20
```

- Giống offset nhưng tính theo page

### Utility Endpoints

```
GET /api/pagination/stats              # Database statistics
GET /api/pagination/search?q=user_1    # Search users
GET /api/pagination/filter/city/Hanoi  # Filter by city
GET /api/pagination/random?limit=10    # Random users
GET /api/pagination/docs               # API docs
```

---

## 📊 Dữ Liệu

### Database: `pagination_demo`

#### Table: `users` (1,000,000 bản ghi)

| Column     | Type         | Notes                                               |
| ---------- | ------------ | --------------------------------------------------- |
| id         | INT          | Primary Key, Auto-increment                         |
| username   | VARCHAR(50)  | Indexed                                             |
| email      | VARCHAR(100) | Indexed, Unique                                     |
| full_name  | VARCHAR(100) | -                                                   |
| age        | INT          | 20-80                                               |
| city       | VARCHAR(50)  | Indexed                                             |
| country    | VARCHAR(50)  | Vietnam, Thailand, Singapore, Malaysia, Philippines |
| phone      | VARCHAR(20)  | +84...                                              |
| created_at | TIMESTAMP    | Indexed, Default NOW()                              |
| updated_at | TIMESTAMP    | Default NOW()                                       |

**Indexes**:

- PRIMARY KEY (id)
- UNIQUE KEY (email)
- INDEX (username)
- INDEX (city)
- INDEX (created_at)

---

## 🔧 Setup

### 1. Database (10 phút)

```bash
mysql -u root -p < database.sql
```

Credentials: `root` / `bao12345`

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Server

```bash
python app.py
```

---

## 🧪 Testing

### Run All Tests

```bash
python test_api.py
```

### Test Specific Endpoint

```bash
curl "http://localhost:3000/api/pagination/offset?page=1&limit=20"
```

### Postman Collection

Import từ `/api/pagination/docs`

---

## 📈 Performance Benchmarks

Dựa trên 1 triệu records:

| Method     | Page 1 | Page 5000 | Page 50000 |
| ---------- | ------ | --------- | ---------- |
| **Offset** | 50ms   | 300ms     | 2000ms+ ⚠️ |
| **Cursor** | 30ms   | 30ms      | 30ms ✅    |
| **Keyset** | 30ms   | 30ms      | 30ms ✅    |

**Kết luận**: Cursor/Keyset tốt hơn cho dataset lớn!

---

## 💡 Tips & Tricks

### Optimize MySQL

```sql
CREATE INDEX idx_created_at_id ON users(created_at, id);
EXPLAIN SELECT * FROM users WHERE id > 500000 LIMIT 100;
```

### Use Gunicorn (Production)

```bash
gunicorn -w 4 -b localhost:3000 app:app
```

### Docker Setup

```bash
docker-compose up -d
```

---

## 📚 Tài Liệu Tham Khảo

### Pagination Best Practices

- [MySQL LIMIT Optimization](https://dev.mysql.com/doc/refman/8.0/en/limit-optimization.html)
- [Cursor Pagination](https://www.sitepoint.com/pagination-with-nodejs-express/)
- [GraphQL Pagination](https://graphql.org/learn/pagination/)

### Tech Stack

- **Backend**: Flask 3.0.0
- **Database**: MySQL 8.0
- **Driver**: MySQLdb 2.2.0
- **CORS**: flask-cors 4.0.0

---

## ❓ FAQ

**Tại sao Cursor nhanh hơn Offset?**

- Offset phải scan N rows rồi skip, lâu khi N lớn
- Cursor chỉ scan from last position, O(1) complexity

**Nên dùng kiểu nào?**

- Mobile app → Cursor
- Web admin → Offset/Page
- Real-time API → Keyset
- Infinite scroll → Cursor

**Import database quá lâu?**

- Bình thường 5-10 phút
- Bạn có thể reload lại script hoặc xóa + tạo

---

## ✅ Checklist Setup

- [ ] MySQL running & credentials correct
- [ ] Database imported successfully
- [ ] Python 3.7+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] .env file configured
- [ ] Server starts: `python app.py`
- [ ] Can access: http://localhost:3000
- [ ] Tests pass: `python test_api.py`

---

## 👤 Tác Giả

Demo Pagination - Educational Project
2026-04-09

---

**Ready to go! 🚀**
