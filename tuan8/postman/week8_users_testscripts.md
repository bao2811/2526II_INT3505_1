# Week 8 Users Test Scripts

Base URL: `https://jsonplaceholder.typicode.com`

Collection goc: [week8_users_collection.json](/g:/2526II_INT3505_1/tuan8/postman/week8_users_collection.json)

## 1. GET /users

Request:

```http
GET {{baseUrl}}/users
```

Test script:

```javascript
pm.test("Status code is 200", function () {
  pm.response.to.have.status(200);
});

pm.test("Response time below configured threshold", function () {
  const threshold = Number(pm.collectionVariables.get("responseTimeThreshold") || 500);
  pm.expect(pm.response.responseTime).to.be.below(threshold);
});

pm.test("Body is a non-empty array", function () {
  const body = pm.response.json();
  pm.expect(body).to.be.an("array");
  pm.expect(body.length).to.be.greaterThan(0);
});

pm.test("First user has required fields", function () {
  const user = pm.response.json()[0];
  pm.expect(user.id).to.be.a("number");
  pm.expect(user.name).to.be.a("string").and.not.empty;
  pm.expect(user.username).to.be.a("string").and.not.empty;
  pm.expect(user.email).to.be.a("string").and.include("@");
  pm.expect(user.address).to.be.an("object");
  pm.expect(user.company).to.be.an("object");
});
```

## 2. GET /users/1

Request:

```http
GET {{baseUrl}}/users/{{userId}}
```

Test script:

```javascript
pm.test("Status code is 200", function () {
  pm.response.to.have.status(200);
});

pm.test("Response time below configured threshold", function () {
  const threshold = Number(pm.collectionVariables.get("responseTimeThreshold") || 500);
  pm.expect(pm.response.responseTime).to.be.below(threshold);
});

pm.test("Returned user matches requested id", function () {
  const body = pm.response.json();
  pm.expect(body.id).to.eql(Number(pm.collectionVariables.get("userId")));
  pm.expect(body.name).to.be.a("string").and.not.empty;
  pm.expect(body.username).to.be.a("string").and.not.empty;
  pm.expect(body.email).to.be.a("string").and.include("@");
});

pm.test("Address and company objects are present", function () {
  const body = pm.response.json();
  pm.expect(body.address).to.be.an("object");
  pm.expect(body.address.city).to.be.a("string");
  pm.expect(body.company).to.be.an("object");
  pm.expect(body.company.name).to.be.a("string");
});
```

## 3. POST /users

Request:

```http
POST {{baseUrl}}/users
Content-Type: application/json; charset=UTF-8
```

Body:

```json
{
  "name": "Le Thi Test",
  "username": "lethitest",
  "email": "lethi.test@example.com",
  "address": {
    "street": "123 Nguyen Trai",
    "suite": "Apt. 8",
    "city": "Ho Chi Minh",
    "zipcode": "700000"
  },
  "phone": "0900000000",
  "website": "example.vn",
  "company": {
    "name": "INT3505 QA Team"
  }
}
```

Test script:

```javascript
pm.test("Status code is 201", function () {
  pm.response.to.have.status(201);
});

pm.test("Response time below configured threshold", function () {
  const threshold = Number(pm.collectionVariables.get("responseTimeThreshold") || 500);
  pm.expect(pm.response.responseTime).to.be.below(threshold);
});

pm.test("Created user payload is echoed back", function () {
  const body = pm.response.json();
  pm.expect(body.id).to.exist;
  pm.expect(body.name).to.eql("Le Thi Test");
  pm.expect(body.username).to.eql("lethitest");
  pm.expect(body.email).to.eql("lethi.test@example.com");
});
```

## 4. PUT /users/1

Request:

```http
PUT {{baseUrl}}/users/{{userId}}
Content-Type: application/json; charset=UTF-8
```

Body:

```json
{
  "id": 1,
  "name": "Le Thi Updated",
  "username": "lethiupdated",
  "email": "updated@example.com",
  "address": {
    "street": "456 Tran Hung Dao",
    "suite": "Suite 10",
    "city": "Da Nang",
    "zipcode": "550000"
  },
  "phone": "0911111111",
  "website": "updated.vn",
  "company": {
    "name": "INT3505 Updated Team"
  }
}
```

Test script:

```javascript
pm.test("Status code is 200", function () {
  pm.response.to.have.status(200);
});

pm.test("Response time below configured threshold", function () {
  const threshold = Number(pm.collectionVariables.get("responseTimeThreshold") || 500);
  pm.expect(pm.response.responseTime).to.be.below(threshold);
});

pm.test("Updated user payload is returned", function () {
  const body = pm.response.json();
  pm.expect(body.id).to.eql(Number(pm.collectionVariables.get("userId")));
  pm.expect(body.name).to.eql("Le Thi Updated");
  pm.expect(body.username).to.eql("lethiupdated");
  pm.expect(body.email).to.eql("updated@example.com");
  pm.expect(body.address.city).to.eql("Da Nang");
  pm.expect(body.company.name).to.eql("INT3505 Updated Team");
});
```

## 5. DELETE /users/1

Request:

```http
DELETE {{baseUrl}}/users/{{userId}}
```

Test script:

```javascript
pm.test("Status code is 200", function () {
  pm.response.to.have.status(200);
});

pm.test("Response time below configured threshold", function () {
  const threshold = Number(pm.collectionVariables.get("responseTimeThreshold") || 500);
  pm.expect(pm.response.responseTime).to.be.below(threshold);
});

pm.test("Delete response body is valid", function () {
  const text = pm.response.text();
  if (!text) {
    pm.expect(text).to.eql("");
    return;
  }

  const body = pm.response.json();
  pm.expect(body).to.be.an("object");
});
```
