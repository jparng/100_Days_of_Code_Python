print("Welcome to the tip calculator.")
bill = input("What was the total bill? $")
percent = input("What percentage tip would you like to give? 10, 12, or 15? ")
people = input("How many people to split the bill? ")

percent = float(percent) / 100
bill = float(bill)
people = int(people)
tip = bill * percent
total = tip + bill
bill_per_person = total / people
final_amt = "{:.2f}".format(bill_per_person)
print(f"Each person should pay: ${final_amt}")
