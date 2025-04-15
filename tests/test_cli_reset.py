# tests/test_cli_reset.py

import os
import shutil
from pathlib import Path
from click.testing import CliRunner
from chroniq.cli import main

# Create a runner for invoking CLI commands
runner = CliRunner()

# Paths used by Chroniq CLI for versioning
VERSION_FILE = Path("version.txt")
CHANGELOG_FILE = Path("CHANGELOG.md")

def test_cli_reset_command_creates_and_removes_files():
    """
    This test verifies that the 'chroniq reset' command:
    1. Creates version.txt and CHANGELOG.md via `init`
    2. Deletes both files when `reset` is run
    """

    # Setup: Ensure clean state
    if VERSION_FILE.exists():
        VERSION_FILE.unlink()
    if CHANGELOG_FILE.exists():
        CHANGELOG_FILE.unlink()

    # Step 1: Run init to create the files
    result_init = runner.invoke(main, ["init"])
    assert result_init.exit_code == 0
    assert VERSION_FILE.exists()
    assert CHANGELOG_FILE.exists()

    # Step 2: Run reset to delete the files
    result_reset = runner.invoke(main, ["reset"])
    assert result_reset.exit_code == 0
    assert not VERSION_FILE.exists()
    assert not CHANGELOG_FILE.exists()

    # Cleanup: Not needed — files should be deleted
