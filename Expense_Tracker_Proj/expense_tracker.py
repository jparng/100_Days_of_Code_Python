#required libraries
import datetime
import json
import os
from collections import defaultdict

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
        self.load_data()  # this will load existing data if available
        
#create the main functions

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
        print(f"Week {week}: ${total: 2.f}")
        
    #Category breakdown
    print("\n=== Category Breakdown ===")
    category_totals = defaultdict(float)
    for expense in self.expenses:
        category_totals[expense['category']] += expense['amount']
        
    for category, total in category_totals.items():
        print(f"{category}: ${total:.2f} ({total/sum(category_totals.values())*100:.1f}%)")
        
#saving data

