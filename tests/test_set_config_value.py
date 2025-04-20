import unittest
import tempfile
from pathlib import Path
from click.testing import CliRunner
from chroniq.cli import main
from chroniq.config import load_config

class TestChroniqConfigSet(unittest.TestCase):
    """
    🧪 Verifies that setting a config key writes it properly to the .chroniq.toml file.
    """

    def test_set_config_value(self):
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / ".chroniq.toml"

            result = runner.invoke(
                main,
                ["--config", str(config_path), "config", "set", "--key", "silent", "--value", "true"]
            )

            self.assertEqual(result.exit_code, 0, msg=f"Command failed: {result.output}")

            config_data, _ = load_config(config_path)
            self.assertIn("silent", config_data)
            self.assertTrue(config_data["silent"])
