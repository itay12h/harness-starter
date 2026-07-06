# Ralph — an autonomous, spec-driven loop

Ralph re-feeds a spec (`PROMPT.md`) to a **fresh headless Claude process each
iteration** until the spec is satisfied or a hard cap is hit. Fresh context every
round, state carried in files, a commit after each step.

```
loop:
  1. run: claude -p  <PROMPT.md   (fresh context; reads tasks.md + fix_plan.md)
  2. git add -A && git commit      (every iteration is reversible)
  3. DONE.txt present?  → stop
  4. hit the iteration cap?  → stop
  5. else repeat
```

## Two drivers

| File | Use |
|------|-----|
| `ralph.sh` | bash (Linux/macOS) |
| `ralph.py` | cross-platform, adds worktree isolation + parallel runs |

## Run it

```bash
cp tasks.example.md tasks.md         # your real, checkable tasks
bash ralph/ralph.sh 8                 # bash, hard cap of 8 rounds
python3 ralph/ralph.py --max 8        # python, same thing
```

## Self-isolating worktree mode (python)

By default Ralph commits onto your current branch — only safe in a throwaway
checkout. Pass `--worktree` and Ralph makes its **own** git worktree on a fresh
branch, runs the loop there, and prints the exact review/merge/discard commands.
Your main tree never moves.

```bash
python3 ralph/ralph.py --worktree --branch ralph/csv-export --cleanup
```

## Scale to parallel agents

The worktree is the unit you scale. Launch several at once — each is an isolated
agent on its own branch, sharing one `.git`:

```bash
python3 ralph/ralph.py --worktree --branch ralph/feature-a &
python3 ralph/ralph.py --worktree --branch ralph/feature-b &
python3 ralph/ralph.py --worktree --branch ralph/feature-c &
wait   # then review each branch and merge / open PRs
```

If runs share a stateful resource (a database, a port), give each its own via
`--setup "<command>"`, which runs once inside the worktree before the loop.

## Guardrails (the three that keep it honest)

| Guardrail | Default | Why |
|-----------|---------|-----|
| hard cap (`--max` / `RALPH_MAX_ITER`) | 10 | never runs forever, never a runaway bill |
| per-iteration timeout (`--timeout`) | 1800 s | one stuck round can't hang the loop |
| `DONE.txt` sentinel | — | written only when every task passes the gate |
| commit per iteration | — | every step reversible; nothing lost |

## ⚠️ `--dangerously-skip-permissions`

Ralph runs headless, so it skips interactive write prompts. **Only run it in a
sandbox or a dedicated `--worktree`.** Never on your main branch.

## Note on headless credits (2026-06-15+)

`claude -p` draws from the **Agent SDK credit pool**, separate from your
interactive Claude Code subscription. Check your Anthropic console before long
runs.

---

Concept and the worktree/parallel operating model credit: Geoffrey Huntley (the
original "Ralph" loop) and Cole Medin's
[harness-engineering-demo](https://github.com/coleam00/harness-engineering-demo).
This is a clean, generic re-implementation.
