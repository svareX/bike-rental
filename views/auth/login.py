from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import forms
from service.user_service import UserService

login = Blueprint('login', __name__)

@login.route('/login', methods=['GET', 'POST'])
def page():
    form = forms.SignInForm(request.form)

    if request.method == 'POST':
        user = UserService.verify(request.form['email'], request.form['password'])
        if not user:
            flash('😣 Špatný e-mail nebo heslo!', 'error')
        else:
            session['authenticated'] = 1
            session['user_id'] = user['id']
            session['first_name'] = user['first_name']
            session['last_name'] = user['last_name']
            session['email'] = user['email']
            session['role'] = user['role']
            session['avatar'] = user['avatar']
            return redirect(url_for('view_dashboard_page'))

    return render_template("login.jinja", form=form)