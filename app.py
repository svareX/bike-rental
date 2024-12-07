import os
import secrets

from flask import Flask, render_template, request, flash, session, redirect, url_for

import forms
from database import database
from service.bike_service import BikeService
from service.brand_service import BrandService
from service.user_service import UserService

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object('config')
database.init_app(app)


@app.route("/")
def view_dashboard_page():
    bikes = BikeService.getAll();
    return render_template("dashboard.jinja", bikes=bikes)

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

@app.route('/login', methods=['GET', 'POST'])
def view_login():
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
            return redirect(url_for('view_dashboard_page'))

    return render_template("login.jinja", form=form)

@app.route('/logout')
def logout():
    session.pop("authenticated")
    session.pop("user_id")
    session.pop("first_name")
    session.pop("last_name")
    session.pop("email")
    session.pop("role")
    return redirect(url_for('view_login'))

@app.route("/add_bike", methods=['GET', 'POST'])
def view_add_bike():
    brands = BrandService.getAll()
    form = forms.AddBikeForm(request.form, brands)

    if request.method == 'POST':
        file = request.files['img']
        _, file_extension = os.path.splitext(file.filename)
        filename = secrets.token_hex(12 // 2) + file_extension

        if file:
            target_folder = os.path.join(app.root_path, 'static/img/')
            os.makedirs(target_folder, exist_ok=True)  # Ensure the folder exists

            file_path = os.path.join(target_folder, filename)

            # Attempt to add the bike

            response = BikeService.add(
                request.form['bike_name'],
                request.form['brand_id'],  # Replace with the correct brand ID
                request.form['price_per_day'],
                filename
            )

            if response:
                flash(response['error'], 'error')  # Show an error message
                return redirect(url_for('view_add_bike'))
            file.save(file_path)
        return redirect(url_for('view_dashboard_page'))

    return render_template("add_bike.jinja", form=form)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)

