### chroniq/config.py

import json
import tomllib  # Python 3.11+
from pathlib import Path
from rich import print
from typing import Dict

# Config file search priority
TOML_PATH = Path(".chroniq.toml")
JSON_PATH = Path(".chroniqrc.json")


def load_config() -> Dict[str, str]:
    """
    Load Chroniq project configuration.

    Supports either a .chroniq.toml or .chroniqrc.json file in the current directory.

    Priority:
        1. .chroniq.toml (recommended, supports [settings] block)
        2. .chroniqrc.json (fallback)

    Returns:
        dict: Parsed configuration values. If no file is found or parsing fails,
              an empty dictionary is returned.

    Example:
        config = load_config()
        silent = config.get("silent", False)
    """
    config: dict = {}

    if TOML_PATH.exists():
        try:
            with open(TOML_PATH, "rb") as f:
                toml_data = tomllib.load(f)
                config = toml_data.get("settings", {})  # flatten from [settings]
            print("⚙️  [green]Loaded configuration from .chroniq.toml[/green]")
        except Exception as e:
            print(f"❌ [red]Error parsing .chroniq.toml:[/red] {e}")

    elif JSON_PATH.exists():
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
            print("⚙️  [green]Loaded configuration from .chroniqrc.json[/green]")
        except Exception as e:
            print(f"❌ [red]Error parsing .chroniqrc.json:[/red] {e}")

    return config


# 🧪 Example .chroniq.toml:
# [settings]
# default_bump = "patch"
# silent = false
# version_file = "version.txt"
# changelog_file = "CHANGELOG.md"
