from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import auth
import forms
from service.bike_event_service import BikeEventService
from service.bike_service import BikeService
from service.user_service import UserService

manage_bike = Blueprint('manage_bike', __name__)

@manage_bike.route('/manage_bike/<bike_id>', methods=["GET", "POST"])
@auth.login_required
@auth.employees_only
def page(bike_id):
    if BikeService.getStatus(bike_id) != 2: #Ochrana proti "managování" kol, které nečekají na vyřízení.
        flash('Neoprávněný přístup!', 'error')
        return redirect(url_for('list_manage_bike.page'))
    bike = BikeService.getByID(bike_id)
    dates = BikeEventService.getRentDatesByID(bike_id)
    eventType = BikeEventService.getEventTypeByID(bike_id)

    form = forms.BikeForm(request.form, None, False)
    if request.method == 'POST' and form.validate():
        if request.form.get('return_bike') and eventType == 1:
            BikeEventService.changeBikeInfo(bike_id, 'Poznámka při vrácení: ' + request.form['description'], 1)
            flash('Kolo bylo úspěšně vráceno zpátky.', 'info')
        elif request.form.get('return_bike') and eventType == 2:
            BikeEventService.changeBikeInfo(bike_id, BikeEventService.getDescriptionByBikeID(bike_id) + '\nPoznámka při vrácení: ' + request.form['description'], 1)
            flash('Kolo bylo úspěšně vráceno zpátky ze servisu.', 'info')
        elif request.form.get('service_bike') and eventType != 2:
            BikeEventService.changeBikeInfo(bike_id, 'Poznámka pro servis: ' + request.form['description'], 2)
            flash('Kolo bylo zasláno do servisu.', 'info')
        return redirect(url_for('list_manage_bike.page'))
    return render_template("manage_bike.jinja", bike=bike, form=form, dates=dates, eventType=eventType)