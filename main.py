from transaction import input_transactions
from interest import define_interest
from account import print_statement


while True:
  print("Welcome to AwesomeGIC Bank! What would you like to do?")
  print("[T] Input transactions") 
  print("[I] Define interest rules")
  print("[P] Print statement")
  print("[Q] Quit")
  choice = input("> ").strip().upper()

  if choice == "T":
    input_transactions()
  elif choice == "I":
    define_interest()
  elif choice == "P":
    print_statement()
  elif choice == "Q":
    print("Thank you for banking with AwesomeGIC Bank.")
    print("Have a nice day!")
    break
  else:
    print("Invalid choice. Please try again. \n")