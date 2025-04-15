import re
from pathlib import Path
from rich import print
from chroniq.utils import emoji  # 🛡️ Custom helper to safely render emojis in all terminals

# 📌 This is the path where Chroniq will store its current version
VERSION_FILE = Path("version.txt")

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
        """
        🛠️ Increase PATCH version only.
        Example: 1.2.3 → 1.2.4
        """
        self.patch += 1
        self.prerelease = ""  # Clear prerelease on stable bump

    def bump_minor(self):
        """
        🧱 Increase MINOR version, reset PATCH.
        Example: 1.2.3 → 1.3.0
        """
        self.minor += 1
        self.patch = 0
        self.prerelease = ""

    def bump_major(self):
        """
        🚀 Increase MAJOR version, reset MINOR + PATCH.
        Example: 1.2.3 → 2.0.0
        """
        self.major += 1
        self.minor = 0
        self.patch = 0
        self.prerelease = ""
    
    def bump_prerelease(self, label: str):
        """
        Bump or initialize a prerelease string.

        Examples:
            ""         → raises ValueError
            "alpha"    → alpha.1
            "alpha.1"  → alpha.2
            "beta"     → beta.1
            "beta.4"   → beta.5
        """
        if not label or not isinstance(label, str):
            raise ValueError("Prerelease label must be a non-empty string.")

        # Match current prerelease: 'label.number'
        match = re.fullmatch(rf"({label})\.(\d+)", self.prerelease)
        if match:
            current_num = int(match.group(2))
            self.prerelease = f"{label}.{current_num + 1}"
        else:
            self.prerelease = f"{label}.1"


    @classmethod
    def from_string(cls, version_str: str) -> "SemVer":
        """
        📥 Parse a version string into a SemVer instance.

        Supports:
        - '1.2.3'
        - '2.0.0-beta.1'

        Raises:
        - ValueError for bad formats or unsafe inputs (leading zeros, whitespace, etc.)
        """
        # ❌ Reject whitespace-padded strings
        if not isinstance(version_str, str) or version_str.strip() != version_str:
            raise ValueError(f"Invalid version format (whitespace): '{version_str}'")

        # 📐 Full semver match with optional -PRERELEASE
        pattern = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z\-.]+))?$"
        match = re.fullmatch(pattern, version_str)
        if not match:
            raise ValueError(f"Invalid version format: '{version_str}'")

        major, minor, patch, prerelease = match.groups()
        return cls(int(major), int(minor), int(patch), prerelease or "")

    @classmethod
    def load(cls, path=VERSION_FILE):
        """
        📂 Load version from a file. If the file is missing or broken,
        fallback to 0.1.0 and save it.

        Returns:
            SemVer instance
        """
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
        """
        💾 Save current version to a file in plain text format.
        Example file contents: `1.2.3` or `1.2.3-alpha.2`
        """
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(str(self))
            print(f"{emoji('💾', '[save]')} Version [bold cyan]{self}[/bold cyan] saved to '{path}'")
        except Exception as e:
            print(f"{emoji('❌', '[error]')} [red]Failed to save version:[/red] {e}")
