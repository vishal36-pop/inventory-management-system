from models.product import Product
from repositories.product_repository import ProductRepository
from repositories.category_repository import CategoryRepository
from repositories.supplier_repository import SupplierRepository


class ProductService:
    """Business-logic layer for product operations.

    Validates domain rules and checks FK references before delegating
    persistence work to ProductRepository.
    """

    def __init__(
        self,
        product_repo: ProductRepository,
        category_repo: CategoryRepository,
        supplier_repo: SupplierRepository,
    ):
        self.product_repo = product_repo
        self.category_repo = category_repo
        self.supplier_repo = supplier_repo

    def add_product(self, product: Product):
        """Validate the product, verify FK references, then insert."""
        product.validate()
        self._check_references(product)
        return self.product_repo.insert(product)

    def update_product(self, product: Product):
        """Validate the product, verify FK references, then update."""
        product.validate()
        self._check_references(product)
        return self.product_repo.update(product)

    def delete_product(self, product_id):
        """Delete a product by ID."""
        return self.product_repo.delete(product_id)

    def get_product_by_id(self, product_id):
        """Return a single Product or None."""
        return self.product_repo.find_by_id(product_id)

    def search_products(self, keyword):
        """Search products by name or description."""
        return self.product_repo.search(keyword)

    def get_all_products(self):
        """Return every product with joined category/supplier names."""
        return self.product_repo.find_all()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _check_references(self, product: Product):
        """Ensure referenced category and supplier actually exist."""
        if product.category_id is not None:
            if self.category_repo.find_by_id(product.category_id) is None:
                raise ValueError(
                    f"Category with ID {product.category_id} does not exist."
                )
        if product.supplier_id is not None:
            if self.supplier_repo.find_by_id(product.supplier_id) is None:
                raise ValueError(
                    f"Supplier with ID {product.supplier_id} does not exist."
                )
