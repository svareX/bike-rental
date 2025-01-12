from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import auth
import forms
from service.brand_service import BrandService

add_brand = Blueprint('add_brand', __name__)

@add_brand.route("/add_brand", methods=['GET', 'POST'])
@auth.login_required
@auth.employees_only
def page():
    form = forms.BrandForm(request.form)
    if request.method == 'POST' and form.validate():
        brand = BrandService.add(request.form['brand_name'])
        if brand == 0:
            flash("Značka již existuje", "error")
        else:
            flash(f'Značka \"{request.form['brand_name']}\" úspěšně přidána.', 'success')
            return redirect(url_for('view_dashboard_page'))
    return render_template("add_brand.jinja", form=form)