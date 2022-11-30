from pony import orm

from server.modules.database import db


class ExpenseItem(db.Entity):
    """Database entity representing expense item"""

    product = orm.Required("Product")
    amount = orm.Required(int)
    price = orm.Required(float)
    expense = orm.Required("Expense")
    shared_with = orm.Set("Household")

    def to_json(self):
        return {
            "id": self.id,
            "product": self.product.to_json(),
            "amount": self.amount,
            "price": self.price,
            "sharedWith": list(self.shared_with)[0].to_json()
            if list(self.shared_with)
            else None,
        }


@orm.db_session
def get_all() -> orm.core.Query:
    """Returns all expense items"""
    return ExpenseItem.select()


@orm.db_session
def get_by_id(expense_item_id) -> ExpenseItem | None:
    """Returns expense item with given id"""
    if not expense_item_id:
        return None
    return ExpenseItem.get(id=expense_item_id)


@orm.db_session
def get_by_product(product_id) -> orm.core.Query:
    """Returns all expense items for given product"""
    return ExpenseItem.select(
        lambda expense_item: expense_item.product.id == product_id
    )


@orm.db_session
def add(product, amount, price, expense) -> ExpenseItem:
    """Adds expense item to database"""
    return ExpenseItem(product=product, amount=amount, price=price, expense=expense)
