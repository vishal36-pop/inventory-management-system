import mysql.connector
from mysql.connector import Error

from config import DB_CONFIG


class DatabaseConnection:
    """Small wrapper around mysql-connector to keep connection handling tidy.

    Supports both explicit open/close and context-manager (``with``) usage::

        with DatabaseConnection() as db:
            connection = db.get_connection()
            ...
    """

    def __init__(self, config=None):
        self.config = config or DB_CONFIG
        self.connection = None

    def connect(self, use_database=True):
        config = self.config.copy()
        if not use_database:
            config.pop("database", None)

        try:
            self.connection = mysql.connector.connect(**config)
            return self.connection
        except Error as exc:
            raise RuntimeError(f"Could not connect to MySQL: {exc}") from exc

    def get_connection(self):
        if self.connection is None or not self.connection.is_connected():
            return self.connect()
        return self.connection

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    # ------------------------------------------------------------------
    # Context-manager support
    # ------------------------------------------------------------------

    def __enter__(self):
        self.get_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False  # do not suppress exceptions
