"""
This file contains all the flask viewer functions
Apart of the presentation layer
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

#Instance variables created here
manageinventory = ManageInventory()
shopCart = Shoppingcart()
order = Order()
authUser = Autheticate_User()
expenses = ManageExpenses()
manage_fees = ManageFee()

#Route for the home page
@app.route('/')
def home():
    """Render website's home page."""
    # show a different home for the admin vs user
    return render_template('home.html')

#Route for the about page
@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

#route for the login page
#authorizes a user and displays a different UI for Admin vs. Customer
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

#route for the sign up page
#Adds a user with a unique Username
@app.route('/signup', methods=["GET", "POST"])
def signup():
    signup = SignUp()
    form = SignUpForm()
    if request.method=="POST":
        if form.validate_on_submit():
                person = Person(request.form['firstname'], request.form['lastname'], request.form['phoneNumber'],
                request.form['username'], request.form['password'], request.form['email'])
                message = signup.addPerson(person)
                flash(message)
                if message=="Welcome to Our Website":
                    return redirect(url_for('login'))
                return render_template('signup.html',form=form)
    return render_template('signup.html', form=form)

#Updates An item in the inventory
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
            if int(request.form['stocklevel']) > 0:
                if float(request.form['cost']) >0:
                    original = ''
                    if form.photo_update.data is not None:
                        image = form.photo_update.data
                        filename = secure_filename(image.filename)
                        upload_image(image,filename)
                        original = item.image
                    else:
                        filename=item.image
                    message = manageinventory.updateItem(item, filename, request.form['name'],request.form['description'],request.form['cost'],request.form['stocklevel'])
                    if message is True:
                        if original !='':
                            manageinventory.removeImage(original)
                        flash("Item Updated succesfully")
                        return redirect(url_for('display_inventory'))
                    flash(message)
        flash('Ensure Cost and Stocklevel Fields are a Number or Non-Zero Value')
    return render_template("update.html", form=form, item=item, button_name=itemname)

#removes an item from the inventory
@app.route('/remove/<button_name>', methods=["GET", "POST"])
@login_required
def remove(button_name):
    item = manageinventory.getItem(button_name)
    removed = manageinventory.removeItem(item)
    if removed:
        flash ("Item Removed")
        return redirect(url_for('display_inventory'))
    return render_template("inventory.html")

#adds an item to the inventory
@app.route('/add-item', methods=["GET", "POST"])
@login_required
def add_item():
    form=InventoryForm()
    if request.method=='POST':
        if form.validate_on_submit():
            if int(request.form['stocklevel']) > 0:
                if float(request.form['cost']) >0:
                    image = form.photo.data
                    filename = secure_filename(image.filename)
                    name = request.form['name']
                    description = request.form['description']
                    cost=request.form['cost']
                    quantity=request.form['stocklevel']
                    item = Item(filename, name, description, cost, quantity)
                    upload_image(image,filename)
                    message = manageinventory.addItem(item)
                    if message== "Item Successfully Added":
                        flash (message)
                        return(redirect(url_for('add_item')))
                    flash (message)
                    return render_template("additem.html",form=form)
        flash('Ensure Cost and Stocklevel Fields are a Number or Non-Zero Value')
    return render_template("additem.html", form=form)

#helper function to upload an image to the uploads folder
def upload_image(photo,filename):
    photo.save(os.path.join(
        app.config['UPLOAD_FOLDER'], filename
    ))

#displays the inventory items
@app.route('/display-inventory')
@login_required
def display_inventory():
    items= manageinventory.viewInventory()
    return render_template("inventory.html",items=items)

#Gets a specific image from the uploads folder
@app.route('/uploads/<filename>')
@login_required
def get_image(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']), filename)

#logs out a user
@app.route('/logout')
def logout():
    authUser.logoutUser()
    flash('Logged out')
    return redirect(url_for('login'))

#adds a delivery/discount fee to the Fees Table
#Ensures that the fee is unique
@app.route('/add-fees/<feetype>',methods=["GET","POST"])
@login_required
def add_fee(feetype):
    form = DiscountForm()
    l_form = DeliveryFeeForm()
    discounts,delivery = manage_fees.getFees()
    if feetype != 'nav':
        if request.method == "POST":    
            if feetype=='discount':
                if form.validate_on_submit():
                    if float(request.form['amount']) >0:
                        code = request.form['discount']
                        amount = request.form['amount']
                        message = manage_fees.addFee('discount',code,amount,0)
                        flash(message)
                        return redirect(url_for('add_fee',feetype='nav'))
                flash('Amount Field Must be a Number or Non-zero value')
            else:
                if l_form.validate_on_submit():
                        location = request.form['delivery']
                        amount = request.form['amount']
                        deliveryTime = request.form['deliveryTime']
                        message =  manage_fees.addFee('delivery',location,amount,deliveryTime)
                        flash(message)
                        return redirect(url_for('add_fee',feetype='nav'))
                flash(l_form.errors)
                flash('Amount Field Must be a Number or Non-zero value')
    return render_template('add_fee.html',form=form,l_form=l_form, delivery=delivery,discounts=discounts)

#Updates a fee in the Fees Table
#Ensures the Fee is unique
@app.route('/update-fees/<id>',methods=["GET","POST"])
@login_required
def updateFee(id):
    fee=manage_fees.getFee(id)
    form = DiscountForm()
    form.discount.data = fee.name
    form.amount.data = fee.amount
    if request.method == "POST":
        try:
            if float(request.form['amount']) >= 0 or form.validate_on_submit():
                name = request.form['discount']
                amount = request.form['amount']
                if fee.fee_type == 'delivery':
                    feetype= fee.fee_type + ' fee'
                    deliveryTime = request.form['deliveryTime']
                else:
                    if float(request.form['amount'])!=0:
                        deliveryTime = 0
                        feetype= fee.fee_type + ' code'
                    else:
                        flash('Discount cannot be a 0 Value')
                        return render_template('update_fee.html',form=form,fee=fee)
                message = manage_fees.updateFee(id,name,amount,deliveryTime)
                if message == 'Fee Updated':
                    flash('Fee Updated')
                    return redirect(url_for('add_fee',feetype='nav'))
                else:
                    flash('Fee already exists. Ensure ' + feetype + ' does not already exist')
                    # return render_template('update_fee.html',form=form,fee=fee)
        except ValueError:
            flash('Amount Must be a Number')
    return render_template('update_fee.html',form=form,fee=fee)

#Removes a fee from the Fees Table
@app.route('/remove-fees/<id>')
@login_required
def removeFee(id):
    manage_fees.removeFee(id)
    flash('Fee has been removed')
    return redirect(url_for('add_fee',feetype='nav'))

#displays the shopping cart and check out form
@app.route('/shoppingcart', methods=["POST","GET"])
@login_required
def shoppingcart():
    form = CheckoutForm()
    ignore,drop_off = manage_fees.getFees() 
    form2 = UpdateQuant()
    cart,total = shopCart.display_cart()
    session['total'] = total
    return render_template('shoppingcart.html', drop_off=drop_off, cart=cart, total=total, form=form, form2=form2)

#Removes an item from the cart
@app.route('/shoppingcart/remove/<itemid>')
@login_required
def remove_cart(itemid):
    shopCart.remove_from_cart(itemid)
    flash("Item Removed")
    return redirect(url_for('shoppingcart'))

#Updates the quantity of an item in the cart
@app.route('/shoppingcart/update-quantity/<itemid>', methods=["POST","GET"])
@login_required
def update_quant(itemid):
    form2=UpdateQuant()
    if request.method=="POST":
        if form2.validate_on_submit():
            quantity = request.form['update_quantity']
            message = shopCart.update_quantity(itemid, quantity)
            if  message == True:
                flash("Updated")
                return redirect(url_for('shoppingcart'))
            flash(message) #dont change or checkout will break
    return redirect(url_for('shoppingcart'))
    
#Adds an item to the cart
@app.route('/shoppingcart/add/<itemid>', methods=["POST"])
@login_required
def add_to_cart(itemid):
    if request.method=="POST":
        quantity = request.form['quantity']
        shopCart.add_to_cart(itemid, quantity)
        flash('Added to Cart')
        return redirect(url_for('display_catalogue'))

#Displays the items in the inventory on the catalogue page
@app.route('/display-catalogue')
@login_required
def display_catalogue():
    items = manageinventory.viewInventory()
    quantity = 10
    return render_template("catalogue.html", items=items, quantity=quantity)

#Gets the checkout form information and sends it to the business layer
@app.route('/checkout', methods=["POST"])
@login_required
def checkout():
    form=CheckoutForm()
    shoppingcart = session['ShoppingCart']
    if request.method=="POST" and form.validate_on_submit():
        if session['ShoppingCart'] == []: #If shopping cart is empty and person tries to checkout.. display shopping cart is empty
            flash("Shopping Cart is Empty")
            return redirect(url_for('shoppingcart'))
        address = request.form['address']
        parish = request.form['parish']
        drop_off = request.form['drop_off']
        fee,message = shopCart.deliveryInfo(drop_off)
        delivery_instructions = request.form['delivery_instructions']
        payment_methods = request.form['payment_methods']
        discountCode = request.form['discountCode']
        if len(discountCode) != 0: #Is the customer entered a discount code
            discount_given = shopCart.validateDiscountCode(discountCode) #validate the discount code and return the amount
            if discount_given != False:
                gct,discount,total = shopCart.checkout(discount_given) #if the discount is valid, calculate the gct, discount and total
            else:
                flash("Invalid Discount Code")
                return redirect(url_for('shoppingcart'))
        else:
            gct,ignore,total = shopCart.checkout(0)
            discount=0.0
        name = authUser.getUser()
        format_name = [name.first_name, name.last_name]
        subtotal = session['total']
        total += fee
        cart,ignore=shopCart.display_cart() #displays the items in the shopping cart
        trackingNumber = shopCart.trackingNumber() #generates a tracking number
        order.addOrder(address,parish,drop_off,delivery_instructions,payment_methods,gct,subtotal,discount, discountCode,total,fee,trackingNumber,message) #creates an order variable
        checkout_items = [address,parish,drop_off,delivery_instructions,payment_methods,gct,subtotal,discount,total,fee,message,trackingNumber] #creates checkout array for the template
        session['ShoppingCart'] = [] #resets the shoppingcart session
        date= datetime.now()
        return render_template('receipt.html', checkout_items=checkout_items, cart=cart, name=format_name, date=date)
    return redirect(url_for('shoppingcart'))

#Adding an expense to the Expenses Table
@app.route('/expenses/add', methods=["GET","POST"])
@login_required
def addExpense():
    form = ExpensesForm()
    year_start = date(date.today().year, 1, 1)
    today=date.today()
    if request.method == "POST":
        if form.validate_on_submit() and float(request.form['amount']) >0:
            selected_date = request.form['date_range']
            name = request.form['name']
            description = request.form['description']
            category = request.form['category']
            amount = request.form['amount']
            expenses.addExpense(selected_date,name,description,category,amount)
            flash("Expense Added")
            return redirect(url_for('displayExpenses'))
        flash('Ensure Amount field is a Number or Non-Zero')
    return render_template('add_expenses.html',form=form,categories=getCategories(), today=today, year_start=year_start)

#Removing an item from the Expenses Table
@app.route('/expenses-remove/<id>', methods=["GET","POST"])
@login_required
def removeExpense(id):
    expenses.removeExpense(id)
    flash("Expense Removed")
    return redirect(url_for('displayExpenses'))

#Updating an item from the Expenses Table
@app.route('/expenses-update/<id>', methods=["GET","POST"])
@login_required
def updateExpense(id):
    form = ExpensesForm()
    expense = expenses.getExpense(id)
    form.name.data = expense.name
    form.description.data = expense.description
    form.amount.data = expense.amount
    year_start = date(date.today().year, 1, 1)
    today=date.today()
    if request.method == "POST":
        if form.validate_on_submit():
            if float(request.form['amount']) >0:
                selected_date = request.form['date_range']
                name = request.form['name']
                description = request.form['description']
                category = request.form['category']
                amount = request.form['amount']
                expenses.updateExpense(expense,selected_date,name,description,category,amount)
                flash("Expense Updated")
                return redirect(url_for('displayExpenses'))
        flash('Ensure Amount field is a Number or Non-Zero')    
    return render_template('updateExpense.html',expense=expense,form=form,categories=getCategories(), today=today, year_start=year_start) 

#Adds a Category to the ExpensesCategory Table
@app.route('/expenses/add-category', methods=["GET","POST"])
@login_required
def addCategory():
    categories=getCategories()
    if request.method=="POST":
        name = request.form['categ_name']
        message = expenses.addCategory(name)
        if message == "Category has been added":
            flash(message)
            return redirect(url_for('addCategory'))
        else:
            flash (message)
            return render_template('categories.html', categories=categories)
    return render_template('categories.html', categories=categories)

#Removes a Category from the ExpensesCategory Table
@app.route('/expenses-remv-cat/<id>', methods=["GET"])
@login_required
def removeCategory(id):
    expenses.removeCategory(id)
    flash('Category Removed')
    return redirect(url_for('addCategory'))

#Helper Function
#Retrieves all the Categories in the Expenses Category
def getCategories():
    return expenses.displayCategories()

#Displays All the Expenses in the Expenses Table
@app.route('/expenses', methods=["GET"])
@login_required
def displayExpenses():
    all_expenses,total = expenses.displayExpenses()
    return render_template('expenses.html',expenses=all_expenses,total=total)

#Generates a dashbaord
@app.route('/dashboard')
@login_required
def dashboard():
    dashb = Dashboard() 
    e_months,expenses = dashb.calculate_expenses()
    s_months,sales = dashb.calculate_sales()
    labels = ["JAN", "FEB", "MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]

    values = dashb.generate_line_points(e_months)
    values_two = dashb.generate_line_points(s_months)
    current_month = (date.today().strftime("%B")[0:3]).upper()
    
    year = date.today().strftime("%Y")
    sorted_categories = dashb.sort_by_categories()
    cat_values = [row[1] for row in sorted_categories]
    cat_labels = [row[0] for row in sorted_categories]
    deliv_statuses = dashb.calculate_deliveries_stats()
    stat_labels = [row[0] for row in deliv_statuses]
    stat_values = [row[1] for row in deliv_statuses]

    color = dashb.generate_random_colour(cat_values)
    
    prof_loss = dashb.profit_or_loss()
    sales_performance = dashb.monthly_performance(s_months)
    items = dashb.item_performance()
    return render_template('dashboard.html',current_month=current_month, sales=sales,expenses=expenses, year=year,items=items,labels=labels,values=values,values_two=values_two, cat_values = cat_values, cat_labels=cat_labels,color=color,sales_performance=sales_performance,prof_loss=prof_loss,stat_labels=stat_labels,stat_values=stat_values)

#Displays all the orders in the orders table
@app.route('/orders', methods=["POST","GET"])
@login_required
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

#Gets a single order from the orders table
@app.route('/orders/<orderid>', methods=["POST", "GET"])
@login_required
def get_order(orderid):
    one_order = order.getOrder(orderid)
    user = authUser.findUser(one_order.username)
    cart = shopCart.display_user_cart(one_order.cart)
    return render_template('single_order.html', order=one_order, cart=cart, user=user, orderStatus=OrderStatus,paymentStatus=PaymentStatus)

#Updating Order Status
@app.route('/order/update_status/<id>', methods=["POST"])
@login_required
def update_status(id):
    order_status = request.form.get('order_stat')
    payment_status = request.form.get('payment_stat')
    order.changeOrderStatus(id, order_status)
    order.changePaymentStatus(id, payment_status)
    flash('Updated')
    return redirect(url_for('get_order',orderid=id))

#Order Tracking
@app.route('/order/track-order',methods=["POST","GET"])
@login_required
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
