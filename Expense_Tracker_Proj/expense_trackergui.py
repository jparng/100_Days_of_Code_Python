from tkinter import *
from tkinter import ttk, messagebox
import datetime
import json
import os
from collections import defaultdict
from expense_tracker import ExpenseTracker

class ExpenseTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.tracker = ExpenseTracker()  # Using our core class
        
        # Create GUI elements
        self.setup_ui()
        self.setup_budget_ui()
        
        #Create status label 
        self.budget_status_label = Label(root, text="", fg="black")
        self.budget_status_label.pack(pady=5)
        
    def setup_budget_ui(self):
        #Budget Frame
        budget_frame = LabelFrame(self.root, text="Budget Management", padx=10, pady=10)
        budget_frame.pack(padx=10, pady=10, fill="x")
        
        #Budget Entry components
        Label(budget_frame, text="Category:").grid(row=0, column=0, sticky="w")
        self.budget_category_var = StringVar()
        self.budget_category_dropdown = ttk.Combobox(
            budget_frame,
            textvariable=self.budget_category_var,
            values=list(self.tracker.categories.keys())
        )
        self.budget_category_dropdown.grid(row=0, column=1, padx=5)
        
        Label(budget_frame, text="Amount:").grid(row=1,column=0, sticky="w")
        self.budget_amount_entry = Entry(budget_frame)
        self.budget_amount_entry.grid(row=1,column=1, padx=5)
        
        #Budget Buttons
        Button(
            budget_frame,
            text="Set Budget",
            command=self.set_budget
        ).grid(row=2, column=0, pady=5)
        
        Button(
            budget_frame,
            text="View Budgets",
            command=self.view_budgets
        ).grid(row=2, column=1, pady=5)
    
    def setup_ui(self):
        self.root.title("Expense Tracker")
        
        # Add Expense Frame
        add_frame = LabelFrame(self.root, text="Add New Expense", padx=10, pady=10)
        add_frame.pack(padx=10, pady=10, fill="x")
        
        # Amount
        Label(add_frame, text="Amount:").grid(row=0, column=0)
        self.amount_entry = Entry(add_frame)
        self.amount_entry.grid(row=0, column=1)
        
        # Category dropdown
        Label(add_frame, text="Category:").grid(row=2, column=0)
        self.category_var = StringVar()
        self.category_dropdown = ttk.Combobox(add_frame, textvariable=self.category_var)
        self.category_dropdown['values'] = list(self.tracker.categories.keys())
        self.category_dropdown.grid(row=2, column=1)
        
        # Add button
        add_btn = Button(add_frame, text="Add Expense", command=self.add_expense)
        add_btn.grid(row=3, columnspan=2, pady=5)
        
        # Summary Frame
        summary_frame = LabelFrame(self.root, text="Expense Summary", padx=10, pady=10)
        summary_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Treeview for displaying expenses
        self.tree = ttk.Treeview(summary_frame, columns=("Date", "Category", "Amount", "Description"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")
        self.tree.pack(fill="both", expand=True)
        
        # Refresh button
        refresh_btn = Button(summary_frame, text="Refresh", command=self.refresh_data)
        refresh_btn.pack(pady=5)
        
        self.refresh_data()
    
    def set_budget(self):
        category = self.budget_category_var.get()
        amount = self.budget_amount_entry.get()
        
        if not category:
            self._show_budget_status("Please select a category", "red")
            return
        
        if not amount:
            self._show_budget_status("Please enter an amount", "red")
            return
        
        try:
            amount = float(amount)
            
            if amount <= 0:
                raise ValueError("Amount must be positive")
            
            #Use ExpenseTracker's method
            self.tracker.set_budget(category, amount)
            self._show_budget_status(
                f"Budget set: {category} = ${amount:.2f}",
                "green"
            )
            self.budget_amount_entry.delete(0, END)
            self.refresh_data() #Update display\
        except ValueError:
            self._show_budget_status("Please enter a valid number", "red")

    def view_budgets(self):
        #Use ExpenseTracker's method to get data
        budgets = self.tracker.get_all_budgets()
        
        if not budgets:
            self._show_budget_status("No budgets set yet", "blue")
            return
        
        budget_window = Toplevel(self.root)
        budget_window.title("Current Budgets")
        budget_window.geometry("600x400")
        
        #Frame for Treeview and scrollbar
        tree_frame = Frame(budget_window)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        #Create treeview
        columns = ("Category", "Budget", "Spent", "Remaining")
        
        tree = ttk.Treeview(tree_frame, columns= columns,show="headings", selectmode="browse")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor = "center")
            
        #Add scrollbar
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, columns=1, sticky="ns")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        #Populate data with ExpenseTracker methods
        for category, budget in budgets.items():
            #Get spending data from ExpenseTracker
            spent = sum(
                e['amount'] for e in self.tracker.expenses 
                if e['category'] == category and
                datetime.datetime.strptime(e['date'], '%Y-%m-%d').month == 
                datetime.datetime.now().month
            )
            remaining = budget - spent
            
            #Color coding

            tree.insert(
                "",
                "end",
                values=(
                category,
                f"${budget:.2f}",
                f"${spent:.2f}",
                f"${remaining:.2f}"
            ),
            tags = ('over' if remaining < 0 else 'under',)
        )
            
        #Configure tag colors
        tree.tag_configure('over', foreground='red')
        tree.tag_configure('under', foreground='green')
        
        #Add close button
        Button(budget_window, text="Close", command=budget_window.destroy).pack(pady=10)
        
        
    def _show_budget_status(self, message, color):
        """Helper to display status messages"""
        self.budget_status_label.config(text=message, fg=color)
        self.budget_status_label.after(5000, lambda: self.budget_status_label.config(text=""))
            
    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_var.get()
            
            if not category:
                messagebox.showerror("Error", "Please select a category")
                return
                
            expense = {
                'amount': amount,
                'category': category,
                'date': datetime.date.today().isoformat(),
                'description': "",
                'subcategory': ""
            }
            
            self.tracker.expenses.append(expense)
            self.tracker.save_data()
            messagebox.showinfo("Success", "Expense added successfully!")
            self.refresh_data()
            self.amount_entry.delete(0, END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
    
    def refresh_data(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        budgets = self.tracker.get_all_budgets()
         
        # Add expenses to treeview
        for expense in self.tracker.expenses:
            category = expense['category']
            amount = expense['amount']
            date = expense['date']
            
            #Use ExpenseTracker to check budget status
            budget_info = ""
            if category in budgets:
                spent, budget = self.tracker.check_budget_status(category)
                if spent is not None:
                    percentage = (spent / budget) * 100
                    budget_info = f" ({percentage:.1f}% of budget)"
                    
            self.tree.insert("", "end", values=(
                date,
                category,
                f"${amount:.2f}",
                expense['description'] + budget_info
            ))

if __name__ == "__main__":
    root = Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()