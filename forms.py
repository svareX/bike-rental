import datetime

from flask_wtf.file import FileAllowed, FileRequired
from wtforms import Form, StringField, validators
from wtforms.fields.choices import SelectField, RadioField
from wtforms.fields.datetime import DateTimeField, DateField
from wtforms.fields.numeric import FloatField, DecimalField
from wtforms.fields.simple import PasswordField, EmailField, FileField, TextAreaField, HiddenField
from wtforms.validators import InputRequired


class RegisterForm(Form):
    first_name = StringField(name="first_name", label="Křestní jméno",validators=[validators.InputRequired(), validators.length(min=1, max=20)])
    last_name = StringField(name="last_name", label="Příjmení",validators=[validators.InputRequired(), validators.length(min=1, max=20)])
    email = EmailField(name="email", label='E-mail', validators=[validators.InputRequired(), validators.Length(min=3, max=40), validators.Email()])
    password = PasswordField(name='password', label='Heslo', validators=[validators.Length(min=3), validators.InputRequired()])

class SignInForm(Form):
    email = EmailField(name="email", label='E-mail', validators=[validators.InputRequired(), validators.Length(min=3, max=40), validators.Email()])
    password = PasswordField(name='password', label='Heslo', validators=[validators.Length(min=3), validators.InputRequired()])

class EditProfileForm(Form):
    first_name = StringField(name="first_name", label="Nové křestní jméno",validators=[validators.InputRequired(), validators.length(min=1, max=20)])
    last_name = StringField(name="last_name", label="Nové příjmení",validators=[validators.InputRequired(), validators.length(min=1, max=20)])
    email = EmailField(name="email", label='Nový e-mail', validators=[validators.InputRequired(), validators.Length(min=3, max=40), validators.Email()])
    prev_password = PasswordField(name='prev_password', label='Aktuální heslo', validators=[validators.Length(min=3), validators.InputRequired()])
    curr_password = PasswordField(name='curr_password', label='Nové heslo', validators=[validators.Length(min=3), validators.InputRequired()])

    img = FileField(name="img", label='Profilový obrázek', validators=[validators.InputRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')])
class BikeForm(Form):
    def __init__(self, data, brands, editing=False):
        super(BikeForm, self).__init__(data)
        if brands is not None:
            self.brand_id.choices = [(item['id'], item['name']) for item in brands]
        self.editing = editing
        if self.editing:
            self.img.render_kw = {'accept': 'image/png, image/jpeg', 'required': False}  # No 'required'
        else:
            self.img.render_kw = {'accept': 'image/png, image/jpeg', 'required': True}
    def fill_with_data(self, bike):
        self.name.data = str(bike['name'])
        self.price_per_day.data = bike['price_per_day']
        self.brand_id.data = str(bike['brand_id'])
        self.img.data = bike['img']

    name = StringField(name="bike_name", label="Název kola", validators=[validators.InputRequired(), validators.Length(min=5, max=30)])
    price_per_day = DecimalField(name="price_per_day", label="Cena za den", validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    brand_id = SelectField(name="brand_id", label="Název značky", choices={}, validators=[validators.InputRequired()])
    img = FileField(name="img", label='Fotografie', validators=[ validators.InputRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])

    #Pouze pro vyřizování kol
    description = TextAreaField(label="", render_kw={'rows': 5, 'placeholder': 'Poznámka'})

#Temporary
class RentBikeForm(Form):
    rent_datetime_from = DateField(name="rent_date_from", label="Datum začátku zápůjčky",render_kw={"min": datetime.date.today().isoformat()}, validators=[validators.InputRequired()])
    rent_datetime_to = DateField(name="rent_date_to", label="Datum konce zápůjčky", validators=[validators.InputRequired()])
    payment_method = RadioField(label="Způsob platby",choices=[('1', 'Platba na místě'), ('2', 'Platba online')],default='1',coerce=str,validators=[validators.InputRequired()]
    )
