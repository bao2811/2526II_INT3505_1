# Pagination Demo (Flask + MySQL)

Demo cac loai phan trang tren bang `users` voi 1,000,000 ban ghi. Moi endpoint tra ve `data` va `performance.duration_ms` de so sanh toc do.

## Yeu cau

- Python 3.7+
- MySQL/MariaDB 5.7+

## Cac buoc chay demo

### Buoc 1: Tao venv va cai thu vien

```powershell
cd demo_pagination
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Buoc 2: Tao database va du lieu

Chay tu terminal (khong phai MySQL shell):

```powershell
mysql -u root -p < database.sql
```

Kiem tra tong ban ghi:

```powershell
mysql -u root -p pagination_demo -e "SELECT COUNT(*) AS total_records FROM users;"
```

Mong doi: `1000000`.

### Buoc 3: Tao file .env

Tao file `.env` trong demo_pagination:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=bao12345
DB_NAME=pagination_demo
DB_PORT=3306
PORT=3000
```

### Buoc 4: Chay server

```powershell
.\.venv\Scripts\python.exe app.py
```

Mo:

- http://localhost:3000
- http://localhost:3000/api/pagination/docs

## Demo cac loai paging

Tat ca response co `performance.duration_ms`.

### Offset/Limit pagination

Cach lam: truyen truc tiep `offset` va `limit`, phu hop UI co the nhay vi tri, nhung cham khi offset lon.

```bash
curl "http://localhost:3000/api/pagination/offset?offset=0&limit=20"
```

### Cursor pagination

Cach lam: dung `last_id` de danh dau vi tri hien tai, truy van `WHERE id > last_id`. Nhanh va on dinh khi du lieu thay doi, nhung khong nhay trang tuy y.

```bash
curl "http://localhost:3000/api/pagination/cursor?limit=20&last_id=0"
```

Lay `next_last_id` tu response, goi trang tiep theo:

```bash
curl "http://localhost:3000/api/pagination/cursor?limit=20&last_id=20"
```

### Page-based

Tuong tu offset/limit, nhung dung tham so `page` va `per_page`. De hieu voi nguoi dung web, nhung van cham khi page lon.

```bash
curl "http://localhost:3000/api/pagination/page-based?page=1&per_page=20"
```

## Test nhanh toc do

```bash
curl "http://localhost:3000/api/pagination/offset?offset=0&limit=100"
curl "http://localhost:3000/api/pagination/offset?offset=500000&limit=100"
curl "http://localhost:3000/api/pagination/cursor?limit=100&last_id=0"
```

## Mo ta API (OpenAPI)

File dac ta: [demo_pagination/pagination_api.yaml](demo_pagination/pagination_api.yaml)

## Ghi chu

- Nếu muon tao lai du lieu, chay lai [demo_pagination/database.sql](demo_pagination/database.sql) (script co `DROP DATABASE`).
- Gioi han `limit` toi da 100 de tranh qua tai.

**Cap nhat**: 2026-04-09
