import re
from pathlib import Path
from rich import print
from rich.console import Console
import click

from chroniq.utils import emoji  # 🛡️ Custom helper to safely render emojis in all terminals
from chroniq.logger import activity_log

# 📌 This is the path where Chroniq will store its current version
VERSION_FILE = Path("version.txt")

console = Console()

class SemVer:
    """
    🔢 Semantic Versioning (SemVer) class to manage versions of the form:
    MAJOR.MINOR.PATCH[-PRERELEASE]

    ✅ Supports:
    - Breaking changes → MAJOR++
    - Feature additions → MINOR++
    - Bug fixes → PATCH++
    - Optional prerelease tag (e.g. alpha, beta.2, rc.1)
    """

    def __init__(self, major=0, minor=1, patch=0, prerelease=""):
        """
        📦 Initialize version components. Default starts at 0.1.0
        """
        self.major = major
        self.minor = minor
        self.patch = patch
        self.prerelease = prerelease  # Optional tag like 'alpha.1'

    def __str__(self):
        """
        🪞 Return full version string.
        Example: '1.2.3' or '1.2.3-beta.2'
        """
        base = f"{self.major}.{self.minor}.{self.patch}"
        return f"{base}-{self.prerelease}" if self.prerelease else base

    def bump_patch(self):
        self.patch += 1
        self.prerelease = ""

    def bump_minor(self):
        self.minor += 1
        self.patch = 0
        self.prerelease = ""

    def bump_major(self):
        self.major += 1
        self.minor = 0
        self.patch = 0
        self.prerelease = ""

    def bump_prerelease(self, label: str):
        if not label or not isinstance(label, str):
            raise ValueError("Prerelease label must be a non-empty string.")

        match = re.fullmatch(rf"({label})\.(\d+)", self.prerelease)
        if match:
            current_num = int(match.group(2))
            self.prerelease = f"{label}.{current_num + 1}"
        else:
            self.prerelease = f"{label}.1"

    @classmethod
    def from_string(cls, version_str: str) -> "SemVer":
        if not isinstance(version_str, str) or version_str.strip() != version_str:
            raise ValueError(f"Invalid version format (whitespace): '{version_str}'")

        pattern = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z\-.]+))?$"
        match = re.fullmatch(pattern, version_str)
        if not match:
            raise ValueError(f"Invalid version format: '{version_str}'")

        major, minor, patch, prerelease = match.groups()
        return cls(int(major), int(minor), int(patch), prerelease or "")

    @classmethod
    def load(cls, path=VERSION_FILE):
        if not path.exists():
            print(f"{emoji('⚠️', '[warn]')} [yellow]No version file found. Creating default version 0.1.0[/yellow]")
            default_version = cls()
            default_version.save(path)
            return default_version

        try:
            with open(path, 'r', encoding="utf-8") as f:
                version_str = f.read().strip()
                return cls.from_string(version_str)
        except Exception as e:
            print(f"{emoji('❌', '[error]')} [red]Failed to read version file:[/red] {e}")
            fallback = cls()
            fallback.save(path)
            return fallback

    def save(self, path: Path = VERSION_FILE):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(str(self))
            print(f"{emoji('💾', '[save]')} Version [bold cyan]{self}[/bold cyan] saved to '{path}'")
        except Exception as e:
            print(f"{emoji('❌', '[error]')} [red]Failed to save version:[/red] {e}")


def perform_rollback(rollback_version=False, yes=False):
    """
    ✅ Core rollback logic)

    This function handles rollback of version.txt from a .version.bak file
    and optionally removes the most recent changelog section.
    """
    version_path = Path("version.txt")
    backup_path = Path(".version.bak")

    if not backup_path.exists():
        console.print(f"{emoji('❌', '[error]')} [red]No backup version found. Cannot rollback.[/red]")
        return

    try:
        current_version = version_path.read_text(encoding="utf-8").strip()
        previous_version = backup_path.read_text(encoding="utf-8").strip()
    except Exception as e:
        console.print(f"{emoji('❌', '[error]')} [red]Error reading version files:[/red] {e}")
        return

    console.print(f"{emoji('🕒', '[info]')} Current version: [bold yellow]{current_version}[/bold yellow]")
    console.print(f"{emoji('⏪', '[rollback]')} Will rollback to: [bold green]{previous_version}[/bold green]")

    if not yes and not click.confirm("Are you sure you want to rollback version.txt?", default=False):
        console.print(f"{emoji('❎', '[cancel]')} [dim]Rollback cancelled.[/dim]")
        return

    if not rollback_version:
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

    try:
        version_path.write_text(previous_version + "\n", encoding="utf-8")
        activity_log.info(f"Rolled back version.txt from {current_version} to {previous_version}")
        console.print(f"{emoji('✅', '[done]')} [green]Rollback complete.[/green]")
    except Exception as e:
        console.print(f"{emoji('❌', '[error]')} [red]Failed to restore backup:[/red] {e}")