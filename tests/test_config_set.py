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
    from click.testing import CliRunner
    from chroniq.cli import main
    from chroniq.config import load_config

    runner = CliRunner()

    # 🚫 Wipe the test config file before setting any values
    if self.config_path.exists():
        self.config_path.unlink()

    # ⚙️ Run the CLI command to set 'silent = true'
    result = runner.invoke(
        main,
        ["--config", str(self.config_path), "config", "set", "--key", "silent", "--value", "true"]
    )

    # ✅ Ensure the CLI ran without error
    self.assertEqual(result.exit_code, 0, msg=f"Command failed: {result.output}")

    # 📖 Load the resulting config
    config_data, _ = load_config(path=self.config_path)

    # ✅ Confirm the silent key is True and not overridden
    self.assertIn("silent", config_data, "Expected 'silent' key to be present")
    self.assertTrue(config_data["silent"], "Expected 'silent' to be truthy")








