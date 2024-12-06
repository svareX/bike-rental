from flask import Flask, render_template, request, flash, session, redirect, url_for

import forms
from database import database
from service.user_service import UserService

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object('config')
database.init_app(app)


@app.route("/")
def view_dashboard_page():
    return render_template("dashboard.jinja")

@app.route("/register", methods=['GET', 'POST'])
def view_register_page():
    form = forms.RegisterForm(request.form)

    if request.method == 'POST':
        user = UserService.register(request.form['first_name'], request.form['last_name'], request.form['email'], request.form['password'])
        if user:
            flash('😣 Uživatel s touto e-mailovou adresou již existuje!', 'error')
        else:
            return redirect(url_for('view_dashboard_page'))
    return render_template("register.jinja", form=form)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)

