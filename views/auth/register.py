from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import forms
import utils
from service.user_service import UserService

register = Blueprint('register', __name__)

@register.route("/register", methods=['GET', 'POST'])
def page():
    form = forms.RegisterForm(request.form)

    if request.method == 'POST':
        user = UserService.register(request.form['first_name'], request.form['last_name'], request.form['email'], request.form['password'])
        if user is None: #Pokud se uživatel se zadaným emailem už našel
            flash('😣 Uživatel s touto e-mailovou adresou již existuje!', 'error')
        else:
            utils.login_user(session, user) #Automaticky přihlásí uživatele po registraci
            flash('Úspěšně jste se zaregistrovali.', 'success')
            return redirect(url_for('view_dashboard_page'))
    return render_template("register.jinja", form=form)