from flask import redirect, render_template, request, url_for
from functools import wraps

from . import globals

# Decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        cookie_session = request.cookies.get(globals.session_key)

        if not cookie_session or cookie_session not in globals.session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def server_open_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not globals.server_is_open:
            return render_template('warning.html')
        return f(*args, **kwargs)
    return decorated_function
