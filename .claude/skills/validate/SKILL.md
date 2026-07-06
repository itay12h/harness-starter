---
name: validate
description: Run the full verification gate (lint, types, tests) and report a clear pass/fail. This is the definition of "done".
---

# Validate

Run the project's gate and report a clear pass/fail. This is what "done" means.

## Steps

1. Run the commands from `CLAUDE.md` ("Test / gate", "Lint"). If the project has
   a `scripts/validate.sh`, run that.
2. Capture failures verbatim — file, line, message.
3. Report either ✅ all gates pass, or ❌ with the exact failures and the smallest
   next action to fix them.

Never report success on unverified work. If you can't run the gate, say so plainly.
