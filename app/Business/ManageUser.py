from app import app, db, login_manager
from flask import render_template, redirect, url_for, flash,session
from flask_login import login_user, logout_user
from app.Database.models import User
from app.Business.shoppingcart import Shoppingcart
from werkzeug.security import check_password_hash
from sqlalchemy.exc import SQLAlchemyError, IntegrityError 

class Autheticate_User():

    #This Authorizes a User, granting them access to the appropriate databases
    def AuthUser(self, username, password):
        user = self.findUser(username)
        if user is not None and check_password_hash(user.password, password):
            login_user(user)
            flash('Successfully Logged in')
            if user.username == 'admin':
                session['name'] = user.username
            else:
                session['name'] = user.first_name
            return True
        return False
    
    #Retrieves a user from the User Table in the Artixa database
    def getUser(self):
        name = session['name']
        return db.session.query(User).filter(User.first_name == name).first()

    #finds a User with a particular Username
    def findUser(self, username):
        return db.session.query(User).filter(User.username == username).first()

    #This logs out a user from the website and clears all session variables
    def logoutUser(self):
        logout_user()
        session.pop('name',None)
        session['ShoppingCart'] = []

class SignUp():
    #accepts a person object and  adds them to the User Table
    def addPerson(self,person):
        try:
            first_name = person.firstname
            last_name = person.lastname
            phone_number = int(''.join(num for num in person.phone_number if num.isdigit()))
            username = person.username
            password = person.password
            email = person.email
            user = User(first_name, last_name, phone_number, username, password,email)
            db.session.add(user)
            db.session.commit()
            return "Welcome to Our Website"
        except IntegrityError:
            return "Username Already Exists"
        

class Person():
    #Creates a person object
    def __init__(self, firstname, lastname,phone_number,username, password, email):
        self.firstname = firstname
        self.lastname = lastname
        self.phone_number = phone_number
        self.username = username
        self.password=password
        self.email = email

