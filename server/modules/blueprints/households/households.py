from flask import Blueprint, request, session
from pony import orm

from server.modules.decorators import login_required
from server.modules.tools import this_name

from server.modules.blueprints.tools import BlueprintInit
from server.modules.blueprints.households import db_households
from server.modules.blueprints.users import db_users


def households_blueprint(_init: BlueprintInit):
    blueprint = Blueprint(this_name(), __name__)

    @blueprint.route("/create_household", methods=["POST"])
    @orm.db_session
    @login_required
    def create_household():
        name = request.json.get("name")

        if not name:
            return {"error": "Name is required"}, 401

        household = db_households.add(name)
        household.flush()

        user = db_users.get_by_id(session.get("user_id"))
        user.households.append(household)

        return {
            "id": household.id,
            "name": household.name,
        }, 201

    @blueprint.route("/household_members")
    @orm.db_session
    @login_required
    def household_members():
        users = []
        for household in db_users.get_current().households:
            for user in household.users:
                users.append(user.to_json())

        return users, 201

    return blueprint
