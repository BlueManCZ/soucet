from flask import Blueprint, request
from pony import orm

from server.modules.decorators import login_required
from server.modules.tools import this_name

from server.modules.blueprints.tools import BlueprintInit
from server.modules.blueprints.expense_items import db_expense_items
from server.modules.blueprints.product_categories import db_product_categories
from server.modules.blueprints.products import db_products


def products_blueprint(_init: BlueprintInit):
    blueprint = Blueprint(this_name(), __name__)

    @blueprint.route("/products")
    @orm.db_session
    @login_required
    def all_products():
        args = request.args
        if "contains" in args:
            products = db_products.get_by_contains(args.get("contains"))
        else:
            products = db_products.get_all()

        products_json = {product.id: product.to_json() for product in products}

        for product_id in products_json:
            last_item = db_expense_items.get_by_product(product_id)[:][-1]
            if last_item:
                last_price = last_item.price
                products_json[product_id]["lastPrice"] = last_price

        return products_json, 201

    @blueprint.route("/add_product", methods=["POST"])
    @orm.db_session
    @login_required
    def add_product_category():
        name = request.json.get("name")
        category_id = request.json.get("category")
        if db_products.get_by_name(name):
            return {"error": "Product with this name already exists"}, 401
        category = db_product_categories.get_by_id(category_id)
        product = db_products.add(name, category)
        product.flush()
        return product.to_json(), 201

    return blueprint
