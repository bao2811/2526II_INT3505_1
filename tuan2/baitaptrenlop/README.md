# Flask Backend API - Cacheable Architecture

Dự án này minh họa việc áp dụng nguyên tắc **Cacheable** trong kiến trúc REST giúp tối ưu hóa hiệu năng và giảm tải dữ liệu cho hệ thống.

## Các cơ chế Cache đã áp dụng:

### 1. Cache-Control Header

- Định rõ dữ liệu có thể được cache trong bao lâu và ai có quyền cache.
- **Public**: Cho phép cả Browser và Proxy (CDN) cache dữ liệu (`max-age=60`).
- **Private**: Chỉ cho phép Browser người dùng cache (`max-age=120`).
- **No-store**: Cấm tuyệt đối việc cache dữ liệu giỏ hàng (Stateful).

### 2. ETag (Entity Tag)

- Server tạo hash (dấu vân tay) cho nội dung dữ liệu trả về.
- Khi dữ liệu không đổi, ETag giữ nguyên, giúp Client xác định nội dung mình đang có là mới nhất hay chưa.

### 3. Conditional Requests (304 Not Modified)

- Client gửi request kèm `If-None-Match: <etag_cu>`.
- Nếu dữ liệu không đổi, Server trả về mã **304** (không truyền body), tiết kiệm tối đa băng thông.

## Cách chạy và Test Cache

1. Chạy server: `python server.py`
2. Test bằng Postman hoặc Browser Network Tab:
   - Gọi `GET /api/products` lần đầu: Nhận dữ liệu + `ETag` trong header.
   - Gọi `GET /api/products` lần hai (Thêm header `If-None-Match` giá trị ETag cũ): Server trả về `304 Not Modified`.
   - Nếu thực hiện `POST` thêm sản phẩm: ETag sẽ thay đổi, request tiếp theo sẽ nhận mã `200 OK` với dữ liệu mới.

---

## Các nguyên tắc REST khác vẫn duy trì:

1. **Stateless**: Dùng API Key (`X-API-KEY`).
2. **Stateful Example**: Giỏ hàng dùng Session/Cookie.
3. **Uniform Interface**: URI, JSON, HATEOAS, Self-descriptive.
