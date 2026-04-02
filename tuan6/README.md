# Tuần 6: Authentication và Authorization

Backend Flask ngắn gọn cho buổi 6, có đủ:

- đăng nhập JWT
- refresh token
- OAuth 2.0 mock flow
- phân quyền theo role/scope
- file API riêng để tra endpoint

## Chạy nhanh

```bash
cd tuan6
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```

Server chạy tại `http://localhost:5000`.

## Tài khoản test

- `admin@example.com` / `admin123`
- `user@example.com` / `user123`

## Endpoint chính

- `POST /auth/login` - đăng nhập lấy JWT
- `POST /auth/refresh` - lấy access token mới
- `POST /oauth/authorize` - bước authorize của OAuth 2.0 mock
- `POST /oauth/token` - đổi code lấy JWT
- `GET /books` - xem sách, cần token
- `POST /books` - tạo sách, cần scope `write:books`
- `GET /security/audit` - kiểm tra rủi ro cơ bản

## Cách dùng nhanh

1. Gọi `POST /auth/login` hoặc `POST /oauth/authorize` rồi `POST /oauth/token`.
2. Lấy `accessToken`.
3. Gửi `Authorization: Bearer <accessToken>` khi gọi API khác.

## File API

Xem danh sách endpoint ở [api.yaml](./api.yaml).
