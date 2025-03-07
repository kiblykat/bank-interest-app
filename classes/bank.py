from classes.interest import define_interest
from classes.account import Account
from classes.transaction import Transaction
import datetime


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
            details = input(
                "Please enter transaction details in <Date> <Account> <Type> <Amount> format (or enter blank to go back to main menu):\n> "
            ).strip()
            if not details:
                break
            parts = details.split()
            if len(parts) != 4:  # check if valid input of 4 elements
                print("Invalid input. Must be <Date> <Account> <Type> <Amount>.")
                continue
            try:
                date_str, account, type_str, amount = details.split()
                if not self.validate_date(date_str):  # check if valid date
                    print("\nInvalid date format. Must be YYYYMMDD.")
                    continue
                type_str = type_str.upper()
                if type_str not in ("D", "W"):  # check if valid type
                    print("Invalid transaction type. Must be D or W.")
                    continue
                amount = float(amount)  # check if valid number
                if amount <= 0:
                    print("Amount must be greater than zero.")
                if account not in self.accounts:
                    self.accounts[account] = Account(account)
                transaction = Transaction(
                    date_str, account, type_str, amount
                )  # create new transaction object
                self.accounts[account].add_transaction(
                    transaction
                )  # add transaction to account
                print(f"{account} \n {transaction}")
            except ValueError as e:
                print(f"Invalid amount. Must be a number")

    def print_statement(self):
        while True:
            details = input(
                "Please enter account and month to generate the statement <Account> <Year><Month> (or enter blank to go back to main menu):\n> "
            ).strip()
            if not details:
                break
            try:
                account, date_str = details.split(" ")
                if not datetime.datetime.strptime(date_str, "%Y%m"):
                    print("\nInvalid date format")
                    continue
                print(self.accounts[account].generate_statement())
            except ValueError as e:
                print(f"Invalid input: {e}")

    def validate_date(self, date_str):
        try:
            datetime.datetime.strptime(date_str, "%Y%m%d")
            return True
        except:
            return False

    def define_interest(self):
        return None
