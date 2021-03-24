from app import app,db
from flask import session
from app.authenticate_user import Autheticate_User
from app.models import Orders, User
from app.person import Person
from app.order_status import OrderStatus
from datetime import datetime, timedelta 
from sqlalchemy import asc

class Order():

    def addOrder(self,address,parish,location,instructions,payment_method,gct,subtotal,discount, discountCode,total,delivery_fee,trackingNumber, message):
        cart = session['ShoppingCart']
        authUser = Autheticate_User()
        username = authUser.getUser().username
        predicted_delivery_date = self.predict_delivery_date(message)
        order = Orders(predicted_delivery_date,trackingNumber,username,address,parish,location,gct,subtotal,discount, discountCode,total,delivery_fee,cart, instructions,payment_method) 
        db.session.add(order)
        db.session.commit()

    def getOrders(self):
        return db.session.query(Orders).order_by(asc(Orders.orderNumber))

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
            if order.order_status == OrderStatus.ORDER_PLACED.value or order.order_status == OrderStatus.PROCESSING.value or order.order_status==OrderStatus. PACKAGED.value:
                predicted_delivery_date = order.predicted_delivery_date
            else:
                predicted_delivery_date = False
            return order.order_status, predicted_delivery_date 
        return False, False

    def predict_delivery_date(self,message):
        if message == 1:
            date = datetime.now()+timedelta(days=3)
        else:
            date= datetime.now()+timedelta(days=5)
        return date

    def filterByStatus(self,orderStatus):
        orders = db.session.query(Orders).filter(Orders.order_status == orderStatus).order_by(asc(Orders.orderNumber))
        if orders:
            return orders
        else:
            return False
    