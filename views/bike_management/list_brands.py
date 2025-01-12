from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import auth
import forms
from service.bike_event_service import BikeEventService
from service.bike_service import BikeService
from service.brand_service import BrandService
from service.user_service import UserService

list_brands = Blueprint('list_brands', __name__)

@list_brands.route('/list_brands', methods=["GET", "POST"])
@auth.login_required
@auth.employees_only
def page():
    brands = BrandService.getAll()
    return render_template("manage_brands.jinja", brands=brands)