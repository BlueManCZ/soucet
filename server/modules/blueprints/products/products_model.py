from pony import orm

from server.modules.database import db

from server.modules.blueprints.product_categories import db_product_categories


class Product(db.Entity):
    """Database entity representing product"""

    name = orm.Required(str)
    category = orm.Optional(db_product_categories.ProductCategory)
    expenseItems = orm.Set("ExpenseItem")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category.to_json() if self.category else None,
        }


@orm.db_session
def get_all() -> list[Product]:
    """Returns all products"""
    return Product.select()


@orm.db_session
def get_by_name(name: str) -> Product | None:
    """Returns product with given name"""
    if not name:
        return None
    return Product.get(name=name)


@orm.db_session
def get_by_name_and_category(
    name: str, category: db_product_categories.ProductCategory
) -> Product | None:
    """Returns product with given name and category"""
    if not name or not category:
        return None
    return Product.get(name=name, category=category)


@orm.db_session
def get_by_contains(contains: str) -> list[Product] | None:
    """Returns products with names containing given string"""
    if not contains:
        return []
    return Product.select(lambda p: contains.lower() in p.name.lower())


@orm.db_session
def add(
    name: str, category: db_product_categories.ProductCategory | None
) -> Product | None:
    """Adds product to database"""
    if not name:
        return None
    return Product(name=name, category=category)
