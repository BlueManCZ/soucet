from server.modules.blueprints.expenses import expenses_blueprint
from server.modules.blueprints.households import households_blueprint
from server.modules.blueprints.product_categories import product_categories_blueprint
from server.modules.blueprints.products import products_blueprint
from server.modules.blueprints.users import users_blueprint
from server.modules.blueprints.vendors import vendors_blueprint

blueprints = [
    expenses_blueprint,
    users_blueprint,
    products_blueprint,
    product_categories_blueprint,
    households_blueprint,
    vendors_blueprint,
]
