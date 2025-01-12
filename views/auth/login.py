from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import forms
import utils
from service.user_service import UserService

login = Blueprint('login', __name__)

@login.route('/login', methods=['GET', 'POST'])
def page():
    form = forms.SignInForm(request.form)

    if request.method == 'POST' and form.validate():
        user = UserService.verify(request.form['email'], request.form['password'])
        if not user:
            flash('😣 Špatný e-mail nebo heslo!', 'error')
        else:
            utils.login_user(session, user)
            flash('Úspěšně jste se přihlásil.', 'success')
            return redirect(url_for('view_dashboard_page'))

    return render_template("login.jinja", form=form)