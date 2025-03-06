class Transaction:
  def __init__(self, date, account, type, amount):
    self.date = date
    self.account = account
    self.type = type
    self.amount = amount

  def __str__(self):
    return f"| {self.date} | {self.account} | {self.type} | {self.amount} |"
