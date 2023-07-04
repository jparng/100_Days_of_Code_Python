from art import logo
#calculator
# add
def add(n1, n2):
  return n1 + n2
# subtract
def subtract(n1, n2):
  return n1 - n2
# multiply
def multiply(n1, n2):
  return n1 * n2
# divide
def divide(n1, n2):
  return n1 / n2

operations = {
  "+" : add,
  "-" : subtract,
  "*" : multiply,
  "/" : divide
}
def calculator():
  print(logo)
  num1 = float(input("What is the first number?: "))
  for operation in operations:
    print(operation)
  new_calc = True
  
  while new_calc:
    operation_symbol = input("Pick an operation : ")
    num2 = float(input("What is the next number?: "))
    calculation_function = operations[operation_symbol]
    answer = calculation_function(num1, num2)
    print(f"{num1} {operation_symbol} {num2} = {answer}")
    keep_calc = input(f"Type 'y' to continue calculating with {answer}, or type 'n' to start a new calculation.: ").lower()
    if keep_calc == "n":
      new_calc = False
      calculator()
    elif keep_calc == "y":
      num1 = answer
    else:
      print("Invalid input. Exiting Program.")
      new_calc = False


calculator()
