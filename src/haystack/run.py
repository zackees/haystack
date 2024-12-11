import argparse
from pathlib import Path
from shutil import which

from haystack.find_plus_context import find_plus_context

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


def unit_test() -> None:
    for index, result in enumerate(find_plus_context("test", Path.cwd())):
        s = str(result)
        print(f"[{index}]: {s}")


if __name__ == "__main__":
    unit_test()
