# OpenAPI (Swagger) Demo

Thư mục này chứa đặc tả API theo chuẩn OpenAPI 3.0 (YAML).

### 🛠 Công cụ hỗ trợ

1. **Swagger Editor**: [https://editor.swagger.io/](https://editor.swagger.io/) (Dán file `library.yaml` vào để xem UI).
2. **OpenAPI Generator**: Công cụ sinh code tự động.

### 🚀 Hướng dẫn chạy Demo

### 🚀 Cách chạy

1. **Kiểm tra API (Test):**
   ```bash\
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install schemathesis
   schemathesis run library.yaml --base-url http://localhost:8080/api
   ```

**1. Sinh Client SDK (Javascript):**
Cài đặt generator và chạy lệnh sau để tự tạo bộ thư viện gọi API:

npm install @openapitools/openapi-generator-cli -g

Di chuyển vào thư mục 0_OpenAPI/ và chạy:

```bash
mã nguồn python
openapi-generator-cli generate -i library.yaml -g python-flask -o ./generated_flask_app
```

```bash
mã nguồn javascript
openapi-generator-cli generate -i library.yaml -g javascript -o ./client-sdk
```

### 🚀 Chạy server Flask đã generate

Sau khi sinh code vào thư mục `generated_flask_app/`, chạy server như sau:

```bash
python -m venv .venv
.\.venv\Scripts\activate
cd generated_flask_app
pip install -r requirements.txt
python -m openapi_server
```

Server sẽ chạy tại:

```bash
http://localhost:8080/ui/
```

OpenAPI JSON của server:

```bash
http://localhost:8080/openapi.json
```
