from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField,IntegerField, FloatField, TextAreaField, SelectField
from wtforms.validators import InputRequired, DataRequired, Length, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class UpdateQuant(FlaskForm):
    update_quantity = StringField('Update', validators=[InputRequired()])

    
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

    drop_off = SelectField('Select Drop off Location',
    choices=
    [('Half Way Tree','Half Way Tree'),
    ('UWI/UTech','UWI/UTech'),
    ('Portmore','Portmore'),
    ('Spanish Town', 'Spanish Town'),
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

    discountCode = StringField('Discount Code',
    validators=
    [
    Length(max=7)
    ])


