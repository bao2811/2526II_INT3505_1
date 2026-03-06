# Flask Backend API - Client-Server Architecture

Dự án này minh họa việc xây dựng một Backend API bằng Flask mạnh mẽ theo kiến trúc **Client-Server**. Đây là một phần quan trọng của REST (Representational State Transfer).

## Các tính chất của kiến trúc Client-Server đã áp dụng:

### 1. Separation of Concerns (Phân tách mối quan tâm)

Kiến trúc này tách rời giao diện người dùng (**Client**) và lưu trữ dữ liệu (**Server**) thành hai phần riêng biệt.

- **Client**: Chịu trách nhiệm hiển thị giao diện, quản lý trạng thái phiên làm việc (session state) của người dùng. Client được thiết kế linh hoạt, có thể là Web (React, Vue), Mobile (Android, iOS) hoặc các công cụ test API (Postman, cURL).
- **Server**: Chịu trách nhiệm về cơ sở dữ liệu, logic nghiệp vụ, bảo mật và khả năng mở rộng. Server không quan tâm đến việc dữ liệu được hiển thị trên giao diện như thế nào.

### 2. Sự độc lập giữa Client và Server

- Việc thay đổi giao diện người dùng (ví dụ: từ mobile app sang web app) không ảnh hưởng đến server.
- Việc thay đổi database (ví dụ: từ MySQL sang MongoDB) không ảnh hưởng tới client, miễn là các API endpoints không thay đổi cấu trúc trả về.

### 3. Giao tiếp qua các giao thức chuẩn (HTTP)

Việc giao tiếp được thực hiện thông qua các HTTP methods chuẩn như:

- `GET`: Lấy thông tin từ server.
- `POST`: Gửi dữ liệu mới lên server.
- `PUT/PATCH`: Cập nhật dữ liệu trên server.
- `DELETE`: Xóa dữ liệu trên server.

### 4. Định dạng dữ liệu chung (JSON)

Dữ liệu được trao đổi dưới định dạng JSON, giúp việc giao tiếp của client và server trở nên nhất quán và dễ dàng xử lý trên mọi nền tảng.

## Cách chạy Project

1. Di chuyển vào thư mục dự án: `cd tuan2/baitaptrenlop/`
2. Cài đặt Flask nếu chưa có: `pip install Flask`
3. Chạy server: `python server.py`
4. Truy cập các API tại `http://127.0.0.1:5000/api/products`

## Các API Endpoints

- `GET /api/products`: Lấy toàn bộ danh sách sản phẩm.
- `GET /api/products/<id>`: Lấy chi tiết một sản phẩm.
- `POST /api/products`: Thêm sản phẩm mới.
- `PUT /api/products/<id>`: Cập nhật sản phẩm.
- `DELETE /api/products/<id>`: Xóa sản phẩm.
