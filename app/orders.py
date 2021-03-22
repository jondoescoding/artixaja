from app import app,db
from flask import session
from app.authenticate_user import Autheticate_User
from app.models import Orders, User
from app.person import Person
from app.order_status import OrderStatus

class Order():

    def addOrder(self,address,parish,location,instructions,payment_method,gct,subtotal,discount, discountCode,total,delivery_fee,trackingNumber):
        cart = session['ShoppingCart']
        authUser = Autheticate_User()
        username = authUser.getUser().username
        order = Orders(trackingNumber,username,address,parish,location,gct,subtotal,discount, discountCode,total,delivery_fee,cart, instructions,payment_method) 
        db.session.add(order)
        db.session.commit()

    def getOrders(self):
        return db.session.query(Orders).all()

    def getOrder(self, id):
        return db.session.query(Orders).filter(Orders.orderNumber == id).first()

    def changeOrderStatus(self,id, status):
        item = self.getOrder(id)
        item.order_status = status
        db.session.commit()

    def changePaymentStatus(self, id, status):
        item = self.getOrder(id)
        item.payment_status = status
        db.session.commit()

    def trackOrder(self, trackingNumber):
        order= db.session.query(Orders).filter(Orders.trackingNumber == trackingNumber).first()
        if order:
            return order.order_status
        return False

    def filterByStatus(self,orderStatus):
        orders = db.session.query(Orders).filter(Orders.order_status == orderStatus).all()
        if orders:
            return orders
        else:
            return False
    