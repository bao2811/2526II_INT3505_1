# Phân tích 3 Public API phổ biến

## 1. GitHub REST API

### Tổng quan

GitHub cung cấp REST API và GraphQL API cho phép truy cập dữ liệu repository, user, issue, pull request và nhiều tài nguyên khác.

Base URL:

```
https://api.github.com
```

### Kiến trúc

- Protocol: HTTPS
- Data format: JSON
- Authentication: Token / OAuth
- HTTP Methods: GET, POST, PATCH, DELETE

### Endpoint phổ biến

#### Repository

```
GET /repos/{owner}/{repo}
```

Ví dụ:

```
GET https://api.github.com/repos/octocat/Hello-World
```

Response mẫu:

```json
{
  "id": 1296269,
  "name": "Hello-World",
  "full_name": "octocat/Hello-World",
  "private": false
}
```

#### Issues

```
GET /repos/{owner}/{repo}/issues
```

#### Pull Requests

```
GET /repos/{owner}/{repo}/pulls
```

#### Users

```
GET /users/{username}
```

### Authentication

GitHub hỗ trợ:

- Personal Access Token
- OAuth
- GitHub App

Header ví dụ:

```
Authorization: Bearer <token>
```

### Rate Limit

| Loại                 | Limit             |
| -------------------- | ----------------- |
| Không authentication | 60 request/hour   |
| Có authentication    | 5000 request/hour |

### Ví dụ sử dụng Node.js

```javascript
const axios = require("axios");

axios.get("https://api.github.com/users/octocat").then((res) => {
  console.log(res.data);
});
```

### Use cases

- DevOps dashboard
- CI/CD automation
- Code analytics
- Repository management

### Ưu điểm

- Documentation tốt
- Ecosystem lớn
- Hỗ trợ REST và GraphQL

### Nhược điểm

- Rate limit chặt
- Một số endpoint phức tạp

---

# 2. OpenWeather API

## Tổng quan

OpenWeather cung cấp dữ liệu thời tiết toàn cầu như:

- Current weather
- Forecast
- Historical weather
- Air pollution

Base URL:

```
https://api.openweathermap.org
```

## Kiến trúc

- Protocol: HTTPS
- Format: JSON / XML
- Authentication: API key
- Method: GET

## Endpoint phổ biến

### Current Weather

```
GET /data/2.5/weather
```

Ví dụ:

```
https://api.openweathermap.org/data/2.5/weather?q=London&appid=API_KEY
```

Response mẫu:

```json
{
  "weather": [{ "main": "Clouds" }],
  "main": {
    "temp": 28.5,
    "humidity": 75
  }
}
```

### Forecast

```
GET /data/2.5/forecast
```

### One Call API

```
/data/3.0/onecall
```

## Parameters phổ biến

| Parameter | Ý nghĩa           |
| --------- | ----------------- |
| q         | city name         |
| lat       | latitude          |
| lon       | longitude         |
| units     | metric / imperial |
| lang      | language          |

## Authentication

Mọi request cần API key:

```
appid=YOUR_API_KEY
```

## Use cases

- Weather apps
- Agriculture systems
- Travel apps
- Smart home

## Ưu điểm

- Dữ liệu toàn cầu
- Dễ tích hợp

## Nhược điểm

- Free tier hạn chế
- Rate limit thấp

---

# 3. Google Maps Platform API

## Tổng quan

Google Maps Platform cung cấp các dịch vụ bản đồ và định vị.

Các API chính:

- Maps JavaScript API
- Geocoding API
- Directions API
- Places API
- Distance Matrix API

## Kiến trúc

- Protocol: HTTPS
- Authentication: API key / OAuth
- Data format: JSON

## Endpoint phổ biến

### Geocoding API

Chuyển địa chỉ thành tọa độ.

```
https://maps.googleapis.com/maps/api/geocode/json
```

Ví dụ:

```
https://maps.googleapis.com/maps/api/geocode/json?address=Hanoi&key=API_KEY
```

Response mẫu:

```json
{
  "results": [
    {
      "geometry": {
        "location": {
          "lat": 21.0278,
          "lng": 105.8342
        }
      }
    }
  ]
}
```

### Directions API

```
/maps/api/directions/json
```

### Places API

```
/maps/api/place/nearbysearch/json
```

## Rate Limit

Tùy vào quota của Google Cloud.

Ví dụ:

- 3 queries/second
- 180 queries/minute

## Use cases

- Ride-sharing apps
- Navigation systems
- Logistics
- Delivery apps

## Ưu điểm

- Bản đồ chính xác
- Nhiều dịch vụ

## Nhược điểm

- Cần bật billing
- Pricing phức tạp

---

# So sánh 3 API

| Tiêu chí       | GitHub API         | OpenWeather API | Google Maps API |
| -------------- | ------------------ | --------------- | --------------- |
| Lĩnh vực       | Developer platform | Weather data    | Mapping         |
| Authentication | Token/OAuth        | API key         | API key/OAuth   |
| Format         | JSON               | JSON/XML        | JSON            |
| Rate limit     | 5000 req/hour      | Plan-based      | Quota-based     |

---

# Kết luận

Ba API này đại diện cho ba loại public API phổ biến:

1. Developer API – GitHub
2. Data service API – OpenWeather
3. Platform service API – Google Maps

Chúng minh họa các đặc điểm phổ biến của hệ thống API hiện đại:

- RESTful architecture
- API authentication
- Rate limiting
- JSON-based communication
