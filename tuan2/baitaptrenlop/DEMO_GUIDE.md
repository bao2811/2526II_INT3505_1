# Hướng dẫn Demo Các Nguyên tắc REST (Flask API)

Tài liệu này hướng dẫn bạn từng bước để demo các nguyên tắc kiến trúc REST đã được cài đặt trong dự án Flask này.

---

## Chuẩn bị

1. Di chuyển vào thư mục: `cd tuan2/baitaptrenlop/`
2. Chạy Server: `python server.py`
3. Công cụ khuyên dùng: **Postman**, **cURL** hoặc **Thunder Client** (VS Code Extension).

---

## Bước 1: Demo Client-Server (Tách biệt Giao diện và Dữ liệu)

**Mục tiêu**: Chứng minh rằng Server chỉ cung cấp dữ liệu, không quan tâm Client là ai.

1. Mở trình duyệt hoặc Postman.
2. Truy cập `http://127.0.0.1:5000/api/products`.
3. **Kết quả**: Server trả về dữ liệu thô (JSON). Bạn có thể viết một ứng dụng React, Flutter hoặc đơn giản là dùng cURL để hiển thị dữ liệu này. Server không thay đổi code dù Client thay đổi.

---

## Bước 2: Demo Stateless (Không lưu trạng thái)

**Mục tiêu**: Chứng minh Server không "ghi nhớ" Client, mỗi Request phải tự mang theo thông tin xác thực.

1. **Lần 1 (Thất bại)**: Gửi `GET /api/products` (Không cài đặt Header).
   - **Kết quả**: `401 Unauthorized`. Server không biết bạn là ai.
2. **Lần 2 (Thành công)**: Gửi lại request trên nhưng thêm Header: `X-API-KEY: admin-token-123`.
   - **Kết quả**: `200 OK` + Danh sách sản phẩm.
3. **Kết luận**: Server không lưu trạng thái "đã đăng nhập" sau request lần 2. Nếu request lần 3 bạn bỏ header, nó sẽ vẫn trả về `401`.

---

## Bước 3: Demo Stateful (Lưu trạng thái - Để so sánh)

**Mục tiêu**: Xem cách Server ghi nhớ thông tin qua Session/Cookie (Trái ngược với REST chuẩn).

1. Thêm vào giỏ hàng: `POST /api/cart/add/1` (Dùng Postman hoặc Trình duyệt).
2. Xem giỏ hàng: `GET /api/cart`.
   - **Kết quả**: Server trả về danh sách sản phẩm bạn vừa thêm.
3. **Giải thích**: Server sử dụng Cookie để nhận diện "phiên làm việc" của bạn. Đây là tính chất **Stateful** (có trạng thái). Nếu bạn xóa Cookie, giỏ hàng sẽ mất.

---

## Bước 4: Demo Uniform Interface (Giao diện thống nhất)

**Mục tiêu**: Kiểm tra tính tự mô tả và khả năng điều hướng của API.

1. Xem chi tiết 1 sản phẩm: `GET /api/products/1` (Kèm Header `X-API-KEY`).
2. **Quan sát kết quả**:
   - Dữ liệu trả về là **JSON** chuẩn.
   - Có mã trạng thái: `200 OK`.
   - **HATEOAS**: Trong kết quả có trường `"links"`. Bạn có thể thấy URL để `update` hoặc `delete` sản phẩm đó mà không cần tra cứu tài liệu.

---

## Bước 5: Demo Cacheable (Khả năng lưu đệm)

**Mục tiêu**: Kiểm tra cách Server giúp tiết kiệm băng thông thông qua ETag.

1. **Request 1**: Gọi `GET /api/products` (Kèm API Key).
   - Quan sát tab **Headers** trong phản hồi, tìm dòng `ETag` (ví dụ: `ETag: "abc123...").
2. **Request 2**: Gọi lại `GET /api/products` nhưng thêm Header yêu cầu: `If-None-Match: "abc123..."` (Giá trị ETag vừa nhận).
   - **Kết quả**: Mã trạng thái trả về là **304 Not Modified**.
   - Body trả về trống rỗng (0 bytes). Client sử dụng lại dữ liệu cũ đã lưu.
3. **Thử nghiệm thay đổi**:
   - Thực hiện `POST` thêm 1 sản phẩm mới.
   - Gọi lại bước 2 với ETag cũ.
   - **Kết quả**: Mã `200 OK` (Dữ liệu mới + ETag mới) vì cache cũ đã bị vô hiệu hóa.
