# API Blueprint Demo

Tai lieu API viet bang Markdown trong file `library.apib`.

## Cong cu ho tro

1. Aglio: render HTML tu file .apib
2. Dredd: contract testing
3. apib2openapi: chuyen .apib sang OpenAPI YAML
4. openapi-generator-cli: sinh server tu OpenAPI

## Cach chay

### 1) Xem tai lieu HTML

```bash
npm install -g aglio
aglio -i library.apib -s
```

### 2) Chay server Flask mau

```bash
cd openapi-comparison/1_APIBlueprint
pip install -r requirements.txt
python server.py
```

Server chay tai http://localhost:8080/api

Test nhanh:

```bash
curl http://localhost:8080/api/books
```

### 3) Chuyen API Blueprint sang OpenAPI YAML

```bash
cd openapi-comparison/1_APIBlueprint
npx apib2openapi -i library.apib -o openapi1.yaml -y
```

### 4) Sinh server tu OpenAPI

```bash
openapi-generator-cli generate -i openapi1.yaml -g python-flask -o server-generated
```

Chay server sinh tu dong:

```bash
cd server-generated
pip install -r requirements.txt
python -m openapi_server
```

Swagger UI: http://localhost:8080/ui/
Server chay tai http://localhost:8080

## Danh sach API (server Flask mau)

- GET /api/books
- POST /api/books
- GET /api/books/{book_id}
- PUT /api/books/{book_id}
- DELETE /api/books/{book_id}

### Vi du nhanh

```bash
curl http://localhost:8080/api/books

curl -X POST http://localhost:8080/api/books \
	-H "Content-Type: application/json" \
	-d "{\"title\": \"Clean Code\", \"author\": \"Robert C. Martin\"}"

curl http://localhost:8080/api/books/1

curl -X PUT http://localhost:8080/api/books/1 \
	-H "Content-Type: application/json" \
	-d "{\"title\": \"Refactoring\", \"author\": \"Martin Fowler\"}"

curl -X DELETE http://localhost:8080/api/books/1
```
