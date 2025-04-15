import click
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from chroniq.core import SemVer
from chroniq.changelog import add_entry
from chroniq.config import load_config
from chroniq.utils import emoji

# Create a console with forced UTF-8 encoding for better emoji safety
console = Console(file=sys.stdout)

# Default file paths for version and changelog
VERSION_FILE = Path("version.txt")
CHANGELOG_FILE = Path("CHANGELOG.md")

@click.group()
def main():
    """
    Chroniq – Smart versioning and changelog management CLI.

    This tool helps developers manage their project's version and changelog files
    using Semantic Versioning (SemVer). You can bump versions, initialize config files,
    and display recent changelog entries with human-friendly CLI feedback.
    """
    console.print(f"[bold magenta]{emoji('🔮', '[start]')} Chroniq CLI initialized.[/bold magenta]")

@main.command()
@click.argument("level", required=False)
@click.option("--pre", default=None, help="Apply a prerelease label like alpha.1 or rc")
@click.option("--silent", is_flag=True, help="Suppress output and interactive prompts.")
def bump(level, pre, silent):
    """
    Apply a version bump based on semantic versioning rules.

    Options:
        patch, minor, major
        --pre alpha.1  (append prerelease label)
    """
    config = load_config()
    silent_mode = silent or config.get("silent", False)

    bump_level = (level or config.get("default_bump", "patch")).lower()
    if bump_level not in ["patch", "minor", "major", "pre"]:
        console.print(f"{emoji('❌', '[error]')} [red]Invalid bump level:[/red] '{bump_level}' — must be patch, minor, major, or pre.")
        return


    try:
        version = SemVer.load()

        if not silent_mode:
            console.print(Panel.fit(
                f"{emoji('📦', '[version]')} Current version: [bold yellow]{version}[/bold yellow]",
                title="Chroniq"))

        if bump_level == "patch":
            version.bump_patch()
        elif bump_level == "minor":
            version.bump_minor()
        elif bump_level == "major":
            version.bump_major()
        elif bump_level == "pre":
            version.bump_prerelease(pre or "alpha")  # default label is "alpha"

# Explicit override for prerelease if user passes --pre with patch/minor/major
        elif pre and bump_level in ["patch", "minor", "major"]:
            version.prerelease = pre

        version.save()

        if not silent_mode:
            console.print(Panel.fit(
                f"{emoji('✅', '[ok]')} New version: [bold green]{version}[/bold green]",
                title="Version Updated"))

            if click.confirm("Would you like to add a changelog entry for this version?", default=True):
                message = click.prompt(f"{emoji('🗘️', '[log]')} Describe the change", default="", show_default=False)
                add_entry(str(version), message)

    except Exception as e:
        console.print(f"{emoji('❌', '[error]')} [bold red]Failed to bump version:[/bold red] {e}")


@main.command()
def init():
    """
    Initialize Chroniq in your project folder by creating `version.txt` and `CHANGELOG.md`
    """
    if VERSION_FILE.exists():
        console.print(f"{emoji('✅', '[ok]')} [green]version.txt already exists.[/green]")
    else:
        SemVer().save()
        console.print(f"{emoji('📄', '[file]')} [cyan]Created version.txt with default version 0.1.0[/cyan]")

    if CHANGELOG_FILE.exists():
        console.print(f"{emoji('✅', '[ok]')} [green]CHANGELOG.md already exists.[/green]")
    else:
        with open(CHANGELOG_FILE, 'w', encoding="utf-8") as f:
            f.write("# Changelog\n\nAll notable changes to this project will be documented here.\n")
        console.print(f"{emoji('📄', '[file]')} [cyan]Created CHANGELOG.md[/cyan]")

@main.command()
@click.option('--lines', default=5, help='Number of recent changelog entries to display')
def log(lines):
    """
    Show the latest changelog entries from the CHANGELOG.md file
    """
    if not CHANGELOG_FILE.exists():
        console.print(f"{emoji('❌', '[error]')} [red]No CHANGELOG.md found. Please run `chroniq init` first.[/red]")
        return

    with open(CHANGELOG_FILE, 'r', encoding="utf-8") as f:
        content = f.readlines()

    filtered = [line.strip() for line in content if line.strip()]
    recent = filtered[-lines:] if lines <= len(filtered) else filtered

    def format_log_line(line):
        if line.startswith("Added"):
            return f"[green]{line}[/green]"
        elif line.startswith("Changed"):
            return f"[yellow]{line}[/yellow]"
        elif line.startswith("Fixed"):
            return f"[red]{line}[/red]"
        return line

    formatted = "\n".join(format_log_line(line) for line in recent)
    console.print(Panel.fit(formatted, title=f"{emoji('🗘️', '[log]')} Last {len(recent)} Changelog Lines"))

@main.command()
def version():
    """
    Show the current version of your project
    """
    try:
        version = SemVer.load()
        console.print(f"{emoji('📌', '[ver]')} [bold cyan]Current project version:[/bold cyan] {version}")
    except Exception as e:
        console.print(f"{emoji('❌', '[error]')} [bold red]Failed to read version:[/bold red] {e}")

@main.command()
def reset():
    """
    Reset Chroniq by deleting version.txt and CHANGELOG.md.
    
    This is useful if you want to wipe versioning state and start over.
    """
    try:
        # Attempt to remove version.txt
        VERSION_FILE.unlink(missing_ok=True)
        # Attempt to remove changelog
        CHANGELOG_FILE.unlink(missing_ok=True)
        console.print(f"{emoji('🧹', '[reset]')} [yellow]Chroniq files have been reset.[/yellow]")
    except Exception as e:
        console.print(f"{emoji('❌', '[error]')} [bold red]Failed to reset files:[/bold red] {e}")


if __name__ == "__main__":
    main()
