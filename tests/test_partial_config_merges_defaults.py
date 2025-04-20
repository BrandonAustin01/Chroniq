import unittest
import tempfile
from pathlib import Path
from chroniq.config import load_config
from chroniq.defaults import DEFAULT_CONFIG
import tomli_w

class TestChroniqConfigLoader(unittest.TestCase):
    """
    Tests that partial .chroniq.toml files still apply all necessary default values.
    """

    def test_partial_config_merges_defaults(self):
        """
        Ensures missing config values are filled using DEFAULT_CONFIG.
        Useful when developers omit optional keys but still expect proper behavior.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / ".chroniq.toml"

            # 🚫 Only define 'active_profile', without any profile values
            partial_config = {
                "active_profile": "default"
                # Note: no [profile.default] section provided
            }

            # 💾 Write the partial config to a temp file
            with open(config_path, "wb") as f:
                f.write(tomli_w.dumps(partial_config).encode("utf-8"))

            # 🧪 Load the config using the fallback logic
            config, profile = load_config(path=config_path)

            # ✅ Validate that DEFAULT_CONFIG is used to fill in the gaps
            self.assertEqual(profile, "default")
            for key, expected in DEFAULT_CONFIG.items():
                self.assertEqual(config[key], expected, f"Missing or incorrect default for '{key}'")
