import unittest
from chroniq.config import get_config_value

class TestConfigFallbacks(unittest.TestCase):

    def test_fallback_to_default(self):
        # Simulate an empty config (no profiles, no keys)
        empty_config = {}

        # Get a key that should fallback to defaults.py
        result = get_config_value("emoji_fallback", empty_config, profile="default")

        self.assertIsNotNone(result)
        self.assertEqual(result["value"], True)  # ✅ Based on your defaults.py
        self.assertEqual(result["origin"], "default")

    def test_missing_key_returns_none(self):
        empty_config = {}
        result = get_config_value("nonexistent_key", empty_config, profile="default")

        self.assertIsNone(result)
