import datetime
import calendar
from collections import defaultdict
from classes.transaction import Transaction


class Account:
    def __init__(self, account):
        self.account = account
        self.transactions = []  # Transaction[]
        self.dates_counter = defaultdict(int)

    def add_transaction(self, date_str, account_id, type_str, amount_str):
        # check if valid date format
        if not self.validate_date(date_str):
            return False, "Invalid date format. Must be YYYYMMDD. \n"
        type_str = type_str.upper()
        # check if valid type (D/W)
        if type_str not in ("D", "W"):
            return False, "Invalid transaction type. Must be D or W. \n"
        # check if valid number && amount > 0
        try:
            amount = round(float(amount_str), 2)
            if amount <= 0:
                return False, "Amount must be greater than zero. \n"
        except ValueError as e:
            return False, "Invalid amount. Must be a number. \n"
        if amount <= 0:
            return False, "Amount must be greater than zero. \n"
        # check if first transaction is a withdrawal
        if len(self.transactions) == 0 and type_str == "W":
            return False, "First transaction cannot be a withdrawal. \n"
        # check if withdraw > balance (before date of transaction)
        if type_str == "W":
            balance = 0
            # find balance before date of transaction
            for txn in self.transactions:
                if txn.date <= date_str:
                    if txn.type == "D":
                        balance += txn.amount
                    else:
                        balance -= txn.amount
            if balance < amount:
                return False, "Insufficient funds. \n"

        # increment date counter
        self.dates_counter[date_str] += 1
        txn_id = f"{date_str}-{self.dates_counter[date_str]:02d}"
        # create new transaction object
        transaction = Transaction(account_id, date_str, txn_id, type_str, amount)
        # add transaction to specified account_id object
        self.transactions.append(transaction)
        # sort transactions by date
        self.transactions.sort(key=lambda txn: txn.date)
        # return success
        return True, "Transaction added successfully"

    def generate_all_statements(self):
        statement = f"Account: {self.account} \n"
        statement += "| Date         | Txn Id           | Type | Amount | Balance | \n"
        balance = 0
        for txn in self.transactions:
            if txn.type == "D":
                balance += txn.amount
            else:
                balance -= txn.amount
            statement += f"| {txn.date}     | {txn.txn_id}      | {txn.type}    | {txn.amount}  | {balance} | \n"
        return statement

    def generate_monthly_statement(self, year, month):
        statement = f"Account: {self.account} \n"
        statement += "| Date         | Txn Id           | Type | Amount | Balance | \n"
        balance = self.get_balance_before_date(year, month)

        monthly_transactions = self.get_transactions_in_month(year, month)

        for txn in monthly_transactions:
            if txn.type == "D":
                balance += txn.amount
            else:
                balance -= txn.amount
            statement += f"| {txn.date}     | {txn.txn_id}      | {txn.type}    | {txn.amount}  | {balance} | \n"
        return statement

    def get_balance_before_date(self, year, month):
        balance = 0
        target_date = f"{year}{month:02}01"
        for txn in self.transactions:
            if txn.date < target_date:
                if txn.type == "D":
                    balance += txn.amount
                else:
                    balance -= txn.amount
        return balance
    
    def get_transactions_in_month(self, year, month):
        start_date = f"{year}{month:02}01"
        last_day = calendar.monthrange(year, month)[1]
        end_date = f"{year}{month:02}{last_day}"
        transactions = []
        # go through each transaction within current account, and find those within range
        for txn in self.transactions:
            if start_date <= txn.date <= end_date:
                transactions.append(txn)
        return transactions

    def validate_date(self, date_str):
        try:
            datetime.datetime.strptime(date_str, "%Y%m%d")
            return True
        except:
            return False
