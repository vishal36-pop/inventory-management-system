CREATE DATABASE IF NOT EXISTS inventory_db;
USE inventory_db;

CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80) NOT NULL UNIQUE,
    description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    address VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255),
    category_id INT,
    supplier_id INT,
    unit_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    quantity_in_stock INT NOT NULL DEFAULT 0,
    reorder_level INT NOT NULL DEFAULT 5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_unit_price CHECK (unit_price >= 0),
    CONSTRAINT chk_quantity_in_stock CHECK (quantity_in_stock >= 0),
    CONSTRAINT chk_reorder_level CHECK (reorder_level >= 0),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
        ON DELETE SET NULL,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    transaction_type ENUM('PURCHASE', 'SALE') NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes VARCHAR(255),
    CONSTRAINT chk_txn_quantity CHECK (quantity > 0),
    CONSTRAINT chk_txn_unit_price CHECK (unit_price >= 0),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE
);

INSERT IGNORE INTO categories (category_id, name, description) VALUES
(1, 'Electronics', 'Electronic items and accessories'),
(2, 'Stationery', 'Office and school supplies'),
(3, 'Groceries', 'Daily grocery items');

INSERT IGNORE INTO suppliers (supplier_id, name, phone, email, address) VALUES
(1, 'Metro Wholesale', '9876543210', 'orders@metrowholesale.com', 'Main Market Road'),
(2, 'City Office Supplies', '9123456780', 'sales@cityoffice.com', 'Industrial Area');
