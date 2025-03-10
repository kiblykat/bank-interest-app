from utils.utils import validate_date
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
        if not validate_date(date_str):
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
        return True, "Transaction added successfully \n"

    def generate_all_statements(self):
        statement = f"Account: {self.account} \n"
        statement += "| Date         | Txn Id           | Type | Amount | Balance | \n"
        balance = 0
        for txn in self.transactions:
            if txn.type == "D":
                balance += txn.amount
            else:
                balance -= txn.amount
            statement += f"| {txn.date}     | {txn.txn_id}      | {txn.type}    | {txn.amount:.2f}  | {balance:.2f} | \n"
        return statement

    def generate_monthly_statement(self, year, month, interest_rules):
        statement = f"Account: {self.account} \n"
        statement += "| Date         | Txn Id           | Type | Amount | Balance | \n"
        initial_balance = self.get_balance_before_date(year, month)

        # get the transactions in requested month
        monthly_transactions = self.get_transactions_in_month(year, month)

        current_balance = initial_balance
        for txn in monthly_transactions:
            if txn.type == "D":
                current_balance += txn.amount
            else:
                current_balance -= txn.amount
            statement += f"| {txn.date}     | {txn.txn_id}      | {txn.type}    | {txn.amount:.2f}  | {current_balance:.2f} | \n"

        # --- CALCULATE INTEREST ---
        daily_balance_dict = defaultdict(int)
        last_day = calendar.monthrange(year, month)[1]

        # reset current balance for interest calculation
        current_balance = initial_balance
        # populate the daily_balance_dict dictionary {[key:date_str]:balance}
        for day in range(1, last_day + 1):
            date_str = f"{year}{month:02}{day:02}"
            # filter transaction in current day
            day_transactions = [
                txn for txn in monthly_transactions if txn.date == date_str
            ]

            # get current balance given multiple txn in a day
            for txn in day_transactions:
                if txn.type == "D":
                    current_balance += txn.amount
                else:
                    current_balance -= txn.amount
            daily_balance_dict[date_str] = current_balance

        # array to hold all dates balance rule within the month
        date_balance_rate_array = []
        for day in range(1, last_day + 1):
            date_str = f"{year}{month:02}{day:02}"
            day_balance = daily_balance_dict.get(date_str, 0)
            applicable_rate = 0  # initialize rate to be 0 if no rule found before date
            for rule in reversed(interest_rules):
                if rule.date <= date_str:
                    applicable_rate = rule.rate
                    break
            date_balance_rate_array.append([date_str, day_balance, applicable_rate])

        annualized_interest = 0
        curr_count = 1
        for i in range(1, len(date_balance_rate_array)):
            # Check if current balance and rate match previous day
            curr_balance = date_balance_rate_array[i][1]
            prev_balance = date_balance_rate_array[i - 1][1]
            curr_rate = date_balance_rate_array[i][2]
            prev_rate = date_balance_rate_array[i - 1][2]

            if curr_balance == prev_balance and curr_rate == prev_rate:
                curr_count += 1
            else:
                # Calculate interest for the streak of identical balance/rate days
                annualized_interest += curr_count * prev_balance * prev_rate / 100
                curr_count = 1  # reset count

        annualized_interest += (
            curr_count
            * date_balance_rate_array[i - 1][1]
            * (date_balance_rate_array[i - 1][2])
            / 100
        )

        total_interest = round(annualized_interest / 365, 2)
        statement += f"| {year}{month:02}{last_day:02}     |                  | I    | {total_interest:.2f}  | {(current_balance + total_interest):.2f} | \n"
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
