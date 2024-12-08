import os
import secrets

from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_wtf.file import FileAllowed

import forms
from database import database
from service.bike_event_service import BikeEventService
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
    return render_template("dashboard.jinja", bikes=bikes, is_rented=BikeService.checkRented, getRentDate=BikeEventService.getRentEndDateByID)

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
    form = forms.BikeForm(request.form, brands)

    if request.method == 'POST':
        file = request.files['img']
        _, file_extension = os.path.splitext(file.filename)
        filename = secrets.token_hex(12 // 2) + file_extension

        if file:
            target_folder = os.path.join(app.root_path, 'static/img/')
            os.makedirs(target_folder, exist_ok=True)

            file_path = os.path.join(target_folder, filename)

            response = BikeService.add(
                request.form['bike_name'],
                request.form['brand_id'],
                request.form['price_per_day'],
                filename
            )

            if response:
                flash(response['error'], 'error')  # Show an error message
                return redirect(url_for('view_add_bike'))
            file.save(file_path)
        return redirect(url_for('view_dashboard_page'))

    return render_template("add_bike.jinja", form=form)

@app.route("/edit_bike/<bike_id>", methods=["GET", "POST"])
def view_edit_bike(bike_id):
    response = None
    bike = BikeService.getByID(bike_id)
    brands = BrandService.getAll()

    # forms
    bike_form = forms.BikeForm(request.form, brands, True)
    bike_form.fill_with_data(bike)

    # edit transaction
    if request.method == 'POST':
        if request.files['img']:
            file = request.files['img']
            _, file_extension = os.path.splitext(file.filename)
            filename = secrets.token_hex(12 // 2) + file_extension

            current_image = bike['img']
            current_image_path = os.path.join(app.root_path, 'static/img', current_image)

            if os.path.exists(current_image_path) and current_image != "bike_placeholder.png":
                os.remove(current_image_path)

            response = BikeService.update(bike_id, request.form['bike_name'], request.form['price_per_day'], request.form['brand_id'], filename)
            if not response:
                file.save(os.path.join(os.path.join(app.root_path, 'static/img/'), filename))
        else:
            response = BikeService.update(bike_id, request.form['bike_name'], request.form['price_per_day'], request.form['brand_id'], bike['img'])

        if response:
            flash(response['error'], 'error')
            return render_template(
                "edit_bike.jinja",
                form=bike_form,
                bike=bike,
                brands=brands
            )

        flash('✅ Kolo bylo úspěšně upraveno.', 'success')
        return redirect(url_for('view_dashboard_page'))

    return render_template(
        "edit_bike.jinja",
        form=bike_form,
        bike=bike
    )

@app.route('/delete_bike/<bike_id>', methods=["GET", "POST"])
def delete_bike(bike_id):
    bike = BikeService.getByID(bike_id)

    if request.method == 'POST':
        if 'delete_button' in request.form:
                current_image = bike['img']
                current_image_path = os.path.join(app.root_path, 'static/img', current_image)
                if os.path.exists(current_image_path) and current_image != "bike_placeholder.png":
                    os.remove(current_image_path)
                BikeService.deleteByID(bike['id'])
                flash('✅ Kolo bylo smazáno z nabídky.', 'success')
        return redirect(url_for('view_dashboard_page'))

        # render
    return render_template(
        "delete_bike.jinja",
        bike=bike
    )

@app.route('/rent_bike/<user_id>/<bike_id>', methods=["GET", "POST"])
def view_rent_bike(user_id,bike_id):
    user = UserService.getByID(user_id)
    bike = BikeService.getByID(bike_id)

    form = forms.RentBikeForm(request.form)
    if request.method == "POST":
        BikeEventService.rent(user['id'], bike['id'], request.form['rent_date_from'], request.form['rent_date_to'])
        return redirect(url_for('view_dashboard_page'))
    return render_template("rent_bike.jinja", form=form, bike=bike, user=user)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)

