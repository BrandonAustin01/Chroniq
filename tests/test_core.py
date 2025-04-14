### tests/test_core.py

import pytest
import tempfile
from pathlib import Path
from chroniq.core import SemVer


def test_default_version():
    """
    Test that a new SemVer instance starts with version 0.1.0 by default.
    """
    v = SemVer()
    assert str(v) == "0.1.0", "Default version should be 0.1.0"


def test_bump_patch():
    """
    Test patch bump: only patch number should increment.
    """
    v = SemVer(1, 2, 3)
    v.bump_patch()
    assert str(v) == "1.2.4", "Patch bump failed"


def test_bump_minor():
    """
    Test minor bump: minor should increment, patch resets to 0.
    """
    v = SemVer(1, 2, 3)
    v.bump_minor()
    assert str(v) == "1.3.0", "Minor bump should reset patch to 0"


def test_bump_major():
    """
    Test major bump: major should increment, minor and patch reset to 0.
    """
    v = SemVer(1, 2, 3)
    v.bump_major()
    assert str(v) == "2.0.0", "Major bump should reset minor and patch"


def test_from_string_valid():
    """
    Test parsing a valid version string.
    """
    v = SemVer.from_string("3.5.9")
    assert (v.major, v.minor, v.patch) == (3, 5, 9), "Version parsing failed"


def test_from_string_invalid():
    """
    Test that an invalid version string raises ValueError.
    """
    with pytest.raises(ValueError, match="Invalid version format"):
        SemVer.from_string("bad.version")


def test_load_save_roundtrip():
    """
    Test saving a version to file and loading it back.
    Ensures SemVer file IO works properly.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "version.txt"
        v1 = SemVer(2, 4, 6)
        v1.save(path)  # Save version to a temporary file

        v2 = SemVer.load(path)  # Load it back
        assert str(v2) == "2.4.6", "Load/save roundtrip failed"