import tomllib  # built-in TOML parser in Python 3.11+
import json
import tomli_w
from pathlib import Path
from rich import print
from chroniq.utils import emoji
from chroniq.logger import system_log, activity_log  # ✅ add this


# Default config file path (can later support multiple tiers)
CONFIG_PATH = Path(".chroniq.toml")

# Default fallback config if no .chroniq.toml is found or fails to load
DEFAULT_CONFIG = {
    "default_bump": "patch",
    "silent": False,
    "strict": False,
    "emoji_fallback": True,
    "version_file": "version.txt",
    "changelog_file": "CHANGELOG.md",
    "log_dir": "data/logs",
    "activity_log": "data/logs/activity.log",
    "auto_increment_prerelease": True,
    "require_changelog_heading": False,
}

def deep_merge(base, update):
    """Recursively merges dictionaries, with 'update' taking precedence."""
    for key, value in update.items():
        if isinstance(value, dict) and key in base:
            base[key] = deep_merge(base.get(key, {}), value)
        else:
            base[key] = value
    return base

def load_config(config_path: Path = CONFIG_PATH) -> dict:
    """
    Load and parse the Chroniq configuration from a TOML file.
    Includes safe fallback to default config and strict profile handling.
    """
    if not config_path.exists():
        system_log.warning("No .chroniq.toml found. Using fallback defaults.")
        return DEFAULT_CONFIG.copy()

    try:
        with open(config_path, "rb") as f:
            parsed = tomllib.load(f)

        config = DEFAULT_CONFIG.copy()
        config = deep_merge(config, parsed)

        profile_name = parsed.get("active_profile", "default")
        profiles = parsed.get("profile", {})
        if not isinstance(profiles, dict):
            profiles = {}

        profile_data = profiles.get(profile_name, {})
        if not isinstance(profile_data, dict):
            profile_data = {}

        config = deep_merge(config, profile_data)
        config["active_profile"] = profile_name

        system_log.info(f"Loaded configuration using profile '{profile_name}'")
        return config

    except Exception as e:
        system_log.error(f"Failed to load .chroniq.toml: {e}")
        return DEFAULT_CONFIG.copy()

def update_config_value(key, value, config_path=CONFIG_PATH):
    """
    Update a value in the .chroniq.toml configuration file.
    Supports nested keys using dot notation (e.g., 'profile.dev.silent').
    """
    existing = load_config(config_path)

    parts = key.split(".")
    current = existing

    for part in parts[:-1]:
        if part not in current or not isinstance(current[part], dict):
            current[part] = {}
        current = current[part]

    val = value
    if isinstance(value, str):
        if value.lower() in ["true", "false"]:
            val = value.lower() == "true"
        elif value.isdigit():
            val = int(value)

    current[parts[-1]] = val

    try:
        with open(config_path, "wb") as f:
            f.write(tomli_w.dumps(existing).encode("utf-8"))

        activity_log.info(f"Updated config key '{key}' to '{val}'")
        return True

    except Exception as e:
        system_log.error(f"Error updating config value '{key}' → '{value}': {e}")
        return False
