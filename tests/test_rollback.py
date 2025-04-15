import unittest
from pathlib import Path
from chroniq.core import perform_rollback as rollback  # ✅ use pure function, not CLI

class TestRollback(unittest.TestCase):
    """
    ✅ Pro Mode Rollback Tests

    These tests validate version.txt restoration and changelog rollback behavior.
    Each test runs in isolation and cleans up test artifacts after execution.
    """

    def setUp(self):
        """Create fresh version, backup, and changelog files before each test."""
        self.version_file = Path("version.txt")
        self.backup_file = Path(".version.bak")
        self.changelog_file = Path("CHANGELOG.md")

        # Write test content
        self.version_file.write_text("1.2.3\n")
        self.backup_file.write_text("1.2.2\n")

        self.changelog_file.write_text(
            "# Changelog\n\n"
            "## [1.2.3] - 2025-04-16\n"
            "- New feature A\n"
            "- Bug fix B\n\n"
            "## [1.2.2] - 2025-04-10\n"
            "- Older stuff\n"
        )

    def tearDown(self):
        """Clean up version and changelog files after each test."""
        for f in [self.version_file, self.backup_file, self.changelog_file]:
            if f.exists():
                f.unlink()

    def test_version_rollback_from_backup(self):
        """Ensure version.txt is correctly restored from .version.bak."""
        rollback(rollback_version=False, yes=True)
        restored = self.version_file.read_text().strip()
        self.assertEqual(restored, "1.2.2")

    def test_changelog_section_is_removed(self):
        """Ensure most recent changelog block is removed correctly."""
        rollback(rollback_version=False, yes=True)
        content = self.changelog_file.read_text()
        self.assertNotIn("## [1.2.3]", content)
        self.assertIn("## [1.2.2]", content)

    def test_skips_changelog_when_version_only(self):
        """Ensure changelog remains untouched when using --version only."""
        rollback(rollback_version=True, yes=True)
        content = self.changelog_file.read_text()
        self.assertIn("## [1.2.3]", content)
        self.assertIn("## [1.2.2]", content)

    def test_no_backup_file_aborts_gracefully(self):
        """Ensure rollback exits if .version.bak is missing."""
        self.backup_file.unlink()
        rollback(rollback_version=True, yes=True)
        current = self.version_file.read_text().strip()
        self.assertEqual(current, "1.2.3")

    def test_no_changelog_file_does_not_crash(self):
        """Ensure rollback skips changelog logic cleanly if file is missing."""
        self.changelog_file.unlink()
        rollback(rollback_version=False, yes=True)
        current = self.version_file.read_text().strip()
        self.assertEqual(current, "1.2.2")
