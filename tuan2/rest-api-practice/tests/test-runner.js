// tests/test-runner.js
// ============================================================
// Test thu cong (khong can thu vien test)
// Chay: node tests/test-runner.js
// Luu y: Dam bao server dang chay tren PORT 3000 truoc
// ============================================================

const http = require("http");

const BASE_URL = "http://localhost:3000";
let passed = 0;
let failed = 0;

// ===================== Helper: Gui HTTP request =====================
function request(method, path, body = null, headers = {}) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, BASE_URL);
    const options = {
      hostname: url.hostname,
      port: url.port || 80,
      path: url.pathname + url.search,
      method,
      headers: {
        "Content-Type": "application/json",
        ...headers,
      },
    };

    const req = http.request(options, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => {
        try {
          resolve({
            status: res.statusCode,
            headers: res.headers,
            body: JSON.parse(data),
          });
        } catch {
          resolve({ status: res.statusCode, headers: res.headers, body: data });
        }
      });
    });

    req.on("error", reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

// ===================== Helper: Kiem tra ket qua =====================
function assert(condition, testName, detail = "") {
  if (condition) {
    console.log(`  ✅ PASS: ${testName}`);
    passed++;
  } else {
    console.log(`  ❌ FAIL: ${testName}${detail ? " → " + detail : ""}`);
    failed++;
  }
}

// ===================== TEST CASES =====================

async function runTests() {
  console.log("\n" + "=".repeat(60));
  console.log("  REST API Practice - Test Runner");
  console.log("=".repeat(60) + "\n");

  // ------------------------------------------------------------------
  // NHOM 1: TRANG CHU & API INFO
  // ------------------------------------------------------------------
  console.log("📦 Nhom 1: Trang chu & API info");

  let res = await request("GET", "/");
  assert(res.status === 200, "GET / → 200 OK");
  assert(res.body._links !== undefined, "GET / → co _links (HATEOAS)");

  res = await request("GET", "/api/v1");
  assert(res.status === 200, "GET /api/v1 → 200 OK");

  // ------------------------------------------------------------------
  // NHOM 2: USERS — Lay danh sach (Tinh huong 1)
  // ------------------------------------------------------------------
  console.log("\n👥 Nhom 2: Users - Lay danh sach (Tinh huong 1)");

  res = await request("GET", "/api/v1/users", null, {
    Authorization: "Bearer token-admin",
  });
  assert(res.status === 200, "GET /api/v1/users (admin) → 200");
  assert(Array.isArray(res.body.data), "GET /users → body.data la array");
  assert(res.body.pagination !== undefined, "GET /users → co pagination");

  // Phan trang
  res = await request("GET", "/api/v1/users?page=1&limit=2", null, {
    Authorization: "Bearer token-admin",
  });
  assert(res.status === 200, "GET /users?page=1&limit=2 → 200");
  assert(res.body.data.length <= 2, "GET /users?limit=2 → tra ve <= 2 ket qua");

  // Filter theo department
  res = await request("GET", "/api/v1/users?department=Engineering", null, {
    Authorization: "Bearer token-admin",
  });
  assert(res.status === 200, "GET /users?department=Engineering → 200");

  // Khong co token → 401
  res = await request("GET", "/api/v1/users");
  assert(res.status === 401, "GET /users (no token) → 401 Unauthorized");
  assert(res.body.error === "UNAUTHORIZED", "401 → error: UNAUTHORIZED");

  // Token sai → 401
  res = await request("GET", "/api/v1/users", null, {
    Authorization: "Bearer invalid-token",
  });
  assert(res.status === 401, "GET /users (invalid token) → 401");

  // ------------------------------------------------------------------
  // NHOM 3: USERS — Lay mot user
  // ------------------------------------------------------------------
  console.log("\n👤 Nhom 3: Users - Lay mot user");

  res = await request("GET", "/api/v1/users/usr_001", null, {
    Authorization: "Bearer token-admin",
  });
  assert(res.status === 200, "GET /users/usr_001 → 200");
  assert(res.body.data.id === "usr_001", "GET /users/usr_001 → dung id");
  assert(
    res.body._links !== undefined,
    "GET /users/usr_001 → co _links (HATEOAS)",
  );

  // User khong ton tai → 404
  res = await request("GET", "/api/v1/users/usr_999", null, {
    Authorization: "Bearer token-admin",
  });
  assert(res.status === 404, "GET /users/usr_999 → 404 Not Found");
  assert(res.body.error === "USER_NOT_FOUND", "404 → error: USER_NOT_FOUND");

  // ------------------------------------------------------------------
  // NHOM 4: USERS — Tao moi (Tinh huong POST)
  // ------------------------------------------------------------------
  console.log("\n➕ Nhom 4: Users - Tao moi");

  const newUserData = {
    name: "Test User ABC",
    email: `test_${Date.now()}@example.com`,
    department: "QA",
    age: 25,
  };

  // Chi admin moi tao duoc
  res = await request("POST", "/api/v1/users", newUserData, {
    Authorization: "Bearer token-admin",
  });
  assert(res.status === 201, "POST /users (admin) → 201 Created");
  assert(
    res.headers.location !== undefined,
    "POST /users → co Location header",
  );
  const createdUserId = res.body.data?.id;

  // User thuong khong tao duoc → 403
  res = await request("POST", "/api/v1/users", newUserData, {
    Authorization: "Bearer token-user",
  });
  assert(res.status === 403, "POST /users (user) → 403 Forbidden");

  // Email da ton tai → 409
  res = await request(
    "POST",
    "/api/v1/users",
    {
      name: "Duplicate",
      email: "nvan@example.com",
      age: 20,
    },
    { Authorization: "Bearer token-admin" },
  );
  assert(res.status === 409, "POST /users (email trung) → 409 Conflict");
  assert(
    res.body.error === "EMAIL_ALREADY_EXISTS",
    "409 → error: EMAIL_ALREADY_EXISTS",
  );

  // Email sai format → 422
  res = await request(
    "POST",
    "/api/v1/users",
    {
      name: "Test",
      email: "not-an-email",
      age: 20,
    },
    { Authorization: "Bearer token-admin" },
  );
  assert(
    res.status === 422,
    "POST /users (email sai) → 422 Unprocessable Entity",
  );
  assert(
    res.body.error === "VALIDATION_ERROR",
    "422 → error: VALIDATION_ERROR",
  );

  // Thieu name → 422
  res = await request(
    "POST",
    "/api/v1/users",
    {
      email: `noname_${Date.now()}@example.com`,
    },
    { Authorization: "Bearer token-admin" },
  );
  assert(res.status === 422, "POST /users (thieu name) → 422");

  // ------------------------------------------------------------------
  // NHOM 5: USERS — Cap nhat email (Tinh huong 2 - PATCH)
  // ------------------------------------------------------------------
  console.log("\n✏️  Nhom 5: Users - Cap nhat email (Tinh huong 2 PATCH)");

  if (createdUserId) {
    const newEmail = `updated_${Date.now()}@example.com`;

    res = await request(
      "PATCH",
      `/api/v1/users/${createdUserId}`,
      { email: newEmail },
      { Authorization: "Bearer token-admin" },
    );
    assert(res.status === 200, "PATCH /users/:id (admin) → 200");
    assert(res.body.data.email === newEmail, "PATCH /users/:id → email da doi");

    // Email trung → 409
    res = await request(
      "PATCH",
      `/api/v1/users/${createdUserId}`,
      { email: "ttbich@example.com" },
      { Authorization: "Bearer token-admin" },
    );
    assert(res.status === 409, "PATCH /users/:id (email trung) → 409");

    // Email sai format → 422
    res = await request(
      "PATCH",
      `/api/v1/users/${createdUserId}`,
      { email: "bad-email" },
      { Authorization: "Bearer token-admin" },
    );
    assert(res.status === 422, "PATCH /users/:id (email sai format) → 422");
  }

  // ------------------------------------------------------------------
  // NHOM 6: USERS — Xoa (Tinh huong 4 - DELETE)
  // ------------------------------------------------------------------
  console.log("\n🗑️  Nhom 6: Users - Xoa (Tinh huong 4 - Soft Delete)");

  if (createdUserId) {
    res = await request("DELETE", `/api/v1/users/${createdUserId}`, null, {
      Authorization: "Bearer token-admin",
    });
    assert(res.status === 200, "DELETE /users/:id (admin) → 200");
    assert(res.body.user.status === "DELETED", "DELETE → status: DELETED");
    assert(
      res.body._actions?.restore !== undefined,
      "DELETE → co _actions.restore (HATEOAS)",
    );

    // Xoa lan 2 → 410 Gone (da xoa roi)
    res = await request("DELETE", `/api/v1/users/${createdUserId}`, null, {
      Authorization: "Bearer token-admin",
    });
    assert(res.status === 410, "DELETE /users/:id lan 2 → 410 Gone");

    // User thuong khong xoa duoc → 403
    res = await request("DELETE", "/api/v1/users/usr_003", null, {
      Authorization: "Bearer token-user",
    });
    assert(res.status === 403, "DELETE /users (user thuong) → 403 Forbidden");
  }

  // ------------------------------------------------------------------
  // NHOM 7: PRODUCTS — Tim kiem (Tinh huong 5)
  // ------------------------------------------------------------------
  console.log("\n🛍️  Nhom 7: Products - Tim kiem (Tinh huong 5)");

  res = await request("GET", "/api/v1/products");
  assert(res.status === 200, "GET /products → 200");
  assert(res.body.facets !== undefined, "GET /products → co facets");

  // Tim kiem full-text
  res = await request("GET", "/api/v1/products?q=laptop");
  assert(res.status === 200, "GET /products?q=laptop → 200");
  assert(res.body.results.length > 0, "GET /products?q=laptop → co ket qua");

  // Filter theo brand
  res = await request("GET", "/api/v1/products?brand=ASUS,MSI&in_stock=true");
  assert(res.status === 200, "GET /products?brand=ASUS,MSI → 200");

  // Khong co ket qua van tra 200 (khong phai 404!)
  res = await request("GET", "/api/v1/products?q=xyznonexistent123");
  assert(
    res.status === 200,
    "GET /products (khong co ket qua) → 200 (khong phai 404)",
  );
  assert(
    res.body.results.length === 0,
    "GET /products (no results) → results: []",
  );

  // ETag caching
  const etag = res.headers["etag"];
  if (etag) {
    res = await request("GET", "/api/v1/products?q=xyznonexistent123", null, {
      "If-None-Match": etag,
    });
    assert(
      res.status === 304,
      "GET /products (If-None-Match) → 304 Not Modified",
    );
  }

  // ------------------------------------------------------------------
  // NHOM 8: ORDERS — Tao don hang (Tinh huong 3)
  // ------------------------------------------------------------------
  console.log("\n📦 Nhom 8: Orders - Tao don hang (Tinh huong 3)");

  const orderData = {
    items: [{ productId: "prod_002", quantity: 1 }],
    shippingAddress: {
      fullName: "Nguyen Test",
      phone: "0901234567",
      street: "123 Test St",
      city: "Ha Noi",
    },
    paymentMethod: "CREDIT_CARD",
  };

  res = await request("POST", "/api/v1/orders", orderData, {
    Authorization: "Bearer token-user",
    "Idempotency-Key": `test-key-${Date.now()}`,
  });
  assert(res.status === 201, "POST /orders → 201 Created");
  assert(
    res.headers.location !== undefined,
    "POST /orders → co Location header",
  );
  assert(res.body.data.pricing !== undefined, "POST /orders → co pricing");

  // Idempotency: Gui lai voi cung key → tra ve don cu
  const idemKey = `idem-test-${Date.now()}`;
  await request("POST", "/api/v1/orders", orderData, {
    Authorization: "Bearer token-user",
    "Idempotency-Key": idemKey,
  });
  res = await request("POST", "/api/v1/orders", orderData, {
    Authorization: "Bearer token-user",
    "Idempotency-Key": idemKey,
  });
  assert(
    res.headers["x-idempotent-replayed"] === "true",
    "POST /orders (idempotency replay) → header X-Idempotent-Replayed: true",
  );

  // San pham het hang → 409
  res = await request(
    "POST",
    "/api/v1/orders",
    {
      ...orderData,
      items: [{ productId: "prod_001", quantity: 9999 }],
    },
    { Authorization: "Bearer token-user" },
  );
  assert(res.status === 409, "POST /orders (het hang) → 409 Conflict");
  assert(
    res.body.error === "INSUFFICIENT_STOCK",
    "409 → error: INSUFFICIENT_STOCK",
  );

  // ------------------------------------------------------------------
  // NHOM 9: LOI 4xx KHAC
  // ------------------------------------------------------------------
  console.log("\n⚠️  Nhom 9: Kiem tra cac loi 4xx khac");

  // 404 route khong ton tai
  res = await request("GET", "/api/v1/nonexistent");
  assert(res.status === 404, "GET /nonexistent → 404 Not Found");

  // 403 — Admin xoa chinh minh
  res = await request("DELETE", "/api/v1/users/usr_001", null, {
    Authorization: "Bearer token-admin",
  });
  assert(res.status === 403, "DELETE /users (tu xoa minh) → 403 Forbidden");

  // ------------------------------------------------------------------
  // TOT KET
  // ------------------------------------------------------------------
  console.log("\n" + "=".repeat(60));
  console.log(`  KET QUA: ${passed} passed, ${failed} failed`);
  console.log(`  Tong:    ${passed + failed} tests`);
  if (failed === 0) {
    console.log("  🎉 Tat ca tests deu PASS!");
  } else {
    console.log(`  ⚠️  ${failed} test(s) FAIL - kiem tra lai code.`);
  }
  console.log("=".repeat(60) + "\n");
}

runTests().catch((err) => {
  console.error("\n❌ Loi khi chay tests:", err.message);
  console.error("Dam bao server dang chay: npm run dev\n");
  process.exit(1);
});
