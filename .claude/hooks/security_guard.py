#!/usr/bin/env python3
"""PreToolUse security guard.

Denies dangerous actions BEFORE they run — even under
`--dangerously-skip-permissions`. This is a feedback *sensor* that fires before
the action instead of after.

Contract: exit code 2 blocks the tool call and shows stderr to the agent.
Any other exit (or a crash we swallow) lets the action through, so a buggy guard
never bricks the session.
"""
import json
import re
import sys


def block(msg: str) -> None:
    print(f"[security_guard] BLOCKED: {msg}", file=sys.stderr)
    sys.exit(2)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # never break the session on a parse error

    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}

    # 1) Protect secrets — no reading or editing .env files
    path = ti.get("file_path") or ti.get("path") or ""
    if path and re.search(r"(^|/)\.env(\.|$)", path):
        block(f"access to secrets file '{path}' is not allowed.")

    # 2) Dangerous shell commands
    if tool == "Bash":
        cmd = ti.get("command", "")
        danger = [
            r"\brm\s+-[a-z]*r[a-z]*f?\s+(/|~|\.|\*)",  # recursive delete of root/home/cwd/glob
            r"\bgit\s+push\b.*--force",                 # force push
            r"\bgit\s+reset\s+--hard\b",                # hard reset
            r":\(\)\s*\{\s*:\s*\|\s*:",                # fork bomb
            r"\bmkfs\b",
            r"\bdd\s+if=",                              # disk wipe
            r"\bcurl\b.*\|\s*(sudo\s+)?(ba)?sh\b",     # curl | sh
        ]
        for pat in danger:
            if re.search(pat, cmd):
                block(f"command matches a blocked pattern: {cmd!r}")
        # never read/copy a .env via the shell
        if re.search(r"\.env(\.|\s|$)", cmd) and re.search(
            r"\b(cat|less|more|head|tail|cp|scp|rsync|echo)\b", cmd
        ):
            block("reading or copying a .env file via the shell is not allowed.")

    sys.exit(0)


if __name__ == "__main__":
    main()
