# Hieu Nang & Quy Trinh QA

Tai lieu nay bo sung phan kiem thu hieu nang va quy trinh QA cho bai thuc hanh tuan 8.

## 1. Muc tieu

- Do hieu nang API `users` bang `k6`
- Mo phong `50` nguoi dung ao trong `30 giay`
- Theo doi cac chi so: response time, error rate, throughput
- Mo ta quy trinh QA tu phat trien den van hanh

## 2. Kich ban load test

Script da tao san:

- [k6_users_50vus_30s.js](/g:/2526II_INT3505_1/tuan8/loadtest/k6_users_50vus_30s.js)

Cau hinh chinh:

- API test: `GET https://jsonplaceholder.typicode.com/users`
- So user dong thoi: `50`
- Thoi gian test: `30s`
- Cong cu: `k6`

Script su dung mo hinh `constant-vus` cua k6, phu hop voi bai toan giu on dinh `50` VUs trong suot thoi gian chay. Theo tai lieu chinh thuc cua Grafana k6, co the dat `vus` va `duration` trong script hoac khi chay CLI; `constant-vus` la executor danh cho so user dong thoi co dinh. Nguon: Grafana k6 docs ve [running k6](https://grafana.com/docs/k6/latest/get-started/running-k6/) va [constant-vus](https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/constant-vus/).

## 3. Cai dat k6 tren Windows

Theo tai lieu chinh thuc cua Grafana k6, tren Windows co the cai bang `winget`:

```powershell
winget install k6 --source winget
```

Sau khi cai xong, kiem tra:

```powershell
k6 version
```

Nguon: [Install k6](https://grafana.com/docs/k6/latest/set-up/install-k6/).

## 4. Cach chay load test

Mo PowerShell tai thu muc `tuan8`:

```powershell
cd g:\2526II_INT3505_1\tuan8
```

Chay script:

```powershell
k6 run .\loadtest\k6_users_50vus_30s.js --summary-export .\reports\k6-users-summary.json
```

Neu muon doi `baseUrl`, co the truyen bien moi truong:

```powershell
$env:BASE_URL="https://jsonplaceholder.typicode.com"
k6 run .\loadtest\k6_users_50vus_30s.js --summary-export .\reports\k6-users-summary.json
```

Sau khi chay xong, k6 se in tong ket ra terminal va luu file tong ket tai:

- [k6-users-summary.json](/g:/2526II_INT3505_1/tuan8/reports/k6-users-summary.json)

Luu y: file tren se chi xuat hien sau khi ban chay `k6` thanh cong.

## 5. Mau trinh bay ket qua hieu nang

Ban co the dua phan nay vao slide hoac bao cao:

```text
Do hieu nang voi k6 - 50 users - 30 giay

Avg Response : dien tu http_req_duration.avg
Error Rate   : dien tu http_req_failed.rate
Req/sec      : dien tu http_reqs.rate
Concurrent   : 50 users
```

Bang tom tat:

| Chi so | Nguon du lieu k6 | Y nghia |
| --- | --- | --- |
| Avg Response | `http_req_duration.avg` | Thoi gian phan hoi trung binh |
| Error Rate | `http_req_failed.rate` | Ty le request loi |
| Req/sec | `http_reqs.rate` | So request trung binh moi giay |
| Concurrent | cau hinh `vus: 50` | So nguoi dung ao dong thoi |

Mau ket luan ngan:

```text
Load test duoc thuc hien bang k6 voi 50 users trong 30 giay.
He thong duoc theo doi qua cac chi so Avg Response, Error Rate va Req/sec.
Neu Error Rate = 0% va Avg Response nam trong nguong chap nhan, API duoc xem la dap ung tot o muc tai da kiem thu.
```

## 6. Quy trinh QA doanh nghiep

Ban co the trinh bay quy trinh QA theo 5 buoc sau:

1. Developer viet API.
2. Tester tao test case.
3. Chay Postman/Newman de xac minh logic API.
4. Load test tren moi truong staging bang k6.
5. Deploy va monitoring de theo doi van hanh thuc te.

Mau trinh bay ngan:

```text
Quy trinh QA doanh nghiep bat dau tu giai doan developer hoan thanh API.
Sau do tester xay dung test case va thuc thi bo test Postman/Newman.
Khi cac test chuc nang dat yeu cau, he thong duoc load test tren staging bang k6.
Cuoi cung, ung dung duoc deploy va theo doi lien tuc qua monitoring de phat hien som loi hoac suy giam hieu nang.
```

## 7. Moi lien he voi bo test Newman

Phan chuc nang:

- [week8_users_collection.json](/g:/2526II_INT3505_1/tuan8/postman/week8_users_collection.json)
- [week8_users_testscripts.md](/g:/2526II_INT3505_1/tuan8/postman/week8_users_testscripts.md)
- [THUC_HANH_NEWMAN.md](/g:/2526II_INT3505_1/tuan8/THUC_HANH_NEWMAN.md)

Phan hieu nang:

- [k6_users_50vus_30s.js](/g:/2526II_INT3505_1/tuan8/loadtest/k6_users_50vus_30s.js)
- [HIEU_NANG_QA.md](/g:/2526II_INT3505_1/tuan8/HIEU_NANG_QA.md)

Tach rieng hai lop kiem thu:

- Newman dung de test tinh dung cua API
- k6 dung de test kha nang chiu tai va toc do phan hoi

## 8. Ghi chu

- Hien tai may dang chua cai `k6`, nen script da duoc tao nhung chua chay thuc te trong workspace.
- Khi ban cai `k6`, chi can chay lai lenh o muc 4 de sinh ket qua that.
