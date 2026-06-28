from database.connection import DatabaseConnection
from database.initializer import DatabaseInitializer
from repositories.category_repository import CategoryRepository
from repositories.product_repository import ProductRepository
from repositories.supplier_repository import SupplierRepository
from repositories.transaction_repository import TransactionRepository
from services.category_service import CategoryService
from services.inventory_service import InventoryService
from services.product_service import ProductService
from services.report_service import ReportService
from services.supplier_service import SupplierService
from models.category import Category
from models.product import Product
from models.supplier import Supplier
from models.transaction import Transaction
from utils.input_helpers import (
    confirm,
    read_decimal,
    read_int,
    read_optional_text,
    read_required_text,
)


class InventoryCLI:
    """Menu-driven CLI for the Inventory Management System.

    Composes repositories → services and delegates all business logic
    and database work to the service layer.
    """

    def __init__(self):
        # Database
        self.db = DatabaseConnection()
        self.connection = self.db.get_connection()

        # Repositories
        self.category_repo = CategoryRepository(self.connection)
        self.supplier_repo = SupplierRepository(self.connection)
        self.product_repo = ProductRepository(self.connection)
        self.transaction_repo = TransactionRepository(self.connection)

        # Services
        self.categories = CategoryService(self.category_repo)
        self.suppliers = SupplierService(self.supplier_repo)
        self.products = ProductService(
            self.product_repo, self.category_repo, self.supplier_repo
        )
        self.inventory = InventoryService(
            self.product_repo, self.transaction_repo
        )
        self.reports = ReportService(
            self.product_repo, self.transaction_repo
        )

    # ==================================================================
    # Main loop
    # ==================================================================

    def run(self):
        while True:
            self.show_main_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.product_menu()
            elif choice == "2":
                self.category_menu()
            elif choice == "3":
                self.supplier_menu()
            elif choice == "4":
                self.transaction_menu()
            elif choice == "5":
                self.reports_menu()
            elif choice == "0":
                self.db.close()
                print("Goodbye!")
                break
            else:
                print("Invalid option.")

    def show_main_menu(self):
        print("\n=== Inventory Management System ===")
        print("1. Product Management")
        print("2. Category Management")
        print("3. Supplier Management")
        print("4. Purchases and Sales")
        print("5. Reports")
        print("0. Exit")

    # ==================================================================
    # Product menu
    # ==================================================================

    def product_menu(self):
        while True:
            print("\n--- Product Management ---")
            print("1. Add Product")
            print("2. Update Product")
            print("3. Delete Product")
            print("4. Search Products")
            print("5. View All Products")
            print("0. Back")

            choice = input("Choose an option: ").strip()
            try:
                if choice == "1":
                    self.add_product()
                elif choice == "2":
                    self.update_product()
                elif choice == "3":
                    self.delete_product()
                elif choice == "4":
                    self.search_products()
                elif choice == "5":
                    self.view_products()
                elif choice == "0":
                    break
                else:
                    print("Invalid option.")
            except (RuntimeError, ValueError) as exc:
                print(exc)

    def add_product(self):
        product = self.read_product_details()
        product_id = self.products.add_product(product)
        print(f"Product added with ID {product_id}.")

    def update_product(self):
        product_id = read_int("Product ID to update: ", minimum=1)
        if self.products.get_product_by_id(product_id) is None:
            print("Product not found.")
            return

        product = self.read_product_details()
        product.product_id = product_id
        updated = self.products.update_product(product)
        print("Product updated." if updated else "No changes were made.")

    def delete_product(self):
        product_id = read_int("Product ID to delete: ", minimum=1)
        product = self.products.get_product_by_id(product_id)
        if product is None:
            print("Product not found.")
            return

        if confirm(f"Delete {product.name}?"):
            deleted = self.products.delete_product(product_id)
            print("Product deleted." if deleted else "Product not found.")

    def search_products(self):
        keyword = read_required_text("Search keyword: ")
        rows = self.products.search_products(keyword)
        self.print_table(rows)

    def view_products(self):
        rows = self.products.get_all_products()
        self.print_table(rows)

    def read_product_details(self):
        name = read_required_text("Product name: ")
        description = read_optional_text("Description: ")
        category_id = read_int("Category ID (blank for none): ", 1, True)
        supplier_id = read_int("Supplier ID (blank for none): ", 1, True)
        unit_price = read_decimal("Unit price: ", minimum=0)
        quantity = read_int("Quantity in stock: ", minimum=0)
        reorder_level = read_int("Reorder level: ", minimum=0)
        return Product(
            product_id=None,
            name=name,
            description=description,
            category_id=category_id,
            supplier_id=supplier_id,
            unit_price=unit_price,
            quantity_in_stock=quantity,
            reorder_level=reorder_level,
        )

    # ==================================================================
    # Category menu
    # ==================================================================

    def category_menu(self):
        while True:
            print("\n--- Category Management ---")
            print("1. Add Category")
            print("2. Update Category")
            print("3. Delete Category")
            print("4. View Categories")
            print("0. Back")

            choice = input("Choose an option: ").strip()
            try:
                if choice == "1":
                    name = read_required_text("Category name: ")
                    description = read_optional_text("Description: ")
                    new_id = self.categories.add_category(
                        Category(name, description)
                    )
                    print(f"Category added with ID {new_id}.")
                elif choice == "2":
                    category_id = read_int("Category ID: ", minimum=1)
                    name = read_required_text("New name: ")
                    description = read_optional_text("New description: ")
                    category = Category(name, description, category_id)
                    count = self.categories.update_category(category)
                    print(
                        "Category updated."
                        if count
                        else "Category not found."
                    )
                elif choice == "3":
                    category_id = read_int("Category ID: ", minimum=1)
                    count = self.categories.delete_category(category_id)
                    print(
                        "Category deleted."
                        if count
                        else "Category not found."
                    )
                elif choice == "4":
                    self.print_table(self.categories.get_all_categories())
                elif choice == "0":
                    break
                else:
                    print("Invalid option.")
            except (RuntimeError, ValueError) as exc:
                print(exc)

    # ==================================================================
    # Supplier menu
    # ==================================================================

    def supplier_menu(self):
        while True:
            print("\n--- Supplier Management ---")
            print("1. Add Supplier")
            print("2. Update Supplier")
            print("3. Delete Supplier")
            print("4. View Suppliers")
            print("0. Back")

            choice = input("Choose an option: ").strip()
            try:
                if choice == "1":
                    supplier = self.read_supplier_details()
                    new_id = self.suppliers.add_supplier(supplier)
                    print(f"Supplier added with ID {new_id}.")
                elif choice == "2":
                    supplier_id = read_int("Supplier ID: ", minimum=1)
                    supplier = self.read_supplier_details()
                    supplier.supplier_id = supplier_id
                    count = self.suppliers.update_supplier(supplier)
                    print(
                        "Supplier updated."
                        if count
                        else "Supplier not found."
                    )
                elif choice == "3":
                    supplier_id = read_int("Supplier ID: ", minimum=1)
                    count = self.suppliers.delete_supplier(supplier_id)
                    print(
                        "Supplier deleted."
                        if count
                        else "Supplier not found."
                    )
                elif choice == "4":
                    self.print_table(self.suppliers.get_all_suppliers())
                elif choice == "0":
                    break
                else:
                    print("Invalid option.")
            except (RuntimeError, ValueError) as exc:
                print(exc)

    def read_supplier_details(self):
        name = read_required_text("Supplier name: ")
        phone = read_optional_text("Phone: ")
        email = read_optional_text("Email: ")
        address = read_optional_text("Address: ")
        return Supplier(name=name, phone=phone, email=email, address=address)

    # ==================================================================
    # Transaction menu
    # ==================================================================

    def transaction_menu(self):
        while True:
            print("\n--- Purchases and Sales ---")
            print("1. Record Purchase")
            print("2. Record Sale")
            print("3. Transaction History")
            print("0. Back")

            choice = input("Choose an option: ").strip()
            try:
                if choice == "1":
                    transaction = self.read_transaction(Transaction.PURCHASE)
                    new_id = self.inventory.record_purchase(transaction)
                    print(
                        f"Purchase recorded with transaction ID {new_id}."
                    )
                elif choice == "2":
                    transaction = self.read_transaction(Transaction.SALE)
                    new_id = self.inventory.record_sale(transaction)
                    print(f"Sale recorded with transaction ID {new_id}.")
                elif choice == "3":
                    self.print_table(self.reports.transaction_history())
                elif choice == "0":
                    break
                else:
                    print("Invalid option.")
            except (RuntimeError, ValueError) as exc:
                print(exc)

    def read_transaction(self, transaction_type):
        product_id = read_int("Product ID: ", minimum=1)
        quantity = read_int("Quantity: ", minimum=1)
        unit_price = read_decimal("Unit price: ", minimum=0)
        notes = read_optional_text("Notes: ")
        return Transaction(
            product_id=product_id,
            transaction_type=transaction_type,
            quantity=quantity,
            unit_price=unit_price,
            notes=notes,
        )

    # ==================================================================
    # Reports menu
    # ==================================================================

    def reports_menu(self):
        while True:
            print("\n--- Reports ---")
            print("1. Low Stock Report")
            print("2. Inventory Value Report")
            print("0. Back")

            choice = input("Choose an option: ").strip()
            if choice == "1":
                products = self.reports.low_stock_report()
                self.print_table(products, row_method="to_low_stock_row")
            elif choice == "2":
                products = self.reports.inventory_value_report()
                self.print_table(products, row_method="to_value_row")
                total = sum(p.inventory_value() for p in products)
                print(f"Total inventory value: {total:.2f}")
            elif choice == "0":
                break
            else:
                print("Invalid option.")

    # ==================================================================
    # Display helper
    # ==================================================================

    def print_table(self, records, row_method="to_display_row"):
        """Pretty-print a list of model objects as a CLI table."""
        if not records:
            print("No records found.")
            return

        rows = []
        for record in records:
            if hasattr(record, row_method):
                rows.append(getattr(record, row_method)())
            else:
                rows.append(record)

        headers = list(rows[0].keys())
        widths = {
            header: max(
                len(str(header)),
                *(len(str(row[header])) for row in rows),
            )
            for header in headers
        }

        header_line = " | ".join(
            header.ljust(widths[header]) for header in headers
        )
        separator = "-+-".join("-" * widths[header] for header in headers)
        print(header_line)
        print(separator)

        for row in rows:
            print(
                " | ".join(
                    str(row[header]).ljust(widths[header])
                    for header in headers
                )
            )


def main():
    print("1. Start application")
    print("2. Initialize database")
    choice = input("Choose an option: ").strip()

    if choice == "2":
        DatabaseInitializer().initialize()
        return

    try:
        app = InventoryCLI()
        app.run()
    except RuntimeError as exc:
        print(exc)
        print(
            "Check config.py or set DB_HOST, DB_USER, DB_PASSWORD, "
            "and DB_NAME."
        )


if __name__ == "__main__":
    main()
