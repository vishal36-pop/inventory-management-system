from decimal import Decimal


class Product:
    MAX_NAME_LENGTH = 100
    MAX_DESCRIPTION_LENGTH = 255

    def __init__(
        self,
        name,
        description,
        category_id,
        supplier_id,
        unit_price,
        quantity_in_stock=0,
        reorder_level=5,
        product_id=None,
        category_name=None,
        supplier_name=None,
    ):
        self.product_id = product_id
        self.name = (name or "").strip()
        self.description = (description or "").strip()
        self.category_id = category_id
        self.supplier_id = supplier_id
        self.unit_price = Decimal(str(unit_price))
        self.quantity_in_stock = int(quantity_in_stock)
        self.reorder_level = int(reorder_level)
        self.category_name = category_name
        self.supplier_name = supplier_name

        self.validate()

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self):
        """Raise ValueError if any field violates business rules."""
        if not self.name:
            raise ValueError("Product name cannot be empty.")
        if len(self.name) > self.MAX_NAME_LENGTH:
            raise ValueError(
                f"Product name must be at most {self.MAX_NAME_LENGTH} characters."
            )
        if len(self.description) > self.MAX_DESCRIPTION_LENGTH:
            raise ValueError(
                f"Description must be at most {self.MAX_DESCRIPTION_LENGTH} characters."
            )
        if self.unit_price < 0:
            raise ValueError("Unit price cannot be negative.")
        if self.quantity_in_stock < 0:
            raise ValueError("Quantity cannot be negative.")
        if self.reorder_level < 0:
            raise ValueError("Reorder level cannot be negative.")
        if self.category_id is not None and int(self.category_id) <= 0:
            raise ValueError("Category ID must be a positive integer.")
        if self.supplier_id is not None and int(self.supplier_id) <= 0:
            raise ValueError("Supplier ID must be a positive integer.")

    # ------------------------------------------------------------------
    # Business helpers
    # ------------------------------------------------------------------

    def is_low_stock(self):
        """Return True if current stock is at or below the reorder level."""
        return self.quantity_in_stock <= self.reorder_level

    def inventory_value(self):
        """Return unit_price × quantity_in_stock."""
        return self.unit_price * self.quantity_in_stock

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------

    def to_insert_values(self):
        """Return a tuple suitable for an INSERT statement."""
        self.validate()
        return (
            self.name,
            self.description,
            self.category_id,
            self.supplier_id,
            self.unit_price,
            self.quantity_in_stock,
            self.reorder_level,
        )

    def to_update_values(self):
        """Return a tuple suitable for an UPDATE … WHERE product_id = %s."""
        self.validate()
        return self.to_insert_values() + (self.product_id,)

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def to_display_row(self):
        return {
            "ID": self.product_id,
            "Name": self.name,
            "Category": self.category_name or "-",
            "Supplier": self.supplier_name or "-",
            "Price": self.unit_price,
            "Stock": self.quantity_in_stock,
            "Reorder": self.reorder_level,
        }

    def to_low_stock_row(self):
        return {
            "ID": self.product_id,
            "Name": self.name,
            "Stock": self.quantity_in_stock,
            "Reorder": self.reorder_level,
        }

    def to_value_row(self):
        return {
            "ID": self.product_id,
            "Name": self.name,
            "Stock": self.quantity_in_stock,
            "Price": self.unit_price,
            "Total Value": self.inventory_value(),
        }

    # ------------------------------------------------------------------
    # Construction helpers
    # ------------------------------------------------------------------

    @classmethod
    def from_row(cls, row):
        return cls(
            product_id=row["product_id"],
            name=row["name"],
            description=row.get("description") or "",
            category_id=row.get("category_id"),
            supplier_id=row.get("supplier_id"),
            unit_price=row["unit_price"],
            quantity_in_stock=row["quantity_in_stock"],
            reorder_level=row["reorder_level"],
            category_name=row.get("category"),
            supplier_name=row.get("supplier"),
        )

    def __repr__(self):
        return (
            f"Product(id={self.product_id}, name={self.name!r}, "
            f"price={self.unit_price}, stock={self.quantity_in_stock})"
        )
