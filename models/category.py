class Category:
    MAX_NAME_LENGTH = 80
    MAX_DESCRIPTION_LENGTH = 255

    def __init__(self, name, description="", category_id=None):
        self.category_id = category_id
        self.name = (name or "").strip()
        self.description = (description or "").strip()

        self.validate()

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self):
        """Raise ValueError if any field violates business rules."""
        if not self.name:
            raise ValueError("Category name cannot be empty.")
        if len(self.name) > self.MAX_NAME_LENGTH:
            raise ValueError(
                f"Category name must be at most {self.MAX_NAME_LENGTH} characters."
            )
        if len(self.description) > self.MAX_DESCRIPTION_LENGTH:
            raise ValueError(
                f"Description must be at most {self.MAX_DESCRIPTION_LENGTH} characters."
            )

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------

    def to_insert_values(self):
        """Return a tuple suitable for an INSERT statement."""
        self.validate()
        return self.name, self.description

    def to_update_values(self):
        """Return a tuple suitable for an UPDATE … WHERE category_id = %s."""
        self.validate()
        return self.name, self.description, self.category_id

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def to_display_row(self):
        return {
            "ID": self.category_id,
            "Name": self.name,
            "Description": self.description,
        }

    # ------------------------------------------------------------------
    # Construction helpers
    # ------------------------------------------------------------------

    @classmethod
    def from_row(cls, row):
        return cls(
            category_id=row["category_id"],
            name=row["name"],
            description=row.get("description") or "",
        )

    def __repr__(self):
        return f"Category(id={self.category_id}, name={self.name!r})"
