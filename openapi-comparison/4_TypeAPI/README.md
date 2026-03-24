### 📂 `4_TypeAPI/README.md`

````markdown
# TypeAPI (Type-Safe API Spec)

Định dạng JSON thuần túy, tối giản metadata để tập trung vào dữ liệu.

### 🛠 Công cụ hỗ trợ

1. **TypeAPI CLI**: Công cụ sinh code cho các ngôn ngữ cần độ chính xác cao.

### 🚀 Hướng dẫn chạy Demo

# 4. TypeAPI

JSON tối giản, dùng để sinh các class dữ liệu (Models) cho Flask một cách tự động.

**1. Sinh code Model (Python Pydantic):**

# Cách 1

Dùng để tạo ra các class dữ liệu tương ứng trong Flask:

`npm install -g @sdkgen/cli`

```bash
# Giả sử bạn dùng tool hỗ trợ TypeAPI
typeapi generate library.json -l python -o ./models
```
````

# Cách 2

`python -m datamodel_code_generator --input library.json --input-file-type json --output models.py`

```bash
# Với Pydantic v2 (recommended)
python -m datamodel_code_generator -i library.json --input-file-type json -o models.py --use-annotated

# Output thành multiple files
python -m datamodel_code_generator -i library.json --input-file-type json -o ./output_dir

# Chỉ định target Python version
python -m datamodel_code_generator -i library.json --input-file-type json -o models.py --target-python-version 3.10
```

**2.Để test API (nếu muốn):**
`pip install schemathesis`
`schemathesis run library.json --base-url http://localhost:8080/api`

