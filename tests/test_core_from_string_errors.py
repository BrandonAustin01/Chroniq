import unittest
from chroniq.core import SemVer

class TestSemVerFromStringErrors(unittest.TestCase):
    """
    Tests that invalid version strings correctly raise a ValueError.
    """

    def test_invalid_version_strings_raise_value_error(self):
        """
        Passes various malformed version strings and expects a ValueError.
        """
        # List of clearly malformed or invalid versions
        invalid_versions = [
            "",                # empty string
            "v1",              # too short
            "1.2",             # missing third component
            "1.2.3.4",         # too many parts
            "1..3",            # missing component
            "a.b.c",           # non-integer parts
            "1.2.beta",        # non-integer patch
            "1.2.-1",          # negative number
            "1.2.3\n",         # newline sneaking in
            "01.02.03"         # leading zeros (optional, but some SemVer tools reject this)
        ]

        for version in invalid_versions:
            with self.subTest(version=version):
                with self.assertRaises(ValueError):
                    SemVer.from_string(version)

if __name__ == "__main__":
    unittest.main()
