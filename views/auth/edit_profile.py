import os
import secrets

from flask import Blueprint, request, flash, session, redirect, url_for, render_template

import auth
import forms
from service.user_service import UserService

edit_profile = Blueprint('edit_profile', __name__)

@edit_profile.route('/edit_profile/', methods=['GET', 'POST'])
@auth.login_required
def page():
    from app import app
    user = UserService.getByID(session['user_id'])
    form = forms.EditProfileForm(request.form)

    if request.method == 'POST'  and form.validate():
        if form.first_name.data and form.last_name.data:
            UserService.changeName(session['user_id'], request.form['first_name'], request.form['last_name'])
            session['first_name'] = request.form['first_name']
            session['last_name'] = request.form['last_name']
            flash('Jméno bylo úspěšně změněno.', 'success')
        elif form.email.data:
            if not UserService.changeEmail(session['user_id'], request.form['email']):
                session['email'] = request.form['email']
                flash(f'Uživatel s emailem {request.form['email']} již existuje', 'error')
            flash('Email byl úspěšně změněn.', 'success')
        elif form.prev_password.data and form.curr_password.data:
            if not UserService.changePassword(session['user_id'], request.form['prev_password'], request.form['curr_password']):
                flash('Zadané aktuální heslo se neshoduje nebo je stejné s aktuálním heslem.', 'error')
                return redirect(url_for('edit_profile.page'))
            flash('Heslo bylo úspešně změněno.', 'success')
        elif request.files['img']:
            file = request.files['img']
            _, file_extension = os.path.splitext(file.filename)
            filename = secrets.token_hex(12 // 2) + file_extension

            current_image = user['avatar']
            current_image_path = os.path.join(app.root_path, 'static/img', current_image)

            if os.path.exists(current_image_path) and current_image != "person.png" and current_image != "person.svg":
                os.remove(current_image_path)

            UserService.changeAvatar(session['user_id'], filename)
            target_folder = os.path.join(app.root_path, 'static/img/')
            os.makedirs(target_folder, exist_ok=True)

            file_path = os.path.join(target_folder, filename)
            file.save(file_path)
            session['avatar'] = filename
            flash('Profilový obrázek byl úspešně změněn.', 'success')
        return redirect(url_for('view_profile_page', user_id=session['user_id']))
    return render_template("edit_profile.jinja", form=form)