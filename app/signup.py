from .person import Person
from app.models import User
from app import db,app

class SignUp():

    def addPerson(self,person):
        first_name = person.firstname
        last_name = person.lastname
        phone_number = int(''.join(num for num in person.phone_number if num.isdigit()))
        username = person.username
        password = person.password
        email = person.email
        user = User(first_name, last_name, phone_number, username, password,email)
        db.session.add(user)
        db.session.commit()
        return user

