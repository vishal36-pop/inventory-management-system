from mysql.connector import Error

from models.category import Category


class CategoryRepository:
    """Handles all SQL operations for the categories table."""

    def __init__(self, connection):
        self.connection = connection

    def insert(self, category: Category):
        """Insert a new category and return the generated ID."""
        query = """
            INSERT INTO categories (name, description)
            VALUES (%s, %s)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, category.to_insert_values())
            self.connection.commit()
            return cursor.lastrowid
        except Error as exc:
            self.connection.rollback()
            raise RuntimeError(f"Could not add category: {exc}") from exc
        finally:
            cursor.close()

    def update(self, category: Category):
        """Update an existing category. Return the number of rows affected."""
        query = """
            UPDATE categories
            SET name = %s, description = %s
            WHERE category_id = %s
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, category.to_update_values())
            self.connection.commit()
            return cursor.rowcount
        except Error as exc:
            self.connection.rollback()
            raise RuntimeError(f"Could not update category: {exc}") from exc
        finally:
            cursor.close()

    def delete(self, category_id):
        """Delete a category by ID. Return the number of rows affected."""
        query = "DELETE FROM categories WHERE category_id = %s"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (category_id,))
            self.connection.commit()
            return cursor.rowcount
        except Error as exc:
            self.connection.rollback()
            raise RuntimeError(f"Could not delete category: {exc}") from exc
        finally:
            cursor.close()

    def find_by_id(self, category_id):
        """Return a Category for the given ID, or None."""
        query = """
            SELECT category_id, name, description
            FROM categories
            WHERE category_id = %s
        """
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, (category_id,))
        row = cursor.fetchone()
        cursor.close()
        return Category.from_row(row) if row else None

    def find_all(self):
        """Return all categories ordered by name."""
        query = """
            SELECT category_id, name, description
            FROM categories
            ORDER BY name
        """
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return [Category.from_row(row) for row in rows]
