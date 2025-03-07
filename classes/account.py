class Account:
  def __init__(self, account):
    self.account = account
    self.transactions = []
    
  def add_transaction(self, transaction):
    self.transactions.append(transaction) # utilizes Transaction class
    
  def generate_statement(self):
    statement = f"Account: {self.account} \n"
    statement += "| Date     | Txn Id      | Type | Amount | Balance | \n"
    balance = 0
    for txn in self.transactions:
      balance += txn.amount
      statement += f"| {txn.date}     | {txn.id}      | {txn.type} | {txn.amount} | {balance} | \n"
    return statement

  def __str__(self):
    return f"Account: {self.account}, Date: {self.date}, Type: {self.type}, Amount: {self.amount}"