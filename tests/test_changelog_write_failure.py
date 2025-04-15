import unittest
from unittest.mock import patch, mock_open
from chroniq.changelog import add_entry

class TestChangelogWriteError(unittest.TestCase):
    """
    Simulates a write failure when updating the changelog.
    Ensures errors are caught and logged gracefully.
    """

    @patch("chroniq.changelog.ensure_changelog_exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_changelog_write_failure(self, mock_file, mock_ensure):
        """
        Mocks a permission error on file write to test error handling.
        """
        # Simulate permission denied when opening the changelog
        mock_file.side_effect = PermissionError("Mocked permission denied.")

        # Should not raise an exception despite the error
        try:
            add_entry("1.2.3", "This is a test entry.")
        except Exception as e:
            self.fail(f"add_entry() raised an unexpected exception: {e}")

if __name__ == "__main__":
    unittest.main()
