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
                self.print_monthly_statement()
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
            date_str, account_id, type_str, amount_str = details.split()
            # check if current account exists in bank, else create new one
            if account_id not in self.accounts:
                self.accounts[account_id] = Account(account_id)
            success, message = self.accounts[account_id].add_transaction(
                date_str, account_id, type_str, amount_str
            )
            if success:
                print(self.accounts[account_id].generate_all_statements())
            else:
                print(f"Error: {message}")

    def print_monthly_statement(self):
        while True:
            details = input(
                "Please enter account and month to generate the statement <Account> <Year><Month> (or enter blank to go back to main menu):\n> "
            ).strip()
            if not details:
                break
            try:
                account, year_month_str = details.split(" ")
                # validate correct year_month_str input
                if not datetime.datetime.strptime(year_month_str, "%Y%m"):
                    print("\nInvalid date format. Must be YYYYMM")
                    continue
                year = int(year_month_str[:4])
                month = int(year_month_str[4:6])
                print(self.accounts[account].generate_monthly_statement(year, month))
            except ValueError as e:
                print(f"Invalid input: {e}")

    def define_interest(self):
        return None
