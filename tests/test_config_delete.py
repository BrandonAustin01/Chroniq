import unittest
from pathlib import Path
from click.testing import CliRunner
from chroniq.cli import config_delete, main
from chroniq.config import CONFIG_PATH
from rich.console import Console
import tempfile
import os
import tomli_w
import tomllib
from unittest.mock import patch
from io import StringIO


class TestChroniqConfigDelete(unittest.TestCase):
    def setUp(self):
        # Create a temporary .chroniq.toml file with global and profile values
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.temp_dir.name, ".chroniq.toml")
        self.test_config = {
            "silent": True,
            "profile": {
                "dev": {
                    "silent": True,
                    "emoji_fallback": False
                }
            }
        }

        with open(self.config_path, "wb") as f:
            f.write(tomli_w.dumps(self.test_config).encode("utf-8"))

        # Patch CONFIG_PATH to use our temp config
        self.config_patch = patch("chroniq.config.CONFIG_PATH", new=self.config_path)
        self.config_patch.start()

    def tearDown(self):
        self.config_patch.stop()
        self.temp_dir.cleanup()

    @patch("chroniq.cli.console", new=Console(file=StringIO()))
    def test_delete_global_key(self):
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / ".chroniq.toml"

            # 🧩 Write a basic config with 'silent' key
            config = {"silent": True}
            with open(config_path, "wb") as f:
                f.write(tomli_w.dumps(config).encode("utf-8"))

            # 🚀 Run delete with --config and --yes to skip prompt
            result = runner.invoke(
                main,
                ["--config", str(config_path), "config", "delete", "silent", "--yes"]
            )

            # ✅ Confirm exit was successful
            self.assertEqual(result.exit_code, 0, msg=f"Command failed: {result.output}")

            # ✅ Patch: Check the config file, not CLI output
            with open(config_path, "rb") as f:
                updated = tomllib.load(f)
            self.assertNotIn("silent", updated)
