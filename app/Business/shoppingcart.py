from flask import session, redirect, url_for, flash
from app import app,db
from app.Database.models import Inventory,User
from app.Business.manageinventory import ManageInventory, ManageFee
from random import randint
fees = ManageFee()

class Shoppingcart():

    #Adds an item to the shooping cart
    def add_to_cart(self, id, quantity):
        #Checks to see if the shopping cart session variable exists
        if 'ShoppingCart' not in session: 
            session['ShoppingCart'] = []
        else:
            notFound= True
            #Checks if the item to be added is already in the cart
            for i in session['ShoppingCart']: 
                if i[0] == id:
                    #Quantity of item is updated to the quantity chosen
                    self.update_quantity(id,quantity) 
                    notFound= False
                    break
            if notFound == True: 
                #The item is not found in the cart and is therefore added to the cart
                cart_item = [id, quantity]
                session['ShoppingCart'].append(cart_item)

    #Updates the quantity of an item to the value input by user
    def update_quantity(self,id, quantity):
        try:
            if self.checkQuantity(id,quantity):
                for i in session['ShoppingCart']:
                    if i[0] == id:
                        i[1] = quantity
                        return True
            #Quantity chosen is greater than the quantity of items in the inventory
            return "Quantity Selected is too large"
        #A non-zero value was entered for the quantity
        except ValueError:
            return "Quantity Must be an Integer"
    
    #Checks the stock level of the item against the quantity entered by user
    def checkQuantity(self,id, selected_quant):
        if int(self.get_item(id).stocklevel) < int(selected_quant):
            return False """Quantity chosen exceeds stock level"""
        return True """Quantity chosen is sufficient"""

    #Displays the items in the shopping cart and returns the items, quanity, cost per unit price and subtotal
    def display_cart(self):
        if 'ShoppingCart' not in session:
            return False
        else:
            total=0
            cart =[]
            for i in session['ShoppingCart']:
                item = self.get_item(i[0])
                subtotal = int(item.cost) * int(i[1])
                total += subtotal
                cart_item = [item, i[1], subtotal]
                cart.append(cart_item)
            return cart,total

    #Displays the user order on the Administration Side
    #Related to View Order Use Case
    def display_user_cart(self, cart):
        user_cart = []
        for i in cart:
            if self.get_item(i[0]) is not None:
                item = self.get_item(i[0]).name
                cart_item = [item, i[1]]
            else:
                item = "Item Removed"
                cart_item=[item,'Not Available']
            user_cart.append(cart_item)
        return user_cart

    #Gets an item object from the inventory table in the artixa database
    def get_item(self,id):
        return db.session.query(Inventory).filter(Inventory.id == id).first()

    #removes an item from the shoppingcart session variable
    def remove_from_cart(self,id):
        for i,v in enumerate(session['ShoppingCart']):
            if v[0] == id:
                session['ShoppingCart'].pop(i)

    #Calculates the GCT, discount Price and Total
    def checkout(self, discount):
        disc_price = discount * int(session['total'])
        gct = 0.15 * int(session['total'])
        total = (int(session['total']) + gct) - disc_price
        self.updateStocklevel()
        return gct, disc_price, total

    #Updates the Stock level in the inventory once an order goes through
    def updateStocklevel(self):
        for x in session['ShoppingCart']:
            item = self.get_item(x[0])
            item.stocklevel -= int(x[1])
            db.session.commit()

    #Validates the Discount code to see if it is among the list of discount codes offered
    def validateDiscountCode(self,discountCode):
        discCodes,ignore = fees.getFees()
        for x in discCodes:
            if discountCode == x.name:
                return x.amount
        return False

    #Gets the DeliveryTime and Fee Amount based on the Delivery Location
    def deliveryInfo(self,drop_off):
        fee = fees.get_fee_by_name(drop_off)
        return fee.amount, fee.deliveryTime

    #Generates a random 8 digit tracking Number for the user to track their order
    def trackingNumber(self):
        n=8
        range_start = 10**(n-1)
        range_end = (10**n)-1
        ranNum = randint(range_start, range_end)
        return ranNum