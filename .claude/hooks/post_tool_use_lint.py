#!/usr/bin/env python3
"""PostToolUse lint (non-blocking).

Runs an available linter on the file that was just edited and reports issues back
to the agent. It's a *sensor*, not a gate — it always exits 0, so it nudges but
never blocks. (The Stop hook is the gate.)
"""
import json
import os
import shutil
import subprocess
import sys


def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except Exception:
        return None


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    path = (data.get("tool_input") or {}).get("file_path", "")
    if not path or not os.path.exists(path):
        sys.exit(0)

    ext = os.path.splitext(path)[1].lower()
    result = None
    if ext == ".py" and shutil.which("ruff"):
        result = run(["ruff", "check", path])
    elif ext in (".js", ".jsx", ".ts", ".tsx") and shutil.which("eslint"):
        result = run(["eslint", path])

    if result and result.returncode != 0:
        out = (result.stdout + result.stderr).strip()
        print(f"[lint] issues in {path}:\n{out}", file=sys.stderr)

    sys.exit(0)  # never block on lint


if __name__ == "__main__":
    main()
