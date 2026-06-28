from models.category import Category
from repositories.category_repository import CategoryRepository


class CategoryService:
    """Business-logic layer for category operations."""

    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    def add_category(self, category: Category):
        """Validate and insert a new category."""
        category.validate()
        return self.category_repo.insert(category)

    def update_category(self, category: Category):
        """Validate and update an existing category."""
        category.validate()
        return self.category_repo.update(category)

    def delete_category(self, category_id):
        """Delete a category by ID."""
        return self.category_repo.delete(category_id)

    def get_all_categories(self):
        """Return all categories."""
        return self.category_repo.find_all()

    def get_category_by_id(self, category_id):
        """Return a single Category or None."""
        return self.category_repo.find_by_id(category_id)
