import unittest
import tempfile
import click
from pathlib import Path
from click.testing import CliRunner
from chroniq.cli import main
import tomli_w
import tomllib

class TestChroniqConfigDelete(unittest.TestCase):
    """
    Verifies config delete removes global keys properly.
    """

    def test_delete_global_key(self):
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / ".chroniq.toml"

            # 🧱 Write a test config file
            test_config = {
                "silent": True,
                "strict": False
            }

            with open(config_path, "wb") as f:
                f.write(tomli_w.dumps(test_config).encode("utf-8"))

            # 🚀 Run CLI with --yes to confirm and --config to target path
            result = runner.invoke(
                main,
                ["--config", str(config_path), "config", "delete", "silent", "--yes"],
                catch_exceptions=False
            )

            # ✅ Check CLI output and exit code
            self.assertEqual(result.exit_code, 0, msg=f"Command failed: {result.output}")
            self.assertIn("🗑️ Deleted silent", result.output)

            # 🧪 Confirm 'silent' was removed from the config file
            with open(config_path, "rb") as f:
                updated_config = tomllib.load(f)

            self.assertNotIn("silent", updated_config)
            self.assertIn("strict", updated_config)  # Still there
