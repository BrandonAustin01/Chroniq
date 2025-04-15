# tests/test_config_override_precedence.py

import unittest
import tempfile
import json
import os
from pathlib import Path
from unittest.mock import patch
from chroniq.config import load_config


class TestConfigFallback:
    def test_falls_back_to_json_if_toml_missing(self, tmp_path):
        """
        If .chroniq.toml is missing, the config loader should fall back to .chroniqrc.json.
        """

        # Setup: create a mock JSON config file in the temporary directory
        json_path = tmp_path / ".chroniqrc.json"
        json_config = {"silent": True, "default_bump": "minor"}
        json_path.write_text(json.dumps(json_config), encoding="utf-8")

        # Change working directory to simulate being inside a project folder
        original_cwd = Path.cwd()
        try:
            # Temporarily switch into tmp_path so the config loader finds our fake files
            Path.chdir(tmp_path)

            # When TOML is missing, JSON config should be loaded
            config = load_config()
            assert config.get("silent") is True
            assert config.get("default_bump") == "minor"
        finally:
            Path.chdir(original_cwd)

    def test_prefers_toml_when_available(self, tmp_path):
        """
        When both .chroniq.toml and .chroniqrc.json exist, .chroniq.toml should take priority.
        This test creates both files and verifies that the TOML config is the one loaded.
        """

        # Define paths to config files in temporary test directory
        toml_path = tmp_path / ".chroniq.toml"
        json_path = tmp_path / ".chroniqrc.json"

        # Write TOML config as plain string (no tomli_w needed)
        toml_path.write_text("[settings]\nsilent = false\ndefault_bump = 'patch'\n", encoding="utf-8")

        # Write JSON config that should be ignored if TOML is present
        json_config = {"silent": True, "default_bump": "major"}
        json_path.write_text(json.dumps(json_config), encoding="utf-8")

        # Save current working directory so we can return to it
        original_cwd = Path.cwd()
        try:
            # Change to the temp test directory
            os.chdir(tmp_path)

            # Load config using the Chroniq logic
            config = load_config()

            # Assert TOML values were loaded (not JSON fallback)
            assert config.get("silent") is False
            assert config.get("default_bump") == "patch"
        finally:
            # Always restore original directory to avoid side effects
            os.chdir(original_cwd)

