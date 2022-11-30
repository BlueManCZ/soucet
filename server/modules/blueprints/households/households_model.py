from pony import orm

from server.modules.database import db


class Household(db.Entity):
    """Database entity representing households"""

    name = orm.Required(str)
    users = orm.Set("User")
    shared_expenses = orm.Set("ExpenseItem")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "users": [user.id for user in self.users],
        }


@orm.db_session
def get_by_id(household_id) -> Household | None:
    """Returns household with given id"""
    if not household_id:
        return None
    return Household.get(id=household_id)


@orm.db_session
def add(name: str) -> Household:
    """Adds households to database"""
    return Household(name=name)
