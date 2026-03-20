### 📂 `3_TypeSpec/README.md`

````markdown
# TypeSpec (Next-Gen API Design)

Viết API bằng ngôn ngữ hướng đối tượng tương tự TypeScript.

### 🛠 Công cụ hỗ trợ

1. **TypeSpec Compiler**: `@typespec/compiler`.

### 🚀 Hướng dẫn chạy Demo

### 🚀 Cách chạy (Quan trọng cho Flask)

1. **Cài đặt:** `npm install` để cài compiler.

`npm install -g @typespec/compiler`

# 2. Cài đặt các thư viện cần thiết trong folder 3_TypeSpec

`npm install @typespec/http @typespec/rest @typespec/openapi3`

# 3. **Biên dịch:** Chạy lệnh sau để tạo file OpenAPI cho Flask:

```bash
npx tsp compile library.tsp --emit @typespec/openapi3
```
````

# 4 Sau khi có file output từ bước trên, bạn có thể sinh Client SDK cho Frontend (React/Vue) để gọi tới Flask:

```bash
# Dùng file vừa sinh ra để tạo bộ thư viện Javascript
openapi-generator-cli generate -i ./tsp-output/@typespec/openapi3/openapi.json -g javasc
```
