import os
import secrets

from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import auth
import forms
from service.bike_service import BikeService
from service.brand_service import BrandService

edit_bike = Blueprint('edit_bike', __name__)

@edit_bike.route("/edit_bike/<bike_id>", methods=["GET", "POST"])
@auth.login_required
@auth.employees_only
@auth.check_bike_exist
def page(bike_id):
    from app import app
    response = None
    bike = BikeService.getByID(bike_id)
    brands = BrandService.getAll()

    # forms
    form = forms.BikeForm(request.form, brands, True)
    form.fill_with_data(bike)

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
                form=form,
                bike=bike,
                brands=brands
            )

        flash('✅ Kolo bylo úspěšně upraveno.', 'success')
        return redirect(url_for('view_dashboard_page'))

    return render_template(
        "edit_bike.jinja",
        form=form,
        bike=bike
    )