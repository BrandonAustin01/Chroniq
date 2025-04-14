### chroniq/core.py

import re
from pathlib import Path
from rich import print
from chroniq.utils import emoji  # Safe emoji wrapper

# Default location for storing the version information.
VERSION_FILE = Path("version.txt")

class SemVer:
    """
    SemVer (Semantic Versioning) class to handle versioning logic in the format:
    MAJOR.MINOR.PATCH

    - MAJOR version: incremented for breaking changes
    - MINOR version: incremented for backward-compatible feature additions
    - PATCH version: incremented for bug fixes and small changes

    This class allows you to load, bump, and save versions in a project-friendly way.
    """

    def __init__(self, major=0, minor=1, patch=0):
        """
        Initialize a new SemVer object.
        Default version starts at 0.1.0 (a safe baseline for early development).
        """
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self):
        """
        Return version as 'MAJOR.MINOR.PATCH', e.g., '1.2.3'.
        """
        return f"{self.major}.{self.minor}.{self.patch}"

    def bump_patch(self):
        """
        Increment PATCH version by 1.
        Example: 1.2.3 → 1.2.4
        """
        self.patch += 1

    def bump_minor(self):
        """
        Increment MINOR version by 1 and reset PATCH to 0.
        Example: 1.2.3 → 1.3.0
        """
        self.minor += 1
        self.patch = 0

    def bump_major(self):
        """
        Increment MAJOR version by 1 and reset MINOR and PATCH to 0.
        Example: 1.2.3 → 2.0.0
        """
        self.major += 1
        self.minor = 0
        self.patch = 0

    @classmethod
    def from_string(cls, version_str):
        """
        Parse a version string and return a SemVer object.

        Parameters:
            version_str (str): A string like '1.2.3'

        Returns:
            SemVer instance

        Raises:
            ValueError: If format is not valid SemVer.
        """
        match = re.match(r"(\d+)\.(\d+)\.(\d+)", version_str)
        if not match:
            raise ValueError(f"{emoji('❌', '[error]')} Invalid version format: '{version_str}'. Expected format is MAJOR.MINOR.PATCH.")
        return cls(int(match.group(1)), int(match.group(2)), int(match.group(3)))

    @classmethod
    def load(cls, path=VERSION_FILE):
        """
        Load version from a file. If missing, defaults to 0.1.0.

        Parameters:
            path (Path): Path to the version file

        Returns:
            SemVer instance
        """
        if not path.exists():
            print(f"{emoji('⚠️', '[warn]')} [yellow]No version file found. Defaulting to 0.1.0[/yellow]")
            return cls()
        try:
            with open(path, 'r', encoding="utf-8") as f:
                version_str = f.read().strip()
                return cls.from_string(version_str)
        except Exception as e:
            print(f"{emoji('❌', '[error]')} [red]Failed to read version file:[/red] {e}")
            return cls()

    def save(self, path: Path = VERSION_FILE):
        """
        Save the current version to a file.

        Parameters:
            path (Path): Path to write version file
        """
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(str(self))
            print(f"{emoji('💾', '[save]')} Version [bold cyan]{self}[/bold cyan] saved to '{path}'")
        except Exception as e:
            print(f"{emoji('❌', '[error]')} [red]Failed to save version:[/red] {e}")
