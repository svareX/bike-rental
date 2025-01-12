from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import auth
import forms
from service.bike_event_service import BikeEventService
from service.bike_service import BikeService
from service.user_service import UserService

bike_history_description = Blueprint('bike_history_description', __name__)

@bike_history_description.route('/bike-history/details/<event_id>', methods=["GET", "POST"])
@auth.login_required
@auth.employees_only
def page(event_id):
    bike_event = BikeEventService.getByID(event_id)
    return render_template("bike_history_details.jinja", bike_event=bike_event, event_id=event_id)