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


# -------------------------
# Tests for add_transaction
# -------------------------
def test_add_transaction_invalid_date(account):
    # Adding a transaction with an invalid date format.
    success, message = account.add_transaction("20250432", "AC001", "D", "100")
    assert success == False
    assert message == "Invalid date format. Must be YYYYMMDD. \n"


def test_add_transaction_invalid_type_str(account):
    # Adding a transaction with an invalid transaction type.
    success, message = account.add_transaction("20250101", "AC001", "A", "100")
    assert success == False
    assert message == "Invalid transaction type. Must be D or W. \n"


def test_add_transaction_value_error(account):
    # Adding a transaction with a non-numeric amount.
    success, message = account.add_transaction("20250101", "AC001", "D", "abc")
    assert success == False
    assert message == "Invalid amount. Must be a number. \n"


def test_add_transaction_zero_amount(account):
    # Adding a transaction with an amount of zero.
    success, message = account.add_transaction("20250101", "AC001", "D", "0")
    assert success == False
    assert message == "Amount must be greater than zero. \n"


def test_add_transaction_negative_amount(account):
    # Adding a transaction with a negative amount.
    success, message = account.add_transaction("20250101", "AC001", "D", "-100")
    assert success == False
    assert message == "Amount must be greater than zero. \n"


def test_add_transaction_first_transaction_withdrawal(account):
    # Test that the first transaction cannot be a withdrawal.
    success, message = account.add_transaction("20250101", "AC001", "W", "100")
    assert success == False
    assert message == "First transaction cannot be a withdrawal. \n"


def test_add_transaction_withdrawal_exceeds_balance(account):
    # Test that a withdrawal exceeding the account balance is not allowed.
    account.add_transaction("20250101", "AC001", "D", "100")
    success, message = account.add_transaction("20250102", "AC001", "W", "150")
    assert success == False
    assert message == "Insufficient funds. \n"


def test_add_transaction_valid_deposit_and_withdrawal(account):
    # Adding a valid deposit and a valid withdrawal.
    success, _ = account.add_transaction("20250101", "AC001", "D", "100")
    assert success == True
    success, message = account.add_transaction("20250102", "AC001", "W", "50")
    assert success == True
    assert message == "Transaction added successfully \n"


def test_add_transaction_multiple_transactions_same_date(account):
    # Multiple transactions on the same date and verify transaction IDs.
    date_str = "20250101"
    account.add_transaction(date_str, "AC001", "D", "100")
    account.add_transaction(date_str, "AC001", "D", "200")
    account.add_transaction(date_str, "AC001", "W", "50")
    transactions = account.transactions
    assert transactions[0].txn_id == "20250101-01"
    assert transactions[1].txn_id == "20250101-02"
    assert transactions[2].txn_id == "20250101-03"


def test_add_transaction_withdrawal_before_deposit_insufficient(account):
    # Test withdrawal attempt before a deposit date, which should fail due to insufficient funds.
    account.add_transaction("20250102", "AC001", "D", "100")
    success, message = account.add_transaction("20250101", "AC001", "W", "50")
    assert success == False
    assert message == "Insufficient funds. \n"


def test_add_transaction_generate_monthly_no_transactions(account):
    # Generating a monthly statement when there are no transactions in the specified month.
    account.add_transaction("20221231", "AC001", "D", "1000")
    rule = MockInterestRule("20220101", 1.0)
    statement = account.generate_monthly_statement(2025, 1, [rule])
    assert "| 20250131     |                  | I    | 0.85  | 1000.85 |" in statement


def test_add_transaction_generate_monthly_with_interest_change(account):
    # Generating a monthly statement when interest rates change during the month.
    rules = [MockInterestRule("20250115", 2.0), MockInterestRule("20250120", 1.5)]
    account.add_transaction("20250110", "AC001", "D", "500")
    account.add_transaction("20250125", "AC001", "W", "200")
    statement = account.generate_monthly_statement(2025, 1, rules)
    assert "| 20250131     |                  | I    | 0.33  | 300.33 |" in statement


def test_add_transaction_get_balance_before_date(account):
    # Retrieving the account balance before a specific date.
    account.add_transaction("20221231", "AC001", "D", "500")
    account.add_transaction("20250101", "AC001", "D", "200")
    balance = account.get_balance_before_date(2025, 1)
    assert balance == 500


def test_add_transaction_get_balance_no_prior_transactions(account):
    # Retrieving the balance when there are no prior transactions.
    balance = account.get_balance_before_date(2025, 1)
    assert balance == 0


def test_add_transaction_generate_all_statements(account):
    # Generating a complete statement for all transactions.
    account.add_transaction("20250101", "AC001", "D", "100")
    account.add_transaction("20250102", "AC001", "W", "50")
    statement = account.generate_all_statements()
    assert "| 20250101     | 20250101-01      | D    | 100.00  | 100.00 |" in statement
    assert "| 20250102     | 20250102-01      | W    | 50.00  | 50.00 |" in statement
