#from replit import clear
from art import logo

print(logo)
# ask for name
# ask for bid
# ask if there are any other bidders
auction = []
max_bid = 0
highest_bidder = ""
print("Welcome to the auction program.")
start_auction = False
def add_user(user_name, user_bid):
  new_bidder = {}
  new_bidder["name"] = user_name
  new_bidder["bid"] = user_bid
  auction.append(new_bidder)


while not start_auction:
  name = input("What is your name?: ")
  bid = int(input("What's your bid?: "))
  add_user(name, bid)
  more_user = input("Are there any other bidders? Type 'yes' or 'no'.\n").lower()
  if more_user == "yes":
    #clear() function using replit.
  else:
    start_auction = True


for bid in range(len(auction)):
  if auction[bid]["bid"] > max_bid:
    max_bid = auction[bid]["bid"]
    highest_bidder = auction[bid]["name"]
print(f"{max_bid} is the highest bid from {highest_bidder}.")
