import os
import secrets

from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import auth
import forms
from service.bike_service import BikeService
from service.brand_service import BrandService
from service.user_service import UserService

add_bike = Blueprint('add_bike', __name__)


@add_bike.route("/add_bike", methods=['GET', 'POST'])
@auth.login_required
@auth.employees_only
def page():
    from app import app
    brands = BrandService.getAll()
    form = forms.BikeForm(request.form, brands)
    show_new_brand = False

    if request.method == 'POST':
        file = request.files['img']
        _, file_extension = os.path.splitext(file.filename)
        filename = secrets.token_hex(12 // 2) + file_extension

        # Handle new brand if provided
        brand_id = request.form.get('brand_id')
        new_brand_name = request.form.get('new_brand_name')

        if new_brand_name:
            # Try to add new brand
            brand_result = BrandService.add(new_brand_name)
            if brand_result == 0:
                flash('Tato značka již existuje!', 'error')
                show_new_brand = True
                return render_template("add_bike.jinja", form=form, show_new_brand=show_new_brand)

            # Get the ID of the newly created brand
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

    return render_template("add_bike.jinja", form=form, show_new_brand=show_new_brand)