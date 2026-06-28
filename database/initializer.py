from pathlib import Path

import mysql.connector

from config import DB_CONFIG


class DatabaseInitializer:
    def __init__(self, schema_path=None):
        default_schema = Path(__file__).resolve().parent.parent / "schema.sql"
        self.schema_path = Path(schema_path) if schema_path else default_schema

    def initialize(self):
        config = DB_CONFIG.copy()
        config.pop("database", None)

        try:
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            statements = self._read_schema()
            for statement in statements:
                cursor.execute(statement)

            connection.commit()
            print("Database is ready.")
        except mysql.connector.Error as exc:
            print(f"Database setup failed: {exc}")
        finally:
            if "cursor" in locals():
                cursor.close()
            if "connection" in locals() and connection.is_connected():
                connection.close()

    def _read_schema(self):
        sql = self.schema_path.read_text(encoding="utf-8")
        return [stmt.strip() for stmt in sql.split(";") if stmt.strip()]


if __name__ == "__main__":
    DatabaseInitializer().initialize()
