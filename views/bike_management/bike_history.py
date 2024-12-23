from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import forms
from service.bike_event_service import BikeEventService
from service.bike_service import BikeService
from service.user_service import UserService

bike_history = Blueprint('bike_history', __name__)

@bike_history.route('/bike-history')
def page():
    bike_events = BikeEventService.getAll()
    return render_template("bike_manage_history.jinja", bike_events=bike_events)