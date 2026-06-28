from models.supplier import Supplier
from repositories.supplier_repository import SupplierRepository


class SupplierService:
    """Business-logic layer for supplier operations."""

    def __init__(self, supplier_repo: SupplierRepository):
        self.supplier_repo = supplier_repo

    def add_supplier(self, supplier: Supplier):
        """Validate and insert a new supplier."""
        supplier.validate()
        return self.supplier_repo.insert(supplier)

    def update_supplier(self, supplier: Supplier):
        """Validate and update an existing supplier."""
        supplier.validate()
        return self.supplier_repo.update(supplier)

    def delete_supplier(self, supplier_id):
        """Delete a supplier by ID."""
        return self.supplier_repo.delete(supplier_id)

    def get_all_suppliers(self):
        """Return all suppliers."""
        return self.supplier_repo.find_all()

    def get_supplier_by_id(self, supplier_id):
        """Return a single Supplier or None."""
        return self.supplier_repo.find_by_id(supplier_id)
