// src/data/db.js
// Giả lập database bằng in-memory arrays (không cần cài DB thật)

const { v4: uuidv4 } = require("uuid");

// ===================== USERS =====================
const users = [
  {
    id: "usr_001",
    name: "Nguyen Van An",
    email: "nvan@example.com",
    role: "admin",
    department: "Engineering",
    age: 28,
    createdAt: "2025-01-10T08:00:00Z",
    updatedAt: "2025-01-10T08:00:00Z",
    deletedAt: null,
  },
  {
    id: "usr_002",
    name: "Tran Thi Bich",
    email: "ttbich@example.com",
    role: "user",
    department: "Marketing",
    age: 25,
    createdAt: "2025-02-15T09:00:00Z",
    updatedAt: "2025-02-15T09:00:00Z",
    deletedAt: null,
  },
  {
    id: "usr_003",
    name: "Le Van Cuong",
    email: "lvcuong@example.com",
    role: "user",
    department: "Engineering",
    age: 30,
    createdAt: "2025-03-20T10:00:00Z",
    updatedAt: "2025-03-20T10:00:00Z",
    deletedAt: null,
  },
  {
    id: "usr_004",
    name: "Pham Thi Dung",
    email: "ptdung@example.com",
    role: "user",
    department: "HR",
    age: 27,
    createdAt: "2025-04-05T11:00:00Z",
    updatedAt: "2025-04-05T11:00:00Z",
    deletedAt: null,
  },
  {
    id: "usr_005",
    name: "Hoang Van Em",
    email: "hvem@example.com",
    role: "user",
    department: "Engineering",
    age: 32,
    createdAt: "2025-05-12T12:00:00Z",
    updatedAt: "2025-05-12T12:00:00Z",
    deletedAt: null,
  },
];

// ===================== POSTS =====================
const posts = [
  {
    id: "post_001",
    title: "Gioi thieu ve REST API",
    content:
      "REST (Representational State Transfer) la mot kieu kien truc phan mem...",
    authorId: "usr_001",
    status: "published",
    tags: ["rest", "api", "web"],
    createdAt: "2025-06-01T08:00:00Z",
    updatedAt: "2025-06-01T08:00:00Z",
    deletedAt: null,
  },
  {
    id: "post_002",
    title: "HTTP Methods trong REST",
    content:
      "GET, POST, PUT, PATCH, DELETE - moi method co mot y nghia rieng...",
    authorId: "usr_001",
    status: "published",
    tags: ["http", "rest", "methods"],
    createdAt: "2025-06-10T09:00:00Z",
    updatedAt: "2025-06-10T09:00:00Z",
    deletedAt: null,
  },
  {
    id: "post_003",
    title: "Status Codes HTTP",
    content: "Cac ma trang thai HTTP giup client hieu ket qua cua request...",
    authorId: "usr_002",
    status: "draft",
    tags: ["http", "status-codes"],
    createdAt: "2025-06-15T10:00:00Z",
    updatedAt: "2025-06-15T10:00:00Z",
    deletedAt: null,
  },
];

// ===================== PRODUCTS =====================
const products = [
  {
    id: "prod_001",
    name: "Laptop Dell XPS 15",
    brand: "Dell",
    category: "laptop",
    price: 35000000,
    stock: 10,
    rating: 4.8,
    createdAt: "2025-01-01T00:00:00Z",
  },
  {
    id: "prod_002",
    name: "Mouse Logitech MX Master 3",
    brand: "Logitech",
    category: "peripheral",
    price: 2500000,
    stock: 50,
    rating: 4.7,
    createdAt: "2025-01-05T00:00:00Z",
  },
  {
    id: "prod_003",
    name: "ASUS ROG Strix G15",
    brand: "ASUS",
    category: "laptop",
    price: 28500000,
    stock: 5,
    rating: 4.6,
    createdAt: "2025-02-10T00:00:00Z",
  },
  {
    id: "prod_004",
    name: "Keyboard Keychron K2",
    brand: "Keychron",
    category: "peripheral",
    price: 1800000,
    stock: 30,
    rating: 4.9,
    createdAt: "2025-02-20T00:00:00Z",
  },
  {
    id: "prod_005",
    name: "MSI Katana 15",
    brand: "MSI",
    category: "laptop",
    price: 24900000,
    stock: 8,
    rating: 4.5,
    createdAt: "2025-03-01T00:00:00Z",
  },
];

// ===================== ORDERS =====================
const orders = [];

// ===================== RATE LIMIT STORE =====================
// { ip: { count, resetAt } }
const rateLimitStore = {};

module.exports = { users, posts, products, orders, rateLimitStore, uuidv4 };
