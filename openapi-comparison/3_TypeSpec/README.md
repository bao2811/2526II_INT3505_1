# TypeSpec (Next-Gen API Design)

## Mục tiêu

- Viết API spec bằng TypeSpec.
- Sinh OpenAPI từ `library.tsp`.
- Chạy Flask server mẫu để test API.

## Biên dịch TypeSpec

```bash
cd openapi-comparison/3_TypeSpec
npm install
npx tsp compile library.tsp --emit @typespec/openapi3
```

OpenAPI sẽ được tạo ở `tsp-output/@typespec/openapi3/openapi.yaml`.

## Chạy server Flask

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

Server chạy tại `http://localhost:8080/api`.

## Test nhanh

```bash
curl http://localhost:8080/api/books
```

## Lệnh test lại sau khi sửa code

Chỉ cần lưu file rồi chạy lại:

```bash
python server.py
```

## Ghi chú

- `library.tsp` chỉ mô tả sách tối giản với `GET`, `POST`, `GET by id`, `DELETE`.
- `server.py` bám theo đúng các endpoint đó.

## Hướng dẫn chạy server

```bash
cd openapi-comparison/3_TypeSpec
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

Server chạy tại `http://localhost:8080/api`.

Test nhanh:

```bash
curl http://localhost:8080/api/books
```

npx @openapitools/openapi-generator-cli generate `  -i .\tsp-output\@typespec\openapi3\openapi.yaml`
-g python-flask `
-o .\server-generated
