from app import db,app
from app.Database.models import Expenses, ExpenseCategories

class ManageExpenses():
    
    #Adds an expense to the Expenses table
    def addExpense(self, date, name, description, category, amount):
        expense = Expenses(date, name, category, description, amount)
        db.session.add(expense)
        db.session.commit()

    #Removes an Expense with a particular id from the Expenses Table in the database
    def removeExpense(self,id):
        item = self.getExpense(id)
        db.session.delete(item)
        db.session.commit()

    #An expense is updated to reflect changes the Administrator wants to make
    #This change is committed to the Expenses table in the Artixa database
    def updateExpense(self,expense, date, name,description,category,amount):
        expense.date = date
        expense.name = name
        expense.description = description
        expense.category = category
        expense.amount = amount
        db.session.commit()

    #An Expense is retrueved based on Identification number
    def getExpense(self,id):
        return db.session.query(Expenses).filter(Expenses.id == id).first()
    
    #A category is retrieved based on the identification number
    def getCategory(self,id):
        return db.session.query(ExpenseCategories).filter(ExpenseCategories.id==id).first()
    
    #A category is added based on user input and is reflected in the ExpensesCategory Table in the Artixa database
    def addCategory(self, name):
        category = ExpenseCategories(name)
        db.session.add(category)
        db.session.commit()

    #Displays all Categories in the ExpenseCategories Table in the Artixaja Database
    def displayCategories(self):
        return db.session.query(ExpenseCategories).all()

    #Removes a category from the ExpenseCategories based on the Identification Number
    #This change is reflected in the ExpenseCategories Table
    def removeCategory(self,id):
        category =self.getCategory(id)
        db.session.delete(category)
        db.session.commit()

    #Displays all Expenses in the Expenses Table
    #The total expenses for the YTD is Calculated and generated
    def displayExpenses(self):
        expenses = db.session.query(Expenses).all()
        total = self.calculateExpenses(expenses)
        return expenses, total

    #The total expenses for the YTD are calculated and returned
    def calculateExpenses(self,expenses):
        total = 0
        for expense in expenses:
            total+=expense.amount
        return total