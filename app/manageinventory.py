from app import db,app
import os
from app.models import Inventory

class ManageInventory():

    def viewInventory(self, Inventory):
        return db.session.query(Inventory).all()

    def addItem(self, item):
        items = Inventory(item.image, item.name,item.description,item.cost,item.stocklevel)
        db.session.add(items)
        db.session.commit()
        return True

    def removeItem(self, item):
        image = item.image
        self.removeImage(image)
        db.session.delete(item)
        db.session.commit()
        return True

    def updateItem(self, item, filename, name, description, cost, stocklevel):
        item.image = filename
        item.name=name
        item.description = description
        item.cost=cost
        item.stocklevel=stocklevel
        db.session.commit()
        return item

    def removeImage(self,image):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'],image))