from app import db
from werkzeug.security import generate_password_hash
from app.Business.order_status import OrderStatus, PaymentStatus
from datetime import datetime

"""This file contains all the tables used to form the database"""

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    phone_number = db.Column(db.BigInteger)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(80))
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)

    def __init__(self, first_name, last_name, phone_number, username, password,email):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email

class Inventory(db.Model):

    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    image=db.Column(db.String(80),unique=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    cost = db.Column(db.Float)
    stocklevel = db.Column(db.Integer)

    def __init__(self,image, name, description, cost, stocklevel):
        self.image=image
        self.name=name
        self.description=description
        self.cost=cost
        self.stocklevel=stocklevel


class Orders(db.Model):

    __tablename__ = 'orders'

    orderNumber= db.Column(db.Integer, primary_key=True)
    currentTime = db.Column(db.DateTime, nullable=False,
        default=datetime.now)
    predicted_delivery_date = db.Column(db.DateTime)
    trackingNumber = db.Column(db.Integer, unique=True)
    username = db.Column(db.String)
    address = db.Column(db.String)
    parish = db.Column(db.String)
    location = db.Column(db.String)
    gct = db.Column(db.Float)
    subtotal = db.Column(db.Float)
    discount = db.Column(db.Float)
    discount_code = db.Column(db.String)
    total = db.Column(db.Float)
    delivery_fee = db.Column(db.Integer)
    cart = db.Column(db.ARRAY(db.String))
    instructions = db.Column(db.String)
    order_status = db.Column(db.String, default = OrderStatus.ORDER_PLACED.value)
    payment_method = db.Column(db.String)
    payment_status = db.Column(db.String, default=PaymentStatus.NOT_PAID.value)

    def __init__(self,predicted_delivery_date,trackingNumber,username,address,parish,location,gct,subtotal,discount, discount_code,total,delivery_fee,cart,instructions,payment_method):
        self.predicted_delivery_date = predicted_delivery_date
        self.trackingNumber = trackingNumber
        self.username = username
        self.address = address
        self.parish = parish
        self.location = location
        self.gct = gct
        self.subtotal = subtotal
        self.discount = discount
        self.discount_code = discount_code
        self.total = total
        self.delivery_fee = delivery_fee
        self.cart = cart
        self.instructions = instructions
        self.payment_method = payment_method

    
class Expenses(db.Model):

    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    name = db.Column(db.String)
    category = db.Column(db.String)
    description = db.Column(db.String)
    amount = db.Column(db.Float)

    def __init__(self,date, name, category, description,amount):
        self.date = date
        self.name = name
        self.category = category
        self.description = description
        self.amount = amount

class ExpenseCategories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,unique=True)
    
    def __init__(self,name):
        self.name = name

class Fees(db.Model):
    __tablename__ = 'fees'
    id = db.Column(db.Integer, primary_key=True)
    fee_type = db.Column(db.String)
    name = db.Column(db.String,unique=True)
    amount = db.Column(db.Float)
    deliveryTime = db.Column(db.Integer)

    def __init__(self,fee_type,name,amount,deliveryTime):
        self.fee_type = fee_type
        self.name = name
        self.amount = amount
        self.deliveryTime = deliveryTime
      