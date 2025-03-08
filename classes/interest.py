class Interest:
    def __init__(self, date, ruleId, rate):
        self.date = date
        self.ruleId = ruleId
        self.rate = rate

    def __str__(self):
        return f"{self.date} | {self.ruleId} | {self.rate} |"