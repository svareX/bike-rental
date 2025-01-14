from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import forms
import utils
from service.user_service import UserService

auth = Blueprint('auth', __name__)

@auth.route("/register", methods=['GET', 'POST'])
def register_page():
    form = forms.RegisterForm(request.form)

    if request.method == 'POST':
        user = UserService.register(
            request.form['first_name'],
            request.form['last_name'],
            request.form['email'],
            request.form['password']
        )
        if user is None:  # Pokud se uživatel se zadaným emailem už našel
            flash('😣 Uživatel s touto e-mailovou adresou již existuje!', 'error')
        else:
            utils.login_user(session, user)  # Automaticky přihlásí uživatele po registraci
            flash('Úspěšně jste se zaregistrovali.', 'success')
            return redirect(url_for('view_dashboard_page'))
    return render_template("auth/register.jinja", form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    form = forms.SignInForm(request.form)

    if request.method == 'POST':
        user = UserService.verify(request.form['email'], request.form['password'])
        if not user:
            flash('😣 Špatný e-mail nebo heslo!', 'error')
        else:
            utils.login_user(session, user)
            flash('Úspěšně jste se přihlásil.', 'success')
            return redirect(url_for('view_dashboard_page'))

    return render_template("auth/login.jinja", form=form)

@auth.route('/logout')
def logout_page():
    session.pop("authenticated")
    session.pop("user_id")
    session.pop("first_name")
    session.pop("last_name")
    session.pop("email")
    session.pop("role")
    return redirect(url_for('auth.login_page'))