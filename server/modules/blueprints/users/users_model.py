from flask import session
from pony import orm

from server.modules.database import db


class User(db.Entity):
    """Database entity representing user"""

    name = orm.Required(str)
    email = orm.Required(str)
    password = orm.Required(bytes)
    households = orm.Set("Household")
    expenses = orm.Set("Expense")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "households": [household.to_json() for household in self.households],
            "logged_in": True,
        }


@orm.db_session
def get_by_id(user_id) -> User | None:
    """Returns user with given id"""
    if not user_id:
        return None
    return User.get(id=user_id)


@orm.db_session
def get_current() -> User | None:
    """Returns current user from session"""
    if not session["user_id"]:
        return None
    return User.get(id=session["user_id"])


@orm.db_session
def get_all() -> list[User]:
    """Returns all users"""
    return User.select()


@orm.db_session
def get_by_email(email: str) -> User | None:
    """Returns user with given email"""
    if not email:
        return None
    return User.get(email=email)


@orm.db_session
def add(name: str, email: str, password: str) -> User:
    """Adds user to database"""
    return User(name=name, email=email, password=password)
