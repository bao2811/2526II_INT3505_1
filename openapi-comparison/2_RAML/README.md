# RAML (RESTful API Modeling Language)

File mau su dung RAML 0.8 trong `library.raml`.

## Cong cu ho tro

1. raml2html: chuyen .raml sang tai lieu HTML
2. api-spec-converter: chuyen RAML sang OpenAPI

## Cach chay

### 1) Xuat tai lieu HTML

```bash
npm install -g raml2html
raml2html library.raml > index.html
```

### 2) Chuyen RAML 0.8 sang OpenAPI 3

```bash
npx api-spec-converter --from=raml --to=openapi_3 library.raml > openapi.yaml
```

Neu file la `library.raml`, doi ten thanh `api.raml` hoac thay ten file trong lenh.

### 3) Sinh server tu OpenAPI

```bash
openapi-generator-cli generate -i openapi.yaml -g python-flask -o server-generated
```

Chay server sinh tu dong:

```bash
cd server-generated
pip install -r requirements.txt
python -m openapi_server
```

Server chay tai http://localhost:8080

Swagger UI của server generate (python-flask) thường ở: `http://localhost:8080/ui/`

## Cách chạy server

```bash
cd openapi-comparison/2_RAML
pip install -r requirements.txt
python server.py
```

Server chạy tại `http://localhost:8080/api`.

### Test nhanh

```bash
curl http://localhost:8080/api/books
```

Nếu sửa code, chạy lại `python server.py` để kiểm tra tiếp.
