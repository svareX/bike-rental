import os
import secrets
from flask import Blueprint, request, flash, session, redirect, url_for, render_template, current_app

import auth
import forms
from service.bike_event_service import BikeEventService
from service.bike_service import BikeService
from service.brand_service import BrandService
from service.user_service import UserService

bikes = Blueprint('bikes', __name__)

@bikes.route("/add_bike", methods=['GET', 'POST'])
@auth.login_required
@auth.employees_only
def add_bike_page():
    from app import app
    brands = BrandService.getAll()
    form = forms.BikeForm(request.form, brands)
    show_new_brand = False

    if request.method == 'POST':
        file = request.files['img']
        _, file_extension = os.path.splitext(file.filename)
        filename = secrets.token_hex(12 // 2) + file_extension

        brand_id = request.form.get('brand_id')
        new_brand_name = request.form.get('new_brand_name')

        if new_brand_name:
            brand_result = BrandService.add(new_brand_name)
            if brand_result == 0:
                flash('Tato značka již existuje!', 'error')
                show_new_brand = True
                return render_template("bikes/add_bike.jinja", form=form, show_new_brand=show_new_brand)

            brand_id = BrandService.getIDByName(new_brand_name)

        if file:
            target_folder = os.path.join(app.root_path, 'static/img/')
            os.makedirs(target_folder, exist_ok=True)
            file_path = os.path.join(target_folder, filename)

            response = BikeService.add(
                request.form['bike_name'],
                brand_id,
                request.form['price_per_day'],
                filename
            )

            if response:
                flash(response['error'], 'error')
                return redirect(url_for('view_dashboard_page'))
            file.save(file_path)

        flash('Kolo bylo úspěšně přidáno!', 'success')
        return redirect(url_for('view_dashboard_page'))

    return render_template("bikes/add_bike.jinja", form=form, show_new_brand=show_new_brand)

@bikes.route("/edit_bike/<bike_id>", methods=["GET", "POST"])
@auth.login_required
@auth.employees_only
@auth.check_bike_exist
def edit_bike_page(bike_id):
    from app import app
    response = None
    bike = BikeService.getByID(bike_id)
    brands = BrandService.getAll()

    form = forms.BikeForm(request.form, brands, True)
    form.fill_with_data(bike)

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
                "bikes/edit_bike.jinja",
                form=form,
                bike=bike,
                brands=brands
            )

        flash('✅ Kolo bylo úspěšně upraveno.', 'success')
        return redirect(url_for('view_dashboard_page'))

    return render_template(
        "bikes/edit_bike.jinja",
        form=form,
        bike=bike
    )

@bikes.route('/delete_bike/<bike_id>', methods=["GET", "POST"])
@auth.login_required
@auth.employees_only
@auth.check_bike_exist
def delete_bike_page(bike_id):
    bike = BikeService.getByID(bike_id)

    if request.method == 'POST':
        if 'delete_button' in request.form:
            current_image = bike['img']
            current_image_path = os.path.join(current_app.root_path, 'static/img', current_image)
            if os.path.exists(current_image_path) and current_image != "bike_placeholder.png":
                os.remove(current_image_path)
            BikeService.deleteByID(bike['id'])
            flash('✅ Kolo bylo smazáno z nabídky.', 'success')
        return redirect(url_for('view_dashboard_page'))

    return render_template(
        "bikes/delete_bike.jinja",
        bike=bike
    )

@bikes.route('/rent_bike/<bike_id>', methods=["GET", "POST"])
@auth.login_required
@auth.check_bike_exist
def rent_bike_page(bike_id):
    if session['role'] != 0:
        flash('Pouze zákazníci si mohou vypůjčit kolo!', 'info')
        return redirect(url_for('view_dashboard_page'))
    user = UserService.getByID(session['user_id'])
    bike = BikeService.getByID(bike_id)
    if BikeService.getStatus(bike['id']) != 0:
        flash('Kolo je aktuálně zapůjčené nebo čeká na vyřízení, počkejte prosím.', 'info')
        return redirect(url_for('view_dashboard_page'))

    form = forms.RentBikeForm(request.form)
    if request.method == "POST":
        payment_method = form.payment_method.data
        price = request.form.get('calculated_price')
        if not price or int(price) <= 0:
            flash('Chyba při výpočtu ceny zápůjčky. Zkuste to znovu.', 'error')
            return redirect(url_for('bikes.rent_bike_page', bike_id=bike_id))


        BikeEventService.rent(user['id'],bike['id'],request.form['rent_date_from'],request.form['rent_date_to'], price, payment_method)
        flash('Kolo bylo úspěšně zapůjčeno.', 'success')
        return redirect(url_for('view_dashboard_page'))

    return render_template("bikes/rent_bike.jinja", form=form, bike=bike, user=user)

@bikes.route('/manage_bike/<bike_id>', methods=["GET", "POST"])
@auth.login_required
@auth.employees_only
@auth.check_bike_exist
def manage_bike_page(bike_id):
    if BikeService.getStatus(bike_id) != 2: #Ochrana proti "managování" kol, které nečekají na vyřízení.
        flash('Neoprávněný přístup!', 'error')
        return redirect(url_for('lists.list_manage_bike_page'))
    description = BikeEventService.getDescriptionByBikeID(bike_id)
    bike = BikeService.getByID(bike_id)
    dates = BikeEventService.getRentDatesByID(bike_id)
    eventType = BikeEventService.getEventTypeByID(bike_id)

    form = forms.BikeForm(request.form, None, False)
    if request.method == 'POST':
        if request.form.get('return_bike') and eventType == 1:
            BikeEventService.changeBikeInfo(bike_id, 'Poznámka při vrácení: ' + request.form['description'], 1)
            flash('Kolo bylo úspěšně vráceno zpátky.', 'info')
        elif request.form.get('return_bike') and eventType == 2:
            BikeEventService.changeBikeInfo(bike_id, BikeEventService.getDescriptionByBikeID(bike_id) + '\nPoznámka při vrácení: ' + request.form['description'], 1)
            flash('Kolo bylo úspěšně vráceno zpátky ze servisu.', 'info')
        elif request.form.get('service_bike') and eventType != 2:
            BikeEventService.changeBikeInfo(bike_id, 'Poznámka pro servis: ' + request.form['description'], 2)
            flash('Kolo bylo zasláno do servisu.', 'info')
        return redirect(url_for('lists.list_manage_bike_page'))
    return render_template("bikes/manage_bike.jinja", bike=bike, form=form, dates=dates, eventType=eventType, description=description)