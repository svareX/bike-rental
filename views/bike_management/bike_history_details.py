from flask import Blueprint, render_template

import auth
from service.bike_event_service import BikeEventService

bike_history_description = Blueprint('bike_history_description', __name__)

@bike_history_description.route('/bike-history/details/<event_id>', methods=["GET", "POST"])
@auth.login_required
@auth.employees_only
@auth.check_event_exist
def page(event_id):
    bike_event = BikeEventService.getByID(event_id)
    return render_template("bikes/history/bike_history_details.jinja", bike_event=bike_event, event_id=event_id)