"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash,session, abort, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, InventoryForm, UpdateForm,SignUpForm, CheckoutForm, UpdateQuant
from app.models import User, Inventory
from app.authenticate_user import Autheticate_User
from .manageinventory import ManageInventory
from .shoppingcart import Shoppingcart
from .order_status import PaymentStatus, OrderStatus
from app.signup import SignUp
from app.person import Person
from app.orders import Order
from app.catalogue import DisplayCatalogue
from app.item import Item
from app.shoppingcart import Shoppingcart
from werkzeug.security import check_password_hash 
from werkzeug.utils import secure_filename
from app.orders import Order

manageinventory = ManageInventory()
shopCart = Shoppingcart()
order = Order()
authUser = Autheticate_User()


@app.route('/')
def home():
    """Render website's home page."""
    # show a different home for the admin vs user
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = request.form['username']
            password = request.form['password']
            authorized = authUser.AuthUser(username, password,form)
            if authorized:
                session['ShoppingCart'] = []
                return redirect(url_for('home'))
            flash("Incorrect Credentials")
            return render_template("login.html", form=form)
    return render_template("login.html", form=form)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    signup = SignUp()
    form = SignUpForm()
    if request.method=="POST" and form.validate_on_submit():
            person = Person(request.form['firstname'], request.form['lastname'], request.form['phoneNumber'],
            request.form['username'], request.form['password'], request.form['email'])
            user = signup.addPerson(person)
            login_user(user)
            flash('Welcome to our website')
            return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/update/<button_name>', methods=["GET", "POST"])
@login_required
def update(button_name):
    form=UpdateForm()
    itemname = button_name
    item = db.session.query(Inventory).filter(Inventory.name == itemname).first()
    form.name.data=item.name
    form.description.data=item.description
    form.cost.data=item.cost
    form.stocklevel.data=item.stocklevel
    if request.method=="POST":
        if form.stocklevel.data == 0:
            form.stocklevel.data=1
        if form.validate_on_submit():
            if form.photo_update.data is not None:
                image = form.photo_update.data
                filename = secure_filename(image.filename)
                upload_image(image,filename)
                original = item.image
                manageinventory.removeImage(original)
            else:
                filename=item.image
            item = manageinventory.updateItem(item, filename, request.form['name'],request.form['description'],request.form['cost'],request.form['stocklevel'])
            if item is not None:
                flash("Item Updated succesfully")
                return redirect(url_for('display_inventory'))
    return render_template("update.html", form=form, item=item, button_name=itemname)

@app.route('/remove/<button_name>', methods=["GET", "POST"])
def remove(button_name):
    item = db.session.query(Inventory).filter(Inventory.name == button_name).first()
    removed = manageinventory.removeItem(item)
    if removed:
        flash ("Item Removed")
        return redirect(url_for('display_inventory'))
    return render_template("inventory.html")

@app.route('/add-item', methods=["GET", "POST"])
@login_required
def add_item():
    form=InventoryForm()
    if form.validate_on_submit() and request.method=='POST':
        image = form.photo.data
        filename = secure_filename(image.filename)
        name = request.form['name']
        description = request.form['description']
        cost=request.form['cost']
        quantity=request.form['stocklevel']
        item = Item(filename, name, description, cost, quantity)
        upload_image(image,filename)
        added = manageinventory.addItem(item)
        if added:
            flash('Item Added')
        else:
            flash('Nope')
        return(redirect(url_for('add_item')))
    return render_template("additem.html", form=form)

def upload_image(photo,filename):
    photo.save(os.path.join(
        app.config['UPLOAD_FOLDER'], filename
    ))

@app.route('/display-inventory')
@login_required
def display_inventory():
    items= db.session.query(Inventory).all()
    return render_template("inventory.html",items=items)


@app.route('/uploads/<filename>')
def get_image(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']), filename)

@app.route('/logout')
def logout():
    logout_user()
    session.pop('name',None)
    session['ShoppingCart'] = []
    flash('Logged out')
    return redirect(url_for('login'))

@app.route('/shoppingcart', methods=["POST","GET"])
def shoppingcart():
    form = CheckoutForm()
    form2 = UpdateQuant()
    cart,total = shopCart.display_cart()
    session['total'] = total
    return render_template('shoppingcart.html', cart=cart, total=total, form=form, form2=form2)

@app.route('/shoppingcart/remove/<itemid>')
def remove_cart(itemid):
    shopCart.remove_from_cart(itemid)
    flash("Item Removed")
    return redirect(url_for('shoppingcart'))

@app.route('/shoppingcart/update-quantity/<itemid>', methods=["POST","GET"])
def update_quant(itemid):
    form2=UpdateQuant()
    if request.method=="POST":
        if form2.validate_on_submit():
            quantity = request.form['update_quantity']
            shopCart.update_quantity(itemid, quantity)
    flash("Updated") #dont change or checkout will break
    return redirect(url_for('shoppingcart'))
    

@app.route('/shoppingcart/add/<itemid>', methods=["POST"])
def add_to_cart(itemid):
    if request.method=="POST":
        quantity = request.form['quantity']
        shopCart.add_to_cart(itemid, quantity)
        flash('Added to Cart')
        return redirect(url_for('display_catalogue'))

@app.route('/display-catalogue')
def display_catalogue():
    catalogue = DisplayCatalogue()
    items = catalogue.display_items()
    quantity = 10
    return render_template("catalogue.html", items=items, quantity=quantity)

@app.route('/checkout', methods=["POST"])
def checkout():
    form=CheckoutForm()
    shoppingcart = session['ShoppingCart']
    if request.method=="POST" and form.validate_on_submit():
        if session['ShoppingCart'] == []:
            flash("Shopping Cart is Empty")
            return redirect(url_for('shoppingcart'))
        address = request.form['address']
        parish = request.form['parish']
        drop_off = request.form['drop_off']
        fee,message = shopCart.deliveryInfo(drop_off)
        delivery_instructions = request.form['delivery_instructions']
        payment_methods = request.form['payment_methods']
        discountCode = request.form['discountCode']
        if len(discountCode) != 0:
            valid = shopCart.validateDiscountCode(discountCode)
            if valid != False:
                gct,discount,total = shopCart.checkout(valid)
            else:
                flash("Invalid Discount Code")
                return redirect(url_for('shoppingcart'))
        else:
            gct,ignore,total = shopCart.checkout(0)
            discount=0.0
        name = shopCart.getName()
        subtotal = session['total']
        total += fee
        cart,ignore=shopCart.display_cart()
        trackingNumber = shopCart.trackingNumber()
        order.addOrder(address,parish,drop_off,delivery_instructions,payment_methods,gct,subtotal,discount, discountCode,total,fee,trackingNumber)
        checkout_items = [address,parish,drop_off,delivery_instructions,payment_methods,gct,subtotal,discount,total,fee,message,trackingNumber]
        session['ShoppingCart'] = []
        return render_template('checkout.html', checkout_items=checkout_items, cart=cart, name=name)
    return redirect(url_for('shoppingcart'))


@app.route('/dashboard')
def dashboard():
    pass

@app.route('/orders', methods=["POST","GET"])
def orders():
    if request.method == "POST":
        orderStatus = request.form.get('order_stat')
        if orderStatus == 'NoFilter':
            orders = order.getOrders()
        else:
            orders = order.filterByStatus(orderStatus)
        return render_template('orders.html', orders=orders, orderStatus=OrderStatus, selectedStatus=orderStatus)
    orders=order.getOrders()
    return render_template('orders.html', orders=orders, orderStatus=OrderStatus, selectedStatus="NoFilter")

@app.route('/orders/<orderid>', methods=["POST", "GET"])
def get_order(orderid):
    one_order = order.getOrder(orderid)
    user = authUser.findUser(one_order.username)
    cart = shopCart.display_user_cart(one_order.cart)
    return render_template('single_order.html', order=one_order, cart=cart, user=user, orderStatus=OrderStatus,paymentStatus=PaymentStatus)

@app.route('/order/update_status/<id>', methods=["POST"])
def update_status(id):
    order_status = request.form.get('order_stat')
    payment_status = request.form.get('payment_stat')
    order.changeOrderStatus(id, order_status)
    order.changePaymentStatus(id, payment_status)
    return redirect(url_for('get_order',orderid=id))

@app.route('/order/track-order',methods=["POST","GET"])
def track_order():
    if request.method=="POST":
        trackingNumber = request.form.get('trackingNumber')
        orderStatus = order.trackOrder(trackingNumber)
        return render_template('track_order.html', orderStatus=orderStatus, status=OrderStatus)
    return render_template('track_order.html',orderStatus='')


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
