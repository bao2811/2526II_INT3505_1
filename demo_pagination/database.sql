-- Database script for Pagination Demo
-- Simple version without procedures

DROP DATABASE IF EXISTS pagination_demo;
CREATE DATABASE pagination_demo;
USE pagination_demo;

-- Create users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    age INT,
    city VARCHAR(50),
    country VARCHAR(50),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_city (city),
    INDEX idx_created_at (created_at),
    INDEX idx_id_created_at (id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert 1 million records
INSERT INTO users (username, email, full_name, age, city, country, phone)
SELECT
    CONCAT('user_', n),
    CONCAT('user_', n, '@example.com'),
    CONCAT('User ', n, ' Test'),
    20 + (n % 60),
    ELT((n % 20) + 1, 'Hanoi', 'Ho Chi Minh', 'Da Nang', 'Hai Phong', 'Can Tho', 'Ha Long', 'Nha Trang', 'Hue', 'Da Lat', 'Ban Me Thuot', 'Vinh', 'Thai Nguyen', 'Ha Giang', 'Cao Bang', 'Bac Kan', 'Lang Son', 'Quang Ninh', 'Hai Duong', 'Nam Dinh', 'Thanh Hoa'),
    ELT((n % 5) + 1, 'Vietnam', 'Thailand', 'Singapore', 'Malaysia', 'Philippines'),
    CONCAT('+84', LPAD(FLOOR(900000000 + (n % 99999999)), 9, '0'))
FROM (
    SELECT t1.n + t2.n * 10 + t3.n * 100 + t4.n * 1000 + t5.n * 10000 + t6.n * 100000 as n
    FROM (SELECT 0 as n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t1
    CROSS JOIN (SELECT 0 as n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t2
    CROSS JOIN (SELECT 0 as n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t3
    CROSS JOIN (SELECT 0 as n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t4
    CROSS JOIN (SELECT 0 as n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t5
    CROSS JOIN (SELECT 0 as n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t6
    WHERE t1.n + t2.n * 10 + t3.n * 100 + t4.n * 1000 + t5.n * 10000 + t6.n * 100000 < 1000000
) numbers;

-- Verify data
SELECT COUNT(*) as total_records FROM users;
SELECT * FROM users LIMIT 5;
