from flask import Blueprint, request, session
from pony import orm

from server.modules.decorators import login_required
from server.modules.tools import this_name

from server.modules.blueprints.tools import BlueprintInit
from server.modules.blueprints.users import db_users


def users_blueprint(init: BlueprintInit):
    blueprint = Blueprint(this_name(), __name__)

    @blueprint.route("/register", methods=["POST"])
    @orm.db_session
    def register():
        name = request.json.get("name")
        email = request.json.get("email")
        password = request.json.get("password")

        user = db_users.get_by_email(email)

        if user:
            return {"error": "An email is already used."}, 409

        hashed_password = init.bcrypt.generate_password_hash(password)
        user = db_users.add(name, email, hashed_password)
        user.flush()

        session["user_id"] = user.id

        return user.to_json(), 201

    @blueprint.route("/login", methods=["POST"])
    @orm.db_session
    def login():
        email = request.json.get("email")
        password = request.json.get("password")

        user = db_users.get_by_email(email)

        if not user:
            return {"error": "Unauthorized"}, 401

        if not init.bcrypt.check_password_hash(user.password, password):
            return {"error": "Unauthorized"}, 401

        session["user_id"] = user.id

        return user.to_json(), 201

    @blueprint.route("/logout", methods=["POST"])
    @login_required
    def logout():
        session.pop("user_id")
        return {"message": "Successfully logged out"}, 200

    @blueprint.route("/current_user", methods=["GET"])
    @orm.db_session
    def current_user():
        user_id = session.get("user_id")
        if not user_id:
            return {
                "id": 0,
                "name": "",
                "email": "",
                "households": [],
                "logged_in": False,
            }, 401
        user = db_users.get_by_id(user_id)
        return user.to_json(), 200

    return blueprint
