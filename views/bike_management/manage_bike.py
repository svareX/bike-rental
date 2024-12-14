from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import forms
from service.bike_event_service import BikeEventService
from service.bike_service import BikeService
from service.user_service import UserService

manage_bike = Blueprint('manage_bike', __name__)

@manage_bike.route('/manage_bike/<bike_id>', methods=["GET", "POST"])
def page(bike_id):
    bike = BikeService.getByID(bike_id)
    dates = BikeEventService.getRentDatesByID(bike_id)
    form = forms.BikeForm(request.form, None, False)
    if request.method == 'POST':
        BikeEventService.returnBike(bike_id, request.form['description'])
        return redirect(url_for('list_bike.page'))
    return render_template("manage_bike.jinja", bike=bike, form=form, dates=dates)