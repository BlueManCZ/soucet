from flask import Blueprint, request
from pony import orm

from server.modules.decorators import login_required
from server.modules.tools import this_name

from server.modules.blueprints.tools import BlueprintInit
from server.modules.blueprints.product_categories import db_product_categories


def product_categories_blueprint(_init: BlueprintInit):
    blueprint = Blueprint(this_name(), __name__)

    @blueprint.route("/product_categories")
    @orm.db_session
    @login_required
    def all_products():
        categories = db_product_categories.get_all()
        return {category.id: category.to_json() for category in categories}, 201

    @blueprint.route("/add_product_category", methods=["POST"])
    @orm.db_session
    @login_required
    def add_product_category():
        name = request.json.get("name")
        icon_name = request.json.get("icon_name")
        if db_product_categories.get_by_name(name):
            return {"error": "Product category already exists"}, 401
        product_category = db_product_categories.add(name, icon_name)
        product_category.flush()
        return product_category.to_json(), 201

    return blueprint
