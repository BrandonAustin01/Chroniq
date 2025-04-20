import unittest
import tempfile
import shutil
from pathlib import Path
from click.testing import CliRunner

from chroniq.config import load_config
from chroniq.cli import main

class TestChroniqConfigSet(unittest.TestCase):
    """
    ✅ Tests for 'chroniq config set' to ensure values are correctly written to a custom config file.
    """

    def setUp(self):
        # 🧪 Create a temporary directory and config path for isolation
        self.tmpdir = tempfile.mkdtemp()
        self.config_path = Path(self.tmpdir) / ".chroniq.toml"

    def tearDown(self):
        # 🧼 Clean up the temp directory after test
        shutil.rmtree(self.tmpdir)

    def test_set_config_value(self):
        """
        🧪 Verifies that setting a config key writes it properly to the .chroniq.toml file.
        """
        runner = CliRunner()

        # ⚙️ Use --config flag to direct the CLI to our isolated config path
        result = runner.invoke(
            main,
            ["--config", str(self.config_path), "config", "set", "silent", "true"]
        )

        # ✅ CLI should succeed with exit code 0
        self.assertEqual(result.exit_code, 0, msg=f"Command failed: {result.output}")

        # 📖 Verify that 'silent' is saved and True
        config_data, _ = load_config(self.config_path)
        self.assertIn("silent", config_data)
        self.assertTrue(config_data["silent"])
