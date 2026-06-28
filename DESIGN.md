# Inventory Management System - Design Document

## 1. Functional Requirements

### Product Management

The system should allow the user to add a new product with its name,
description, category, supplier, unit price, current stock quantity, and reorder
level.

The user should be able to update product details. Updating a product should not
delete its past transactions.

The user should be able to delete a product when it is no longer needed. The
system should ask for confirmation before deleting.

The user should be able to search products by name or description.

The user should be able to view all products with category name, supplier name,
unit price, stock quantity, and reorder level.

### Category Management

The system should allow the user to add categories such as Electronics,
Stationery, or Groceries.

The user should be able to update category name and description.

The user should be able to delete categories. If products still exist under a
deleted category, their category reference should be set to `NULL`.

The user should be able to view all categories.

### Supplier Management

The system should allow the user to add supplier information including name,
phone, email, and address.

The user should be able to update supplier details.

The user should be able to delete suppliers. If products still use the supplier,
their supplier reference should be set to `NULL`.

The user should be able to view all suppliers.

### Purchase Transactions

The system should allow the user to record a purchase for an existing product.

When a purchase is recorded, the product stock should increase by the purchased
quantity.

The purchase should also be saved in transaction history with product, quantity,
unit price, date, and optional notes.

### Sale Transactions

The system should allow the user to record a sale for an existing product.

Before saving a sale, the system should check that enough stock is available.

When a sale is recorded, the product stock should decrease by the sold quantity.

The sale should be saved in transaction history.

### Transaction History

The user should be able to view all purchase and sale transactions.

Transactions should be shown with product name, transaction type, quantity, unit
price, total amount, date, and notes.

### Low Stock Report

The system should show products whose stock quantity is less than or equal to
their reorder level.

This report helps the user decide what products need to be purchased soon.

### Inventory Value Report

The system should calculate the value of each product using:

```text
quantity_in_stock * unit_price
```

The report should show the total value per product and the grand total value of
the inventory.

## 2. Non-Functional Requirements

### Maintainability

The project should be divided into small modules with clear responsibilities.
Database code, business logic, object models, and CLI input/output should not be
mixed together.

Names should be meaningful and easy to understand. A student reading the code
after a few weeks should still be able to follow it.

### Readability

The code should follow PEP 8.

Methods should be short enough to understand without scrolling too much.

Comments should be used only when they explain a decision or a non-obvious block
of logic.

### Error Handling

The system should handle invalid menu choices, wrong input types, empty required
fields, negative prices, negative quantities, and failed database operations.

The application should not crash for normal user mistakes.

Database write operations should use transactions. If one step fails, such as
updating stock after recording a sale, the operation should roll back.

### Scalability Within Student Project Scope

The architecture should allow new reports, new search filters, or new transaction
types to be added without rewriting the entire CLI.

The project does not need enterprise features such as dependency injection
containers, caching, web APIs, or complex design patterns.

## 3. Object-Oriented Design

### Domain Classes

#### Product

Represents an item stored in inventory.

Responsibilities:

- Store product details.
- Validate product data.
- Calculate inventory value.
- Decide whether the product is low on stock.
- Produce display-friendly values for reports.

Important behavior:

- `validate()`
- `is_low_stock()`
- `inventory_value()`

#### Category

Represents a product category.

Responsibilities:

- Store category details.
- Validate that category name is present.
- Provide a display form for the CLI.

#### Supplier

Represents a supplier that provides products.

Responsibilities:

- Store supplier contact details.
- Validate supplier data.
- Provide a display form for the CLI.

#### Transaction

Represents one purchase or sale.

Responsibilities:

- Store transaction details.
- Validate transaction quantity, price, product ID, and type.
- Calculate transaction total amount.
- Calculate stock change caused by the transaction.

Important behavior:

- `stock_change()`
- `total_amount()`
- `validate()`

### Service / Manager Classes

#### ProductService

Coordinates product-related use cases.

Responsibilities:

- Add, update, delete, search, and view products.
- Ask the repository to save or load products.
- Use `Product` behavior for validation and inventory value calculations.

#### CategoryService

Coordinates category-related use cases.

Responsibilities:

- Add, update, delete, and list categories.
- Use `Category` validation before saving.

#### SupplierService

Coordinates supplier-related use cases.

Responsibilities:

- Add, update, delete, and list suppliers.
- Use `Supplier` validation before saving.

#### InventoryService

Handles stock-changing operations.

Responsibilities:

- Record purchases.
- Record sales.
- Check stock before sale.
- Update product stock and save transaction as one database transaction.

#### ReportService

Builds report data for the CLI.

Responsibilities:

- Low stock report.
- Inventory value report.
- Transaction history.

### Repository / DAO Classes

Repository classes contain raw SQL and database operations.

#### ProductRepository

Responsibilities:

- Insert, update, delete, search, and fetch products.
- Convert database rows into `Product` objects.
- Use parameterized SQL queries.

#### CategoryRepository

Responsibilities:

- Insert, update, delete, and fetch categories.
- Convert rows into `Category` objects.

#### SupplierRepository

Responsibilities:

- Insert, update, delete, and fetch suppliers.
- Convert rows into `Supplier` objects.

#### TransactionRepository

Responsibilities:

- Insert transactions.
- Fetch transaction history.
- Convert rows into `Transaction` objects.

### Database Classes

#### DatabaseConnection

Responsibilities:

- Create and close MySQL connections.
- Keep database configuration in one place.

#### DatabaseInitializer

Responsibilities:

- Read the SQL schema file.
- Create the database and tables before the application is used.

### CLI Class

#### InventoryCLI

Responsibilities:

- Show menus.
- Read user input.
- Call services.
- Display results.

The CLI should not contain raw SQL or inventory rules.

### OOP Principles Used

#### Encapsulation

Each domain object keeps its data and related behavior together. For example,
`Product` owns the logic for calculating inventory value instead of leaving that
calculation scattered through the CLI.

Repositories hide SQL details from the rest of the project.

Services hide business workflows from the CLI.

#### Composition

The CLI is composed of service objects.

Services are composed of repository objects.

Repositories are composed with a database connection.

This keeps dependencies simple and understandable.

#### Inheritance

Inheritance is not necessary for the first version.

A base repository could be added later, but forcing inheritance now would make
the project look more complex than it needs to be.

#### Polymorphism

Polymorphism can be used lightly through shared method names such as
`validate()` and `to_display_row()` across domain classes.

The CLI can display different objects as long as they provide a display method.

## 4. Database Design

### Database Name

`inventory_db`

### Table: categories

Stores product categories.

Attributes:

- `category_id` INT AUTO_INCREMENT
- `name` VARCHAR(80) NOT NULL UNIQUE
- `description` VARCHAR(255)

Primary key:

- `category_id`

Relationships:

- One category can be linked to many products.

### Table: suppliers

Stores supplier contact information.

Attributes:

- `supplier_id` INT AUTO_INCREMENT
- `name` VARCHAR(100) NOT NULL
- `phone` VARCHAR(20)
- `email` VARCHAR(100)
- `address` VARCHAR(255)

Primary key:

- `supplier_id`

Relationships:

- One supplier can supply many products.

### Table: products

Stores inventory items.

Attributes:

- `product_id` INT AUTO_INCREMENT
- `name` VARCHAR(100) NOT NULL
- `description` VARCHAR(255)
- `category_id` INT NULL
- `supplier_id` INT NULL
- `unit_price` DECIMAL(10, 2) NOT NULL
- `quantity_in_stock` INT NOT NULL
- `reorder_level` INT NOT NULL
- `created_at` TIMESTAMP

Primary key:

- `product_id`

Foreign keys:

- `category_id` references `categories(category_id)`
- `supplier_id` references `suppliers(supplier_id)`

Relationships:

- Many products can belong to one category.
- Many products can be supplied by one supplier.
- One product can have many transactions.

### Table: transactions

Stores purchase and sale history.

Attributes:

- `transaction_id` INT AUTO_INCREMENT
- `product_id` INT NOT NULL
- `transaction_type` ENUM('PURCHASE', 'SALE') NOT NULL
- `quantity` INT NOT NULL
- `unit_price` DECIMAL(10, 2) NOT NULL
- `transaction_date` TIMESTAMP
- `notes` VARCHAR(255)

Primary key:

- `transaction_id`

Foreign key:

- `product_id` references `products(product_id)`

Relationships:

- Many transactions belong to one product.

## 5. UML Class Diagram

```text
+-------------------+
| Product           |
+-------------------+
| product_id        |
| name              |
| description       |
| category_id       |
| supplier_id       |
| unit_price        |
| quantity_in_stock |
| reorder_level     |
+-------------------+
| validate()        |
| is_low_stock()    |
| inventory_value() |
| to_display_row()  |
+-------------------+

+-------------------+
| Category          |
+-------------------+
| category_id       |
| name              |
| description       |
+-------------------+
| validate()        |
| to_display_row()  |
+-------------------+

+-------------------+
| Supplier          |
+-------------------+
| supplier_id       |
| name              |
| phone             |
| email             |
| address           |
+-------------------+
| validate()        |
| to_display_row()  |
+-------------------+

+-------------------+
| Transaction       |
+-------------------+
| transaction_id    |
| product_id        |
| transaction_type  |
| quantity          |
| unit_price        |
| transaction_date  |
| notes             |
+-------------------+
| validate()        |
| stock_change()    |
| total_amount()    |
| to_display_row()  |
+-------------------+

+---------------------+       +---------------------+
| ProductService      | ----> | ProductRepository   |
+---------------------+       +---------------------+
| add_product()       |       | insert()            |
| update_product()    |       | update()            |
| delete_product()    |       | delete()            |
| search_products()   |       | find_by_id()        |
| list_products()     |       | search()            |
+---------------------+       +---------------------+

+---------------------+       +-------------------------+
| InventoryService    | ----> | ProductRepository       |
+---------------------+       +-------------------------+
| record_purchase()   | ----> | TransactionRepository   |
| record_sale()       |       +-------------------------+
+---------------------+

+---------------------+       +-------------------------+
| ReportService       | ----> | ProductRepository       |
+---------------------+       +-------------------------+
| low_stock_report()  | ----> | TransactionRepository   |
| inventory_value()   |       +-------------------------+
| history()           |
+---------------------+

+---------------------+
| InventoryCLI        |
+---------------------+
| run()               |
| product_menu()      |
| category_menu()     |
| supplier_menu()     |
| transaction_menu()  |
| reports_menu()      |
+---------------------+
          |
          v
   Service classes
```

Relationship summary:

- `Category` 1-to-many `Product`
- `Supplier` 1-to-many `Product`
- `Product` 1-to-many `Transaction`
- `InventoryCLI` uses service classes
- Service classes use repository classes
- Repository classes use `DatabaseConnection`

## 6. Package / Folder Structure

```text
inventory_management_system/
├── config.py
├── main.py
├── init_database.py
├── schema.sql
├── database/
│   ├── __init__.py
│   ├── connection.py
│   └── initializer.py
├── models/
│   ├── __init__.py
│   ├── product.py
│   ├── category.py
│   ├── supplier.py
│   └── transaction.py
├── repositories/
│   ├── __init__.py
│   ├── product_repository.py
│   ├── category_repository.py
│   ├── supplier_repository.py
│   └── transaction_repository.py
├── services/
│   ├── __init__.py
│   ├── product_service.py
│   ├── category_service.py
│   ├── supplier_service.py
│   ├── inventory_service.py
│   └── report_service.py
└── utils/
    ├── __init__.py
    └── input_helpers.py
```

### Module Responsibilities

`models/` contains real domain objects with meaningful behavior.

`repositories/` contains SQL queries and maps rows to model objects.

`services/` contains business workflows and coordinates multiple repositories.

`database/` contains connection setup and database initialization.

`utils/` contains simple reusable input helpers.

`main.py` contains the CLI application and menu navigation.

## 7. Layered Architecture

### CLI Layer

The CLI is responsible for user interaction only.

It should:

- Print menus.
- Read input.
- Show success or error messages.
- Display tables.
- Call service methods.

It should not:

- Write SQL.
- Decide stock rules.
- Directly update product quantities.

### Services / Managers Layer

Services contain the application logic.

They should:

- Validate business workflows.
- Call model behavior.
- Coordinate repositories.
- Handle operations that affect more than one table.

Example:

When selling a product, `InventoryService` checks stock, creates a `Transaction`,
updates the product quantity, and saves both changes.

### Repository / DAO Layer

Repositories contain database access logic.

They should:

- Use `cursor.execute()`.
- Use parameterized queries with `%s`.
- Convert rows into model objects.
- Commit or roll back when appropriate.

They should not:

- Print menu messages.
- Ask for user input.
- Contain CLI-specific formatting.

### Database Layer

The database layer manages connection setup and schema initialization.

It should:

- Read database configuration.
- Create MySQL connections.
- Close connections.
- Run the schema file.

## 8. Program Flow

### Add Product

1. User selects Add Product from the product menu.
2. CLI asks for product details.
3. CLI creates a `Product` object.
4. `ProductService.add_product()` receives the object.
5. `Product.validate()` checks product data.
6. `ProductRepository.insert()` saves the product using SQL.
7. The new product ID is returned.
8. CLI prints a success message.

### Purchase Stock

1. User selects Record Purchase.
2. CLI asks for product ID, quantity, price, and notes.
3. CLI creates a `Transaction` object with type `PURCHASE`.
4. `InventoryService.record_purchase()` validates the transaction.
5. Service checks that the product exists.
6. Service uses `transaction.stock_change()` to get the quantity increase.
7. Product stock is updated.
8. Transaction is inserted.
9. Database changes are committed.
10. CLI prints a success message.

### Sell Product

1. User selects Record Sale.
2. CLI asks for product ID, quantity, price, and notes.
3. CLI creates a `Transaction` object with type `SALE`.
4. `InventoryService.record_sale()` validates the transaction.
5. Service loads the product.
6. Service checks if enough stock is available.
7. Service uses `transaction.stock_change()` to get the quantity decrease.
8. Product stock is updated.
9. Transaction is inserted.
10. Database changes are committed.
11. CLI prints a success message.

If stock is not enough, no database changes should be saved.

### Generate Reports

Low stock report:

1. User selects Low Stock Report.
2. CLI calls `ReportService.low_stock_report()`.
3. Service loads products from the repository.
4. Each product is checked with `product.is_low_stock()`.
5. CLI displays matching products.

Inventory value report:

1. User selects Inventory Value Report.
2. CLI calls `ReportService.inventory_value_report()`.
3. Service loads products from the repository.
4. Each product calculates its value using `product.inventory_value()`.
5. CLI displays product values and grand total.

## 9. Sequence Diagrams

### Add Product

```text
User -> InventoryCLI: choose Add Product
InventoryCLI -> User: ask for product details
User -> InventoryCLI: enter details
InventoryCLI -> Product: create product object
InventoryCLI -> ProductService: add_product(product)
ProductService -> Product: validate()
ProductService -> ProductRepository: insert(product)
ProductRepository -> DatabaseConnection: get connection
ProductRepository -> MySQL: INSERT product
MySQL -> ProductRepository: new product id
ProductRepository -> ProductService: product id
ProductService -> InventoryCLI: product id
InventoryCLI -> User: show success message
```

### Purchase Stock

```text
User -> InventoryCLI: choose Record Purchase
InventoryCLI -> User: ask for transaction details
User -> InventoryCLI: enter details
InventoryCLI -> Transaction: create PURCHASE transaction
InventoryCLI -> InventoryService: record_purchase(transaction)
InventoryService -> Transaction: validate()
InventoryService -> ProductRepository: find_by_id(product_id)
ProductRepository -> MySQL: SELECT product
MySQL -> ProductRepository: product row
ProductRepository -> InventoryService: Product object
InventoryService -> Transaction: stock_change()
InventoryService -> ProductRepository: update_stock(product_id, change)
InventoryService -> TransactionRepository: insert(transaction)
InventoryService -> DatabaseConnection: commit
InventoryService -> InventoryCLI: transaction id
InventoryCLI -> User: show success message
```

### Sell Product

```text
User -> InventoryCLI: choose Record Sale
InventoryCLI -> User: ask for transaction details
User -> InventoryCLI: enter details
InventoryCLI -> Transaction: create SALE transaction
InventoryCLI -> InventoryService: record_sale(transaction)
InventoryService -> Transaction: validate()
InventoryService -> ProductRepository: find_by_id(product_id)
ProductRepository -> MySQL: SELECT product
MySQL -> ProductRepository: product row
ProductRepository -> InventoryService: Product object
InventoryService -> Product: check quantity_in_stock
InventoryService -> Transaction: stock_change()
InventoryService -> ProductRepository: update_stock(product_id, change)
InventoryService -> TransactionRepository: insert(transaction)
InventoryService -> DatabaseConnection: commit
InventoryService -> InventoryCLI: transaction id
InventoryCLI -> User: show success message
```

### Low Stock Report

```text
User -> InventoryCLI: choose Low Stock Report
InventoryCLI -> ReportService: low_stock_report()
ReportService -> ProductRepository: get_all()
ProductRepository -> MySQL: SELECT products
MySQL -> ProductRepository: product rows
ProductRepository -> ReportService: Product objects
ReportService -> Product: is_low_stock()
ReportService -> InventoryCLI: low stock products
InventoryCLI -> User: display report
```

## 10. Design Decisions

### Why Use Layered Architecture?

Layered architecture keeps the project understandable. A second-year student can
open one folder at a time and understand what it does.

The CLI handles input and output, services handle use cases, repositories handle
SQL, and models represent real inventory concepts.

This separation also makes debugging easier. If a query is wrong, look in a
repository. If stock logic is wrong, look in a service or model. If the menu is
wrong, look in the CLI.

### Why Each Class Exists

`Product` exists because products have both data and behavior. A product can
validate itself, calculate its value, and know whether it is low on stock.

`Category` exists because categories are separate objects with their own table
and product relationship.

`Supplier` exists because supplier information is independent from products and
can be reused by many products.

`Transaction` exists because purchases and sales have common behavior such as
total amount and stock change.

`InventoryService` exists because purchase and sale workflows affect both
products and transactions.

`ReportService` exists because reports should not be mixed with menu code or SQL
code.

Repository classes exist to keep SQL away from business logic and the CLI.

### Why Put Logic Inside Objects?

Putting `inventory_value()` inside `Product` is better than calculating it in
many different menus or reports. The meaning of inventory value belongs to the
product itself.

Putting `stock_change()` inside `Transaction` is better than writing `if`
conditions everywhere. A purchase increases stock and a sale decreases stock, so
that rule belongs with the transaction object.

Putting validation inside model objects keeps invalid objects from spreading
through the program.

### Why Avoid Heavy Patterns?

The goal is a clean student project, not an enterprise framework. Simple classes,
repositories, services, and a CLI are enough.

Adding abstract factories, complex inheritance, or large generic utility classes
would make the project harder to understand without adding much value.

## 11. Future Improvements

Possible future improvements:

- User login for admin and staff users.
- Export reports to CSV.
- Search products by category or supplier.
- Date range filters for transaction history.
- Separate purchase price and selling price.
- Product barcode field.
- Soft delete for products instead of permanent delete.
- Unit tests for model and service classes.
- Better email and phone validation.
- Pagination for large product lists.
- A small GUI or web interface using the same service and repository layers.

## Final Feature Check

The desired feature set is covered by this design:

```text
[x] Product Management: Add, Update, Delete, Search, View
[x] Category Management
[x] Supplier Management
[x] Purchase Transactions
[x] Sale Transactions
[x] Transaction History
[x] Low Stock Report
[x] Inventory Value Report
[x] OOP domain classes with meaningful behavior
[x] MySQL schema with primary and foreign keys
[x] Raw SQL with parameterized queries planned
[x] Menu-driven CLI planned
```

Current project note:

The existing project already contains most feature behavior, but to match this
design exactly, the SQL currently inside manager classes should be moved into a
new `repositories/` layer, and the managers should become service classes that
coordinate repositories and model objects.

No implementation code is included in this design document.
