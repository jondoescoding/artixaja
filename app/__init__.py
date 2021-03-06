from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .config import Config

"""This is where the Flask app is initialized"""

app = Flask(__name__,template_folder='Presentation/templates',static_folder="Presentation/static")

db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(Config)

from app.Presentation import views
