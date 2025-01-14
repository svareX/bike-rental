from flask import Blueprint, render_template

import auth
from service.bike_event_service import BikeEventService
from service.brand_service import BrandService

lists = Blueprint('lists', __name__)

@lists.route('/list_brands', methods=["GET", "POST"])
@auth.login_required
@auth.employees_only
def list_brands_page():
    brands = BrandService.getAll()
    return render_template("brands/manage_brands.jinja", brands=brands)

@lists.route('/list_manage_bike', methods=["GET", "POST"])
@auth.login_required
@auth.employees_only
def list_manage_bike_page():
    bikes = BikeEventService.getByType(1)
    return render_template("bikes/lists/list_manage_bike.jinja", bikes=bikes)

@lists.route('/list_service_bike', methods=["GET", "POST"])
@auth.login_required
@auth.employees_only
def list_service_bike_page():
    bikes = BikeEventService.getByType(2)
    return render_template("bikes/lists/list_service_bike.jinja", bikes=bikes)