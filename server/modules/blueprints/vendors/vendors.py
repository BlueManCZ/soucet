from flask import Blueprint, request
from pony import orm

from server.modules.decorators import login_required
from server.modules.tools import this_name

from server.modules.blueprints.tools import BlueprintInit
from server.modules.blueprints.vendors import db_vendors


def vendors_blueprint(_init: BlueprintInit):
    blueprint = Blueprint(this_name(), __name__)

    @blueprint.route("/vendors", methods=["GET"])
    @orm.db_session
    @login_required
    def get_vendors():
        args = request.args
        if "contains" in args:
            vendors = db_vendors.get_by_contains(args.get("contains"))
        else:
            vendors = db_vendors.get_all()

        return {vendor.id: vendor.to_json() for vendor in vendors}, 201

    return blueprint
