from app import db
from app.models import Inventory

class DisplayCatalogue():

    def display_items(self):
        return db.session.query(Inventory).all()