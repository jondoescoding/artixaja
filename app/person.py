from app import db

class Person():

    def __init__(self, firstname, lastname,phone_number,username, password, email):
        self.firstname = firstname
        self.lastname = lastname
        self.phone_number = phone_number
        self.username = username
        self.password=password
        self.email = email

    