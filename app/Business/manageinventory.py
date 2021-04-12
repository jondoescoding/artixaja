from app import db,app
import os
from app.Database.models import Inventory, Fees
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

class ManageInventory():

    #Displays All items in the inventory
    def viewInventory(self):
        return db.session.query(Inventory).all()

    #Adds an item object to the Inventory Class
    def addItem(self, item):
        items = Inventory(item.image, item.name,item.description,item.cost,item.stocklevel)
        db.session.add(items)
        db.session.commit()
        return True

    #Removes an Item object from the items class
    #The image associated with the item is removed from the uploads folder
    def removeItem(self, item):
        image = item.image
        self.removeImage(image)
        db.session.delete(item)
        db.session.commit()
        return True

    #An item is updated and the changes made by the user is reflected in the database
    def updateItem(self, item, filename, name, description, cost, stocklevel):
        item.image = filename
        item.name=name
        item.description = description
        item.cost=cost
        item.stocklevel=stocklevel
        db.session.commit()
        return item

    #This is a helper function that removes an image from the uploads folder
    def removeImage(self,image):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'],image))

    def getItem(self,name):
        return db.session.query(Inventory).filter(Inventory.name == name).first()

class ManageFee:
    #This function adds a fee of a specific type along with its relevant information
    #The fee type can either be dicount our delivery
    def addFee(self,fee_type,name,amount):
        try:
            fee = Fees(fee_type,name,amount)
            db.session.add(fee)
            db.session.commit()
            return "Added Succesfully"
        except IntegrityError:
            return "Aredy Deh deh"

    #This function returns all delivery and discount fees present in the Fees Table
    def getFees(self):
        fees = db.session.query(Fees).all()
        delivery = []
        discount=[]
        for x in fees:
            if x.fee_type == 'discount':
                discount.append(x)
            else:
                delivery.append(x)
        return discount,delivery

    def getFee(self,id):
        return db.session.query(Fees).filter(Fees.id == id).first()


    def removeFee(self,id):
        fee = self.getFee(id)
        db.session.delete(fee)
        db.session.commit()

    def updateFee(self,id,name,amount):
        fee = self.getFee(id)
        fee.name = name
        fee.amount = amount
        db.session.commit()
        
