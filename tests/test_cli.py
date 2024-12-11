"""
Unit test file.
"""

import os
import unittest
from pathlib import Path

HERE = Path(__file__).parent.resolve()
TEST_DIR = HERE / "test_data"
TEXT_TXT = TEST_DIR / "text.txt"

assert TEST_DIR.exists(), f"Test directory not found: {TEST_DIR}"
assert TEXT_TXT.exists(), f"Test file not found: {TEXT_TXT}"

COMMAND = "haystack"


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_imports(self) -> None:
        """Test command line interface (CLI)."""
        rtn = os.system(COMMAND)
        self.assertEqual(0, rtn)


if __name__ == "__main__":
    unittest.main()
