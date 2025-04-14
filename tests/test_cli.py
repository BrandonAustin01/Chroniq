### tests/test_cli.py

import tempfile
from pathlib import Path
from click.testing import CliRunner
from chroniq import cli
from chroniq.core import SemVer


def test_init_creates_files():
    """
    Test that `chroniq init` creates version.txt and CHANGELOG.md.
    """
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        with runner.isolated_filesystem(temp_dir=tmpdir):
            result = runner.invoke(cli.main, ["init"])
            assert Path("version.txt").exists(), "version.txt not created"
            assert Path("CHANGELOG.md").exists(), "CHANGELOG.md not created"
            assert result.exit_code == 0


def test_version_command():
    """
    Test that `chroniq version` prints the current version.
    """
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        with runner.isolated_filesystem(temp_dir=tmpdir):
            SemVer(9, 9, 9).save(Path("version.txt"))  # Save inside isolated FS
            result = runner.invoke(cli.main, ["version"])
            assert "9.9.9" in result.output, "Incorrect version printed"
            assert result.exit_code == 0



def test_bump_patch_updates_version():
    """
    Test `chroniq bump patch` updates version correctly.
    """
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        with runner.isolated_filesystem(temp_dir=tmpdir):
            SemVer(1, 0, 0).save()
            result = runner.invoke(cli.main, ["bump", "patch"], input="n\n")
            assert Path("version.txt").read_text().strip() == "1.0.1"
            assert result.exit_code == 0


def test_bump_with_changelog_entry():
    """
    Test `chroniq bump` with changelog entry prompt.
    """
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        with runner.isolated_filesystem(temp_dir=tmpdir):
            changelog_path = Path("CHANGELOG.md")
            version_path = Path("version.txt")

            # Patch changelog module to use test file path
            import chroniq.changelog as changelog
            changelog.CHANGELOG_FILE = changelog_path

            # Setup baseline
            runner.invoke(cli.main, ["init"])
            SemVer(2, 0, 0).save(version_path)

            result = runner.invoke(
                cli.main,
                ["bump", "minor"],
                input="y\nAdded something cool\n"
            )

            content = changelog_path.read_text()
            assert "Added something cool" in content, "Expected changelog entry not found."
            assert "2.1.0" in version_path.read_text()
            assert result.exit_code == 0





def test_log_reads_changelog():
    """
    Test `chroniq log` shows entries from the changelog.
    """
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmpdir:
        with runner.isolated_filesystem(temp_dir=tmpdir):
            Path("CHANGELOG.md").write_text("## [1.0.0] - 2025-04-13\n- First entry\n")
            result = runner.invoke(cli.main, ["log", "--lines", "2"])
            assert "First entry" in result.output
            assert result.exit_code == 0