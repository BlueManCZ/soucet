from datetime import datetime
from flask import Blueprint, request, session
from pony import orm

from server.modules.decorators import login_required
from server.modules.tools import this_name

from server.modules.blueprints.tools import BlueprintInit
from server.modules.blueprints.households import db_households
from server.modules.blueprints.expense_items import db_expense_items
from server.modules.blueprints.expenses import db_expenses
from server.modules.blueprints.product_categories import db_product_categories
from server.modules.blueprints.products import db_products
from server.modules.blueprints.users import db_users
from server.modules.blueprints.vendors import db_vendors


def expenses_blueprint(_init: BlueprintInit):
    blueprint = Blueprint(this_name(), __name__)

    @blueprint.route("/expenses")
    @orm.db_session
    @login_required
    def get_expenses():
        expenses = db_expenses.get_by_user(session["user_id"])
        return [expense.to_json() for expense in expenses], 201

    @blueprint.route("/add_expense", methods=["POST"])
    @orm.db_session
    @login_required
    def add_expense():
        print(request.json)
        date_time = datetime.fromtimestamp(request.json.get("date") / 1000)
        db_user = db_users.get_current()
        db_vendor = db_vendors.get_by_id(request.json.get("vendor")["id"])
        if not db_vendor:
            db_vendor = db_vendors.add(
                request.json.get("vendor")["name"],
                request.json.get("vendor")["description"],
            )
        db_expense = db_expenses.add(date_time, db_user, db_vendor)

        expense_items = request.json.get("items")
        for expense_item in expense_items:
            product = expense_item.get("product")
            product_name = product.get("name")
            product_category_id = product.get("category")["id"]
            db_category = db_product_categories.get_by_id(product_category_id)
            amount = expense_item.get("amount")
            price = expense_item.get("price")

            db_product = db_products.get_by_name_and_category(product_name, db_category)
            if not db_product:
                db_product = db_products.add(product_name, db_category)

            db_household = None
            if expense_item.get("shareWith"):
                db_household = db_households.get_by_id(
                    expense_item.get("shareWith")["id"]
                )

            db_expense_item = db_expense_items.add(
                db_product, amount, price, db_expense
            )
            if db_household:
                db_expense_item.shared_with.add(db_household)
            db_expense.expense_items.add(db_expense_item)

        db_expense.flush()

        return db_expense.to_json(), 201

    @blueprint.route("/edit_expense", methods=["POST"])
    @orm.db_session
    @login_required
    def edit_expense():
        print(request.json)

        db_expense = db_expenses.get_by_id(request.json.get("id"))

        if not db_expense:
            return {"error": "Expense not found"}, 404

        db_user = db_users.get_current()
        if db_expense.user.id != db_user.id:
            return {"error": "Unauthorized"}, 401

        db_expense.datetime = datetime.fromtimestamp(request.json.get("date") / 1000)

        db_vendor = db_vendors.get_by_id(request.json.get("vendor")["id"])
        if not db_vendor:
            db_vendor = db_vendors.add(
                request.json.get("vendor")["name"],
                request.json.get("vendor")["description"],
            )

        db_expense.vendor = db_vendor

        expense_items = request.json.get("items")
        for expense_item in expense_items:
            product = expense_item.get("product")
            product_name = product.get("name")
            product_category_id = product.get("category")["id"]
            db_category = db_product_categories.get_by_id(product_category_id)
            amount = expense_item.get("amount")
            price = expense_item.get("price")
            db_product = db_products.get_by_name_and_category(product_name, db_category)
            if not db_product:
                db_product = db_products.add(product_name, db_category)

            db_household = None
            if expense_item.get("shareWith"):
                db_household = db_households.get_by_id(
                    expense_item.get("shareWith")["id"]
                )

            db_expense_item = db_expense_items.get_by_id(expense_item.get("id"))
            if not db_expense_item:
                db_expense_item = db_expense_items.add(
                    db_product, amount, price, db_expense
                )
                db_expense.expense_items.add(db_expense_item)
            db_expense_item.price = expense_item.get("price")
            db_expense_item.amount = expense_item.get("amount")
            db_expense_item.product = db_product
            if db_household:
                db_expense_item.shared_with = db_household

        db_expense.flush()

        return db_expense.to_json(), 201

    @blueprint.route("/household_expenses")
    @orm.db_session
    @login_required
    def household_expenses():
        db_household_members = []
        user_households = db_users.get_current().households
        for household in user_households:
            for user in household.users:
                if user not in db_household_members:
                    db_household_members.append(user)

        db_expenses_all = []
        for user in db_household_members:
            db_user_expenses = db_expenses.get_by_user(user.id)
            for expense in db_user_expenses:
                hit = False
                for item in expense.expense_items:
                    if any(
                        household in user_households for household in item.shared_with
                    ):
                        hit = True
                        break
                if hit:
                    json_expense = expense.to_json()
                    json_expense["items"] = [
                        item.to_json()
                        for item in filter(
                            lambda expense_item: any(
                                item_household in user_households
                                for item_household in expense_item.shared_with
                            ),
                            expense.expense_items,
                        )
                    ]
                    db_expenses_all.append(json_expense)

        return [expense for expense in db_expenses_all], 201

    return blueprint
