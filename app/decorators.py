from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorator_func(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            else:
                return f(*args, **kwargs)
        return decorator_func
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMIN)(f)