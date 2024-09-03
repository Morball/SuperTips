from functools import wraps
from flask import redirect, url_for, session,flash

def login_required():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                flash("Authentication required!","error")
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        return wrapper
    return decorator



