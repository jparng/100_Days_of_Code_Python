import expense_tracker
import expense_trackergui
from tkinter import *

#Create the core data structure

if __name__ == "__main__":
    root = Tk()
    app = expense_trackergui.ExpenseTrackerGUI(root)
    root.mainloop()
    # tracker = expense_tracker.ExpenseTracker()
    # tracker.run()