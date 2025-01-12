from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import auth
import forms
from service.bike_event_service import BikeEventService
from service.bike_service import BikeService
from service.user_service import UserService

rent_bike = Blueprint('rent_bike', __name__)

@rent_bike.route('/rent_bike/<bike_id>', methods=["GET", "POST"])
@auth.login_required
@auth.customers_only
def page(bike_id):
    user = UserService.getByID(session['user_id'])
    bike = BikeService.getByID(bike_id)
    if BikeService.getStatus(bike['id']) != 0:
        flash('Kolo je aktuálně zapůjčené nebo čeká na vyřízení, počkejte prosím.', 'info')
        return redirect(url_for('view_dashboard_page'))

    form = forms.RentBikeForm(request.form)
    if request.method == "POST" and form.validate():
        payment_method = form.payment_method.data
        price = request.form.get('calculated_price')
        if not price or int(price) <= 0:
            flash('Chyba při výpočtu ceny zápůjčky. Zkuste to znovu.', 'error')
            return redirect(url_for('rent_bike.page', bike_id=bike_id))


        BikeEventService.rent(user['id'],bike['id'],request.form['rent_date_from'],request.form['rent_date_to'], price, payment_method)
        return redirect(url_for('view_dashboard_page'))

    return render_template("rent_bike.jinja", form=form, bike=bike, user=user)
