import unittest
from io import StringIO
import sys
from unittest.mock import patch
from classes.bank import Bank
from classes.account import Account


class TestBank(unittest.TestCase):
    def setUp(self):
        self.bank = Bank()

    # ----------------------------
    # Tests for input_transactions
    # ----------------------------
    def test_input_transactions_blank(self):
        # When the user just presses enter, the method should exit gracefully.
        with patch("builtins.input", side_effect=[""]):
            captured_output = StringIO()
            sys.stdout = captured_output
            self.bank.input_transactions()
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            self.assertIn("", output)

    def test_input_transactions_valid_deposit(self):
        # Valid deposit: expect success message and a printed statement.
        inputs = ["20230301 ACC001 D 1000", ""]
        with patch("builtins.input", side_effect=inputs):
            captured_output = StringIO()
            sys.stdout = captured_output
            self.bank.input_transactions()
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            self.assertIn("| Txn Id           | Type | Amount | Balance |", output)
            self.assertIn("ACC001", output)

    def test_input_transactions_invalid_date(self):
        # Date not in YYYYMMDD format.
        inputs = ["2023-03-01 ACC001 D 1000", ""]
        with patch("builtins.input", side_effect=inputs):
            captured_output = StringIO()
            sys.stdout = captured_output
            self.bank.input_transactions()
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            self.assertIn("Invalid date format", output)

    def test_input_transactions_invalid_type(self):
        # Invalid transaction type (should be either D or W).
        inputs = ["20230301 ACC001 X 1000", ""]
        with patch("builtins.input", side_effect=inputs):
            captured_output = StringIO()
            sys.stdout = captured_output
            self.bank.input_transactions()
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            self.assertIn("Invalid transaction type", output)

    def test_input_transactions_negative_amount(self):
        # Negative amount should be rejected.
        inputs = ["20230301 ACC001 D -500", ""]
        with patch("builtins.input", side_effect=inputs):
            captured_output = StringIO()
            sys.stdout = captured_output
            self.bank.input_transactions()
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            self.assertIn("Amount must be greater than zero", output)

    def test_input_transactions_first_withdrawal(self):
        # The first transaction for an account cannot be a withdrawal.
        inputs = ["20230301 ACC001 W 500", ""]
        with patch("builtins.input", side_effect=inputs):
            captured_output = StringIO()
            sys.stdout = captured_output
            self.bank.input_transactions()
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            self.assertIn("First transaction cannot be a withdrawal", output)

    def test_input_transactions_insufficient_funds(self):
        # Deposit a small amount and then attempt to withdraw more than the balance.
        inputs = ["20230301 ACC001 D 500", "20230302 ACC001 W 600", ""]
        with patch("builtins.input", side_effect=inputs):
            captured_output = StringIO()
            sys.stdout = captured_output
            self.bank.input_transactions()
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            self.assertIn("Insufficient funds", output)

    def test_input_transactions_multiple_same_day(self):
        # Two transactions on the same day should generate different transaction IDs.
        inputs = ["20230301 ACC001 D 1000", "20230301 ACC001 D 500", ""]
        with patch("builtins.input", side_effect=inputs):
            captured_output = StringIO()
            sys.stdout = captured_output
            self.bank.input_transactions()
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            self.assertIn("20230301-01", output)
            self.assertIn("20230301-02", output)

    # ----------------------------
    # Tests for print_monthly_statement
    # ----------------------------
    def test_print_monthly_statement_valid(self):
        # Preload an account with transactions and then generate a monthly statement.
        self.bank.accounts["ACC001"] = Account("ACC001")
        # Add a deposit and a withdrawal (assumed valid as per Account.add_transaction).
        self.bank.accounts["ACC001"].add_transaction("20230301", "ACC001", "D", "1000")
        self.bank.accounts["ACC001"].add_transaction("20230315", "ACC001", "W", "200")
        inputs = ["ACC001 202303", ""]
        with patch("builtins.input", side_effect=inputs):
            captured_output = StringIO()
            sys.stdout = captured_output
            self.bank.print_monthly_statement()
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            self.assertIn("Account: ACC001", output)
            # Check that the interest calculation row is present (row starts with date and "I" type)
            self.assertIn(" I    ", output)

    def test_print_monthly_statement_invalid_account(self):
        # Test statement generation for a non-existent account.
        inputs = ["abc 202303", ""]
        with patch("builtins.input", side_effect=inputs):
            captured_output = StringIO()
            sys.stdout = captured_output
            self.bank.print_monthly_statement()
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            self.assertIn("Account abc not found", output)

    # ----------------------------
    # Tests for input_interest
    # ----------------------------
    def test_input_interest_valid(self):
        # Valid interest rule input should add/update the interest rule list.
        inputs = ["20230301 RULE1 5", ""]
        with patch("builtins.input", side_effect=inputs):
            captured_output = StringIO()
            sys.stdout = captured_output
            self.bank.input_interest()
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            self.assertIn("Interest Rules", output)
            self.assertEqual(len(self.bank.interest_rules), 1)
            # Assuming the Interest class stores the rule id as an attribute named "ruleId"
            self.assertEqual(self.bank.interest_rules[0].ruleId, "RULE1")

    def test_input_interest_invalid_date(self):
        # Interest rule input with an invalid date format.
        inputs = ["2023-03-01 RULE1 5", ""]
        with patch("builtins.input", side_effect=inputs):
            captured_output = StringIO()
            sys.stdout = captured_output
            self.bank.input_interest()
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            self.assertIn("Invalid date format", output)

    def test_input_interest_invalid_rate(self):
        # Test various invalid rate inputs: rate not between 0 and 100 or non-numeric.
        inputs = ["20230301 RULE1 0", "20230301 RULE1 105", "20230301 RULE1 abc", ""]
        with patch("builtins.input", side_effect=inputs):
            captured_output = StringIO()
            sys.stdout = captured_output
            self.bank.input_interest()
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            self.assertIn("Rate must be between 0 and 100", output)
            self.assertIn("Invalid rate", output)
