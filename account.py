class Account:
  def __init__(self, account):
    self.account = account
    self.transactions = []
    
  def add_transaction(self, transaction):
    self.transactions.append(transaction) # utilizes Transaction class

  def __str__(self):
    return f"Account: {self.account}, Date: {self.date}, Type: {self.type}, Amount: {self.amount}"