### chroniq/core.py

import re
from pathlib import Path

# Default location for storing the version information.
# You can change this path if your project requires a different location.
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
        By default, the version is set to 0.1.0 (a common starting point).
        """
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self):
        """
        Return the version as a formatted string (e.g., '1.2.3').
        This is what gets written to the version file and displayed to users.
        """
        return f"{self.major}.{self.minor}.{self.patch}"

    def bump_patch(self):
        """
        Increment the PATCH version by 1.
        Use this when making backwards-compatible bug fixes.
        Example: 1.2.3 → 1.2.4
        """
        self.patch += 1

    def bump_minor(self):
        """
        Increment the MINOR version by 1 and reset PATCH to 0.
        Use this when adding functionality in a backward-compatible manner.
        Example: 1.2.3 → 1.3.0
        """
        self.minor += 1
        self.patch = 0

    def bump_major(self):
        """
        Increment the MAJOR version by 1 and reset MINOR and PATCH to 0.
        Use this when making incompatible API changes.
        Example: 1.2.3 → 2.0.0
        """
        self.major += 1
        self.minor = 0
        self.patch = 0

    @classmethod
    def from_string(cls, version_str):
        """
        Parse a version string (e.g., '1.2.3') and return a SemVer object.
        This is used internally to read and validate version strings.

        :param version_str: A string in MAJOR.MINOR.PATCH format
        :return: SemVer instance
        :raises ValueError: if the string is not a valid version format
        """
        match = re.match(r"(\d+)\.(\d+)\.(\d+)", version_str)
        if not match:
            raise ValueError(f"❌ Invalid version format: '{version_str}'. Expected format is MAJOR.MINOR.PATCH, e.g., '1.0.0'")
        return cls(int(match.group(1)), int(match.group(2)), int(match.group(3)))

    @classmethod
    def load(cls, path=VERSION_FILE):
        """
        Load version from a file.
        If the file does not exist, it will return a default version (0.1.0).

        :param path: Path to the version file
        :return: SemVer instance representing the current version
        """
        if not path.exists():
            print("🔍 No version file found. Defaulting to 0.1.0")
            return cls()
        with open(path, 'r') as f:
            version_str = f.read().strip()
            return cls.from_string(version_str)

    def save(self, path=VERSION_FILE):
        """
        Save the current version to a file (overwrites existing version).
        Creates the file if it doesn't exist.

        :param path: Path to save the version to
        """
        with open(path, 'w') as f:
            f.write(str(self))
        print(f"💾 Version {self} saved to '{path}'")


# 🔧 Developer Example:
# Use the following snippet in your script to bump and save a version:
#
# from chroniq.core import SemVer
# version = SemVer.load()
# version.bump_patch()         # or bump_minor(), bump_major()
# version.save()
# print("✅ New version:", version)
