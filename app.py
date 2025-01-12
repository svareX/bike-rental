import os
import secrets
from datetime import datetime

from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask_wtf.file import FileAllowed

import forms
from database import database
from service.bike_event_service import BikeEventService
from service.bike_service import BikeService
from service.brand_service import BrandService
from service.user_service import UserService
from views.auth.add_employee import add_employee
from views.auth.delete_user import delete_user
from views.auth.edit_profile import edit_profile
from views.auth.login import login
from views.auth.logout import page, logout
from views.auth.manage_users import manage_users
from views.auth.register import register
from views.bike_management.add_bike import add_bike
from views.bike_management.add_brand import add_brand
from views.bike_management.bike_history import bike_history
from views.bike_management.bike_history_details import bike_history_description
from views.bike_management.delete_bike import page, delete_bike
from views.bike_management.delete_brand import delete_brand
from views.bike_management.edit_bike import edit_bike
from views.bike_management.list_brands import list_brands
from views.bike_management.list_manage_bike import list_manage_bike
from views.bike_management.list_service_bike import list_service_bike
from views.bike_management.manage_bike import manage_bike
from views.bike_management.rent_bike import rent_bike
from views.statistics import statistics

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object('config')
database.init_app(app)

csrf = CSRFProtect()
csrf.init_app(app)


app.register_blueprint(login)
app.register_blueprint(register)
app.register_blueprint(logout)
app.register_blueprint(edit_profile)

app.register_blueprint(add_bike)
app.register_blueprint(edit_bike)
app.register_blueprint(delete_bike)
app.register_blueprint(rent_bike)
app.register_blueprint(list_manage_bike)
app.register_blueprint(list_service_bike)
app.register_blueprint(manage_bike)
app.register_blueprint(bike_history_description)
app.register_blueprint(add_brand)

app.register_blueprint(bike_history)
app.register_blueprint(statistics)
app.register_blueprint(add_employee)
app.register_blueprint(manage_users)
app.register_blueprint(delete_user)
app.register_blueprint(list_brands)
app.register_blueprint(delete_brand)

@app.before_request
def before_request():
    BikeEventService.check_rents()
@app.route("/", methods=['GET'])
def view_dashboard_page():
    brand_id = request.args.get('brand_id', None)
    search_query = request.args.get('search', None)
    rent_status = request.args.get('rent_status', 'all')
    brands = BrandService.getAll()
    bikes = BikeService.getBikesFiltered(brand_id, search_query, rent_status)

    return render_template(
        "dashboard.jinja",
        bikes=bikes,
        is_rented=BikeService.getStatus,
        getRentDate=BikeEventService.getRentDatesByID,
        brands=brands,
        selected_brand=brand_id,
        search_query=search_query,
        rent_status = rent_status
    )


@app.route('/profile/<user_id>')
def view_profile_page(user_id):
    user = UserService.getByID(user_id)
    bikes = BikeEventService.getRentedBikesByID(user_id)
    return render_template("profile.jinja", user=user, bikes=bikes, getReliability=UserService.getReliability)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)

