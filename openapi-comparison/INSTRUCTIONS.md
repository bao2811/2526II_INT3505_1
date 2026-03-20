# Hướng dẫn & Mục đích Dự án

## 1. Mục đích

So sánh các phương pháp tiếp cận tài liệu hóa API (API Documentation) từ truyền thống (Markdown-based) đến hiện đại (Code-like).

## 2. Đối tượng so sánh

- **OpenAPI (YAML/JSON):** Tiêu chuẩn công nghiệp.
- **API Blueprint (Markdown):** Dễ đọc cho con người.
- **RAML (YAML):** Mạnh về tái sử dụng component.
- **TypeSpec (TS-like):** Thế hệ mới, tối ưu cho lập trình viên.
- **TypeAPI (JSON):** Tập trung vào tính an toàn kiểu dữ liệu (Type-safety).

## 3. Quy trình Demo

1. Chạy server Flask để có API thực tế.
2. Sử dụng công cụ tương ứng của mỗi format (ví dụ: Swagger UI, Dredd, Schemathesis) để kiểm tra API.

# Mục đích và Phương pháp so sánh

## Mục đích

Giúp lập trình viên lựa chọn công cụ phù hợp để thiết kế API (Design-First) dựa trên nhu cầu về tính dễ đọc, khả năng sinh code và hệ sinh thái.

## Phương pháp so sánh

1. **Syntax**: So sánh tính dễ viết (Markdown vs YAML vs DSL).
2. **Tooling**: Khả năng sinh Mock Server, Client SDK và Tài liệu (HTML).
3. **Integration**: Mức độ hỗ trợ từ các Framework (Flask, Express, v.v.).

## Dàn ý so sánh

- **OpenAPI**: Tiêu chuẩn vàng, hệ sinh thái lớn nhất.
- **API Blueprint**: Thân thiện với con người (Markdown).
- **RAML**: Tập trung vào việc tái sử dụng và mô hình hóa dữ liệu phức tạp.
- **TypeSpec/TypeAPI**: Tiếp cận theo hướng lập trình, tối ưu cho Developer.
