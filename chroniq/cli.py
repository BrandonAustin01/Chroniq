### chroniq/cli.py

import click
from rich import print
from rich.panel import Panel
from rich.console import Console
from chroniq.core import SemVer
from chroniq.changelog import add_entry
from chroniq.config import load_config
from pathlib import Path

console = Console()
VERSION_FILE = Path("version.txt")
CHANGELOG_FILE = Path("CHANGELOG.md")

@click.group()
def main():
    """
    Chroniq – Smart versioning and changelog management CLI.

    This tool helps developers manage their project's version and changelog files
    using Semantic Versioning (SemVer). You can bump versions, initialize config files,
    and display recent changelog entries with human-friendly CLI feedback.

    Example usage:
      chroniq init          # Sets up version.txt and CHANGELOG.md
      chroniq bump patch    # Bumps the patch number (e.g., 1.2.3 -> 1.2.4)
      chroniq log --lines 5 # Shows last 5 changelog entries
    """
    pass

@main.command()
@click.argument("level", required=False)
def bump(level):
    """
    Apply a version bump based on semantic versioning rules.

    If no level is provided, uses default_bump from config or 'patch'.
    Options:
      patch → Backwards-compatible bug fix
      minor → Backwards-compatible new feature
      major → Incompatible API change

    Example:
      chroniq bump minor
    """
    config = load_config()
    silent_mode = config.get("silent", False)

    # Use passed CLI argument or config fallback
    bump_level = level or config.get("default_bump", "patch")
    bump_level = bump_level.lower()

    if bump_level not in ["patch", "minor", "major"]:
        print(f"❌ [red]Invalid bump level:[/red] '{bump_level}' — must be patch, minor, or major.")
        return

    try:
        version = SemVer.load()

        if not silent_mode:
            print(Panel.fit(f"📦 Current version: [bold yellow]{version}[/bold yellow]", title="Chroniq"))

        # Apply the version bump
        if bump_level == "patch":
            version.bump_patch()
        elif bump_level == "minor":
            version.bump_minor()
        elif bump_level == "major":
            version.bump_major()

        version.save()

        if not silent_mode:
            print(Panel.fit(f"✅ New version: [bold green]{version}[/bold green]", title="Version Updated"))

            if click.confirm("Would you like to add a changelog entry for this version?", default=True):
                message = click.prompt("📝 Describe the change", default="", show_default=False)
                add_entry(str(version), message)

    except Exception as e:
        print(f"[bold red]❌ Failed to bump version:[/bold red] {e}")

@main.command()
def init():
    """
    Set up Chroniq in your project.

    This command will create `version.txt` and `CHANGELOG.md` if they don't exist yet.
    These files store your current project version and track your changelog entries.
    """
    if VERSION_FILE.exists():
        print("✅ [green]version.txt already exists.[/green]")
    else:
        SemVer().save()
        print("📄 [cyan]Created version.txt with default version 0.1.0[/cyan]")

    if CHANGELOG_FILE.exists():
        print("✅ [green]CHANGELOG.md already exists.[/green]")
    else:
        with open(CHANGELOG_FILE, 'w') as f:
            f.write("# Changelog\n\nAll notable changes to this project will be documented here.\n")
        print("📄 [cyan]Created CHANGELOG.md[/cyan]")

@main.command()
@click.option('--lines', default=5, help='Number of recent changelog entries to display')
def log(lines):
    """
    Display recent changelog entries from CHANGELOG.md.

    Example:
      chroniq log --lines 5
    """
    if not CHANGELOG_FILE.exists():
        print("❌ [red]No CHANGELOG.md found. Please run `chroniq init` first.[/red]")
        return

    with open(CHANGELOG_FILE, 'r') as f:
        content = f.readlines()

    # Extract and show the latest non-empty lines
    filtered = [line.strip() for line in content if line.strip() != '']
    recent = filtered[-lines:] if lines <= len(filtered) else filtered

    print(Panel.fit("\n".join(recent), title=f"📝 Last {len(recent)} Changelog Lines"))

@main.command()
def version():
    """
    Display the current project version stored in version.txt.

    Example:
      chroniq version
    """
    try:
        version = SemVer.load()
        print(f"📌 [bold cyan]Current project version:[/bold cyan] {version}")
    except Exception as e:
        print(f"[bold red]❌ Failed to read version:[/bold red] {e}")

if __name__ == "__main__":
    main()