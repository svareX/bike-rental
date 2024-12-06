from wtforms import Form, StringField, validators
from wtforms.fields.simple import PasswordField, EmailField


class RegisterForm(Form):
    first_name = StringField(name="first_name", label="Křestní jméno",validators=[validators.InputRequired(), validators.length(min=1, max=20)])
    last_name = StringField(name="last_name", label="Příjmení",validators=[validators.InputRequired(), validators.length(min=1, max=20)])
    email = EmailField(name="email", label='Email', validators=[validators.InputRequired(), validators.Email()])
    password = PasswordField(name='password', label='Heslo', validators=[validators.Length(min=3), validators.InputRequired()])

