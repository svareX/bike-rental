from flask import session
from flask import redirect
from flask import url_for
from flask import flash
from functools import wraps

from service.bike_event_service import BikeEventService
from service.bike_service import BikeService


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print(session)
        if "authenticated" not in session:
            flash("🚫 Musíte být přihlášen pro přístup na tuto stránku.", "error")
            return redirect(url_for("auth.login_page"))
        return func(*args, **kwargs)
    return decorated_function


def roles_required(*roles):
    def roles_decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if session['role'] not in roles:
                flash('🚫 Nemáte oprávnění pro tuto akci.', 'error')
                return redirect(url_for('auth.login_page'))
            return func(*args, **kwargs)
        return decorated_function
    return roles_decorator

def user_permission_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if str(session['user_id']) != str(kwargs.get('user_id')):
            flash('🚫 Nemáte oprávnění pro tuto akci.', 'error')
            return redirect(url_for('view_dashboard_page'))
        return func(*args, **kwargs)
    return decorated_function

def employees_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session['role'] != 1:
            flash('🚫 Nemáte oprávnění pro tuto akci (nejste zaměstnanec).', 'error')
            return redirect(url_for('view_dashboard_page'))
        return func(*args, **kwargs)
    return decorated_function

def admin_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session['role'] != 2:
            flash('🚫 Nemáte oprávnění pro tuto akci (nejste správce).', 'error')
            return redirect(url_for('view_dashboard_page'))
        return func(*args, **kwargs)
    return decorated_function

def check_bike_exist(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        bike_id = kwargs.get('bike_id')
        if not bike_id or not BikeService.getByID(bike_id):
            flash('🚫 Kolo nebylo nalezeno.', 'error')
            return redirect(url_for('view_dashboard_page'))
        return func(*args, **kwargs)
    return decorated_function

def check_event_exist(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        event_id = kwargs.get('event_id')
        if not event_id or not BikeEventService.getByID(event_id):
            flash('🚫 Event nebyl nalezen.', 'error')
            return redirect(url_for('view_dashboard_page'))
        return func(*args, **kwargs)
    return decorated_function
