from flask_wtf.file import FileAllowed, FileRequired
from wtforms import Form, StringField, validators
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import FloatField, DecimalField
from wtforms.fields.simple import PasswordField, EmailField, FileField

class RegisterForm(Form):
    first_name = StringField(name="first_name", label="Křestní jméno",validators=[validators.InputRequired(), validators.length(min=1, max=20)])
    last_name = StringField(name="last_name", label="Příjmení",validators=[validators.InputRequired(), validators.length(min=1, max=20)])
    email = EmailField(name="email", label='E-mail', validators=[validators.InputRequired(), validators.Length(min=3, max=40), validators.Email()])
    password = PasswordField(name='password', label='Heslo', validators=[validators.Length(min=3), validators.InputRequired()])

class SignInForm(Form):
    email = EmailField(name="email", label='E-mail', validators=[validators.InputRequired(), validators.Length(min=3, max=40), validators.Email()])
    password = PasswordField(name='password', label='Heslo', validators=[validators.Length(min=3), validators.InputRequired()])

class AddBikeForm(Form):
    def __init__(self, data, brands):
        super(AddBikeForm, self).__init__(data)
        self.brand_id.choices = [(item['id'], item['name']) for item in brands]

    name = StringField(name="bike_name", label="Název kola", validators=[validators.InputRequired(), validators.Length(min=5, max=30)])
    price_per_day = DecimalField(name="price_per_day", label="Cena za den", validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    brand_id = SelectField(name="brand_id", label="Název značky", choices={}, validators=[validators.InputRequired()])
    img = FileField(name="img", label='image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])