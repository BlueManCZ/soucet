from pony import orm

from server.modules.database import db


class ProductCategory(db.Entity):
    """Database entity representing product category"""

    name = orm.Required(str)
    icon_name = orm.Optional(str)
    products = orm.Set("Product")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "iconName": self.icon_name,
        }


def get_all() -> list[ProductCategory]:
    """Returns all products categories"""
    return ProductCategory.select()


def get_by_id(category_id: int) -> ProductCategory | None:
    """Returns product category with given id"""
    if not category_id:
        return None
    return ProductCategory.get(id=category_id)


def get_by_name(name: str) -> ProductCategory | None:
    """Returns product category with given name"""
    if not name:
        return None
    return ProductCategory.get(name=name)


def add(name: str, icon_name: str) -> ProductCategory | None:
    """Adds product category to database"""
    if not name:
        return None
    return ProductCategory(name=name, icon_name=icon_name)
