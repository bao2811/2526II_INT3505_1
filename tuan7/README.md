# Tuần 7: Nguyên lý Triển khai Backend Service

Buổi 7 tập trung vào cách đi từ OpenAPI spec đến backend Flask chạy thật, có kết nối MongoDB.

## Mục tiêu buổi học

### Kiến thức cần đạt

- Sử dụng OpenAPI để sinh code backend (Swagger Codegen)
- Kết nối API với database MongoDB

### Kỹ năng cần làm được

- Triển khai backend từ OpenAPI spec
- Tích hợp với database để lưu trữ dữ liệu

### Thực hành bắt buộc

- Cài đặt backend từ file OpenAPI có sẵn
- Tạo CRUD operations cho resource `Product`

## Yêu cầu môi trường

- Python 3.10+
- pip
- MongoDB (local hoặc Docker)
- Java 11+ (để chạy Swagger Codegen CLI)

## Quy trình triển khai tổng quát

1. Chuẩn bị file OpenAPI có định nghĩa `Product`.
2. Dùng Swagger Codegen sinh skeleton backend Flask.
3. Cài dependency Python.
4. Kết nối MongoDB qua PyMongo.
5. Cài đặt logic CRUD cho `Product`.
6. Test endpoint bằng Postman/curl.

## 1) Chuẩn bị OpenAPI spec

Tạo file `openapi.yaml` (hoặc dùng file được cung cấp sẵn). Cần có các endpoint cơ bản:

- `GET /products`
- `GET /products/{id}`
- `POST /products`
- `PUT /products/{id}`
- `DELETE /products/{id}`

Ví dụ schema `Product`:

```yaml
components:
  schemas:
    Product:
      type: object
      required: [name, price]
      properties:
        id:
          type: string
        name:
          type: string
        description:
          type: string
        price:
          type: number
          format: double
        inStock:
          type: boolean
```

## Cấu trúc đã chuẩn bị trong thư mục tuần 7

- `openapi.yaml`: Đặc tả API Product CRUD
- `app.py`: Flask app (Connexion) đọc OpenAPI
- `controllers/product_controller.py`: Xử lý CRUD Product
- `db.py`: Kết nối MongoDB
- `requirements.txt`: Dependency Python
- `generate_server.ps1`: Script sinh skeleton Flask từ OpenAPI bằng Swagger Codegen

## 2) Sinh backend bằng Swagger Codegen (Python Flask)

### Cách A: Chạy script có sẵn

```powershell
cd tuan7
./generate_server.ps1
```

Script sẽ tạo thư mục `generated-flask-server`.

### Cách B: Dùng JAR trực tiếp

```bash
cd tuan7
curl -L -o swagger-codegen-cli.jar https://repo1.maven.org/maven2/io/swagger/codegen/v3/swagger-codegen-cli/3.0.52/swagger-codegen-cli-3.0.52.jar

java -jar swagger-codegen-cli.jar generate \
  -i openapi.yaml \
  -l python-flask \
  -o generated-flask-server
```

### Cách C: Dùng Docker (không cần cài Java local)

```bash
docker run --rm -v ${PWD}:/local swaggerapi/swagger-codegen-cli-v3 generate \
  -i /local/openapi.yaml \
  -l python-flask \
  -o /local/generated-flask-server
```

## 3) Cài đặt và chạy backend thực hành

```bash
cd tuan7
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Tạo file `.env` từ `.env.example`:

```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=tuan7_products
```

Nếu chưa có MongoDB local, chạy bằng Docker:

```bash
docker run -d --name mongo-tuan7 -p 27017:27017 mongo:7
```

Chạy ứng dụng:

```bash
python app.py
```

API chạy tại `http://localhost:5000`.

## 4) Kết nối MongoDB trong Flask

Phần này đã được cài trong `db.py` và gọi khi khởi động ở `app.py`:

- Đọc `MONGODB_URI` và `MONGODB_DB` từ biến môi trường
- Tạo Mongo client
- Truy cập collection `products`

## 5) Cài đặt CRUD cho `Product`

Mapping nghiệp vụ cần hoàn thành:

- `GET /products`: lấy danh sách sản phẩm
- `GET /products/{id}`: lấy chi tiết theo id
- `POST /products`: tạo sản phẩm mới
- `PUT /products/{id}`: cập nhật sản phẩm
- `DELETE /products/{id}`: xóa sản phẩm

Gợi ý triển khai trong handler/controller:

- Dùng `collection.find()` cho list
- Dùng `find_one({"_id": ObjectId(id)})` cho detail
- Dùng `insert_one(payload)` cho create
- Dùng `find_one_and_update(..., return_document=AFTER)` cho update
- Dùng `delete_one(...)` cho delete

## 6) Kịch bản test nhanh

### Tạo mới

```bash
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Keyboard","price":35.5,"inStock":true}'
```

### Lấy danh sách

```bash
curl http://localhost:5000/products
```

### Cập nhật

```bash
curl -X PUT http://localhost:5000/products/<id> \
  -H "Content-Type: application/json" \
  -d '{"name":"Mechanical Keyboard","price":49.9,"inStock":true}'
```

### Xóa

```bash
curl -X DELETE http://localhost:5000/products/<id>
```

## Checklist hoàn thành buổi 7

- [ ] Sinh được backend từ OpenAPI bằng Swagger Codegen
- [ ] Chạy server thành công
- [ ] Kết nối thành công MongoDB từ Flask
- [ ] Hoàn thành đủ 5 API CRUD cho `Product`
- [ ] Test được tất cả API với dữ liệu thật trong DB

## Kết quả mong đợi

Sau buổi 7, bạn có một backend service có thể:

- Sinh từ OpenAPI spec (giảm viết tay boilerplate)
- Lưu và truy xuất dữ liệu thật từ MongoDB
- Vận hành đầy đủ CRUD cho resource `Product`

cd tuan7
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
Khởi động MongoDB local hoặc Docker
python app.py
