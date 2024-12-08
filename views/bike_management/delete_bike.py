import os

from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import forms
from service.bike_service import BikeService
from service.user_service import UserService

delete_bike = Blueprint('delete_bike', __name__)

@delete_bike.route('/delete_bike/<bike_id>', methods=["GET", "POST"])
def page(bike_id):
    from app import app
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