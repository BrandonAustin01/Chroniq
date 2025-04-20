import unittest
import tempfile
from pathlib import Path
from chroniq.config import load_config
from chroniq.defaults import DEFAULT_CONFIG  # ← live default import

class TestChroniqConfigLoader(unittest.TestCase):

    def test_fallback_when_missing(self):
        """
        ✅ Should return DEFAULT_CONFIG if the config file doesn't exist.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_path = Path(tmpdir) / ".no_config.toml"

            # Load config using a path we know doesn't exist
            config, profile = load_config(path=fake_path)

            # ✅ Assert fallback values match DEFAULT_CONFIG
            for key, expected_val in DEFAULT_CONFIG.items():
                actual_val = config.get(key)
                self.assertEqual(
                    actual_val,
                    expected_val,
                    f"Mismatch on fallback key: {key} → expected {expected_val}, got {actual_val}"
                )

            # ✅ Assert fallback profile is returned
            self.assertEqual(profile, "default")

    def test_loads_toml_and_applies_profile(self):
        """
        🧪 Loads .chroniq.toml with [profile.dev] and merges it properly.
        """
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / ".chroniq.toml"

            EXAMPLE_TOML = """
            silent = true
            strict = true
            emoji_fallback = false
            changelog_file = "logs/CHANGELOG.md"
            version_file = "meta/version.txt"
            active_profile = "dev"

            [profile.dev]
            default_bump = "major"
            silent = false
            """

            config_path.write_text(EXAMPLE_TOML.strip(), encoding="utf-8")
            config, profile = load_config(config_path)

            # 🧪 Values overridden by [profile.dev]
            self.assertEqual(config["default_bump"], "major")
            self.assertEqual(config["silent"], False)

            # ✅ Values from global section
            self.assertEqual(config["strict"], True)
            self.assertEqual(config["emoji_fallback"], False)
            self.assertEqual(config["changelog_file"], "logs/CHANGELOG.md")
            self.assertEqual(config["version_file"], "meta/version.txt")

            # ✅ Profile returned correctly
            self.assertEqual(profile, "dev")

    def test_partial_config_merges_defaults(self):
        """
        Partial config files still apply default fallbacks.
        """
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / ".chroniq.toml"
            config_path.write_text('default_bump = "minor"\n', encoding="utf-8")

            config, _ = load_config(config_path)
            self.assertEqual(config["default_bump"], "minor")
            self.assertEqual(config["silent"], DEFAULT_CONFIG["silent"])
            self.assertEqual(config["strict"], DEFAULT_CONFIG["strict"])

if __name__ == "__main__":
    unittest.main()
