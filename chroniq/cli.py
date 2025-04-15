import click
import sys
import tomli_w
import tomllib

from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich import print
from chroniq.core import SemVer
from chroniq.changelog import add_entry
from chroniq.config import load_config, CONFIG_PATH, update_config_value
from chroniq.utils import emoji
from chroniq.logger import system_log, activity_log
from chroniq.rollback import perform_rollback

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
    system_log.info("Chroniq CLI initialized.")  # ✅ Log CLI boot
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
        pre            → Auto-increment prerelease (e.g., alpha.1 → alpha.2)
        --pre alpha.1  → Explicitly set a prerelease label
    """
    config = load_config()
    silent_mode = silent or config.get("silent", False)

    # Use CLI arg, fallback to config value, then default to "patch"
    bump_level = (level or config.get("default_bump", "patch")).lower()

    if bump_level not in ["patch", "minor", "major", "pre"]:
        console.print(f"{emoji('❌', '[error]')} [red]Invalid bump level:[/red] '{bump_level}' — must be patch, minor, major, or pre.")
        return

    try:
        version = SemVer.load()
        # 🧠 Save current version as backup before bumping
        Path(".version.bak").write_text(str(version) + "\n", encoding="utf-8")

        if not silent_mode:
            console.print(Panel.fit(
                f"{emoji('📦', '[version]')} Current version: [bold yellow]{version}[/bold yellow]",
                title="Chroniq"))

        # Handle the special 'pre' mode which auto-bumps or adds prerelease
        if bump_level == "pre":
            version.bump_prerelease(pre or "alpha")
        else:
            # Perform a normal version bump
            if bump_level == "patch":
                version.bump_patch()
            elif bump_level == "minor":
                version.bump_minor()
            elif bump_level == "major":
                version.bump_major()

            # If a prerelease is passed with --pre, attach it after bumping
            if pre:
                version.prerelease = pre

        # Save updated version to disk
        version.save()
        activity_log.info(f"Version bumped to {version}")  # ✅ Log version bump

        if not silent_mode:
            console.print(Panel.fit(
                f"{emoji('✅', '[ok]')} New version: [bold green]{version}[/bold green]",
                title="Version Updated"))

        # ✅ Ask to add changelog entry
        if click.confirm("Would you like to add a changelog entry for this version?", default=True):
            message = click.prompt(f"{emoji('🗘️', '[log]')} Describe the change", default="", show_default=False)
            if message.strip():
                add_entry(str(version), message)
                activity_log.info(f"Changelog entry added for {version}")


    except Exception as e:
        console.print(f"{emoji('❌', '[error]')} [bold red]Failed to bump version:[/bold red] {e}")
        system_log.error(f"Version bump failed: {e}")



@main.command()
@click.option("--smoke", is_flag=True, help="Only run smoke tests (quick check).")
def test(smoke):
    """
    Run Chroniq's internal test suite.

    Use --smoke to run only smoke tests (init, bump, etc).
    """
    try:
        import subprocess

        if smoke:
            console.print(f"{emoji('🧪', '[test]')} [cyan]Running Chroniq smoke tests...[/cyan]")
            subprocess.run([sys.executable, "run_local_tests.py", "--smoke"], check=True)
        else:
            console.print(f"{emoji('🧪', '[test]')} [cyan]Running all Chroniq tests...[/cyan]")
            subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], check=True)

        console.print(f"{emoji('✅', '[ok]')} [green]All tests completed.[/green]")

    except subprocess.CalledProcessError:
        console.print(f"{emoji('❌', '[error]')} [bold red]Some tests failed. Check output above.[/bold red]")
    except Exception as e:
        console.print(f"{emoji('❌', '[error]')} [bold red]Failed to run tests:[/bold red] {e}")


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
        activity_log.info("Created version.txt with default version 0.1.0")  # ✅

    if CHANGELOG_FILE.exists():
        console.print(f"{emoji('✅', '[ok]')} [green]CHANGELOG.md already exists.[/green]")
    else:
        with open(CHANGELOG_FILE, 'w', encoding="utf-8") as f:
            f.write("# Changelog\n\nAll notable changes to this project will be documented here.\n")
        console.print(f"{emoji('📄', '[file]')} [cyan]Created CHANGELOG.md[/cyan]")
        activity_log.info("Created CHANGELOG.md")  # ✅

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
        activity_log.info("Reset version.txt and CHANGELOG.md")  # ✅
    except Exception as e:
        console.print(f"{emoji('❌', '[error]')} [bold red]Failed to reset files:[/bold red] {e}")
        system_log.error(f"Version bump failed: {e}")

import tomli_w  # Safe TOML writer

@main.command("config")
@click.argument("action", type=click.Choice(["set"]))
@click.argument("key")
@click.argument("value")
@click.option("--profile", help="Optional profile scope (e.g. dev, release)")
def config_set(action, key, value, profile):
    """
    Update Chroniq configuration values in .chroniq.toml

    Examples:
        chroniq config set silent true
        chroniq config set default_bump minor
        chroniq config set silent false --profile dev
    """
    from chroniq.config import CONFIG_PATH
    import tomllib
    import tomli_w

    try:
        # Load existing config or use empty fallback
        existing = {}
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "rb") as f:
                existing = tomllib.load(f)

        # 🧠 Apply profile logic: prefix key with profile if needed
        if profile and not key.startswith("profile."):
            key = f"profile.{profile}.{key}"

        # 🧩 Split key using dot notation
        parts = key.split(".")
        current = existing

        # 🔁 Traverse or build nested dictionaries
        for part in parts[:-1]:
            if part not in current or not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]

        # 🔄 Auto-convert value into bool or int if applicable
        val = value
        if value.lower() in ["true", "false"]:
            val = value.lower() == "true"
        elif value.isdigit():
            val = int(value)

        # ✅ Set the new value
        current[parts[-1]] = val

        # 💾 Save updated config
        with open(CONFIG_PATH, "wb") as f:
            f.write(tomli_w.dumps(existing).encode("utf-8"))

        console.print(f"{emoji('🛠️', '[config]')} [green]Updated[/green] '[bold]{key}[/bold]' → [bold]{val}[/bold] in .chroniq.toml")
        activity_log.info(f"CLI config set: {key} = {val}")  # ✅

    except Exception as e:
        console.print(f"{emoji('❌', '[error]')} [red]Failed to update configuration:[/red] {e}")
        system_log.error(f"Version bump failed: {e}")



@main.command()
@click.option("--strict", is_flag=True, help="Enable strict mode for additional checks.")
def audit(strict):
    """
    Audit your Chroniq setup for potential problems and inconsistencies.

    Use --strict to enable extra validations (e.g. changelog header format).
    """
    from chroniq.audit import run_audit

    try:
        config = load_config()
        strict_mode = strict or config.get("strict", False)

        system_log.info(f"Running audit (strict={strict_mode})")  # ✅
        run_audit(strict=strict_mode)

    except Exception as e:
        console.print(f"{emoji('❌', '[error]')} [bold red]Audit failed:[/bold red] {e}")

@main.command("config-show")
def config_show():
    """
    Display the currently loaded Chroniq configuration, including active profile.
    """
    from chroniq.config import load_config

    try:
        config = load_config()

        # Extract and show profile info
        profile = config.get("active_profile", "default")
        console.print(f"{emoji('📂', '[profile]')} [bold]Active Profile:[/bold] {profile}")

        # Pretty print config dictionary
        console.print("\n[bold cyan]Loaded Configuration:[/bold cyan]")
        for key, value in config.items():
            if isinstance(value, dict):
                console.print(f"\n[blue]{key}[/blue]:")
                for sub_key, sub_value in value.items():
                    console.print(f"  [dim]{sub_key}[/dim] = {sub_value}")
            else:
                console.print(f"{key} = {value}")

    except Exception as e:
        console.print(f"{emoji('❌', '[error]')} [red]Failed to load configuration:[/red] {e}")

@main.command("changelog-preview")
@click.option("--message", "-m", multiple=True, help="Changelog message(s) to preview. Supports multiple.")
@click.option("--date", help="Optional date override in YYYY-MM-DD format.")
@click.option("--style", type=click.Choice(["default", "compact"]), default="default", help="Preview format style.")
def preview_changelog(message, date, style):
    """
    Preview what the next changelog entry will look like, without writing to file.

    Examples:
        chroniq changelog-preview
        chroniq changelog-preview --message "Fixed typo" --message "Improved logging"
        chroniq changelog-preview --style compact --date 2025-04-15
    """
    from datetime import datetime
    from chroniq.core import SemVer

    try:
        # ✅ Step 1: Load current version from version.txt
        version = SemVer.load()

        # ✅ Step 2: Determine messages (interactive fallback if none passed)
        if not message:
            console.print(f"{emoji('🗘️', '[log]')} [bold]No messages passed. Please enter a description:[/bold]")
            user_input = click.prompt("Describe the change", default="", show_default=False)
            if not user_input.strip():
                console.print(f"{emoji('⚠️', '[warn]')} [yellow]No message provided. Preview aborted.[/yellow]")
                return
            message = [user_input.strip()]

        # ✅ Step 3: Determine the date
        entry_date = date or datetime.today().strftime("%Y-%m-%d")

        # ✅ Step 4: Format the changelog preview
        if style == "compact":
            formatted = "\n".join(f"- {m}" for m in message)
        else:
            formatted = f"## [{version}] - {entry_date}\n\n" + "\n".join(f"- {m}" for m in message)

        # ✅ Step 5: Render it in a Rich Panel
        console.rule(f"{emoji(' 👁️ ', '[preview]')} [bold cyan]Changelog Preview[/bold cyan]")
        console.print(Panel.fit(formatted, title="📄 Would-be Entry", border_style="cyan"))
        console.rule()

    except Exception as e:
        console.print(f"{emoji('❌', '[error]')} [bold red]Failed to preview changelog:[/bold red] {e}")

@main.command("rollback")
@click.option("--version", "rollback_version", is_flag=True, help="Rollback only version.txt")
@click.option("--yes", is_flag=True, help="Skip confirmation prompt")
def rollback(rollback_version, yes):
    """
    Rollback the most recent version bump and optionally the latest changelog entry.

    By default, this will:
    - Restore version.txt from .version.bak
    - Remove the most recent changelog section (unless --version is passed)

    Examples:
        chroniq rollback
        chroniq rollback --version
        chroniq rollback --yes
    """
    perform_rollback(rollback_version=rollback_version, yes=yes)


if __name__ == "__main__":
    main()
