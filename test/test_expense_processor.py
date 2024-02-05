import unittest
from unittest.mock import patch
from main import load_config_from_env_or_cli, adjust_cost_and_shares, create_expense
import argparse


class TestExpenseProcessor(unittest.TestCase):

    def test_load_config_from_env_or_cli(self):
        # Test loading config from environment variables
        with patch('main.os.getenv') as mock_getenv:
            mock_getenv.side_effect = lambda key: {
                "CONSUMER_KEY": "mock_consumer_key",
                "CONSUMER_SECRET": "mock_consumer_secret",
                "API_KEY": "mock_api_key",
                "GROUP_ID": "mock_group_id"
            }.get(key)
            args = argparse.Namespace(
                consumer_key=None,
                consumer_secret=None,
                api_key=None,
                group_id=None,
                user_ids=[],
                user_shares=[]
            )
            config = load_config_from_env_or_cli(args)
            self.assertEqual(config["CONSUMER_KEY"], "mock_consumer_key")
            self.assertEqual(config["CONSUMER_SECRET"], "mock_consumer_secret")
            self.assertEqual(config["API_KEY"], "mock_api_key")
            self.assertEqual(config["GROUP_ID"], "mock_group_id")

        # Test overriding config with CLI arguments
        args = argparse.Namespace(
            consumer_key="cli_consumer_key",
            consumer_secret="cli_consumer_secret",
            api_key="cli_api_key",
            group_id="cli_group_id",
            user_ids=[],
            user_shares=[]
        )
        config = load_config_from_env_or_cli(args)
        self.assertEqual(config["CONSUMER_KEY"], "cli_consumer_key")
        self.assertEqual(config["CONSUMER_SECRET"], "cli_consumer_secret")
        self.assertEqual(config["API_KEY"], "cli_api_key")
        self.assertEqual(config["GROUP_ID"], "cli_group_id")

    def test_adjust_cost_and_shares(self):
        cost = 100.0
        user_shares = {"1": 30, "2": 70}
        adjusted_cost, owed_shares = adjust_cost_and_shares(cost, user_shares)
        self.assertEqual(adjusted_cost, 100.0)  # No rounding needed
        self.assertEqual(owed_shares, {"1": 30.0, "2": 70.0})  # No rounding needed

        cost = 100.01
        user_shares = {"1": 30, "2": 70}
        adjusted_cost, owed_shares = adjust_cost_and_shares(cost, user_shares)
        self.assertEqual(adjusted_cost, 100.01)  # No rounding needed
        self.assertEqual(owed_shares, {"1": 30.0, "2": 70.01})  # Rounding needed

    def test_create_expense(self):
        cost = 100.0
        description = "Test Expense"
        date = "2022-01-01"
        config = {
            "GROUP_ID": "mock_group_id",
            "USERS": {"1": 30, "2": 70}
        }
        expense = create_expense(cost, description, date, config)
        self.assertEqual(expense.getCost(), "100.0")
        self.assertEqual(expense.getDescription(), "Test Expense")
        self.assertEqual(expense.getDate(), "2022-01-01")
        self.assertEqual(expense.getGroupId(), "mock_group_id")
        users = expense.getUsers()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].getId(), 1)
        self.assertEqual(users[0].getOwedShare(), "30.0")
        self.assertEqual(users[0].getPaidShare(), "100.0")
        self.assertEqual(users[1].getId(), 2)
        self.assertEqual(users[1].getOwedShare(), "70.0")


if __name__ == '__main__':
    unittest.main()
