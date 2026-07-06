# Ralph — one task per run

You are running headless, one iteration of a loop, with a **fresh context**.
Everything you need is in the files. Do NOT try to finish everything at once.

## Each run

1. Read `ralph/tasks.md` and pick the **first unchecked** task.
2. Read `CLAUDE.md` and any relevant `.claude/context/*.md`.
3. Complete that one task. Make the smallest change that does it.
4. **Validate** it — run the gate from `CLAUDE.md`. If it fails, fix it this run.
5. Check the box in `ralph/tasks.md` and append a short line to `reports/ralph.md`
   (task · what you ran · result).

## Stop condition

When **every** task in `ralph/tasks.md` is checked AND the full gate passes,
write a file named `DONE.txt` containing a one-line summary.

Otherwise, end the run **without** writing `DONE.txt` — the loop will start you
again with a fresh context.

Never write `DONE.txt` on unverified work. A separate reviewer will check you.
