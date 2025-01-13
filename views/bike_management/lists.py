from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import auth
import forms
from service.bike_event_service import BikeEventService
from service.bike_service import BikeService
from service.brand_service import BrandService
from service.user_service import UserService

# Create a single blueprint for all list operations
lists = Blueprint('lists', __name__)

@lists.route('/list_brands', methods=["GET", "POST"])
@auth.login_required
@auth.employees_only
def list_brands_page():
    brands = BrandService.getAll()
    return render_template("manage_brands.jinja", brands=brands)

@lists.route('/list_manage_bike', methods=["GET", "POST"])
@auth.login_required
@auth.employees_only
def list_manage_bike_page():
    bikes = BikeEventService.getByType(1)
    return render_template("list_manage_bike.jinja", bikes=bikes)

@lists.route('/list_service_bike', methods=["GET", "POST"])
@auth.login_required
@auth.employees_only
def list_service_bike_page():
    bikes = BikeEventService.getByType(2)
    return render_template("list_service_bike.jinja", bikes=bikes)