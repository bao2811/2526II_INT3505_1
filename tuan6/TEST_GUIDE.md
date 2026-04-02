# Tuần 6 - Hướng dẫn test từng bước

## 1. Chạy server

```bash
cd tuan6
python app.py
```

Server mặc định chạy ở `http://localhost:5000`.

## 2. Test trang chủ

```bash
curl http://localhost:5000/
```

Kỳ vọng: trả về danh sách endpoint và tài khoản test.

## 3. Đăng nhập JWT

### Admin

```bash
curl -X POST http://localhost:5000/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"admin@example.com\",\"password\":\"admin123\"}"
```

### User

```bash
curl -X POST http://localhost:5000/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"user@example.com\",\"password\":\"user123\"}"
```

Kỳ vọng: nhận `accessToken` và `refreshToken`.

## 4. Test API có JWT

Lấy `accessToken` từ bước 3, rồi gọi:

```bash
curl http://localhost:5000/books ^
  -H "Authorization: Bearer <accessToken>"
```

### Test xem thông tin user

```bash
curl http://localhost:5000/auth/me ^
  -H "Authorization: Bearer <accessToken>"
```

## 5. Test refresh token

Lấy `refreshToken` từ bước 3, rồi gọi:

```bash
curl -X POST http://localhost:5000/auth/refresh ^
  -H "Content-Type: application/json" ^
  -d "{\"refreshToken\":\"<refreshToken>\"}"
```

Kỳ vọng: nhận `accessToken` mới.

## 6. Test tạo sách

Chỉ token có scope `write:books` mới tạo được.

```bash
curl -X POST http://localhost:5000/books ^
  -H "Authorization: Bearer <accessToken>" ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Dune\",\"author\":\"Frank Herbert\",\"genre\":\"Sci-Fi\",\"publishedDate\":\"1965-08-01\",\"summary\":\"A science fiction novel\",\"availableCopies\":2}"
```

Kỳ vọng:

- Admin: `201 Created`
- User thường: `403 Forbidden`

## 7. Test OAuth 2.0 mock

### Bước 1: Xin authorization code

```bash
curl -X POST http://localhost:5000/oauth/authorize ^
  -H "Content-Type: application/json" ^
  -d "{\"client_id\":\"demo-client\",\"email\":\"admin@example.com\",\"password\":\"admin123\",\"scope\":\"read:books write:books\"}"
```

Kỳ vọng: nhận `authorizationCode`.

### Bước 2: Đổi code lấy token

```bash
curl -X POST http://localhost:5000/oauth/token ^
  -H "Content-Type: application/json" ^
  -d "{\"client_id\":\"demo-client\",\"client_secret\":\"demo-secret\",\"code\":\"<authorizationCode>\"}"
```

Kỳ vọng: nhận `access_token`.

### Bước 3: Test token OAuth

```bash
curl http://localhost:5000/oauth/me ^
  -H "Authorization: Bearer <access_token>"
```

## 8. Test lỗi bảo mật cơ bản

### Không gửi token

```bash
curl http://localhost:5000/books
```

Kỳ vọng: `401 Unauthorized`.

### Token sai

```bash
curl http://localhost:5000/books ^
  -H "Authorization: Bearer wrong-token"
```

Kỳ vọng: `401 Unauthorized`.

### Xem audit

```bash
curl http://localhost:5000/security/audit
```

Kỳ vọng: danh sách rủi ro cơ bản và khuyến nghị xử lý.
