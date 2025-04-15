import unittest
import tempfile
from pathlib import Path

from chroniq.config import load_config, DEFAULT_CONFIG

class TestChroniqConfigLoader(unittest.TestCase):

    def test_fallback_when_missing(self):
        """Returns default config when .chroniq.toml doesn't exist."""
        config = load_config(Path("nonexistent.toml"))
        self.assertEqual(config, DEFAULT_CONFIG)

    def test_loads_toml_and_applies_profile(self):
        """Loads .chroniq.toml with [profile.dev] and merges it properly."""
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / ".chroniq.toml"

            # Write TOML using standard string, then encode as UTF-8
            EXAMPLE_TOML = """
            silent = true
            strict = true
            emoji_fallback = false
            changelog_path = "logs/CHANGELOG.md"
            version_path = "meta/version.txt"
            active_profile = "dev"

            [profile.dev]
            default_bump = "major"
            silent = false
            """
            config_path.write_text(EXAMPLE_TOML.strip(), encoding="utf-8")

            config = load_config(config_path)

            # ✅ From [profile.dev] override
            self.assertEqual(config["default_bump"], "major")
            self.assertEqual(config["silent"], False)

            # ✅ From base-level keys
            self.assertEqual(config["strict"], True)
            self.assertEqual(config["emoji_fallback"], False)
            self.assertEqual(config["changelog_path"], "logs/CHANGELOG.md")
            self.assertEqual(config["version_path"], "meta/version.txt")
            self.assertEqual(config["active_profile"], "dev")  # <- correct usage


    def test_partial_config_merges_defaults(self):
        """Partial config files still apply default fallbacks."""
        with tempfile.TemporaryDirectory() as tmp:
            partial_toml = b'default_bump = "minor"\n'
            config_path = Path(tmp) / ".chroniq.toml"
            config_path.write_bytes(partial_toml)

            config = load_config(config_path)
            self.assertEqual(config["default_bump"], "minor")
            self.assertEqual(config["silent"], False)  # fallback
            self.assertEqual(config["strict"], False)  # fallback

if __name__ == "__main__":
    unittest.main()
