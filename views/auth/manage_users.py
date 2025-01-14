from flask import Blueprint, render_template

import auth
from service.user_service import UserService

manage_users = Blueprint('manage_users', __name__)

@manage_users.route("/manage_users", methods=['GET', 'POST'])
@auth.login_required
@auth.admin_only
def page():
    users = UserService.getAll()
    return render_template("manage_users.jinja", users=users)