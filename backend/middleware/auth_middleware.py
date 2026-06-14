from functools import wraps
from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user_model import User
from utils.helpers import error_response


def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = int(get_jwt_identity())
            user = User.query.get(user_id)
            if not user:
                return error_response('User not found', 401)
            request.current_user = user
            return fn(*args, **kwargs)
        except Exception:
            return error_response('Invalid or expired token', 401)
    return wrapper
