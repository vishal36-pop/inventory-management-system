# Inventory Management System

A console-based inventory management system built with **Python** and **MySQL**.  
It uses raw SQL queries, a layered OOP architecture (Models → Repositories → Services → CLI), and `mysql-connector-python` for all database operations.

---

## Features

| Area | Capabilities |
|---|---|
| **Products** | Add, update, delete, search by keyword, view all (with joined category & supplier names) |
| **Categories** | Add, update, delete, view all |
| **Suppliers** | Add, update, delete, view all (with phone, email, address) |
| **Purchases** | Record stock-in transactions; stock is updated atomically with the transaction record |
| **Sales** | Record stock-out transactions; validates sufficient stock before committing |
| **Reports** | Low-stock alert list · Inventory value report (price × quantity, sorted by value) |
| **Transaction History** | Full log of every purchase and sale, newest first |

---

## Requirements

- Python 3.10+
- MySQL 8.0+
- `mysql-connector-python==9.1.0`

---

## Setup

### 1. Create and activate a virtual environment

**Windows (PowerShell)**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure database credentials

Open [`config.py`](config.py) and set your MySQL credentials directly, **or** use environment variables (the file reads env vars first):

```python
# config.py
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "your_password"),
    "database": os.getenv("DB_NAME", "inventory_db"),
}
```

**Using environment variables (optional)**

```bash
# Windows PowerShell
$env:DB_PASSWORD = "your_password"

# macOS / Linux
export DB_PASSWORD="your_password"
```

### 4. Initialize the database

This creates the `inventory_db` database, all tables, and inserts a few sample categories and suppliers.

```bash
python init_database.py
```

Expected output:
```
Database is ready.
```

### 5. Run the application

```bash
python main.py
```

At the startup prompt, choose **`1` – Start application**.

---

## Usage

```
=== Inventory Management System ===
1. Product Management
2. Category Management
3. Supplier Management
4. Purchases and Sales
5. Reports
0. Exit
```

### Product Management
```
1. Add Product       – enter name, description, category ID, supplier ID, price, stock, reorder level
2. Update Product    – look up by ID, then re-enter all fields
3. Delete Product    – confirm before deleting
4. Search Products   – keyword matches name or description
5. View All Products – table with category and supplier names joined
```

### Category & Supplier Management
Standard CRUD menus: **Add → Update → Delete → View All**.

### Purchases and Sales
```
1. Record Purchase – increases stock atomically
2. Record Sale     – validates stock first, then decreases atomically
3. Transaction History – full log, newest first
```

### Reports
```
1. Low Stock Report         – products at or below their reorder level
2. Inventory Value Report   – price × quantity per product, with grand total
```

---

## Project Structure

```
inventory_management_system/
│
├── main.py                    # CLI entry-point (InventoryCLI class)
├── config.py                  # Database configuration (env-var aware)
├── schema.sql                 # DDL – creates tables and inserts seed data
├── init_database.py           # Standalone DB initialiser script
├── requirements.txt           # Python dependencies
│
├── database/
│   ├── connection.py          # DatabaseConnection – connect / close / context manager
│   └── initializer.py         # DatabaseInitializer – runs schema.sql
│
├── models/
│   ├── category.py            # Category – validation, persistence helpers, display rows
│   ├── product.py             # Product  – validation, stock/value helpers, display rows
│   ├── supplier.py            # Supplier – phone/email validation, display rows
│   └── transaction.py         # Transaction – type enum, stock_change(), total_amount()
│
├── repositories/
│   ├── category_repository.py   # SQL CRUD for categories
│   ├── product_repository.py    # SQL CRUD + update_stock() for products
│   ├── supplier_repository.py   # SQL CRUD for suppliers
│   └── transaction_repository.py # INSERT + find_all_history()
│
├── services/
│   ├── category_service.py    # Business logic for categories
│   ├── inventory_service.py   # Atomic purchase / sale recording
│   ├── product_service.py     # FK validation before insert/update
│   ├── report_service.py      # Low-stock and value report queries
│   └── supplier_service.py    # Business logic for suppliers
│
└── utils/
    └── input_helpers.py       # read_required_text, read_int, read_decimal, confirm
```

---

## Architecture

```
  CLI (main.py)
       │
       ▼
  Services  ←── business rules, validation, atomic ops
       │
       ▼
  Repositories  ←── raw SQL, parameterised queries
       │
       ▼
  MySQL (inventory_db)
```

Models are plain Python classes used across all layers for data transfer and validation.  
Repositories never call other repositories directly; the `InventoryService` coordinates the stock update and transaction insert in a single atomic commit.

---

## Database Schema

| Table | Key Columns |
|---|---|
| `categories` | `category_id`, `name` (unique), `description` |
| `suppliers` | `supplier_id`, `name`, `phone`, `email` (unique), `address` |
| `products` | `product_id`, `name`, `unit_price`, `quantity_in_stock`, `reorder_level`, FK → categories, suppliers |
| `transactions` | `transaction_id`, `product_id` (FK), `transaction_type` (ENUM), `quantity`, `unit_price`, `transaction_date`, `notes` |

Foreign keys use `ON DELETE SET NULL` for categories/suppliers and `ON DELETE CASCADE` for transactions.

---

## Seed Data

`schema.sql` pre-populates:

**Categories** – Electronics, Stationery, Groceries  
**Suppliers** – Metro Wholesale, City Office Supplies
