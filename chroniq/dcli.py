from chroniq.core import SemVer
from chroniq.changelog import add_entry
from chroniq.config import load_config

def bump_version(level: str = None, silent: bool = False):
    """
    Programmatically bump the project version and optionally update the changelog.

    Parameters:
        level (str): One of 'patch', 'minor', or 'major'. If None, uses config default.
        silent (bool): If True, skips prompts and outputs (used for automation).
    
    Returns:
        str: The new version string after bumping.
    """
    config = load_config()
    bump_level = (level or config.get("default_bump", "patch")).lower()

    if bump_level not in ("patch", "minor", "major"):
        raise ValueError(f"Invalid bump level: '{bump_level}'. Use 'patch', 'minor', or 'major'.")

    version = SemVer.load()

    if bump_level == "patch":
        version.bump_patch()
    elif bump_level == "minor":
        version.bump_minor()
    elif bump_level == "major":
        version.bump_major()

    version.save()

    # Optionally add changelog entry if not in silent mode
    if not silent:
        print("Version bumped to:", version)
        if input("Add changelog entry? (y/N): ").lower().startswith("y"):
            message = input("Describe the change: ")
            add_entry(str(version), message)

    return str(version)

def current_version():
    """
    Return the current project version as a string.

    Returns:
        str: The version (e.g., "1.2.3")
    """
    return str(SemVer.load())

def reset_files():
    """
    Delete version.txt and CHANGELOG.md if they exist.

    Use this when starting over or reinitializing a project.
    """
    from pathlib import Path
    for file in ("version.txt", "CHANGELOG.md"):
        path = Path(file)
        if path.exists():
            path.unlink()
