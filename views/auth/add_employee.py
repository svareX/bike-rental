from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import forms
import utils
from service.user_service import UserService

add_employee = Blueprint('add_employee', __name__)

@add_employee.route("/add_employee", methods=['GET', 'POST'])
def page():
    form = forms.RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        password = UserService.addEmployee(request.form['first_name'], request.form['last_name'], request.form['email'])
        if password is None:
            flash('Účet s tímto emailem již existuje!', 'error')
            return redirect('/add_employee')
        else:
            return render_template("add_employee.jinja", form=form, password=password)
    return render_template("add_employee.jinja", form=form)