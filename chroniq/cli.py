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
from chroniq.config import load_config, CONFIG_PATH, update_config_value, get_config_value
from chroniq.utils import emoji
from chroniq.logger import system_log, activity_log
from chroniq.rollback import perform_rollback

# Create a console with forced UTF-8 encoding for better emoji safety
console = Console(file=sys.stdout)

# Default file paths for version and changelog
VERSION_FILE = Path("version.txt")
CHANGELOG_FILE = Path("CHANGELOG.md")

# 🧱 Define the config command group
@click.group()
def config():
    """Manage Chroniq configuration settings."""
    pass

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

# 🧠 Define the `get` subcommand
@config.command("get")
@click.argument("key", required=True)
@click.option("--profile", help="Profile to read from (default: active profile)")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.option("--toml", "as_toml", is_flag=True, help="Output as TOML")
def config_get(key, profile, as_json, as_toml):
    """
    Get a configuration value by key with fallback awareness.
    """
    config_data, active_profile = load_config(profile)
    result = get_config_value(key, config_data, active_profile)

    if result is None:
        console.print(f"❌ Config key not found: '{key}'", style="bold red")
        return

    value, origin = result["value"], result["origin"]

    if as_json:
        import json
        console.print_json(json.dumps({key: value}))
    elif as_toml:
        import tomli_w
        click.echo(tomli_w.dumps({key: value}))
    else:
        console.print(Panel.fit(
            f"[bold yellow]{key}[/bold yellow] → [green]{value}[/green]\\n[dim]Source: {origin}[/dim]",
            title="[ config:get ]",
            border_style="cyan"
        ))

@config.command("list")
@click.option("--profile", help="Show values from a specific profile")
@click.option("--all", "show_all", is_flag=True, help="Show all profiles and values")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.option("--toml", "as_toml", is_flag=True, help="Output as TOML")
def config_list(profile, show_all, as_json, as_toml):
    """
    List current Chroniq configuration values with origin awareness.
    """
    config_data, active_profile = load_config(profile)
    target_profile = profile or active_profile

    from chroniq.defaults import DEFAULT_CONFIG
    import json

    merged = {}

    # Helper to resolve config value with fallback logic
    def resolve_value(key):
        result = get_config_value(key, config_data, target_profile)
        return result["value"] if result else None

    if as_json:
        merged = {key: resolve_value(key) for key in DEFAULT_CONFIG}
        click.echo(json.dumps(merged, indent=2))
        return

    if as_toml:
        import tomli_w
        merged = {key: resolve_value(key) for key in DEFAULT_CONFIG}
        click.echo(tomli_w.dumps(merged))
        return

    from rich.table import Table

    # 🔍 Build config output table
    table = Table(title=f"📂 Config for Profile: {target_profile}")
    table.add_column("Key", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")
    table.add_column("Source", style="dim")

    all_keys = set(DEFAULT_CONFIG.keys())

    if show_all:
        # 🔍 Display all profiles
        all_profiles = config_data.get("profiles", {}).keys()
        for prof in sorted(all_profiles):
            prof_table = Table(title=f"📂 Profile: {prof}")
            prof_table.add_column("Key", style="cyan")
            prof_table.add_column("Value", style="green")
            prof_table.add_column("Source", style="dim")

            for key in sorted(DEFAULT_CONFIG.keys()):
                result = get_config_value(key, config_data, prof)
                if result:
                    prof_table.add_row(key, str(result['value']), result['origin'])
            console.print(prof_table)
        return

    # 👇 Default: Show only current profile
    for key in sorted(all_keys):
        result = get_config_value(key, config_data, target_profile)
        if result:
            table.add_row(key, str(result["value"]), result["origin"])

    console.print(table)

main.add_command(config)

if __name__ == "__main__":
    main()
