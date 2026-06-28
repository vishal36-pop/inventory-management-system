from repositories.product_repository import ProductRepository
from repositories.transaction_repository import TransactionRepository


class ReportService:
    """Builds report data for the CLI layer."""

    def __init__(
        self,
        product_repo: ProductRepository,
        transaction_repo: TransactionRepository,
    ):
        self.product_repo = product_repo
        self.transaction_repo = transaction_repo

    def low_stock_report(self):
        """Return products whose stock is at or below their reorder level."""
        return self.product_repo.find_low_stock()

    def inventory_value_report(self):
        """Return all products ordered by descending inventory value."""
        return self.product_repo.find_all_for_value()

    def transaction_history(self):
        """Return full transaction history, newest first."""
        return self.transaction_repo.find_all_history()
