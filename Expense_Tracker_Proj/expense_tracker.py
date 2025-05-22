#required libraries
import datetime
import json
import os
from collections import defaultdict
import matplotlib.pyplot as plt

from tkinter import *
from tkinter import ttk, messagebox

class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.categories = {
            'Food': ['groceries', 'restaurant', 'coffee'],
            'Transport': ['bus', 'train','gas', 'parking'],
            'Housing' : ['rent', 'utilities', 'maintenance'],
            'Entertainment' : ['movies', 'games', 'subscriptions', 'electronics','furniture'],
            'Other' : []
        }
        self.budgets = {} #stores budgets
        self.load_data()  # this will load existing data if available
        
#create the main functions

#data visualization
    def plot_spending(self):
        category_totals = defaultdict(float)
        for expense in self.expenses:
            category_totals[expense['category']] += expense['amount']
            
        plt.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%')
        plt.title('Spending by Category')
        plt.show()

#add expense

    def add_expense(self):
        amount = float(input("Enter amount spent:"))
        print("Available categories:")
        for i, category in enumerate(self.categories.keys(), 1):
            print(f"{i}, {category}")
        
        cat_choice = int(input("Select category number: ")) - 1
        category = list(self.categories.keys())[cat_choice]
    
    # categories with subcategories
        if self.categories[category]:
            print("Subcategories:")
            for i, subcat in enumerate(self.categories[category], 1):
                print(f"{i}, {subcat}")
            
            sub_choice = input("Select subcategory number (or leave blank): ")
            subcategory = self.categories[category][int(sub_choice) - 1] if sub_choice else ""
        else:
            subcategory = ""
        
        description = input("Description (optional): ")
        date = input("Date (YYYY-MM-DD, today if blank): ")
    
        expense = {
            'amount': amount,
            'category': category,
            'subcategory': subcategory,
            'description': description,
            'date': date if date else datetime.date.today().isoformat()
        }
    
        self.expenses.append(expense)
        self.save_data()
        print("Expense added successfully!")

#reporting expenses
    def view_summary(self):
        if not self.expenses:
            print("No expenses recorded yet.")
            return
        
    #Weekly summary
        print("\n=== Weekly Summary ===")
        weekly = defaultdict(float)
        for expense in self.expenses:
            week = datetime.datetime.strptime(expense['date'], '%Y-%m-%d').isocalendar()[1]
            weekly[week] += expense['amount']
        
        for week, total in weekly.items():
            print(f"Week {week}: ${total:.2f}")
        
    #Category breakdown
        print("\n=== Category Breakdown ===")
        category_totals = defaultdict(float)
        for expense in self.expenses:
            category_totals[expense['category']] += expense['amount']
        
        for category, total in category_totals.items():
            print(f"{category}: ${total:.2f} ({total/sum(category_totals.values())*100:.1f}%)")
        
#saving data
    def save_data(self):
        data = {
            'expenses': self.expenses,
            'categories': self.categories,
            'budgets': self.budgets
        }
        with open('expense_data.json', 'w') as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if os.path.exists('expense_data.json'):
            with open('expense_data.json', 'r') as f:
                data = json.load(f)
            self.expenses = data['expenses']
            self.categories = data.get('categories', self.categories)
            self.budgets = data.get('budgets', {}) #loads budgets or default to empty
            
#Budgeting system
    def set_budget(self, category, amount):
        self.budgets[category] = float(amount)
        self.save_data()
            
        # while True:
        #     print("1. Check Budget")
        #     print("2. Go back to Main Menu")
        #     print("3. Exit")
            
        #     choice = input("Select an option: ")
            
        #     if choice == '1':
        #         self.check_budgets()
        #     elif choice == '2':
        #         self.run()
        #     elif choice == '3':
        #         self.save_data()
        #         print("Goodbye!")
        #         break
        #     else:
        #         print("Invalid option. Please try again.")

    def get_budget(self, category):
        """Get budget for a category, return none if not set"""
        return self.budgets.get(category)
    
    def get_all_budgets(self):
        """Return all budgets as a dictionary"""
        return self.budgets.copy()
    
    def check_budgets(self):
        if not self.budgets:
            print("No budgets set yet. Use 'set_budget' to create budgets.")
            return
        
        print("\n=== Budget Status ===")
        grand_total = sum(self.budgets.values())
        total_spent = 0
        overspent_categories = []
        
        for category, budget in self.budgets.items():
            spent = sum(e['amount'] for e in self.expenses
                        if e['category'] == category and
                        datetime.datetime.strptime(e['date'], '%Y-%m-%d').month == datetime.datetime.now().month)
            total_spent += spent
            
            remaining = budget - spent
            status = "UNDER" if remaining >= 0 else "OVER"
            color_code = "\033[92m" if remaining >= 0 else "\033[91m" #green and red codes
            
            print(f"{category}: Spent ${spent:.2f} of ${budget:.2f} | {color_code} {status} by ${abs(remaining):.2f}\033[0m | ({spent/budget*100:.1f}%)")
        
            if remaining < 0:
                overspent_categories.append(category)
                
        print(f"\nTotal budgeted: ${grand_total:.2f}")
        print(f"Total spent: ${total_spent:.2f}")
        if overspent_categories:
            print("\n\033[91mWARNING: Overspent in categories:", ", ".join(overspent_categories),"\033[0m")
            
        # while True:
        #     print("1. Go back to Main Menu")
        #     print("2. Exit")
            
        #     choice = input("Select an option: ")
            
        #     if choice == '1':
        #         self.run()
        #     elif choice == '2':
        #         self.save_data()
        #         print("Goodbye!")
        #         break
        #     else:
        #         print("Invalid option. Please try again.")
          

#main menu

    def run(self):
        while True:
            print("\nExpense Tracker Menu:")
            print("1. Add Expense")
            print("2. View Summary")
            print("3. Manage Budgets")
            print("4. Check Budget Status")
            print("5. Visualize Spending on a Chart")
            print("6. Exit")
            
            choice = input("Select an option: ")
            
            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_summary()
            elif choice == '3':
                self.manage_budgets()
            elif choice == '4':
                self.check_budgets()
            elif choice == '5':
                self.plot_spending()
            elif choice == '6':
                self.save_data()
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def manage_budgets(self):
        while True:
            print("\nBudget Management:")
            print("1. Set/Update Budget")
            print("2. View All Budgets")
            print("3. Back to Main Menu")
            
            choice = input("Select an option: ")
            
            if choice == '1':
                print("\nAvailable categories:")
                for i, category in enumerate(self.categories.keys(), 1):
                    print(f"{i}.{category}")
                cat_choice = int(input("Select category number: ")) - 1
                category = list(self.categories.keys())[cat_choice]
                amount = float(input(f"Enter monthly budget for {category}: $"))
                self.set_budget(category, amount)
                print(f"Budget for {category} set to ${amount:.2f}")
            elif choice == '2':
                print("\n Current Budgets:")
                for category, amount in self.budgets.items():
                    print(f"{category}: ${amount:.2f}")
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")