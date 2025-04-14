# chroniq/changelog.py

from datetime import datetime
from pathlib import Path
from typing import List
from rich import print
from chroniq.utils import emoji  # 👈 fallback-safe emoji rendering

# Default changelog path
CHANGELOG_FILE = Path("CHANGELOG.md")


def ensure_changelog_exists() -> None:
    """
    Ensure that the changelog file exists.

    If the file does not exist, it is created with a default header to help
    guide users in documenting project changes over time.
    """
    if not CHANGELOG_FILE.exists():
        try:
            with open(CHANGELOG_FILE, 'w', encoding='utf-8') as f:
                f.write("# Changelog\n\nAll notable changes to this project will be documented here.\n")
            print(f"{emoji('📄', '[file]')} [cyan]CHANGELOG.md created successfully.[/cyan]")
        except Exception as e:
            print(f"{emoji('❌', '[error]')} [red]Failed to create CHANGELOG.md:[/red] {e}")


def add_entry(version: str, message: str) -> None:
    """
    Add a new changelog entry under the specified version.

    Parameters:
    - version (str): The version identifier (e.g., "1.2.0")
    - message (str): The user-provided description of the changes made

    This function appends a markdown-formatted entry to the changelog.

    Example:
        add_entry("0.3.1", "Fixed voice fallback timeout crash.")
    """
    if not message.strip():
        print(f"{emoji('⚠️', '[skip]')} [yellow]Skipped changelog update: message was empty.[/yellow]")
        return

    ensure_changelog_exists()
    timestamp = datetime.now().strftime("%Y-%m-%d")
    entry_header = f"\n\n## [{version}] - {timestamp}\n"
    entry_body = f"- {message.strip()}"

    try:
        with open(CHANGELOG_FILE, 'a', encoding='utf-8') as f:
            f.write(entry_header + entry_body + "\n")
        print(f"{emoji('📝', '[write]')} [green]Changelog updated with version:[/green] {version}")
    except Exception as e:
        print(f"{emoji('❌', '[error]')} [red]Failed to write to changelog:[/red] {e}")


def get_recent_entries(limit: int = 5) -> List[str]:
    """
    Retrieve the most recent non-empty lines from the changelog.

    Parameters:
    - limit (int): Number of most recent lines to return (default: 5)

    Returns:
    - List[str]: A list of non-empty changelog lines (most recent at the end)

    Example:
        entries = get_recent_entries(3)
        for line in entries:
            print(line)
    """
    if not CHANGELOG_FILE.exists():
        print(f"{emoji('❌', '[error]')} [red]No CHANGELOG.md found. Please run `chroniq init` first.[/red]")
        return []

    try:
        with open(CHANGELOG_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        entries = [line.strip() for line in lines if line.strip()]
        return entries[-limit:] if limit <= len(entries) else entries
    except Exception as e:
        print(f"{emoji('❌', '[error]')} [red]Error reading changelog:[/red] {e}")
        return []


# 🧪 Example (safe for CLI testing)
# add_entry("0.2.0", "Added CLI fallback for wake word timeout.")
# for line in get_recent_entries(3):
#     print(line)
