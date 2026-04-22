# Lenh Test va Lay Ket Qua

Tai lieu nay tong hop cac lenh can dung de chay test va lay ket qua trong bai thuc hanh tuan 8.

## 1. Test chuc nang bang Newman

### Cai Newman

```powershell
cd g:\2526II_INT3505_1\tuan8
npm.cmd init -y
npm.cmd install --save-dev newman newman-reporter-html
```

### Chay collection `users`

```powershell
cd g:\2526II_INT3505_1\tuan8
.\node_modules\.bin\newman.cmd run .\postman\week8_users_collection.json
```

### Chay va xuat bao cao HTML

```powershell
cd g:\2526II_INT3505_1\tuan8
New-Item -ItemType Directory -Force .\reports
.\node_modules\.bin\newman.cmd run .\postman\week8_users_collection.json -r cli,html --reporter-html-export .\reports\week8-users-report.html
```

### File ket qua Newman

- [week8-users-report.html](/g:/2526II_INT3505_1/tuan8/reports/week8-users-report.html)

## 2. Load test bang k6

### Cai k6 tren Windows

```powershell
winget install k6 --source winget
```

### Kiem tra k6

```powershell
& 'C:\Program Files\k6\k6.exe' version
```

### Chay load test `50 users / 30s`

```powershell
cd g:\2526II_INT3505_1\tuan8
& 'C:\Program Files\k6\k6.exe' run .\loadtest\k6_users_50vus_30s.js --summary-export .\reports\k6-users-summary.json
```

### File ket qua k6

- [k6-users-summary.json](/g:/2526II_INT3505_1/tuan8/reports/k6-users-summary.json)
- [K6_TEST_RESULT.md](/g:/2526II_INT3505_1/tuan8/reports/K6_TEST_RESULT.md)

## 3. Lay so lieu tu file ket qua k6

### Xem toan bo file JSON

```powershell
Get-Content g:\2526II_INT3505_1\tuan8\reports\k6-users-summary.json
```

### Xem rieng phan metrics

```powershell
Get-Content g:\2526II_INT3505_1\tuan8\reports\k6-users-summary.json | ConvertFrom-Json | Select-Object -ExpandProperty metrics | ConvertTo-Json -Depth 6
```

## 4. Test bo local `products`

### Chay app local

```powershell
cd g:\2526II_INT3505_1\tuan8
python app.py
```

### Chay Newman cho `products`

Mo mot terminal khac:

```powershell
cd g:\2526II_INT3505_1\tuan8
.\node_modules\.bin\newman.cmd run .\postman\week8_collection.json -e .\postman\week8_environment.json
```

## 5. Tom tat nhanh

### Newman

```powershell
.\node_modules\.bin\newman.cmd run .\postman\week8_users_collection.json -r cli,html --reporter-html-export .\reports\week8-users-report.html
```

### k6

```powershell
& 'C:\Program Files\k6\k6.exe' run .\loadtest\k6_users_50vus_30s.js --summary-export .\reports\k6-users-summary.json
```
