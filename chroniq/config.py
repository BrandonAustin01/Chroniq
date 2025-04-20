import tomllib  # built-in TOML parser in Python 3.11+
import json
import tomli_w
from pathlib import Path
from rich import print
from chroniq.utils import emoji
from chroniq.logger import system_log, activity_log 


# Default config file path (can later support multiple tiers)
CONFIG_PATH = Path(".chroniq.toml")

def deep_merge(base, update):
    """Recursively merges dictionaries, with 'update' taking precedence."""
    for key, value in update.items():
        if isinstance(value, dict) and key in base:
            base[key] = deep_merge(base.get(key, {}), value)
        else:
            base[key] = value
    return base

def load_config(profile: str = None, path: Path = None):
    """
    Load the Chroniq configuration from .chroniq.toml.
    Returns a tuple of (merged_config: dict, active_profile: str)
    """
    from chroniq.logger import system_log
    from chroniq.defaults import DEFAULT_CONFIG

    config_path = path or CONFIG_PATH

    # 🧱 Start with full default config
    merged_config = DEFAULT_CONFIG.copy()

    # 📭 If config file doesn't exist, just return the defaults
    if not config_path.exists():
        return merged_config, "default"

    try:
        # 📖 Load the .toml file using Python's built-in TOML reader
        with open(config_path, "rb") as f:
            config_data = tomllib.load(f)
    except Exception as e:
        system_log.error(f"Failed to load .chroniq.toml: {e}")
        return merged_config, "default"

    # 🧠 Determine the active profile (CLI override > config file > fallback to "default")
    active_profile = profile or config_data.get("active_profile", "default")

    # 🌍 First, apply top-level/global config keys (excluding profiles)
    for key, value in config_data.items():
        if key not in ("profile", "profiles"):
            # 🧪 Convert "true"/"false" strings to proper bools
            if isinstance(value, str) and value.strip().lower() in ("true", "false"):
                value = value.strip().lower() == "true"
            merged_config[key] = value

    # 🎯 Next, apply profile-specific overrides if defined
    profile_section = None
    if "profile" in config_data and isinstance(config_data["profile"], dict):
        profile_section = config_data["profile"].get(active_profile)
    if not profile_section and "profiles" in config_data and isinstance(config_data["profiles"], dict):
        profile_section = config_data["profiles"].get(active_profile)

    if profile_section and isinstance(profile_section, dict):
        for key, value in profile_section.items():
            if isinstance(value, str) and value.strip().lower() in ("true", "false"):
                value = value.strip().lower() == "true"
            merged_config[key] = value

    return merged_config, active_profile


def update_config_value(key, value, config_path=CONFIG_PATH):
    """
    Update a value in the .chroniq.toml configuration file.
    Supports nested keys using dot notation (e.g., 'profile.dev.silent').
    """
    existing, _ = load_config(path=config_path)

    # 🔍 Traverse into nested dicts if using dot notation
    parts = key.split(".")
    current = existing

    for part in parts[:-1]:
        if part not in current or not isinstance(current[part], dict):
            current[part] = {}
        current = current[part]

    # 🧠 Normalize value types: str → bool/int where applicable
    val = value
    if isinstance(value, str):
        lowered = value.strip().lower()

        # ✅ Convert boolean-like strings to real bools
        if lowered in ("true", "yes", "on"):
            val = True
        elif lowered in ("false", "no", "off"):
            val = False

        # ✅ Convert integers (e.g. "42") safely
        elif lowered.isdigit():
            val = int(lowered)

        # ✅ Special case: allow quoted boolean TOML values like "True" or "False"
        elif lowered in ("\"true\"", "'true'"):
            val = True
        elif lowered in ("\"false\"", "'false'"):
            val = False


    # ✍️ Set final key
    current[parts[-1]] = val

    try:
        with open(config_path, "wb") as f:
            f.write(tomli_w.dumps(existing).encode("utf-8"))
        activity_log.info(f"Updated config key '{key}' to '{val}'")
        return True
    except Exception as e:
        system_log.error(f"Error updating config value '{key}' → '{value}': {e}")
        return False


def get_config_value(key: str, config_data: dict, profile: str = None) -> dict | None:
    """
    Retrieve a config value from the active profile, top-level, or fallback defaults.
    Returns a dict: {"value": ..., "origin": ...}
    """

    # ✅ 1. Look inside the active profile first
    profile_data = config_data.get("profiles", {}).get(profile or "default", {})
    if key in profile_data:
        return {
            "value": profile_data[key],
            "origin": f"profile:{profile or 'default'}"
        }

    # ✅ 2. Check top-level config (global values)
    if key in config_data:
        return {
            "value": config_data[key],
            "origin": "user-defined"
        }

    # ✅ 3. Fallback to internal default config (if available)
    try:
        from chroniq.defaults import DEFAULT_CONFIG
        if key in DEFAULT_CONFIG:
            return {
                "value": DEFAULT_CONFIG[key],
                "origin": "default"
            }
    except ImportError:
        pass  # No defaults module or fallback defined

    # ❌ 4. Key not found anywhere
    return None
