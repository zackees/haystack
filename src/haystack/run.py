import argparse
import re
from pathlib import Path
from shutil import which
from typing import Generator

from haystack.find_plus_context import find_plus_context
from haystack.types import SearchResult

assert which(
    "rg"
), "ripgrep (rg) is required to run this script. Please install it and ensure it is in your PATH."


def parse_args():
    parser = argparse.ArgumentParser(
        description="Refined Search Tool with ripgrep and fzf"
    )
    parser.add_argument("--term1", help="First search term")
    parser.add_argument("--term2", help="Second search term")
    return parser.parse_args()


def single_phase() -> None:
    for index, result in enumerate(find_plus_context("test", Path.cwd())):
        s = str(result)
        o = f"[{index}]: {s}"
        print(o)


def double_search(
    q1: str, q2: str, start_dir: Path = Path.cwd()
) -> Generator[SearchResult, None, None]:
    if not q1:
        print("Error: First search term (--term1) is required.")
        return None

    second_regex = re.compile(q2)
    for result in find_plus_context(q1, start_dir):
        print(result)
        if q2:
            term_in_at_least_one_line = any(
                second_regex.search(line) for line in result.lines
            )
            if term_in_at_least_one_line:
                yield result
        else:
            yield result

    return None


def unit_test() -> None:
    # Simulate command-line arguments for testing
    import sys

    sys.argv = ["haystack", "--term1", "test", "--term2", "this"]
    double_search("test", "this")


if __name__ == "__main__":
    unit_test()
