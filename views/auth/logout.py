from flask import Blueprint, session, redirect, url_for

logout = Blueprint('logout', __name__)

@logout.route('/logout')
def page():
    session.pop("authenticated")
    session.pop("user_id")
    session.pop("first_name")
    session.pop("last_name")
    session.pop("email")
    session.pop("role")
    return redirect(url_for('login.page'))