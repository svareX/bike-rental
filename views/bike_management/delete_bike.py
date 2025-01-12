import os

from flask import Blueprint, request, flash, session, redirect, url_for, render_template, current_app

import auth
from service.bike_service import BikeService

delete_bike = Blueprint('delete_bike', __name__)

@delete_bike.route('/delete_bike/<bike_id>', methods=["GET", "POST"])
@auth.login_required
@auth.employees_only
def page(bike_id):
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

        # render
    return render_template(
        "delete_bike.jinja",
        bike=bike
    )