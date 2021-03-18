from . import db
from werkzeug.security import generate_password_hash

class User(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
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
    cost = db.Column(db.Integer)
    stocklevel = db.Column(db.Integer)

    def __init__(self,image, name, description, cost, stocklevel):
        self.image=image
        self.name=name
        self.description=description
        self.cost=cost
        self.stocklevel=stocklevel