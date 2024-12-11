"""
Unit test file.
"""

import unittest
from pathlib import Path

from haystack.run import find_plus_context

HERE = Path(__file__).parent.resolve()
TEST_DIR = HERE / "test_data"
TEXT_TXT = TEST_DIR / "text.txt"

assert TEST_DIR.exists(), f"Test directory not found: {TEST_DIR}"
assert TEXT_TXT.exists(), f"Test file not found: {TEXT_TXT}"


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_other(self) -> None:
        for result in find_plus_context("test", Path.cwd()):
            print(result)


if __name__ == "__main__":
    unittest.main()
