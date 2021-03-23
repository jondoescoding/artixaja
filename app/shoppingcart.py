from flask import session, redirect, url_for, flash
from app import app,db
from .item import Item
from app.models import Inventory,User
from random import randint

class Shoppingcart():
    
    def add_to_cart(self, id, quantity):
        if 'ShoppingCart' not in session:
            session['ShoppingCart'] = []
        else:
            notFound= True
            for i in session['ShoppingCart']:
                if i[0] == id:
                    self.update_quantity(id,quantity)
                    notFound= False
                    break
            if notFound == True:
                cart_item = [id, quantity]
                session['ShoppingCart'].append(cart_item)

    def update_quantity(self,id, quantity):
        for i in session['ShoppingCart']:
            if i[0] == id:
                i[1] = quantity

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

    def display_user_cart(self, cart):
        user_cart = []
        for i in cart:
            item = self.get_item(i[0]).name
            cart_item = [item, i[1]]
            user_cart.append(cart_item)
        return user_cart


    def get_item(self,id):
        return db.session.query(Inventory).filter(Inventory.id == id).first()

    def remove_from_cart(self,id):
        for i,v in enumerate(session['ShoppingCart']):
            if v[0] == id:
                session['ShoppingCart'].pop(i)

    def checkout(self, discount):
        disc_price = discount * int(session['total'])
        gct = 0.15 * int(session['total'])
        total = (int(session['total']) + gct) - disc_price
        self.updateStocklevel()
        return gct, disc_price, total

    def updateStocklevel(self):
        for x in session['ShoppingCart']:
            item = self.get_item(x[0])
            item.stocklevel -= int(x[1])
            db.session.commit()

    def validateDiscountCode(self,discountCode):
        discCodes = [["DB7ECQT",0.25], ["E1T4DAH",0.5],["RDWGJ1W",0.1]]
        for x in discCodes:
            if discountCode == x[0]:
                return x[1]
        return False

    def getName(self):
        f_name = session['name']
        name = db.session.query(User).filter(User.first_name == f_name).first()
        return [name.first_name, name.last_name]


    def deliveryInfo(self,drop_off):
        delivery_fee = [['Half Way Tree',400],['UWI/UTech',0],['Portmore',200],['Spanish Town', 300],['Hanover',1200],['Saint Elizabeth',800],['Saint James',900],['Trelawny',800],['Westmoreland',1500],['Clarendon', 600],['Manchester',800],['Saint Ann',900],['Saint Mary',2000],['Portland',1800],['Saint Thomas', 1300]]

        message=[['Half Way Tree',1],['UWI/UTech',1],['Portmore',1],['Spanish Town',1],['Hanover',2],['Saint Elizabeth',2],['Saint James',2],['Trelawny',2],['Westmoreland',2],['Clarendon', 1],['Manchester',2],['Saint Ann',2],['Saint Mary',2],['Portland',2],['Saint Thomas', 2]]

        fee = [x[1] for x in delivery_fee if drop_off == x[0]]
        deliv_message = [x[1] for x in message if drop_off == x[0]]
        return fee[0], deliv_message[0]

    def trackingNumber(self):
        n=8
        range_start = 10**(n-1)
        range_end = (10**n)-1
        ranNum = randint(range_start, range_end)
        return ranNum