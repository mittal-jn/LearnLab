"""CLI entry point — `uv run learnlab` opens the app in the browser."""
import subprocess
import sys
from pathlib import Path


def main() -> None:
    app = Path(__file__).parent / "app.py"
    sys.exit(subprocess.call(
        ["streamlit", "run", str(app)],
        stdout=sys.stdout,
        stderr=sys.stderr,
    ))


if __name__ == "__main__":
    main()
