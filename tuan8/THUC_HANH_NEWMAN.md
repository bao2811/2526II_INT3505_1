# Thuc Hanh Newman - Week 8

Tai lieu nay huong dan tao collection, chay kiem thu API bang Newman va tong hop ket qua cho bo `users` su dung JSONPlaceholder.

## 1. Muc tieu

- Chay Postman Collection bang dong lenh voi Newman
- Kiem tra 5 endpoint cua API `users`
- Theo doi so request, assertions va failures
- Luu ket qua de dua vao bao cao thuc hanh

## 2. Collection su dung

Collection da tao san:

- [week8_users_collection.json](/g:/2526II_INT3505_1/tuan8/postman/week8_users_collection.json)
- [week8_users_testscripts.md](/g:/2526II_INT3505_1/tuan8/postman/week8_users_testscripts.md)

Cau truc collection:

```text
Week 8 - JSONPlaceholder Users Testing
|-- 1. GET /users
|-- 2. GET /users/1
|-- 3. POST /users
|-- 4. PUT /users/1
`-- 5. DELETE /users/1
```

Collection nay da tu khai bao:

- `baseUrl = https://jsonplaceholder.typicode.com`
- `userId = 1`
- `responseTimeThreshold = 1000`

Vi vay khi chay Newman khong can them file environment rieng.

## 3. Chuan bi moi truong

Yeu cau:

- Da cai Node.js
- Co ket noi internet de goi API JSONPlaceholder

Mo PowerShell tai thu muc `tuan8`:

```powershell
cd g:\2526II_INT3505_1\tuan8
```

Khoi tao `package.json` neu thu muc chua co:

```powershell
npm init -y
```

Cai Newman:

```powershell
npm install --save-dev newman
```

Neu muon xuat bao cao HTML:

```powershell
npm install --save-dev newman-reporter-html
```

## 4. Chay collection bang Newman

### Cach 1: Chi hien ket qua tren terminal

```powershell
npx newman run .\postman\week8_users_collection.json
```

Lenh nay se chay 5 request trong collection va in ket qua pass/fail ngay tren man hinh.

### Cach 2: Hien thi them bao cao JSON

```powershell
npx newman run .\postman\week8_users_collection.json -r cli,json --reporter-json-export .\reports\week8-users-report.json
```

Neu thu muc `reports` chua ton tai, tao truoc:

```powershell
New-Item -ItemType Directory -Force .\reports
```

### Cach 3: Xuat bao cao HTML

```powershell
npx newman run .\postman\week8_users_collection.json -r cli,html --reporter-html-export .\reports\week8-users-report.html
```

## 5. Giai thich ket qua

Sau khi chay Newman, ban se thay cac thong tin chinh:

- `iterations`: so lan chay collection
- `requests`: tong so request da gui
- `test-scripts`: tong so block test duoc thuc thi
- `assertions`: tong so dieu kien kiem tra
- `failures`: tong so loi phat sinh

Cach danh gia:

- `failures = 0`: tat ca test deu pass
- `failures > 0`: co it nhat mot assertion that bai
- response time vuot nguong `1000ms`: test ve hieu nang se fail

## 6. Ket qua mong doi

Voi collection `users`, ket qua mong doi la:

- 5 requests duoc chay
- Tat ca assertions pass
- `failures = 0`

Vi day la API public de hoc tap, cac request `POST`, `PUT`, `DELETE` chi mo phong ghi du lieu. Nghia la API tra ve response thanh cong, nhung du lieu tren server khong thay doi that sau khi chay xong.

## 7. Mau trinh bay bao cao

Ban co the dua vao bao cao ngan nhu sau:

```text
Da su dung Newman de chay collection "Week 8 - JSONPlaceholder Users Testing".
Collection gom 5 request: GET /users, GET /users/1, POST /users, PUT /users/1, DELETE /users/1.
Ket qua chay cho thay tat ca test cases deu passed, khong co failures.
Dieu nay xac nhan cac endpoint users hoat dong dung theo cac dieu kien kiem thu da dat ra.
```

## 8. Lenh day du de thuc hanh nhanh

```powershell
cd g:\2526II_INT3505_1\tuan8
npm init -y
npm install --save-dev newman
npx newman run .\postman\week8_users_collection.json
```

Neu muon co file bao cao HTML:

```powershell
cd g:\2526II_INT3505_1\tuan8
npm install --save-dev newman-reporter-html
New-Item -ItemType Directory -Force .\reports
npx newman run .\postman\week8_users_collection.json -r cli,html --reporter-html-export .\reports\week8-users-report.html
```

## 9. Ghi chu bo sung

- Neu ban muon chay bo local `products`, su dung:

```powershell
npx newman run .\postman\week8_collection.json -e .\postman\week8_environment.json
```

- Bo `products` can app Flask trong [app.py](/g:/2526II_INT3505_1/tuan8/app.py) dang chay tai `http://localhost:5000`.
- Bo `users` khong can chay server local vi dung API public.

## 10. Phan hieu nang va QA

Tai lieu va script bo sung:

- [HIEU_NANG_QA.md](/g:/2526II_INT3505_1/tuan8/HIEU_NANG_QA.md)
- [k6_users_50vus_30s.js](/g:/2526II_INT3505_1/tuan8/loadtest/k6_users_50vus_30s.js)

Phan nay dung de trinh bay load test `50 users / 30 giay` bang `k6` va quy trinh QA doanh nghiep sau khi da hoan thanh test chuc nang bang Newman.
