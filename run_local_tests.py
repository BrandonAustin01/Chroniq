import subprocess
import tempfile
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
    print("\n\n🏁 Starting Chroniq Smoke Test\n" + "="*40)
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"📂 Using temporary project directory: {tmpdir}\n")
        cwd = Path(tmpdir)

        for name, cmd, *input_text in COMMANDS:
            run_command(name, cmd, input_text[0] if input_text else None, cwd=cwd)

    print("\n✅\033[1m All smoke tests completed.\033[0m\n")


if __name__ == "__main__":
    run_all()