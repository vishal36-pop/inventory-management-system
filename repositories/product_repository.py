from mysql.connector import Error

from models.product import Product


class ProductRepository:
    """Handles all SQL operations for the products table."""

    def __init__(self, connection):
        self.connection = connection

    def insert(self, product: Product):
        """Insert a new product and return the generated ID."""
        query = """
            INSERT INTO products
                (name, description, category_id, supplier_id, unit_price,
                 quantity_in_stock, reorder_level)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, product.to_insert_values())
            self.connection.commit()
            return cursor.lastrowid
        except Error as exc:
            self.connection.rollback()
            raise RuntimeError(f"Could not add product: {exc}") from exc
        finally:
            cursor.close()

    def update(self, product: Product):
        """Update an existing product. Return the number of rows affected."""
        query = """
            UPDATE products
            SET name = %s,
                description = %s,
                category_id = %s,
                supplier_id = %s,
                unit_price = %s,
                quantity_in_stock = %s,
                reorder_level = %s
            WHERE product_id = %s
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, product.to_update_values())
            self.connection.commit()
            return cursor.rowcount
        except Error as exc:
            self.connection.rollback()
            raise RuntimeError(f"Could not update product: {exc}") from exc
        finally:
            cursor.close()

    def delete(self, product_id):
        """Delete a product by ID. Return the number of rows affected."""
        query = "DELETE FROM products WHERE product_id = %s"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (product_id,))
            self.connection.commit()
            return cursor.rowcount
        except Error as exc:
            self.connection.rollback()
            raise RuntimeError(f"Could not delete product: {exc}") from exc
        finally:
            cursor.close()

    def find_by_id(self, product_id):
        """Return a Product for the given ID, or None."""
        query = """
            SELECT product_id, name, description, category_id, supplier_id,
                   unit_price, quantity_in_stock, reorder_level
            FROM products
            WHERE product_id = %s
        """
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, (product_id,))
        row = cursor.fetchone()
        cursor.close()
        return Product.from_row(row) if row else None

    def search(self, keyword):
        """Search products by name or description. Return a list of Product."""
        query = """
            SELECT p.product_id, p.name, p.description, c.name AS category,
                   s.name AS supplier, p.category_id, p.supplier_id,
                   p.unit_price, p.quantity_in_stock, p.reorder_level
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
            WHERE p.name LIKE %s OR p.description LIKE %s
            ORDER BY p.name
        """
        term = f"%{keyword}%"
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, (term, term))
        rows = cursor.fetchall()
        cursor.close()
        return [Product.from_row(row) for row in rows]

    def find_all(self):
        """Return all products with joined category / supplier names."""
        query = """
            SELECT p.product_id, p.name, p.description, p.category_id,
                   p.supplier_id, c.name AS category, s.name AS supplier,
                   p.unit_price, p.quantity_in_stock, p.reorder_level
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
            ORDER BY p.product_id
        """
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return [Product.from_row(row) for row in rows]

    def find_low_stock(self):
        """Return products whose stock is at or below their reorder level."""
        query = """
            SELECT product_id, name, description, category_id, supplier_id,
                   unit_price, quantity_in_stock, reorder_level
            FROM products
            WHERE quantity_in_stock <= reorder_level
            ORDER BY quantity_in_stock
        """
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return [Product.from_row(row) for row in rows]

    def find_all_for_value(self):
        """Return all products ordered by inventory value (descending)."""
        query = """
            SELECT product_id, name, description, category_id, supplier_id,
                   unit_price, quantity_in_stock, reorder_level
            FROM products
            ORDER BY quantity_in_stock * unit_price DESC
        """
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return [Product.from_row(row) for row in rows]

    def update_stock(self, product_id, quantity_change, cursor=None):
        """Increment quantity_in_stock by *quantity_change*.

        When called inside a multi-step transaction, pass an existing
        *cursor* so the caller controls commit / rollback.
        Returns the number of rows affected.
        """
        query = """
            UPDATE products
            SET quantity_in_stock = quantity_in_stock + %s
            WHERE product_id = %s
        """
        own_cursor = cursor is None
        if own_cursor:
            cursor = self.connection.cursor()
        try:
            cursor.execute(query, (quantity_change, product_id))
            if own_cursor:
                self.connection.commit()
            return cursor.rowcount
        except Error as exc:
            if own_cursor:
                self.connection.rollback()
            raise RuntimeError(f"Could not update stock: {exc}") from exc
        finally:
            if own_cursor:
                cursor.close()
