import os

from flask import Blueprint, request, flash, session, redirect, url_for, render_template, current_app

import auth
from service.bike_event_service import BikeEventService
from service.bike_service import BikeService
from service.brand_service import BrandService

delete_brand = Blueprint('delete_brand', __name__)

@delete_brand.route('/delete_brand/<brand_id>', methods=["GET", "POST"])
@auth.login_required
@auth.employees_only
def page(brand_id):
    BrandService.delete(brand_id)
    BikeEventService.deleteByBrandID(brand_id)
    BikeService.deleteByBrand(brand_id)
    flash('Značka byla úspěšně smazaná.','success')
    return redirect(url_for('view_dashboard_page'))