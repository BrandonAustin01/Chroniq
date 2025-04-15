from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from chroniq.core import SemVer
from chroniq.config import load_config
from chroniq.utils import emoji
import os
import re

console = Console()
VERSION_FILE = Path("version.txt")
CHANGELOG_FILE = Path("CHANGELOG.md")

def run_audit(strict=False):
    """
    Run a diagnostic scan on versioning setup, changelog state, and config health.
    
    Parameters:
        strict (bool): If True, enables additional changelog format validations.
    """
    console.print(f"\n{emoji('🕵️‍♂️', '[audit]')} [bold cyan]Chroniq Hyper Audit[/bold cyan]\n{'='*30}")

    # 🧩 Load project configuration using Chroniq's config loader
    config = load_config()
    active_profile = config.get("active_profile", "default")
    console.print(f"{emoji('⚙️', '[config]')} Using profile: [bold]{active_profile}[/bold]")

    # 📁 Resolve paths from config or use defaults
    version_path = Path(config.get("version_path", "version.txt"))
    changelog_path = Path(config.get("changelog_path", "CHANGELOG.md"))
    log_dir = Path(config.get("log_dir", "logs"))

    # 🧪 Version file existence + format validation
    if not version_path.exists():
        console.print(f"{emoji('⚠️', '[warn]')} [yellow]Missing version file:[/yellow] {version_path}")
    else:
        try:
            # Try to parse the version file using SemVer loader
            version = SemVer.load(version_path)
            console.print(f"{emoji('📦', '[ver]')} Version file found: [bold green]{version}[/bold green]")
        except Exception as e:
            # Warn if version file is present but not semver compatible
            console.print(f"{emoji('❌', '[error]')} [red]Invalid version format:[/red] {e}")

    # 📄 Ensure the changelog file exists
    if not changelog_path.exists():
        console.print(f"{emoji('⚠️', '[warn]')} [yellow]Missing changelog file:[/yellow] {changelog_path}")
        return  # Exit early if changelog is missing

    with open(changelog_path, encoding="utf-8") as f:
        content = f.read()

    # 🔍 Ensure changelog contains a top-level heading
    if "# Changelog" not in content:
        console.print(f"{emoji('❌', '[error]')} [red]CHANGELOG.md missing top-level heading[/red]")

    # 🧾 Check that current version is mentioned in changelog
    try:
        current_version = SemVer.load(version_path)
        if str(current_version) not in content:
            console.print(f"{emoji('⚠️', '[warn]')} [yellow]Current version {current_version} not found in changelog[/yellow]")
        else:
            console.print(f"{emoji('🧾', '[log]')} CHANGELOG contains current version.")
    except Exception as e:
        console.print(f"{emoji('❌', '[error]')} [red]Error parsing version:[/red] {e}")

    # 🔍 Extra validation when strict mode is on
    if strict or config.get("strict", False):
        console.print(f"{emoji('🔍', '[strict]')} [bold]Strict mode enabled[/bold]")

        # ✅ Look for headings like: ## [1.2.3] - 2024-01-01
        headings = re.findall(r"^## \[(.*?)\] - (\d{4}-\d{2}-\d{2})", content, flags=re.MULTILINE)
        if not headings:
            console.print(f"{emoji('❗', '[warn]')} [yellow]No properly formatted changelog headings found.[/yellow]")
        else:
            console.print(f"{emoji('✅', '[ok]')} Found {len(headings)} valid changelog headings.")

    # 📁 Ensure logs folder exists
    if not log_dir.exists():
        console.print(f"{emoji('📂', '[logdir]')} [yellow]Log directory not found:[/yellow] {log_dir}")
    else:
        console.print(f"{emoji('📂', '[logdir]')} Log directory OK: {log_dir}")

    # 💬 Helpful suggestions if strict mode is off
    if not strict and not config.get("strict", False):
        console.print(f"{emoji('💡', '[tip]')} [dim]Tip: Enable --strict mode or set `strict = true` in .chroniq.toml for deeper audits.[/dim]")

    # 📉 Warn if changelog has no version sections at all
    if "## [" not in content:
        console.print(f"{emoji('📉', '[warn]')} [yellow]No version sections detected in changelog. Consider using changelog headings for tracking.[/yellow]")

    # ✅ Wrap-up message
    console.print(f"\n{emoji('✅', '[done]')} [green]Audit complete.[/green]\n")
