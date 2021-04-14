from app.Database.models import Expenses, Orders, Inventory
from app import db
from datetime import date
from app.Business.shoppingcart import Shoppingcart
from app.Business.order_status import OrderStatus
import random


class Dashboard:
    '''Generates the Tables and Graphs for the Expenses, Sales and Performance'''

    #Calculates the Expenses for a specific year
    def calculate_expenses(self):
        total = 0
        current = date.today().year
        expenses = db.session.query(Expenses).all()
        sort_month = self.sort_by_month('expenses',expenses, current)
        for i in expenses:
            total+= i.amount
        return sort_month,total

    #Calculates the Sales for a given year
    def calculate_sales(self):
        total = 0
        sales = db.session.query(Orders).all()
        current = date.today().year
        sort = self.sort_by_month('sales',sales,current)
        for i in sales:
            total+= i.total
        return sort,total

    #Sorts the sales or expenses by month and calculates the amount per month
    def sort_by_month(self, query_type, query, current):
        months = {}
        for i in query:
            if query_type == 'expenses':
                if i.date.year == current:  
                    month = (i.date.strftime("%B")[0:3]).upper()
                    if months.get(month) is not None:
                        months[month] = months.get(month) + i.amount
                    else:
                        months[month] = i.amount
            else:
                if i.currentTime.year == current:
                    month = (i.currentTime.strftime("%B")[0:3]).upper()
                    if months.get(month) is not None:
                        months[month] = months.get(month) + i.total
                    else:
                        months[month] = i.total
        return list(months.items())

    #Determines the top three least performing Months for the year (based on sales)
    def monthly_performance(self, sales_month):
        sales_month.sort(key= lambda x: x[1])
        if len(sales_month) <=3:
            best_performing = sales_month
            worst_performing = sales_month
        else:
            best_performing = sales_month[-3:]
            worst_performing = sales_month[:3]
        return [best_performing,worst_performing]

    #Determines the profit or loss for each month based on sales/expenses
    def profit_or_loss(self):
        sales,ignore = self.calculate_sales()
        expenses,ignore = self.calculate_expenses()
        s_points = self.generate_line_points(sales)
        e_points = self.generate_line_points(expenses)

        return [abs(s_points[i]-e_points[i]) for i in range(len(s_points))]
            
        
    #Generates the points for the line graph
    def generate_line_points(self,plot_list):
        values = []
        months = ["JAN", "FEB", "MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
        current_month = (date.today().strftime("%B")[0:3]).upper()
        labels = months[:months.index(current_month)+1]
        for i in labels:
            try:
                val = [y[0] for y in plot_list].index(i)
                value = plot_list[val][1]
            except:
                value=0
            values.append(value)
        return values

    #Calculates the total sales of each item in the inventory
    def calculate_item_performance(self,inventory,order):
        shoppingcart = Shoppingcart()
        invent_items = {}
        for i in inventory:
            invent_items[i.name] = 0
        for x in order:
            for y in x.cart:
                item = shoppingcart.get_item(y[0])
                if item:
                    invent_items[item.name] =invent_items.get(item.name) + int(y[1])
        return list(invent_items.items())

    #Determines the top 3 least and best performing items sold by the company
    def item_performance(self):
        inventory = db.session.query(Inventory).all()
        orders = db.session.query(Orders).all()
        items = self.calculate_item_performance(inventory,orders)
        items.sort(key=lambda x:x[1])
        if len(items) <= 3:
            best_performing = items
            worst_performing = items
        else:
            best_performing = items[-3:]
            worst_performing = items[:3]
        return best_performing,worst_performing

    #sorts the expenses by categories and calculates the amount spent per category 
    def sort_by_categories(self):
        expenses = db.session.query(Expenses).all()
        categories = {}
        for expense in expenses:
            if categories.get(expense.category) is not None:
                categories[expense.category] = categories.get(expense.category) + expense.amount
            else:
                categories[expense.category] = expense.amount
        return list(categories.items())

    #calculates the number of orders per delivery status for a given month in a year
    def calculate_deliveries_stats(self):
        c_year = date.today().year
        c_month = date.today().month
        orders = db.session.query(Orders).all()
        statuses = {OrderStatus.ORDER_PLACED.value:0,OrderStatus.PROCESSING.value:0,OrderStatus.PACKAGED.value:0,OrderStatus.DELIVERED.value: 0,OrderStatus.CLOSED.value:0,OrderStatus.CANCELLED.value:0}    
        for order in orders:
            if order.currentTime.year == c_year:
                if order.currentTime.month == c_month:
                    orderStatus = order.order_status 
                    statuses[orderStatus] = statuses.get(orderStatus) + 1
        return list(statuses.items())

    #Generates random colours for the pie chart
    def generate_random_colour(self,cat_values):
        color = []
        for x in range(len(cat_values)):
            r = lambda: random.randint(0,255)
            rgb = ('#%02X%02X%02X' % (r(),r(),r()))
            if rgb in color:
                r = lambda: random.randint(0,255)
                rgb = ('#%02X%02X%02X' % (r(),r(),r()))
            color.append(rgb)
        return color