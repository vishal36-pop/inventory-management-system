import re


class Supplier:
    MAX_NAME_LENGTH = 100
    MAX_PHONE_LENGTH = 20
    MAX_EMAIL_LENGTH = 100
    MAX_ADDRESS_LENGTH = 255

    # Simple pattern: at least one char, then @, then at least one char.
    _EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    # Phone may contain digits, spaces, dashes, plus sign, and parentheses.
    _PHONE_PATTERN = re.compile(r"^[\d\s\-\+\(\)]+$")

    def __init__(self, name, phone="", email="", address="", supplier_id=None):
        self.supplier_id = supplier_id
        self.name = (name or "").strip()
        self.phone = (phone or "").strip()
        self.email = (email or "").strip()
        self.address = (address or "").strip()

        self.validate()

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self):
        """Raise ValueError if any field violates business rules."""
        if not self.name:
            raise ValueError("Supplier name cannot be empty.")
        if len(self.name) > self.MAX_NAME_LENGTH:
            raise ValueError(
                f"Supplier name must be at most {self.MAX_NAME_LENGTH} characters."
            )

        # Phone (optional but validated when provided)
        if self.phone:
            if len(self.phone) > self.MAX_PHONE_LENGTH:
                raise ValueError(
                    f"Phone must be at most {self.MAX_PHONE_LENGTH} characters."
                )
            if not self._PHONE_PATTERN.match(self.phone):
                raise ValueError(
                    "Phone may only contain digits, spaces, dashes, "
                    "plus sign, and parentheses."
                )

        # Email (optional but validated when provided)
        if self.email:
            if len(self.email) > self.MAX_EMAIL_LENGTH:
                raise ValueError(
                    f"Email must be at most {self.MAX_EMAIL_LENGTH} characters."
                )
            if not self._EMAIL_PATTERN.match(self.email):
                raise ValueError("Email format is invalid.")

        if len(self.address) > self.MAX_ADDRESS_LENGTH:
            raise ValueError(
                f"Address must be at most {self.MAX_ADDRESS_LENGTH} characters."
            )

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------

    def to_insert_values(self):
        """Return a tuple suitable for an INSERT statement."""
        self.validate()
        return self.name, self.phone, self.email, self.address

    def to_update_values(self):
        """Return a tuple suitable for an UPDATE … WHERE supplier_id = %s."""
        self.validate()
        return self.name, self.phone, self.email, self.address, self.supplier_id

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def to_display_row(self):
        return {
            "ID": self.supplier_id,
            "Name": self.name,
            "Phone": self.phone,
            "Email": self.email,
            "Address": self.address,
        }

    # ------------------------------------------------------------------
    # Construction helpers
    # ------------------------------------------------------------------

    @classmethod
    def from_row(cls, row):
        return cls(
            supplier_id=row["supplier_id"],
            name=row["name"],
            phone=row.get("phone") or "",
            email=row.get("email") or "",
            address=row.get("address") or "",
        )

    def __repr__(self):
        return f"Supplier(id={self.supplier_id}, name={self.name!r})"
