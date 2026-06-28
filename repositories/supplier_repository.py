from mysql.connector import Error

from models.supplier import Supplier


class SupplierRepository:
    """Handles all SQL operations for the suppliers table."""

    def __init__(self, connection):
        self.connection = connection

    def insert(self, supplier: Supplier):
        """Insert a new supplier and return the generated ID."""
        query = """
            INSERT INTO suppliers (name, phone, email, address)
            VALUES (%s, %s, %s, %s)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, supplier.to_insert_values())
            self.connection.commit()
            return cursor.lastrowid
        except Error as exc:
            self.connection.rollback()
            raise RuntimeError(f"Could not add supplier: {exc}") from exc
        finally:
            cursor.close()

    def update(self, supplier: Supplier):
        """Update an existing supplier. Return the number of rows affected."""
        query = """
            UPDATE suppliers
            SET name = %s, phone = %s, email = %s, address = %s
            WHERE supplier_id = %s
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, supplier.to_update_values())
            self.connection.commit()
            return cursor.rowcount
        except Error as exc:
            self.connection.rollback()
            raise RuntimeError(f"Could not update supplier: {exc}") from exc
        finally:
            cursor.close()

    def delete(self, supplier_id):
        """Delete a supplier by ID. Return the number of rows affected."""
        query = "DELETE FROM suppliers WHERE supplier_id = %s"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (supplier_id,))
            self.connection.commit()
            return cursor.rowcount
        except Error as exc:
            self.connection.rollback()
            raise RuntimeError(f"Could not delete supplier: {exc}") from exc
        finally:
            cursor.close()

    def find_by_id(self, supplier_id):
        """Return a Supplier for the given ID, or None."""
        query = """
            SELECT supplier_id, name, phone, email, address
            FROM suppliers
            WHERE supplier_id = %s
        """
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, (supplier_id,))
        row = cursor.fetchone()
        cursor.close()
        return Supplier.from_row(row) if row else None

    def find_all(self):
        """Return all suppliers ordered by name."""
        query = """
            SELECT supplier_id, name, phone, email, address
            FROM suppliers
            ORDER BY name
        """
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return [Supplier.from_row(row) for row in rows]
