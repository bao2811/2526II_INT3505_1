# Nội dung Slide Thuyết trình

## 1: Tại sao cần API Specification?

- Đồng bộ giữa Frontend và Backend.
- Tự động hóa việc sinh tài liệu (Docs).
- Tự động hóa việc sinh Code (SDK) và Testing.

## 2. OpenAPI (Swagger)

- Ngôn ngữ: YAML/JSON.
- Ưu điểm: Phổ biến nhất, công cụ cực mạnh (Swagger UI). Tiêu chuẩn vàng, hỗ trợ Flask cực tốt.
- Nhược điểm: Dễ bị quá dài và phức tạp với API lớn.

## 3. API Blueprint

- Ngôn ngữ: Markdown.
- Ưu điểm: Đọc như một văn bản bình thường, tài liệu sinh ra rất đẹp. Viết như viết ghi chú, tài liệu rất đẹp.
- Nhược điểm: Công cụ sinh code (Codegen) ít hơn OpenAPI.

## 4. RAML

- Ngôn ngữ: YAML.
- Ưu điểm: Tính kế thừa cao, cấu trúc chặt chẽ. Quản lý kiểu dữ liệu (Types) rất chặt chẽ.

## 5. TypeSpec & TypeAPI

- Ngôn ngữ: Type-system (giống TypeScript).
- Ưu điểm: Viết nhanh, ít lỗi logic, dễ dàng export sang OpenAPI. Bắt lỗi ngay khi gõ, hiện đại nhất. Siêu nhẹ, sinh Model Python cực nhanh.

## 6: So sánh các định dạng

| Feature        | OpenAPI   | API Blueprint | RAML              | TypeSpec            |
| -------------- | --------- | ------------- | ----------------- | ------------------- |
| Syntax         | YAML/JSON | Markdown      | YAML              | DSL (TS-like)       |
| Learning Curve | Medium    | Easy          | Medium            | Medium-Hard         |
| Ecosystem      | Huge      | Medium        | Strong (Mulesoft) | Growing (Microsoft) |

## 7: Demo thực tế với Library Management

- Show case: Cách định nghĩa Model `Book`.
- Show case: Cách định nghĩa Endpoint `GET /books`.
- Demo: Sinh code tự động cho Flask.
