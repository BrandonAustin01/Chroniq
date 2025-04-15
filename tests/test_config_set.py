import unittest
import tempfile
from pathlib import Path
from chroniq.config import load_config, update_config_value

class TestChroniqConfigSet(unittest.TestCase):

    def test_set_config_value(self):
        """Test setting and saving configuration values."""

        # Create a temporary directory to simulate the config file path
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / ".chroniq.toml"

            # Simulate writing the .chroniq.toml file with initial data (fixed indentation)
            config_data = """
default_bump = "patch"
silent = false
"""
            with open(config_path, "w") as f:
                f.write(config_data)
            
            # Set the 'silent' value to 'true'
            update_config_value("silent", "true", config_path)

            # Reload the config to check if the change persisted
            config = load_config(config_path)

            # Assert that the 'silent' value has been updated correctly
            self.assertEqual(config["silent"], True)
