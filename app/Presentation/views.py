"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, login_manager
from app.Database.models import User
from flask import render_template, request, redirect, url_for, flash,session, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app.Presentation.forms import LoginForm, InventoryForm, UpdateForm,SignUpForm, CheckoutForm, UpdateQuant, ExpensesForm,DiscountForm,DeliveryFeeForm
from app.Business.ManageUser import Autheticate_User,SignUp,Person
from app.Business.manageinventory import ManageInventory, ManageFee
from app.Business.shoppingcart import Shoppingcart
from app.Business.order_status import PaymentStatus, OrderStatus 
from app.Business.orders import Order
from app.Business.item import Item
from app.Business.dashboard import Dashboard
from app.Business.shoppingcart import Shoppingcart
from app.Business.expenses import ManageExpenses
from werkzeug.security import check_password_hash 
from werkzeug.utils import secure_filename
from datetime import date,datetime


manageinventory = ManageInventory()
shopCart = Shoppingcart()
order = Order()
authUser = Autheticate_User()
expenses = ManageExpenses()
manage_fees = ManageFee()


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
            authorized = authUser.AuthUser(username, password)
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
            flash('Welcome to our website')
            return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/update/<button_name>', methods=["GET", "POST"])
@login_required
def update(button_name):
    form=UpdateForm()
    itemname = button_name
    item = manageinventory.getItem(itemname)
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
    item = manageinventory.getItem(button_name)
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


#remove db.
@app.route('/display-inventory')
@login_required
def display_inventory():
    items= manageinventory.viewInventory()
    return render_template("inventory.html",items=items)


@app.route('/uploads/<filename>')
def get_image(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']), filename)

@app.route('/logout')
def logout():
    authUser.logoutUser()
    flash('Logged out')
    return redirect(url_for('login'))


@app.route('/add-fees/<feetype>',methods=["GET","POST"])
def add_fee(feetype):
    form = DiscountForm()
    l_form = DeliveryFeeForm()
    discounts,delivery = manage_fees.getFees()
    if feetype != 'nav':
        if request.method == "POST":    
            if feetype=='discount':
                if form.validate_on_submit():
                    code = request.form['discount']
                    amount = request.form['amount']
                    message = manage_fees.addFee('discount',code,amount)
                    flash(message)
                    return redirect(url_for('add_fee',feetype='nav'))
                flash(form.errors)
            else:
                if l_form.validate_on_submit():
                    location = request.form['delivery']
                    amount = request.form['amount']
                    message =  manage_fees.addFee('delivery',location,amount)
                    flash(message)
                    return redirect(url_for('add_fee',feetype='nav'))
                flash(form.errors)
    return render_template('add_fee.html',form=form,l_form=l_form, delivery=delivery,discounts=discounts)

@app.route('/update-fees/<id>',methods=["GET","POST"])
def updateFee(id):
    fee=manage_fees.getFee(id)
    form = DiscountForm()
    form.discount.data = fee.name
    form.amount.data = fee.amount
    if form.validate_on_submit() and request.method == "POST":
        name = request.form['discount']
        amount = request.form['amount']
        manage_fees.updateFee(id,name,amount)
        flash('Fee Updated')
        return redirect(url_for('add_fee',feetype='nav'))
    return render_template('update_fee.html',form=form,fee=fee)

@app.route('/remove-fees/<id>')
def removeFee(id):
    manage_fees.removeFee(id)
    flash('Fee has been removed')
    return redirect(url_for('add_fee',feetype='nav'))

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
    items = manageinventory.viewInventory()
    quantity = 10
    return render_template("catalogue.html", items=items, quantity=quantity)


#fix up this function
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
        order.addOrder(address,parish,drop_off,delivery_instructions,payment_methods,gct,subtotal,discount, discountCode,total,fee,trackingNumber,message)
        checkout_items = [address,parish,drop_off,delivery_instructions,payment_methods,gct,subtotal,discount,total,fee,message,trackingNumber]
        session['ShoppingCart'] = []
        date= datetime.now()
        return render_template('checkout.html', checkout_items=checkout_items, cart=cart, name=name, date=date)
    return redirect(url_for('shoppingcart'))


@app.route('/expenses/add', methods=["GET","POST"])
def addExpense():
    form = ExpensesForm()
    year_start = date(date.today().year, 1, 1)
    today=date.today()
    if request.method == "POST" and form.validate_on_submit():
        selected_date = request.form['date_range']
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        amount = request.form['amount']
        expenses.addExpense(selected_date,name,description,category,amount)
        flash("Expense Added")
        return redirect(url_for('displayExpenses'))
    return render_template('add_expenses.html',form=form,categories=getCategories(), today=today, year_start=year_start)

@app.route('/expenses/remove/<id>', methods=["GET","POST"])
def removeExpense(id):
    expenses.removeExpense(id)
    flash("Expense Removed")
    return redirect(url_for('displayExpenses'))

@app.route('/expenses/update/<id>', methods=["GET","POST"])
def updateExpense(id):
    form = ExpensesForm()
    expense = expenses.getExpense(id)
    form.name.data = expense.name
    form.description.data = expense.description
    form.amount.data = expense.amount
    year_start = date(date.today().year, 1, 1)
    today=date.today()
    if request.method == "POST" and form.validate_on_submit():
        selected_date = request.form['date_range']
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        amount = request.form['amount']
        expenses.updateExpense(expense,selected_date,name,description,category,amount)
        flash("Expense Updated")
        return redirect(url_for('displayExpenses'))    
    return render_template('updateExpense.html',expense=expense,form=form,categories=getCategories(), today=today, year_start=year_start) 

@app.route('/expenses/add-category', methods=["GET","POST"])
def addCategory():
    categories=getCategories()
    if request.method=="POST":
        name = request.form['categ_name']
        expenses.addCategory(name)
        flash("Category has been added")
        return redirect(url_for('addCategory'))
    return render_template('categories.html', categories=categories)

@app.route('/expenses/remove-category/<id>', methods=["GET"])
def removeCategory(id):
    expenses.removeCategory(id)
    flash('Category Removed')
    return redirect(url_for('addCategory'))

def getCategories():
    return expenses.displayCategories()

@app.route('/expenses', methods=["GET"])
def displayExpenses():
    all_expenses,total = expenses.displayExpenses()
    return render_template('expenses.html',expenses=all_expenses,total=total)

#Sort out this function
@app.route('/dashboard')
def dashboard():
    dashb = Dashboard()
    months = ["JAN", "FEB", "MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
    
    e_months,expenses = dashb.calculate_expenses()
    s_months,sales = dashb.calculate_sales()

    values = dashb.generate_line_points(e_months)
    values_two = dashb.generate_line_points(s_months)
    current_month = (date.today().strftime("%B")[0:3]).upper()
    labels = months[:months.index(current_month)+1]
    
    something = dashb.sort_by_categories()
    cat_values = [row[1] for row in something]
    cat_labels = [row[0] for row in something]
    deliv = dashb.calculate_deliveries()
    stat_labels = [row[0] for row in deliv]
    stat_values = [row[1] for row in deliv]

    color = dashb.generate_random_colour(cat_values)
    
    prof_loss = dashb.profit_or_loss()
    sales_performance = dashb.monthly_performance(s_months)
    items = dashb.item_performance()
    return render_template('dashboard.html', sales=sales,expenses=expenses, items=items,labels=labels,values=values,values_two=values_two, cat_values = cat_values, cat_labels=cat_labels,color=color,sales_performance=sales_performance,prof_loss=prof_loss,stat_labels=stat_labels,stat_values=stat_values)

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
        orderStatus,predicted_delivery_date = order.trackOrder(trackingNumber)
        return render_template('track_order.html', orderStatus=orderStatus, status=OrderStatus, predicted_delivery_date=predicted_delivery_date)
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
