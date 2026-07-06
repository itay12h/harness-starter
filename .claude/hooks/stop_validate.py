#!/usr/bin/env python3
"""Stop hook — the gate.

Before the agent is allowed to finish, run the project's validation gate. If it
fails, exit 2 to block the stop and feed the failures back, forcing the agent to
keep going. This is what turns "looks done" into "actually done".

Wire your gate by creating `scripts/validate.sh` (or a `validate:` Makefile
target). With no gate configured, this hook passes — so it's safe on day one.
"""
import json
import os
import subprocess
import sys


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    # Avoid an infinite stop-loop: if we already blocked this stop, let it go.
    if data.get("stop_hook_active"):
        sys.exit(0)

    gate = None
    if os.path.exists("scripts/validate.sh"):
        gate = ["bash", "scripts/validate.sh"]
    elif os.path.exists("Makefile"):
        try:
            mk = open("Makefile").read()
            if mk.startswith("validate:") or "\nvalidate:" in mk:
                gate = ["make", "validate"]
        except Exception:
            pass

    if not gate:
        sys.exit(0)  # no gate wired yet — pass

    try:
        r = subprocess.run(gate, capture_output=True, text=True, timeout=600)
    except Exception as e:
        print(f"[stop_validate] could not run gate ({e}); allowing stop.", file=sys.stderr)
        sys.exit(0)

    if r.returncode != 0:
        out = (r.stdout + r.stderr).strip()[-2000:]
        print(
            "[stop_validate] gate FAILED — not done yet. Fix these, then continue:\n" + out,
            file=sys.stderr,
        )
        sys.exit(2)  # block the stop, feed the reason back

    sys.exit(0)


if __name__ == "__main__":
    main()
