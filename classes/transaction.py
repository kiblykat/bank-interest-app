class Transaction:

    def __init__(self, account, date, txn_id, type, amount):
        self.account = account
        self.date = date
        self.txn_id = txn_id
        self.type = type
        self.amount = amount

    def __str__(self):
        return f"| {self.date} | {self.account} | {self.type} | {self.amount} |"
