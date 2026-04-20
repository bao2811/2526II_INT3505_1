# Tuần 8: API Testing và Quality Assurance

Buổi 8 tập trung vào kiểm thử API tự động và đo chất lượng dịch vụ trước khi triển khai.

## Mục tiêu buổi học

### Kiến thức cần đạt

- Các loại test cho API: unit test, integration test, performance test
- Công cụ chính: Postman, Newman, load testing tools

### Kỹ năng cần làm được

- Viết bộ test tự động cho các endpoint
- Đo hiệu năng API với các chỉ số: response time, error rate

### Thực hành bắt buộc

- Tạo test suite trong Postman cho 5 endpoints
- Chạy test tự động bằng Newman

## Workflow Tuần 8

1. Chuẩn bị API đang chạy local (ví dụ `http://localhost:5000`).
2. Chọn 5 endpoint cần kiểm thử (ưu tiên các endpoint chính của nghiệp vụ).
3. Tạo Postman Collection và Environment (`baseUrl`, token nếu có).
4. Viết test cho từng endpoint trong Postman:
   - Status code đúng (200/201/4xx theo kỳ vọng)
   - Response schema/field quan trọng đúng định dạng
   - Thời gian phản hồi nhỏ hơn ngưỡng đặt ra
5. Chạy toàn bộ collection trong Postman để xác nhận logic test.
6. Export collection + environment ra file JSON.
7. Chạy tự động bằng Newman từ command line.
8. Thu thập kết quả pass/fail, response time, error rate.
9. Chạy load test cơ bản bằng công cụ phù hợp (k6/JMeter/Artillery) để đánh giá tải.
10. Tổng hợp báo cáo QA và đề xuất cải thiện endpoint chậm/lỗi.

## Chạy mã nguồn Flask thực hành

```powershell
cd g:\2526II_INT3505_1\tuan8
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

API chạy tại `http://localhost:5000`.

## Bộ endpoint mẫu cho bài thực hành

- `GET /products`
- `GET /products/{id}`
- `POST /products`
- `PUT /products/{id}`
- `DELETE /products/{id}`

### JSON mẫu cho `POST /products` và `PUT /products/{id}`

```json
{
  "name": "Mouse",
  "description": "Wireless mouse",
  "price": 19.9,
  "inStock": true
}
```

## Mẫu test script trong Postman

```javascript
pm.test("Status code is 200", function () {
  pm.response.to.have.status(200);
});

pm.test("Response time < 500ms", function () {
  pm.expect(pm.response.responseTime).to.be.below(500);
});
```

## Chạy test tự động bằng Newman

```powershell
cd g:\2526II_INT3505_1\tuan8
npm init -y
npm install --save-dev newman
npx newman run .\postman\week8_collection.json -e .\postman\week8_environment.json
```

Ví dụ xuất báo cáo HTML:

```powershell
npm install --save-dev newman-reporter-htmlextra
npx newman run .\postman\week8_collection.json -e .\postman\week8_environment.json -r cli,htmlextra --reporter-htmlextra-export .\reports\week8-report.html
```

## Tiêu chí hoàn thành Tuần 8

- Có collection Postman với đủ 5 endpoint
- Mỗi endpoint có assertions cho status code và dữ liệu trả về
- Chạy Newman thành công từ command line
- Có số liệu response time và error rate để đánh giá chất lượng API

cd g:\2526II_INT3505_1\tuan8
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
