import subprocess
import tempfile
import unittest
import argparse

from pathlib import Path
from textwrap import dedent
from rich.console import Console

# Argument parser lets you run the script with --smoke to skip unit tests
parser = argparse.ArgumentParser()
parser.add_argument("--smoke", action="store_true", help="Only run smoke tests.")
args = parser.parse_args()

# A list of Chroniq CLI commands with optional simulated input
COMMANDS = [
    # Initialize version.txt and CHANGELOG.md
    ("Init", ["chroniq", "init"]),
    # Bump patch, minor, and major (skipping changelog input with 'n\n')
    ("Bump Patch", ["chroniq", "bump", "patch"], "n\n"),
    ("Bump Minor", ["chroniq", "bump", "minor"], "n\n"),
    ("Bump Major", ["chroniq", "bump", "major"], "n\n"),
    # Bump patch again, this time accepting changelog with 'y\n'
    ("Bump with Changelog", ["chroniq", "bump", "patch"], "y\nAdded via test script\n"),
    # Display version and log, then reset to clean state
    ("Show Version", ["chroniq", "version"]),
    ("Show Log", ["chroniq", "log", "--lines", "10"]),
    ("Reset", ["chroniq", "reset"]),
]

def run_command(name, args, input_text=None, cwd=None):
    """
    Run a CLI command as a subprocess and capture its output.

    Args:
        name (str): Friendly name for the command
        args (list): List of command-line arguments
        input_text (str): Optional input to simulate user input (e.g. 'y\n')
        cwd (Path): Working directory to run the command in (isolated temp folder)
    """
    console = Console()
    print("\n" + "=" * 60)
    print(f"\033[1m🧪 Running: {name}\033[0m")
    print("=" * 60)
    try:
        result = subprocess.run(
            args,
            input=input_text,
            capture_output=True,
            text=True,
            check=True,
            cwd=cwd
        )
        console.print(f"[bold green]✔ Success:[/bold green] {args}")
        console.print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]✘ Failed:[/bold red] {args}")
        console.print(e.stderr.strip() or str(e))

def run_smoke_only():
    """
    Run only the smoke tests (CLI-level commands using subprocess).
    These tests simulate typical user workflows using an isolated temp folder.
    """
    print("\n\n🏁 Starting Chroniq Smoke Test\n" + "="*40)
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"📂 Using temporary project directory: {tmpdir}\n")
        cwd = Path(tmpdir)

        for name, cmd, *input_text in COMMANDS:
            run_command(name, cmd, input_text[0] if input_text else None, cwd=cwd)

    print("\n✅\033[1m All smoke tests completed.\033[0m\n")

def run_smoke_and_unit():
    """
    Run both smoke tests and full unit test suite.

    - Smoke tests: simulate full CLI interaction
    - Unit tests: validate internal logic with unittest discovery
    """
    print("\n\n🏁 Starting Chroniq Smoke Test\n" + "="*40)
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"📂 Using temporary project directory: {tmpdir}\n")
        cwd = Path(tmpdir)

        for name, cmd, *input_text in COMMANDS:
            run_command(name, cmd, input_text[0] if input_text else None, cwd=cwd)

    print("\n✅\033[1m All smoke tests completed.\033[0m\n")

    # Now run unit tests
    print("\n\n🧪 Running Unit Tests\n" + "="*40)
    suite = unittest.TestLoader().discover("tests")
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if result.wasSuccessful():
        print("\n✅\033[1m All unit tests passed.\033[0m\n")
    else:
        print("\n❌\033[1m Some unit tests failed.\033[0m\n")


if __name__ == "__main__":
    # If --smoke flag is passed, skip unit tests
    if args.smoke:
        run_smoke_only()
    else:
        run_smoke_and_unit()
