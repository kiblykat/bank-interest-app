from interest import define_interest
from account import Account
from transaction import Transaction


class Bank:
  def __init__(self):
    self.accounts = {}  # {account_id: Account}
  
  def run(self):
    while True:
      print("Welcome to AwesomeGIC Bank! What would you like to do?")
      print("[T] Input transactions") 
      print("[I] Define interest rules")
      print("[P] Print statement")
      print("[Q] Quit")
      choice = input("> ").strip().upper()

      if choice == "T":
        self.input_transactions()
      elif choice == "I":
        self.define_interest()
      elif choice == "P":
        self.print_statement()
      elif choice == "Q":
        print("Thank you for banking with AwesomeGIC Bank.")
        print("Have a nice day!")
        break
      else:
        print("Invalid choice. Please try again. \n")

  def input_transactions(self):
    while True:
      transaction_details = input("Please enter transaction details in <Date> <Account> <Type> <Amount> format (or enter blank to go back to main menu):\n> ").strip()
      if not transaction_details:
          break
      try:
          date, account, type, amount = transaction_details.split()
          amount = float(amount)
          if account not in self.accounts:
              self.accounts[account] = Account(account)
          transaction = Transaction(date, account, type, amount)  #create new transaction object
          self.accounts[account].add_transaction(transaction)     #add transaction to account
          print(f"{account} \n {transaction}")
      except ValueError as e:
          print(f"Invalid input: {e}")

  def print_statement():
      return None
  
  def define_interest():
      return None