import os

from flask import Blueprint, session, redirect, url_for, flash, current_app

import auth
from service.user_service import UserService

delete_user = Blueprint('delete_user', __name__)

@delete_user.route('/delete_user/<user_id>', methods=["GET", "POST"])
@auth.login_required
def page(user_id):
    user = UserService.getByID(user_id)
    if session['role'] == 2 and int(user_id) != 1:  # Admin can delete any user except themselves
        current_image = user['avatar']
        current_image_path = os.path.join(current_app.root_path, 'static/img', current_image)
        if os.path.exists(current_image_path) and current_image != "person.png":
            os.remove(current_image_path)
        UserService.remove(user_id)
        flash('Účet byl úspěšně smazán.', 'success')

    elif session['user_id'] == int(user_id) and int(user_id) != 1:  # Allow users to delete themselves
        current_image = user['avatar']
        current_image_path = os.path.join(current_app.root_path, 'static/img', current_image)
        if os.path.exists(current_image_path) and current_image != "person.png":
            os.remove(current_image_path)
        UserService.remove(user_id)
        flash('Účet byl úspěšně odstraněn.', 'success')
        session.pop("authenticated")
        session.pop("user_id")
        session.pop("first_name")
        session.pop("last_name")
        session.pop("email")
        session.pop("role")
        flash('Účet byl úspěšně smazán.', 'success')
    else:
        flash('Nemáte oprávnění k provedení této akce!', 'error')

    return redirect(url_for('view_dashboard_page'))