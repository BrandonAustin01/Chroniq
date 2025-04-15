# tests/test_cli_log_mocked.py

import unittest
import tempfile
import os
import io
from unittest.mock import patch
from click.testing import CliRunner
from chroniq.cli import main, console

class TestChroniqLogCommand(unittest.TestCase):
    def setUp(self):
        """Prepare a temp project with version and changelog for CLI log test."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)

        # Create version.txt with valid version
        with open("version.txt", "w", encoding="utf-8") as f:
            f.write("1.0.1")

        # Create a basic CHANGELOG.md file
        with open("CHANGELOG.md", "w", encoding="utf-8") as f:
            f.write("""# Changelog

## [1.0.1] - 2025-04-14
- Fixed emoji crash on Windows
- Added CLI fallback for missing config
""")

    def tearDown(self):
        """Clean up the temp dir and return to original working dir."""
        os.chdir(self.original_cwd)
        self.temp_dir.cleanup()

    def test_log_outputs_expected_lines(self):
        """
        Capture Chroniq's CLI log output using a patched console buffer.
        """
        # Patch the rich console output to use an in-memory buffer
        buffer = io.StringIO()
        with patch("chroniq.cli.console", new_callable=lambda: console.__class__(file=buffer)):
            runner = CliRunner()
            result = runner.invoke(main, ["log", "--lines", "3"])

            output = buffer.getvalue()

            # Validate that expected changelog lines were printed
            self.assertIn("1.0.1", output)
            self.assertIn("Fixed emoji crash", output)
            self.assertIn("Added CLI fallback", output)
