from tkinter import *
from tkinter import ttk, messagebox
from expense_tracker import ExpenseTracker

class ExpenseTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.tracker = ExpenseTracker()  # Using our core class
        
        # Create GUI elements
        self.setup_ui()
    
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
            
        # Add expenses to treeview
        for expense in self.tracker.expenses:
            self.tree.insert("", "end", values=(
                expense['date'],
                expense['category'],
                f"${expense['amount']:.2f}",
                expense['description']
            ))

if __name__ == "__main__":
    root = Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()