import pytest
from classes.bank import Bank


def test_add_transaction():
    bank = Bank()
    success, _ = bank.add_transaction("20230601", "AC001", "D", "100.00")
    assert success
    assert "AC001" in bank.accounts
    account = bank.accounts["AC001"]
    assert len(account.transactions) == 1
    txn = account.transactions[0]
    assert txn.date == "20230601"
    assert txn.type == "D"
    assert txn.amount == 100.00


def test_insufficient_balance():
    bank = Bank()
    bank.add_transaction("20230601", "AC001", "D", "100.00")
    success, msg = bank.add_transaction("20230602", "AC001", "W", "150.00")
    assert not success
    assert "negative balance" in msg


def test_interest_rule_replacement():
    bank = Bank()
    bank.add_interest_rule("20230101", "RULE01", "1.95")
    bank.add_interest_rule("20230101", "RULE02", "2.00")
    assert len(bank.interest_rules) == 1
    assert bank.interest_rules[0].rule_id == "RULE02"
    assert bank.interest_rules[0].rate == 2.00


def test_statement_generation():
    bank = Bank()
    bank.add_interest_rule("20230520", "RULE02", "1.90")
    bank.add_interest_rule("20230615", "RULE03", "2.20")
    bank.add_transaction("20230505", "AC001", "D", "100.00")
    bank.add_transaction("20230601", "AC001", "D", "150.00")
    bank.add_transaction("20230626", "AC001", "W", "20.00")
    bank.add_transaction("20230626", "AC001", "W", "100.00")
    success, result = bank.generate_statement("AC001", "202306")
    assert success
    assert len(result) == 5  # 4 transactions + interest
    interest = result[-1]
    assert interest["type"] == "I"
    assert interest["amount"] == 0.39
    assert interest["balance"] == 130.39
