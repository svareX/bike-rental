import os
import secrets
from datetime import datetime

from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_wtf.file import FileAllowed

import forms
from database import database
from service.bike_event_service import BikeEventService
from service.bike_service import BikeService
from service.brand_service import BrandService
from service.user_service import UserService
from views.auth.login import login
from views.auth.logout import page, logout
from views.auth.register import register
from views.bike_management.add_bike import add_bike
from views.bike_management.delete_bike import page, delete_bike
from views.bike_management.edit_bike import edit_bike
from views.bike_management.rent_bike import rent_bike

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object('config')
database.init_app(app)


app.register_blueprint(login)
app.register_blueprint(register)
app.register_blueprint(logout)

app.register_blueprint(add_bike)
app.register_blueprint(edit_bike)
app.register_blueprint(delete_bike)
app.register_blueprint(rent_bike)

@app.route("/")
def view_dashboard_page():
    bikes = BikeService.getAll();
    return render_template("dashboard.jinja", bikes=bikes, is_rented=BikeService.checkRented, getRentDate=BikeEventService.getRentEndDateByID)


@app.route('/profile/<user_id>')
def view_profile_page(user_id):
    user = UserService.getByID(user_id)
    bikes = BikeEventService.getRentedBikesByID(user_id)
    return render_template("profile.jinja", user=user, bikes=bikes)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)

