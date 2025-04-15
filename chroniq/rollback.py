from pathlib import Path
from chroniq.utils import emoji
from chroniq.logger import activity_log
from rich.console import Console
import click

# Create a rich console for consistent output
console = Console()

def perform_rollback(rollback_version=False, yes=False):
    """
    ✅ Core rollback logic (Pro Mode)

    This function handles rollback of version.txt from a .version.bak file
    and optionally removes the most recent changelog section.

    Parameters:
    - rollback_version (bool): If True, rollback only version.txt.
    - yes (bool): If True, skip confirmation prompts.
    """
    version_path = Path("version.txt")
    backup_path = Path(".version.bak")

    # ⛔ Abort if backup file doesn't exist
    if not backup_path.exists():
        console.print(f"{emoji('❌', '[error]')} [red]No backup version found. Cannot rollback.[/red]")
        return

    # 🧾 Read current and previous versions
    try:
        current_version = version_path.read_text(encoding="utf-8").strip()
        previous_version = backup_path.read_text(encoding="utf-8").strip()
    except Exception as e:
        console.print(f"{emoji('❌', '[error]')} [red]Error reading version files:[/red] {e}")
        return

    console.print(f"{emoji('🕒', '[info]')} Current version: [bold yellow]{current_version}[/bold yellow]")
    console.print(f"{emoji('⏪', '[rollback]')} Will rollback to: [bold green]{previous_version}[/bold green]")

    # ❓ Confirm rollback unless --yes flag is passed
    if not yes and not click.confirm("Are you sure you want to rollback version.txt?", default=False):
        console.print(f"{emoji('❎', '[cancel]')} [dim]Rollback cancelled.[/dim]")
        return

    # 🧹 Optional changelog rollback (default unless --version is used)
    if rollback_version is False:
        changelog_path = Path("CHANGELOG.md")
        if not changelog_path.exists():
            console.print(f"{emoji('⚠️', '[warn]')} [yellow]No CHANGELOG.md found. Skipping changelog rollback.[/yellow]")
        else:
            try:
                lines = changelog_path.read_text(encoding="utf-8").splitlines(keepends=True)
                start = next((i for i, line in enumerate(lines) if line.startswith("## [")), None)
                if start is not None:
                    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## [")), len(lines))
                    removed = lines[start:end]
                    lines = lines[:start] + lines[end:]
                    changelog_path.write_text("".join(lines), encoding="utf-8")
                    activity_log.info(f"Rolled back changelog section: {removed[0].strip()}")
                    console.print(f"{emoji('🧹', '[cleanup]')} [green]Removed changelog entry:[/green] {removed[0].strip()}")
                else:
                    console.print(f"{emoji('❌', '[error]')} [red]No changelog headings found to rollback.[/red]")
            except Exception as e:
                console.print(f"{emoji('❌', '[error]')} [red]Failed to rollback changelog:[/red] {e}")

    # 💾 Restore version file
    try:
        version_path.write_text(previous_version + "\n", encoding="utf-8")
        activity_log.info(f"Rolled back version.txt from {current_version} to {previous_version}")
        console.print(f"{emoji('✅', '[done]')} [green]Rollback complete.[/green]")
    except Exception as e:
        console.print(f"{emoji('❌', '[error]')} [red]Failed to restore backup:[/red] {e}")
