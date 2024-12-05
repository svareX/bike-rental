from wtforms import Form, StringField, SelectField, validators
from wtforms.fields.choices import RadioField
from wtforms.fields.numeric import DecimalField
from wtforms.fields.simple import TextAreaField, PasswordField
from wtforms.validators import InputRequired, NumberRange


class FilterTransactionsForm(Form):
    search = StringField(label='Hledat')
    min_amount = DecimalField(label='Min. částka')


class TransactionForm(Form):
    def __init__(self, data, types, categories):
        super(TransactionForm, self).__init__(data)
        self.type.choices = [(item['id'], item['name']) for item in types]
        self.category.choices = [(item['id'], item['name']) for item in categories]

    def fill_with_transaction(self, transaction):
        self.type.data = str(transaction['transaction_type_id'])
        self.amount.data = transaction['amount']
        self.category.data = str(transaction['transaction_category_id'])
        self.description.data = transaction['description']

    type = RadioField(label='Typ', choices=[], validators=[InputRequired()])
    amount = DecimalField(label='Částka (Kč)', validators=[InputRequired(), NumberRange(min=1)])
    category = SelectField(label='Kategorie', choices=[], validators=[InputRequired()])
    description = TextAreaField(label='Poznámka', render_kw={'rows': 10})


class SignInForm(Form):
    login = StringField(name='login', label='Uživatelské jméno', validators=[validators.Length(min=2, max=30), validators.InputRequired()])
    password = PasswordField(name='password', label='Heslo', validators=[validators.Length(min=3), validators.InputRequired()])

