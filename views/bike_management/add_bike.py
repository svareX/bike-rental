import os
import secrets

from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import forms
from service.bike_service import BikeService
from service.brand_service import BrandService
from service.user_service import UserService

add_bike = Blueprint('add_bike', __name__)

@add_bike.route("/add_bike", methods=['GET', 'POST'])
def page():
    from app import app
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
                return redirect(url_for('page'))
            file.save(file_path)
        return redirect(url_for('view_dashboard_page'))

    return render_template("add_bike.jinja", form=form)