from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect

from database import database
from service.bike_event_service import BikeEventService
from service.bike_service import BikeService
from service.brand_service import BrandService
from service.user_service import UserService
from views.auth.add_employee import add_employee
from views.auth.auth import auth
from views.auth.delete_user import delete_user
from views.auth.edit_profile import edit_profile
from views.auth.manage_users import manage_users
from views.bike_management.add_brand import add_brand
from views.bike_management.bike_history import bike_history
from views.bike_management.bike_history_details import bike_history_description
from views.bike_management.bikes import bikes
from views.bike_management.delete_brand import delete_brand
from views.bike_management.lists import lists
from views.statistics import statistics

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object('config')
database.init_app(app)

csrf = CSRFProtect()
csrf.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(edit_profile)

app.register_blueprint(bikes)
app.register_blueprint(lists)

app.register_blueprint(bike_history_description)
app.register_blueprint(add_brand)

app.register_blueprint(bike_history)
app.register_blueprint(statistics)
app.register_blueprint(add_employee)
app.register_blueprint(manage_users)
app.register_blueprint(delete_user)
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

