import unittest
import tempfile
from pathlib import Path
from chroniq.config import load_config
from chroniq.defaults import DEFAULT_CONFIG
import tomli_w

class TestChroniqConfigLoader(unittest.TestCase):
    """
    Tests for loading .chroniq.toml and applying profile merging logic.
    """

    def test_loads_toml_and_applies_profile(self):
        """
        Verifies that the loader merges profile values with base defaults
        and respects the active profile (e.g., [profile.dev]).
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / ".chroniq.toml"

            # 🔧 Define a config with an active profile and profile-specific override
            test_config = {
                "active_profile": "dev",
                "profile": {
                    "dev": {
                        "default_bump": "major",
                        "emoji_fallback": True
                    }
                }
            }

            # 📝 Write config to the temporary file
            with open(config_path, "wb") as f:
                f.write(tomli_w.dumps(test_config).encode("utf-8"))

            # 🧪 Run loader with path override
            config, profile = load_config(path=config_path)

            # ✅ Ensure the active profile is applied and merged
            self.assertEqual(profile, "dev")
            self.assertEqual(config["default_bump"], "major")
            self.assertEqual(config["emoji_fallback"], True)
            self.assertEqual(config["silent"], DEFAULT_CONFIG["silent"])  # fallback

