from mysql.connector import Error

from models.transaction import Transaction


class TransactionRepository:
    """Handles all SQL operations for the transactions table."""

    def __init__(self, connection):
        self.connection = connection

    def insert(self, transaction: Transaction, cursor=None):
        """Insert a new transaction record.

        When called inside a multi-step DB transaction, pass an existing
        *cursor* so the caller controls commit / rollback.
        Returns the lastrowid.
        """
        query = """
            INSERT INTO transactions
                (product_id, transaction_type, quantity, unit_price, notes)
            VALUES (%s, %s, %s, %s, %s)
        """
        own_cursor = cursor is None
        if own_cursor:
            cursor = self.connection.cursor()
        try:
            cursor.execute(query, transaction.to_insert_values())
            last_id = cursor.lastrowid
            if own_cursor:
                self.connection.commit()
            return last_id
        except Error as exc:
            if own_cursor:
                self.connection.rollback()
            raise RuntimeError(
                f"Could not record transaction: {exc}"
            ) from exc
        finally:
            if own_cursor:
                cursor.close()

    def find_all_history(self):
        """Return all transactions with product names, newest first."""
        query = """
            SELECT t.transaction_id, t.product_id, p.name AS product,
                   t.transaction_type, t.quantity, t.unit_price,
                   t.transaction_date, t.notes
            FROM transactions t
            INNER JOIN products p ON t.product_id = p.product_id
            ORDER BY t.transaction_date DESC, t.transaction_id DESC
        """
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return [Transaction.from_row(row) for row in rows]

    def find_product_for_update(self, product_id):
        """Fetch minimal product data needed before recording a transaction.

        Returns a dict with 'product_id' and 'quantity_in_stock', or None.
        """
        query = """
            SELECT product_id, quantity_in_stock
            FROM products
            WHERE product_id = %s
        """
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, (product_id,))
        row = cursor.fetchone()
        cursor.close()
        return row
