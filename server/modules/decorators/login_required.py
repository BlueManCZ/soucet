from flask import session
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if session.get("user_id"):
            return f(*args, **kwargs)
        return {"error": "Unauthorized"}, 401

    return decorator
