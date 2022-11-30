from datetime import datetime
from pony import orm

from server.modules.database import db

from server.modules.blueprints.expense_items import db_expense_items


class Expense(db.Entity):
    """Database entity representing expense"""

    datetime: datetime = orm.Required(datetime)
    user = orm.Required("User")
    vendor = orm.Required("Vendor")
    expense_items = orm.Set(db_expense_items.ExpenseItem)

    def to_json(self):
        return {
            "id": self.id,
            "date": self.datetime.timestamp() * 1000,
            "userId": self.user.id,
            "vendor": self.vendor.to_json(),
            "items": [expense_item.to_json() for expense_item in self.expense_items],
        }


@orm.db_session
def get_all() -> list[Expense]:
    """Returns all expenses"""
    return Expense.select()


@orm.db_session
def get_by_user(user_id) -> list[Expense]:
    """Returns all expenses for given user"""
    return Expense.select(lambda expense: expense.user.id == user_id)


@orm.db_session
def get_by_id(expense_id) -> Expense | None:
    """Returns expense with given id"""
    if not expense_id:
        return None
    return Expense.get(id=expense_id)


@orm.db_session
def add(date_time, user, vendor) -> Expense:
    """Adds expense to database"""
    return Expense(datetime=date_time, user=user, vendor=vendor)
