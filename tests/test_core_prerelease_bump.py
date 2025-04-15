import unittest
from chroniq.core import SemVer

class TestPrereleaseBump(unittest.TestCase):
    """
    Unit tests for SemVer.bump_prerelease() behavior.
    """

    def test_initial_prerelease_bump_sets_dot_one(self):
        """
        If a version has no prerelease, bumping should initialize to 'label.1'
        """
        v = SemVer(1, 2, 3)
        v.bump_prerelease("alpha")
        self.assertEqual(str(v), "1.2.3-alpha.1")

    def test_bumping_existing_same_label_increments_number(self):
        """
        If prerelease already exists with same label, increment the number.
        """
        v = SemVer(1, 2, 3, "alpha.1")
        v.bump_prerelease("alpha")
        self.assertEqual(str(v), "1.2.3-alpha.2")

    def test_bumping_with_different_label_resets_to_dot_one(self):
        """
        If prerelease label is different, reset suffix to '.1'
        """
        v = SemVer(1, 2, 3, "alpha.4")
        v.bump_prerelease("beta")
        self.assertEqual(str(v), "1.2.3-beta.1")

    def test_bumping_without_label_raises(self):
        """
        Calling bump_prerelease with empty label should raise ValueError.
        """
        v = SemVer(1, 0, 0)
        with self.assertRaises(ValueError):
            v.bump_prerelease("")

if __name__ == "__main__":
    unittest.main()
