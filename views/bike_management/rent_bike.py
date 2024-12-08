from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import forms
from service.bike_event_service import BikeEventService
from service.bike_service import BikeService
from service.user_service import UserService

rent_bike = Blueprint('rent_bike', __name__)

@rent_bike.route('/rent_bike/<user_id>/<bike_id>', methods=["GET", "POST"])
def page(user_id, bike_id):
    user = UserService.getByID(user_id)
    bike = BikeService.getByID(bike_id)

    form = forms.RentBikeForm(request.form)
    if request.method == "POST":
        BikeEventService.rent(user['id'], bike['id'], request.form['rent_date_from'], request.form['rent_date_to'])
        return redirect(url_for('view_dashboard_page'))
    return render_template("rent_bike.jinja", form=form, bike=bike, user=user)