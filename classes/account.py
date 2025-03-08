import calendar


class Account:
    def __init__(self, account):
        self.account = account
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)  # utilizes Transaction class

    def generate_monthly_statement(self, year, month):

        statement = f"Account: {self.account} \n"
        statement += "| Date     | Txn Id      | Type | Amount | Balance | \n"
        balance = 0

        monthly_transactions = self.get_transactions_in_month(year, month)

        for txn in monthly_transactions:
            balance += txn.amount
            statement += f"| {txn.date}     | {txn.id}      | {txn.type} | {txn.amount} | {balance} | \n"
        return statement

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
