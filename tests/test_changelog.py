### tests/test_changelog.py

import tempfile
from pathlib import Path
from chroniq import changelog


def test_add_entry_creates_file():
    """
    Test that a changelog entry creates the file if it doesn't exist.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_path = Path(tmpdir) / "CHANGELOG.md"
        changelog.CHANGELOG_FILE = temp_path

        changelog.add_entry("1.0.0", "Initial release")

        assert temp_path.exists(), "Changelog file was not created."
        content = temp_path.read_text()
        assert "Initial release" in content, "Changelog content missing."


def test_add_entry_appends_correctly():
    """
    Test that multiple changelog entries are appended properly.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_path = Path(tmpdir) / "CHANGELOG.md"
        changelog.CHANGELOG_FILE = temp_path

        changelog.add_entry("1.0.0", "First entry")
        changelog.add_entry("1.1.0", "Second entry")

        content = temp_path.read_text()
        assert "First entry" in content
        assert "Second entry" in content
        assert content.count("## [") >= 2, "Expected multiple version headers."


def test_add_entry_ignores_blank():
    """
    Test that blank changelog messages do not write anything.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_path = Path(tmpdir) / "CHANGELOG.md"
        changelog.CHANGELOG_FILE = temp_path

        changelog.add_entry("1.0.0", "")
        assert not temp_path.exists(), "Empty changelog entry should not create file."


def test_get_recent_entries():
    """
    Test that get_recent_entries returns the expected number of non-empty lines.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_path = Path(tmpdir) / "CHANGELOG.md"
        changelog.CHANGELOG_FILE = temp_path

        changelog.add_entry("1.0.0", "One")
        changelog.add_entry("1.1.0", "Two")
        changelog.add_entry("1.2.0", "Three")

        recent = changelog.get_recent_entries(limit=6)
        assert any("Two" in line for line in recent)
        assert any("Three" in line for line in recent)




def test_get_recent_entries_empty_file():
    """
    Test get_recent_entries handles empty changelog file gracefully.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_path = Path(tmpdir) / "CHANGELOG.md"
        temp_path.touch()  # Create empty file
        changelog.CHANGELOG_FILE = temp_path

        recent = changelog.get_recent_entries()
        assert recent == [], "Expected empty list from empty changelog."
