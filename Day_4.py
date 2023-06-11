
import random

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

user = input("What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors\n")
user = int(user)
player = [rock, paper, scissors]
computer = [rock, paper, scissors]
play = computer[random.randint(0,2)]

if user >= 3:
  print("Invalid input. Game over.")

else:
  print(player[user])
  print("Computer chose:")
  print(play)
  if player[user] == rock and play == rock or player[user] == paper and play == paper or player[user] == scissors and play == scissors:
    print("It's a draw.")
  elif player[user] == rock and play == paper or player[user] == paper and play == scissors or player[user] == scissors and play == rock:
    print("You lose.")
  elif player[user] == scissors and play == paper or player[user] == paper and play == rock or player[user] == rock and play == scissors:
    print("You Win!")
