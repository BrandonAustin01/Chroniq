### tests/test_config.py

import tempfile
from pathlib import Path
from chroniq import config


def test_loads_valid_toml():
    """
    Test that a valid .chroniq.toml with [settings] is loaded correctly.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        toml_path = Path(tmpdir) / ".chroniq.toml"
        toml_path.write_text("""
[settings]
default_bump = "minor"
silent = true
""")

        config.TOML_PATH = toml_path  # Override default path
        result = config.load_config()

        assert result["default_bump"] == "minor"
        assert result["silent"] is True


def test_loads_valid_json():
    """
    Test that a valid .chroniqrc.json is loaded when no TOML is present.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        json_path = Path(tmpdir) / ".chroniqrc.json"
        json_path.write_text('{"default_bump": "major", "silent": false}')

        config.TOML_PATH = Path(tmpdir) / "not_used.toml"  # Skip TOML
        config.JSON_PATH = json_path
        result = config.load_config()

        assert result["default_bump"] == "major"
        assert result["silent"] is False


def test_missing_config_returns_empty_dict():
    """
    Test that no config file returns an empty dictionary.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        config.TOML_PATH = Path(tmpdir) / "none.toml"
        config.JSON_PATH = Path(tmpdir) / "none.json"
        result = config.load_config()
        assert result == {}, "Expected empty config when no file exists"


def test_bad_toml_prints_error():
    """
    Test that malformed TOML file does not crash and prints error.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        toml_path = Path(tmpdir) / ".chroniq.toml"
        toml_path.write_text("not: valid: toml:::\n")

        config.TOML_PATH = toml_path
        result = config.load_config()

        assert isinstance(result, dict), "Should still return a dict even if broken"


def test_bad_json_prints_error():
    """
    Test that malformed JSON file does not crash and prints error.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        json_path = Path(tmpdir) / ".chroniqrc.json"
        json_path.write_text('{ not valid json')

        config.TOML_PATH = Path(tmpdir) / "skip.toml"
        config.JSON_PATH = json_path
        result = config.load_config()

        assert isinstance(result, dict), "Should still return a dict even if broken"