import pytest
from classes.bank import Bank
from classes.account import Account
from classes.interest import Interest
from classes.transaction import Transaction


@pytest.fixture
def bank():
    """Fixture to create a fresh Bank instance for each test."""
    return Bank()


@pytest.fixture
def account():
    """Fixture to create a fresh Account instance for each test."""
    return Account("AC001")


@pytest.fixture
def interest():
    """Fixture to create a fresh Interest instance for each test."""
    return Interest("20221001", "RULE01", "1.23")


@pytest.fixture
def transaction():
    """Fixture to create a fresh Transaction instance for each test."""
    return Transaction("AC001", "20250601", "20250601-01", "W", "500")


# Account tests
def test_invalid_date(account):
    success, message = account.add_transaction("20250432", "AC001", "D", "100")
    assert success == False
    assert message == "Invalid date format. Must be YYYYMMDD. \n"


def test_invalid_type_str(account):
    success, message = account.add_transaction("20250411", "AC001", "A", "100")
    assert success == False
    assert message == "Invalid transaction type. Must be D or W. \n"


def test_value_error(account):
    success, message = account.add_transaction("20250411", "AC001", "D", "abc")
    assert success == False
    assert message == "Invalid amount. Must be a number. \n"


def test_negative_deposit(account):
    success, message = account.add_transaction("20250411", "AC001", "D", "-100")
    assert success == False
    assert message == "Amount must be greater than zero. \n"


def test_first_transaction_witdrawal(account):
    success, message = account.add_transaction("20250411", "AC001", "W", "100")
    assert success == False
    assert message == "First transaction cannot be a withdrawal. \n"


def test_insufficient_funds(account):
    account.add_transaction("20250411", "AC001", "D", "100")
    success, message = account.add_transaction("20250411", "AC001", "W", "101")
    assert success == False
    assert message == "Insufficient funds. \n"


def test_successful_txn(account):
    success, message = account.add_transaction("20250411", "AC001", "D", "100")
    assert success == True
    assert message == "Transaction added successfully \n"


# def test_insufficient_balance(bank):


# def test_interest_rule_replacement(bank):


# def test_statement_generation(bank):
