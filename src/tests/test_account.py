import pytest
from classes.account import Account


class MockInterestRule:
    def __init__(self, date, rate):
        self.date = date
        self.rate = rate


@pytest.fixture
def account():
    """Fixture to create a fresh Account instance for each test."""
    return Account("AC001")


# add_transaction tests
def test_invalid_date(account):
    success, message = account.add_transaction("20250432", "AC001", "D", "100")
    assert success == False
    assert message == "Invalid date format. Must be YYYYMMDD. \n"


def test_invalid_type_str(account):
    success, message = account.add_transaction("20250101", "AC001", "A", "100")
    assert success == False
    assert message == "Invalid transaction type. Must be D or W. \n"


def test_value_error(account):
    success, message = account.add_transaction("20250101", "AC001", "D", "abc")
    assert success == False
    assert message == "Invalid amount. Must be a number. \n"


def test_zero_amount(account):
    success, message = account.add_transaction("20250101", "AC001", "D", "0")
    assert success == False
    assert message == "Amount must be greater than zero. \n"


def test_negative_amount(account):
    success, message = account.add_transaction("20250101", "AC001", "D", "-100")
    assert success == False
    assert message == "Amount must be greater than zero. \n"


def test_first_transaction_withdrawal(account):
    success, message = account.add_transaction("20250101", "AC001", "W", "100")
    assert success == False
    assert message == "First transaction cannot be a withdrawal. \n"


def test_withdrawal_exceeds_balance(account):
    account.add_transaction("20250101", "AC001", "D", "100")
    success, message = account.add_transaction("20250102", "AC001", "W", "150")
    assert success == False
    assert message == "Insufficient funds. \n"


def test_valid_deposit_and_withdrawal(account):
    success, _ = account.add_transaction("20250101", "AC001", "D", "100")
    assert success == True
    success, message = account.add_transaction("20250102", "AC001", "W", "50")
    assert success == True
    assert message == "Transaction added successfully \n"


def test_multiple_transactions_same_date(account):
    date_str = "20250101"
    account.add_transaction(date_str, "AC001", "D", "100")
    account.add_transaction(date_str, "AC001", "D", "200")
    account.add_transaction(date_str, "AC001", "W", "50")
    transactions = account.transactions
    assert transactions[0].txn_id == "20250101-01"
    assert transactions[1].txn_id == "20250101-02"
    assert transactions[2].txn_id == "20250101-03"


def test_withdrawal_before_deposit_date_insufficient(account):
    account.add_transaction("20250102", "AC001", "D", "100")
    success, message = account.add_transaction("20250101", "AC001", "W", "50")
    assert success == False
    assert message == "Insufficient funds. \n"


def test_generate_monthly_no_transactions(account):
    account.add_transaction("20221231", "AC001", "D", "1000")
    rule = MockInterestRule("20220101", 1.0)
    statement = account.generate_monthly_statement(2025, 1, [rule])
    assert "| 20250131     |                  | I    | 0.85  | 1000.85 |" in statement


def test_generate_monthly_with_interest_change(account):
    rules = [MockInterestRule("20250115", 2.0), MockInterestRule("20250120", 1.5)]
    account.add_transaction("20250110", "AC001", "D", "500")
    account.add_transaction("20250125", "AC001", "W", "200")
    statement = account.generate_monthly_statement(2025, 1, rules)
    assert "| 20250131     |                  | I    | 0.33  | 300.33 |" in statement


def test_get_balance_before_date(account):
    account.add_transaction("20221231", "AC001", "D", "500")
    account.add_transaction("20250101", "AC001", "D", "200")
    balance = account.get_balance_before_date(2025, 1)
    assert balance == 500


def test_get_balance_no_prior_transactions(account):
    balance = account.get_balance_before_date(2025, 1)
    assert balance == 0


def test_generate_all_statements(account):
    account.add_transaction("20250101", "AC001", "D", "100")
    account.add_transaction("20250102", "AC001", "W", "50")
    statement = account.generate_all_statements()
    assert "| 20250101     | 20250101-01      | D    | 100.00  | 100.00 |" in statement
    assert "| 20250102     | 20250102-01      | W    | 50.00  | 50.00 |" in statement
