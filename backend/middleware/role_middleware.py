from functools import wraps
from flask import request
from utils.helpers import error_response


def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = getattr(request, 'current_user', None)
            if not user:
                return error_response('Authentication required', 401)
            if user.role not in roles:
                return error_response('Access denied for this role', 403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
