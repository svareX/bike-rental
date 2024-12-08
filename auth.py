from flask import session
from flask import redirect
from flask import url_for
from flask import flash
from functools import wraps


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print(session)
        if "authenticated" not in session:
            flash("🚫 Musíte být přihlášen pro přístup na tuto stránku", "error")
            return redirect(url_for("login.page"))
        return func(*args, **kwargs)
    return decorated_function


def roles_required(*roles):
    def roles_decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if session['role'] not in roles:
                flash('🚫 Nemáte oprávnění pro tuto akci', 'error')
                return redirect(url_for('login.page'))
            return func(*args, **kwargs)
        return decorated_function
    return roles_decorator