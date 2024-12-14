from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import forms
from service.bike_event_service import BikeEventService
from service.bike_service import BikeService
from service.user_service import UserService

list_bike = Blueprint('list_bike', __name__)

@list_bike.route('/list_bike', methods=["GET", "POST"])
def page():
    bikes = BikeEventService.getRented()
    return render_template("list_bike.jinja", bikes=bikes)