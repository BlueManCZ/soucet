from pony import orm

from server.modules.database import db


class Vendor(db.Entity):
    """Database entity representing vendor"""

    name = orm.Required(str)
    description = orm.Optional(str)
    expenses = orm.Set("Expense")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }


@orm.db_session
def get_all() -> list[Vendor]:
    """Returns all vendors"""
    return Vendor.select()


@orm.db_session
def get_by_contains(contains: str) -> list[Vendor]:
    """Returns vendors with names containing given string"""
    if not contains:
        return []
    return Vendor.select(lambda v: contains.lower() in v.name.lower())


@orm.db_session
def get_by_id(vendor_id) -> Vendor | None:
    """Returns vendor with given id"""
    if not vendor_id:
        return None
    return Vendor.get(id=vendor_id)


@orm.db_session
def add(name: str, description: str) -> Vendor:
    """Adds vendor to database"""
    return Vendor(name=name, description=description)
