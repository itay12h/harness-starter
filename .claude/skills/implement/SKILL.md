---
name: implement
description: Execute an approved plan one task at a time, validating each step and logging progress. Use after a plan is reviewed.
---

# Implement

Work an approved `plans/<slug>.md`, one task at a time.

## Loop

For each unchecked task, in order:

1. Make the smallest change that completes it.
2. Run its validation step (from the plan).
3. If it fails, fix it before moving on. Never batch failures.
4. Check the box in the plan and append a line to `reports/<slug>.md`
   (what changed · what you ran · the result).

When every task is checked and the gate passes, say so. Don't declare done early —
the `Stop` hook runs the gate and sends you back if it isn't actually done.
