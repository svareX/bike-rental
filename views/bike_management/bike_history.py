from flask import Blueprint, render_template

import auth
from service.bike_event_service import BikeEventService

bike_history = Blueprint('bike_history', __name__)

@bike_history.route('/bike-history')
@auth.login_required
@auth.employees_only
def page():
    bike_events = BikeEventService.getAll()
    return render_template("bikes/history/bike_manage_history.jinja", bike_events=bike_events)