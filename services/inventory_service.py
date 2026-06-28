from mysql.connector import Error

from models.transaction import Transaction
from repositories.product_repository import ProductRepository
from repositories.transaction_repository import TransactionRepository


class InventoryService:
    """Handles stock-changing operations (purchases and sales).

    Coordinates ProductRepository and TransactionRepository within a
    single database transaction so that stock updates and transaction
    records are committed atomically.
    """

    def __init__(
        self,
        product_repo: ProductRepository,
        transaction_repo: TransactionRepository,
    ):
        self.product_repo = product_repo
        self.transaction_repo = transaction_repo
        self.connection = product_repo.connection

    def record_purchase(self, transaction: Transaction):
        """Validate, update stock, and insert a PURCHASE transaction."""
        return self._record_transaction(transaction)

    def record_sale(self, transaction: Transaction):
        """Validate stock availability, update stock, and insert a SALE."""
        product = self.transaction_repo.find_product_for_update(
            transaction.product_id
        )
        if product is None:
            raise ValueError("Product not found.")
        if product["quantity_in_stock"] < transaction.quantity:
            raise ValueError("Not enough stock available for this sale.")

        return self._record_transaction(transaction)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _record_transaction(self, transaction: Transaction):
        """Atomically update stock and insert the transaction record."""
        transaction.validate()
        try:
            cursor = self.connection.cursor()

            # 1. Update product stock
            self.product_repo.update_stock(
                transaction.product_id,
                transaction.stock_change(),
                cursor=cursor,
            )
            if cursor.rowcount == 0:
                raise ValueError("Product not found.")

            # 2. Insert transaction record
            last_id = self.transaction_repo.insert(
                transaction, cursor=cursor
            )

            self.connection.commit()
            return last_id
        except Error as exc:
            self.connection.rollback()
            raise RuntimeError(
                f"Could not record transaction: {exc}"
            ) from exc
        except ValueError:
            self.connection.rollback()
            raise
        finally:
            cursor.close()
