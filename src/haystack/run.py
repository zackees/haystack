import argparse
import subprocess
import sys
from pathlib import Path
from shutil import which

from haystack.find_plus_context import find_plus_context

assert which(
    "rg"
), "ripgrep (rg) is required to run this script. Please install it and ensure it is in your PATH."


def run_command(command: str | list[str]):
    try:
        cmd_str = (
            subprocess.list2cmdline(command) if isinstance(command, list) else command
        )
        print(f"Executing command: {cmd_str}")
        # Add stderr=subprocess.STDOUT to redirect stderr to stdout
        result = subprocess.run(
            command,
            shell=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        error_msg = (
            e.output
            if e.output
            else "Command failed. Please ensure ripgrep (rg) is installed and accessible."
        )
        print(f"Error message: {error_msg}")
        sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Refined Search Tool with ripgrep and fzf"
    )
    parser.add_argument("--term1", help="First search term")
    parser.add_argument("--term2", help="Second search term")
    return parser.parse_args()


def main():
    print("Refined Search Tool with ripgrep and fzf")

    args = parse_args()

    # Get terms from args or prompt
    term1 = args.term1 if args.term1 else input("Enter the first search term: ").strip()
    term2 = (
        args.term2 if args.term2 else input("Enter the second search term: ").strip()
    )

    # Use ripgrep to search for the first term with context
    print(f"Searching for '{term1}' using ripgrep...")
    # rg_command = f"rg -C 3 '{term1}'"
    rg_command: list[str] = ["rg", "-C", "3", term1]
    rg_output = run_command(rg_command)

    if not rg_output:
        print(f"No results found for '{term1}'. Exiting.")
        sys.exit(0)

    print(f"Search results for '{term1}':")
    print(rg_output)

    # Pipe ripgrep results into fzf for interactive refinement
    print("Refining search with fzf...")
    try:
        fzf_command = "fzf --preview 'echo {}'"
        fzf_result = subprocess.run(
            fzf_command, shell=True, text=True, input=rg_output, capture_output=True
        )

        if fzf_result.returncode != 0 or not fzf_result.stdout.strip():
            print("No selection made in fzf. Exiting.")
            sys.exit(0)

        selected_line = fzf_result.stdout.strip()
        print(f"Selected line: {selected_line}")

        # Search the selected context for the second term
        print(f"Searching for '{term2}' within the selected context...")
        if term2.lower() in selected_line.lower():
            print(f"'{term2}' found in the selected context:")
            print(selected_line)
        else:
            print(f"'{term2}' not found in the selected context.")

    except KeyboardInterrupt:
        print("Interrupted by user. Exiting.")
        sys.exit(0)


def unit_test() -> None:
    for index, result in enumerate(find_plus_context("test", Path.cwd())):
        s = str(result)
        print(f"[{index}]: {s}")


if __name__ == "__main__":
    unit_test()
