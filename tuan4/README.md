# Tuần 4 – API Specification và OpenAPI

## Mục tiêu học tập

- **Hiểu vai trò** của OpenAPI (Swagger) trong việc tạo tài liệu API chính xác, cập nhật và dễ chia sẻ.
- **Nắm được cấu trúc** file OpenAPI: các `paths`, `components`, `schemas`, `parameters` và các thành phần metadata của tài liệu API.

## Kỹ năng cần luyện

1. Viết OpenAPI YAML mô tả một API quản lý sách với **ít nhất 5 endpoints** (CRUD logic + tìm kiếm/loc theo danh mục).
2. Dùng Swagger UI để render tài liệu tự động và chia sẻ link/URL cho nhóm.

## Hướng dẫn thực hành

1. **Thiết kế mô hình tài nguyên sách**
   - Liệt kê các trường dữ liệu: `id`, `title`, `author`, `publishedDate`, `genre`, `summary`, `availableCopies`.
   - Xác định các hành vi cần hỗ trợ: lấy danh sách, xem chi tiết, tạo mới, cập nhật, xóa, lọc theo `genre`.

2. **Viết OpenAPI spec (YAML)**
   - Bắt đầu file với metadata (`openapi`, `info`, `servers`). Nên định nghĩa http://localhost:3000 cho môi trường dev.
   - Trong `components/schemas`, mô tả `Book` và `BookInput` cùng kiểu dữ liệu rõ ràng.
   - Trong `paths`, định nghĩa các đường dẫn sau với request/response phù hợp:
     - `GET /books`: trả về danh sách sách, hỗ trợ query `genre` và `author`.
     - `GET /books/{bookId}`: trả về chi tiết sách theo `bookId`.
     - `POST /books`: tạo sách mới (body theo `BookInput`).
     - `PUT /books/{bookId}`: cập nhật hết thông tin sách.
     - `DELETE /books/{bookId}`: xóa sách.
   - Dùng `components/parameters` để tái sử dụng `bookId` path parameter và `components/responses` cho lỗi chung (404, 400).
   - Cung cấp ví dụ (`example` hoặc `examples`) cho mỗi response để dễ hình dung.

3. **Kiểm tra spec bằng Swagger Editor**
   - Cách nhanh: mở https://editor.swagger.io và dán YAML vào để kiểm tra lỗi cú pháp.
   - Cách offline: dùng `npx swagger-cli validate spec.yaml` (cài bằng `npm install -g swagger-cli`).

4. **Render Swagger UI**
   - Khởi động Swagger UI bằng một trong các cách:
     - Dùng `docker run --rm -p 8080:8080 -e SWAGGER_JSON=/specs/books.yaml -v $(pwd):/specs swaggerapi/swagger-ui`.
     - Hoặc cài `swagger-ui-express` trong miniserver Node, mount `swaggerUi.setup(require('./spec.yaml'))`.
   - Mở trình duyệt tới `http://localhost:8080/` để xem tài liệu tự động.
   - Chia sẻ link này với nhóm (hoặc chụp ảnh/lưu URL nếu docker chạy trong container và forward port).

5. **Ghi chú thêm**
   - Gắn `description` rõ ràng cho các tham số và response để Swagger UI hiển thị giải thích.
   - Thêm tag như `Books` cho mỗi endpoint để tài liệu dễ lọc.
   - Có thể mở rộng bằng `components/securitySchemes` nếu muốn giả lập API key/token.

## Bài tập mở rộng (tuỳ chọn)

- Viết thêm `GET /books/search` dùng `Query parameters` phức tạp (`minDate`, `maxDate`, `availableOnly`).
- Kết hợp `oneOf`/`anyOf` trong schema để mô tả `physicalBook` vs `ebook` nếu muốn mở rộng mẫu thiết kế.
- Tự động hoá bằng GitHub Pages + swagger-ui-dist để chia sẻ spec trực tiếp từ repo.

## Thực hành Python Flask

1. Tạo môi trường ảo trong thư mục `tuan4` và cài các thư viện:
   - `python -m venv .venv`
   - `./.venv/Scripts/activate`
   - `pip install -r requirements.txt`
2. Khởi chạy ứng dụng mẫu với `python app.py` và truy cập các endpoint sau:
   - `GET /books` (với query `genre` và `author` nếu muốn lọc).
   - `GET /books/{bookId}`, `POST /books`, `PUT /books/{bookId}`, `DELETE /books/{bookId}`.
3. Swagger UI tự động render spec đã viết tại `static/books.yaml`, truy cập tại `/docs` (ví dụ `http://localhost:5000/docs`).
4. Nếu muốn mở rộng, cập nhật `static/books.yaml` rồi dùng Swagger Editor hoặc chạy lại Flask để kiểm tra tài liệu động.
