from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField,IntegerField, FloatField, TextAreaField, SelectField, DateField, TimeField
from wtforms_components import DateRange
from wtforms.validators import InputRequired, DataRequired, Length, Email, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed
from datetime import datetime, date

# Declaration of Form Classes using the Flask WTForms components.
# Where Validation is also added

#login forn
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

#This form updates the quantity of items in the shopping cart
class UpdateQuant(FlaskForm):
    update_quantity = StringField('Update', validators=[InputRequired()])

#This form allows a user to add an item to the inventory  
class InventoryForm(FlaskForm):
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg', 'Image Files Only'])
    ])

    name= StringField('Name',
    validators=[DataRequired()])

    description = TextAreaField(
            'Description',
            [
                DataRequired(),
                Length(5, 255,
                message=('Your message is too short.'))
            ]
        )

    stocklevel = IntegerField(
        'Stock Level',
        [
            DataRequired()
        ]
    )
    
    cost = FloatField(
        'Cost',
        [
            DataRequired()
        ]
    )

#This form allows a user to update an item in the inventory
class UpdateForm(FlaskForm):
    photo_update = FileField('Update Photo', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'Image Files Only'])
    ])

    name= StringField('Name',
    validators=[DataRequired()])

    description = TextAreaField(
            'Description',
            [
                DataRequired(),
                Length(5, 255,
                message=('Your message is too short.'))
            ]
        )

    stocklevel = IntegerField(
        'Stock Level',
        [
            DataRequired()
        ]
    )
    
    cost = FloatField(
        'Cost',
        [
            DataRequired()
        ]
    )

#This form allows a user to sign up
class SignUpForm(FlaskForm):
    firstname= StringField('First Name',
    validators=[InputRequired(),
    Length(max=40)])

    lastname= StringField('Last Name',
    validators=[InputRequired(),
    Length(max=40)])

    phoneNumber = StringField('Phone Number',
    validators=[
        InputRequired(),
        Length(min=7, max=25)
    ])

    username = StringField('Username', 
    validators=[InputRequired()])
    
    password = PasswordField('Password',
    validators=[InputRequired()])

    email = StringField(
        'E-mail',
        validators=[
            Email(message=('Not a valid email address.')),
            DataRequired()
        ]
    )

#This forms contains the relevant fields for a user to checkout an order
class CheckoutForm(FlaskForm):
    address = StringField('Address')


    parish = SelectField('Parish',
    choices=
    [('Kingston','Kingston'),
    ('Saint Andrew', 'Saint Andrew'),
    ('Saint Catherine', 'Saint Catherine'),
    ('Hanover','Hanover'),
    ('Saint Elizabeth','Saint Elizabeth'),
    ('Saint James','Saint James'),
    ('Trelawny','Trelawny'),
    ('Westmoreland','Westmoreland'),
    ('Clarendon','Clarendon'),
    ('Manchester','Manchester'),
    ('Saint Ann','Saint Ann'),
    ('Saint Mary','Saint Mary'),
    ('Portland','Portland'),
    ('Saint Thomas', 'Saint Thomas')]
    
    )

    delivery_instructions= TextAreaField('Delivery Instructions')

    payment_methods = RadioField('Payment Methods',
    choices=[('Cash','Cash'),('NCB','NCB'),('Scotiabank','Scotiabank')], default="Cash",
    validators=[DataRequired()])

    discountCode = StringField('Discount Code')

#This form allows the user to add an expense to the expenses table
class ExpensesForm(FlaskForm):
    date_range = DateField(
        'Date',
        validators=[DataRequired()])
    
    name = StringField('Name', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[InputRequired()])

#This form allows a user to add a discount Code and amount
class DiscountForm(FlaskForm):
    discount = StringField('Discount Code',validators=[DataRequired()]) 
    amount = FloatField('Amount', validators=[DataRequired()])

#This form allows a user to add a Delivery Location and Fee
class DeliveryFeeForm(FlaskForm):
    delivery = StringField('Location',validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])