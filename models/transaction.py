import enum
from decimal import Decimal


class TransactionType(enum.Enum):
    """Allowed transaction types matching the DB ENUM column."""

    PURCHASE = "PURCHASE"
    SALE = "SALE"


class Transaction:
    # Keep short aliases for convenience (e.g. Transaction.PURCHASE).
    PURCHASE = TransactionType.PURCHASE
    SALE = TransactionType.SALE

    MAX_NOTES_LENGTH = 255

    def __init__(
        self,
        product_id,
        transaction_type,
        quantity,
        unit_price,
        notes="",
        transaction_id=None,
        transaction_date=None,
        product_name=None,
    ):
        self.transaction_id = transaction_id
        self.product_id = int(product_id)
        self.transaction_type = self._coerce_type(transaction_type)
        self.quantity = int(quantity)
        self.unit_price = Decimal(str(unit_price))
        self.notes = (notes or "").strip()
        self.transaction_date = transaction_date
        self.product_name = product_name

        self.validate()

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self):
        """Raise ValueError if any field violates business rules."""
        if self.transaction_type not in TransactionType:
            raise ValueError("Transaction type must be PURCHASE or SALE.")
        if self.product_id <= 0:
            raise ValueError("Product ID must be positive.")
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if self.unit_price < 0:
            raise ValueError("Unit price cannot be negative.")
        if len(self.notes) > self.MAX_NOTES_LENGTH:
            raise ValueError(
                f"Notes must be at most {self.MAX_NOTES_LENGTH} characters."
            )

    # ------------------------------------------------------------------
    # Business helpers
    # ------------------------------------------------------------------

    def stock_change(self):
        """Return the signed quantity change for inventory.

        Positive for purchases, negative for sales.
        """
        if self.transaction_type is TransactionType.PURCHASE:
            return self.quantity
        return -self.quantity

    def total_amount(self):
        """Return quantity × unit_price."""
        return self.quantity * self.unit_price

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------

    def to_insert_values(self):
        """Return a tuple suitable for an INSERT statement."""
        self.validate()
        return (
            self.product_id,
            self.transaction_type.value,
            self.quantity,
            self.unit_price,
            self.notes,
        )

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def to_display_row(self):
        return {
            "ID": self.transaction_id,
            "Product": self.product_name or self.product_id,
            "Type": self.transaction_type.value,
            "Quantity": self.quantity,
            "Price": self.unit_price,
            "Total": self.total_amount(),
            "Date": self.transaction_date,
            "Notes": self.notes,
        }

    # ------------------------------------------------------------------
    # Construction helpers
    # ------------------------------------------------------------------

    @classmethod
    def from_row(cls, row):
        return cls(
            transaction_id=row["transaction_id"],
            product_id=row.get("product_id", 0),
            product_name=row.get("product"),
            transaction_type=row["transaction_type"],
            quantity=row["quantity"],
            unit_price=row["unit_price"],
            transaction_date=row.get("transaction_date"),
            notes=row.get("notes") or "",
        )

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    @staticmethod
    def _coerce_type(value):
        """Accept both TransactionType members and plain strings."""
        if isinstance(value, TransactionType):
            return value
        return TransactionType(value)

    def __repr__(self):
        return (
            f"Transaction(id={self.transaction_id}, product_id={self.product_id}, "
            f"type={self.transaction_type.value}, qty={self.quantity}, "
            f"price={self.unit_price})"
        )
