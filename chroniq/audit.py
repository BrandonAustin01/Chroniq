from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from chroniq.core import SemVer
from chroniq.config import load_config
from chroniq.utils import emoji
import os
import re

console = Console()

def run_audit(strict=False, config_path: Path = None):
    """
    Run a diagnostic scan on versioning setup, changelog state, and config health.
    
    Parameters:
        strict (bool): If True, enables additional changelog format validations.
        config_path (Path): Optional override path for config file
    """
    console.print(f"\n{emoji('🕵️‍♂️', '[audit]')} [bold cyan]Chroniq Hyper Audit[/bold cyan]\n{'='*30}")

    # 🧩 Load project configuration using Chroniq's config loader
    config, active_profile = load_config(path=config_path)
    console.print(f"{emoji('⚙️', '[config]')} Using profile: [bold]{active_profile}[/bold]")

    # 📁 Resolve paths from config or use defaults
    version_path = Path(config.get("version_file", "version.txt"))
    changelog_path = Path(config.get("changelog_file", "CHANGELOG.md"))
    log_dir = Path(config.get("log_dir", "logs"))

    # 🧪 Version file existence + format validation
    if not version_path.exists():
        console.print(f"{emoji('⚠️', '[warn]')} [yellow]Missing version file:[/yellow] {version_path}")
    else:
        try:
            version = SemVer.load(version_path)
            console.print(f"{emoji('📦', '[ver]')} Version file found: [bold green]{version}[/bold green]")
        except Exception as e:
            console.print(f"{emoji('❌', '[error]')} [red]Invalid version format:[/red] {e}")

    # 📄 Ensure the changelog file exists
    if not changelog_path.exists():
        console.print(f"{emoji('⚠️', '[warn]')} [yellow]Missing changelog file:[/yellow] {changelog_path}")
        return

    try:
        with open(changelog_path, encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        console.print(f"{emoji('❌', '[error]')} [red]Failed to read changelog file:[/red] {e}")
        return

    if "# Changelog" not in content:
        console.print(f"{emoji('❌', '[error]')} [red]CHANGELOG.md missing top-level heading[/red]")

    try:
        current_version = SemVer.load(version_path)
        if str(current_version) not in content:
            console.print(f"{emoji('⚠️', '[warn]')} [yellow]Current version {current_version} not found in changelog[/yellow]")
        else:
            console.print(f"{emoji('🧾', '[log]')} CHANGELOG contains current version.")
    except Exception as e:
        console.print(f"{emoji('❌', '[error]')} [red]Error parsing version:[/red] {e}")

    # 🔍 Extra validation when strict mode is on (from CLI or config)
    strict_enabled = strict or config.get("strict", False)
    if strict_enabled:
        console.print(f"{emoji('🔍', '[strict]')} [bold]Strict mode enabled[/bold]")
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

    # 💡 Tip if not in strict mode
    if not strict_enabled:
        console.print(f"{emoji('💡', '[tip]')} [dim]Tip: Enable --strict or set `strict = true` in .chroniq.toml for deeper audits.[/dim]")

    # 📉 Check for any version headings at all
    if "## [" not in content:
        console.print(f"{emoji('📉', '[warn]')} [yellow]No version sections detected in changelog. Consider using changelog headings.[/yellow]")

    console.print(f"\n{emoji('✅', '[done]')} [green]Audit complete.[/green]\n")
