#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


COMMANDS = {
    "create-flat": SCRIPT_DIR / "forge_create_flat.py",
    "approve": SCRIPT_DIR / "forge_approve.py",
    "reject": SCRIPT_DIR / "forge_reject.py",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Hermes Forge P0 CLI wrapper",
        usage=(
            "forge.py {create-flat,approve,reject} [args...]\n\n"
            "Examples:\n"
            "  forge.py create-flat --project freelancer --title 'Note' --dry-run --json\n"
            "  forge.py approve --path wiki/freelancer/forge-inbox/example.md --json\n"
            "  forge.py reject --path wiki/freelancer/forge-inbox/example.md --reason 'not needed' --json"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("command", choices=sorted(COMMANDS))
    parser.add_argument("args", nargs=argparse.REMAINDER)

    ns = parser.parse_args()

    script = COMMANDS[ns.command]

    if not script.exists():
        print(f"ERROR: command script not found: {script}", file=sys.stderr)
        return 2

    cmd = [sys.executable, str(script), *ns.args]

    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
