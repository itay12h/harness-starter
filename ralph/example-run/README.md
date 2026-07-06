# Captured example run — demo insurance

A **representative** captured Ralph run you can walk through (or replay the
narrative of) if the live loop misbehaves during a demo — keys, network, rate
limits. The task list is the one in `ralph/tasks.example.md`.

| File | What it shows |
|------|---------------|
| `tasks.md` | the checklist the loop worked through (all boxes checked) |
| `fix_plan.md` | the running log the agent kept across iterations — its memory |
| `run.log` | the driver's per-iteration log (3 iterations → `DONE.txt`) |
| `DONE.txt` | the sentinel it wrote only when every task passed the gate |

> This sample is **illustrative** (hand-authored to show the shape). To capture a
> real one: run `bash ralph/ralph.sh` on a tiny safe spec and save the resulting
> `ralph/ralph.log`, `ralph/fix_plan.md`, and `DONE.txt` here.
