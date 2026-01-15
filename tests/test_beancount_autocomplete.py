import sys
import os
import unittest
import tempfile
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path to import the plugin
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock sublime and sublime_plugin modules before importing the plugin
sublime_mock = MagicMock()
sublime_plugin_mock = MagicMock()

# Create a proper EventListener base class mock
class EventListenerMock:
    pass

sublime_plugin_mock.EventListener = EventListenerMock

sys.modules['sublime'] = sublime_mock
sys.modules['sublime_plugin'] = sublime_plugin_mock

from beancount_autocomplete import BeancountAutocompleteListener


class TestBeancountAutocompleteListener(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.listener = BeancountAutocompleteListener()
        self.test_beancount_content = """
2020-01-01 open Assets:Bank:Checking
2020-01-01 open Assets:Bank:Savings
2020-01-01 open Expenses:Food:Groceries
2020-01-01 open Expenses:Food:Restaurants
2020-01-01 open Expenses:Transport:Public
2020-01-01 open Income:Salary
2020-01-01 open Liabilities:CreditCard

2020-01-15 * "Grocery Shopping"
  Expenses:Food:Groceries  50.00 USD
  Assets:Bank:Checking
"""

    def test_account_pattern_matching(self):
        """Test that the regex pattern correctly matches account names."""
        import re
        account_pattern = re.compile(r'(?:[A-Z][A-Za-z0-9-]+)(?::[A-Z][A-Za-z0-9-]+)+')

        # Valid account names
        valid_accounts = [
            "Assets:Bank:Checking",
            "Expenses:Food:Groceries",
            "Income:Salary",
            "Liabilities:Credit-Card"
        ]

        for account in valid_accounts:
            match = account_pattern.search(account)
            self.assertIsNotNone(match, f"Should match valid account: {account}")
            self.assertEqual(match.group(), account)

        # Invalid account names (shouldn't match or should match differently)
        invalid_accounts = [
            "assets:bank",  # lowercase start
            "Assets",  # no colon separator
            "Assets:bank",  # lowercase segment
        ]

        # These should either not match or not match the full string correctly
        for account in invalid_accounts:
            match = account_pattern.search(account)
            if match:
                self.assertNotEqual(match.group(), account,
                    f"Should not fully match invalid account: {account}")

    def test_load_accounts_with_valid_file(self):
        """Test loading accounts from a valid Beancount file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.beancount', delete=False) as f:
            f.write(self.test_beancount_content)
            temp_file = f.name

        try:
            # Mock the settings
            mock_settings = Mock()
            mock_settings.get.return_value = temp_file

            with patch.object(self.listener, 'get_settings', return_value=mock_settings):
                accounts = self.listener.load_accounts()

            # Check that accounts were loaded
            self.assertGreater(len(accounts), 0, "Should load at least one account")

            # Check specific accounts
            expected_accounts = [
                "Assets:Bank:Checking",
                "Assets:Bank:Savings",
                "Expenses:Food:Groceries",
                "Expenses:Food:Restaurants",
                "Expenses:Transport:Public",
                "Income:Salary",
                "Liabilities:CreditCard"
            ]

            for account in expected_accounts:
                self.assertIn(account, accounts, f"Should contain account: {account}")

            # Check that accounts are sorted
            self.assertEqual(accounts, sorted(accounts), "Accounts should be sorted")

        finally:
            os.unlink(temp_file)

    def test_load_accounts_with_missing_file(self):
        """Test that missing file returns empty list."""
        mock_settings = Mock()
        mock_settings.get.return_value = "/nonexistent/path/to/file.beancount"

        with patch.object(self.listener, 'get_settings', return_value=mock_settings):
            accounts = self.listener.load_accounts()

        self.assertEqual(accounts, [], "Should return empty list for missing file")

    def test_load_accounts_with_no_path_configured(self):
        """Test that no configured path returns empty list."""
        mock_settings = Mock()
        mock_settings.get.return_value = None

        with patch.object(self.listener, 'get_settings', return_value=mock_settings):
            accounts = self.listener.load_accounts()

        self.assertEqual(accounts, [], "Should return empty list when no path configured")

    def test_caching_behavior(self):
        """Test that accounts are cached and only reloaded when file changes."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.beancount', delete=False) as f:
            f.write(self.test_beancount_content)
            temp_file = f.name

        try:
            mock_settings = Mock()
            mock_settings.get.return_value = temp_file

            with patch.object(self.listener, 'get_settings', return_value=mock_settings):
                # First load
                accounts1 = self.listener.load_accounts()
                initial_cache = self.listener.accounts_cache.copy()
                initial_time = self.listener.last_load_time

                # Second load without file modification should use cache
                accounts2 = self.listener.load_accounts()

                self.assertEqual(accounts1, accounts2, "Should return same accounts")
                self.assertEqual(initial_time, self.listener.last_load_time,
                    "Should not reload file if not modified")
                self.assertIs(accounts2, self.listener.accounts_cache,
                    "Should return cached list")

        finally:
            os.unlink(temp_file)

    def test_on_query_completions_with_prefix(self):
        """Test that completions are filtered by prefix."""
        # Set up cached accounts
        self.listener.accounts_cache = [
            "Assets:Bank:Checking",
            "Assets:Bank:Savings",
            "Expenses:Food:Groceries",
            "Income:Salary"
        ]
        self.listener.last_load_time = 1

        # Mock settings to prevent file loading
        mock_settings = Mock()
        mock_settings.get.return_value = None

        with patch.object(self.listener, 'load_accounts', return_value=self.listener.accounts_cache):
            # Test with "Assets" prefix
            mock_view = Mock()
            completions, flags = self.listener.on_query_completions(
                mock_view, "Assets", [0]
            )

            completion_accounts = [c[1] for c in completions]
            self.assertEqual(len(completion_accounts), 2, "Should return 2 Assets accounts")
            self.assertIn("Assets:Bank:Checking", completion_accounts)
            self.assertIn("Assets:Bank:Savings", completion_accounts)

            # Test with "Expenses" prefix
            completions, flags = self.listener.on_query_completions(
                mock_view, "Expenses", [0]
            )

            completion_accounts = [c[1] for c in completions]
            self.assertEqual(len(completion_accounts), 1, "Should return 1 Expenses account")
            self.assertIn("Expenses:Food:Groceries", completion_accounts)

    def test_on_query_completions_case_insensitive(self):
        """Test that prefix matching is case insensitive."""
        self.listener.accounts_cache = ["Assets:Bank:Checking"]
        self.listener.last_load_time = 1

        with patch.object(self.listener, 'load_accounts', return_value=self.listener.accounts_cache):
            mock_view = Mock()

            # Test lowercase prefix
            completions, _ = self.listener.on_query_completions(
                mock_view, "assets", [0]
            )
            self.assertEqual(len(completions), 1, "Should match case insensitively")

            # Test mixed case prefix
            completions, _ = self.listener.on_query_completions(
                mock_view, "AsSeTs", [0]
            )
            self.assertEqual(len(completions), 1, "Should match case insensitively")


if __name__ == '__main__':
    unittest.main()
