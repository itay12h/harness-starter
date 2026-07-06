---
name: plan
description: Turn a task or ticket into a concrete, reviewable plan file before any code is written. Use for anything non-trivial.
---

# Plan

Produce a plan a human will read line by line before implementation starts.

## Steps

1. Read the request and the relevant code. Explore before deciding — for a broad
   task, fan out parallel sub-agents to research.
2. Read `CLAUDE.md` and any relevant `.claude/context/*.md`.
3. Write `plans/<slug>.md` with:
   - **Goal** — one sentence, checkable ("done when …").
   - **Context** — the files and functions that matter, with paths.
   - **Tasks** — a numbered, ordered checklist of small, independent steps.
   - **Validation** — how each task is verified (the exact command to run).
   - **Risks / open questions.**
4. Stop. Do not implement. Hand the plan back for review.

Keep it concrete. A vague plan drifts further off target with every step.
