from app import app, db, login_manager
from flask import render_template, redirect, url_for, flash,session
from flask_login import login_user
from app.models import User
from app.person import Person
from app.shoppingcart import Shoppingcart
from werkzeug.security import check_password_hash 

class Autheticate_User():

    def AuthUser(self, username, password,form):
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
    
    def getUser(self):
        name = session['name']
        return db.session.query(User).filter(User.first_name == name).first()

    def findUser(self, username):
        return db.session.query(User).filter(User.username == username).first()

    