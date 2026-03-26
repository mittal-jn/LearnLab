"""CLI entry point — `uv run learnlab` launches the Streamlit app."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    app_path = Path(__file__).parent / "app.py"
    sys.exit(
        subprocess.call(
            ["streamlit", "run", str(app_path), "--server.headless", "true"],
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
    )


if __name__ == "__main__":
    main()

