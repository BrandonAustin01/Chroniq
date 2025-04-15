import subprocess
import tempfile
import unittest

from pathlib import Path
from textwrap import dedent
from rich.console import Console

COMMANDS = [
    ("Init", ["chroniq", "init"]),
    ("Bump Patch", ["chroniq", "bump", "patch"], "n\n"),
    ("Bump Minor", ["chroniq", "bump", "minor"], "n\n"),
    ("Bump Major", ["chroniq", "bump", "major"], "n\n"),
    ("Bump with Changelog", ["chroniq", "bump", "patch"], "y\nAdded via test script\n"),
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

def run_all():
    """
    Run all Chroniq smoke tests followed by Python unit tests.

    This method ensures both CLI-level behavior and internal logic are working as expected.
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
    run_all()