# K6 Test Result

Kich ban da chay:

- Script: [k6_users_50vus_30s.js](/g:/2526II_INT3505_1/tuan8/loadtest/k6_users_50vus_30s.js)
- API: `GET https://jsonplaceholder.typicode.com/users`
- Cau hinh: `50` virtual users trong `30` giay

File tong ket:

- [k6-users-summary.json](/g:/2526II_INT3505_1/tuan8/reports/k6-users-summary.json)

Ket qua chinh:

| Chi so | Gia tri |
| --- | --- |
| Avg Response | `110.36 ms` |
| P95 Response | `175.43 ms` |
| Max Response | `816.28 ms` |
| Error Rate | `0%` |
| Requests | `1349` |
| Req/sec | `44.59 req/s` |
| Concurrent Users | `50` |
| Checks | `2698/2698 passed` |

Danh gia:

- API dap ung on dinh trong bai test `50 users / 30 giay`
- Khong ghi nhan request loi
- Avg response time nam thap hon nguong `1000 ms`
- P95 cung nam thap hon nguong `1500 ms`

Mau mo ta ngan de dua vao bao cao:

```text
Da thuc hien load test bang k6 voi 50 virtual users trong 30 giay cho endpoint GET /users.
Ket qua ghi nhan 1349 requests, throughput trung binh 44.59 req/s, Avg Response 110.36 ms va Error Rate 0%.
Tat ca checks deu dat, cho thay API hoat dong on dinh o muc tai da kiem thu.
```
