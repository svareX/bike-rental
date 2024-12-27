from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import auth
import forms
from service.bike_event_service import BikeEventService
from service.bike_service import BikeService
from service.user_service import UserService

list_service_bike = Blueprint('list_service_bike', __name__)

@list_service_bike.route('/list_service_bike', methods=["GET", "POST"])
@auth.login_required
@auth.employees_only
def page():
    bikes = BikeEventService.getByType(2)
    return render_template("list_service_bike.jinja", bikes=bikes)