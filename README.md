# Harness Starter

A **clone-this-to-start** Claude Code project. It's not an app — it's the
**harness**: the layer you wrap around the model so it can work on your codebase
reliably, check its own work, and run in a loop without you babysitting it.

> `Agent = Model + Harness.` The model you rent. The harness is yours — and it's
> where the leverage is. This repo is a ready-made one.

Language-neutral skeleton, generalized from Cole Medin's
[harness-engineering-demo](https://github.com/coleam00/harness-engineering-demo).
Bring your own app; keep the `.claude/` + `ralph/` layer.

## What's in the box

```
.
├── CLAUDE.md                 # project DNA — loaded into every session
├── .mcp.json                 # outside tools (MCP servers)
├── .claude/
│   ├── settings.json         # wires the hooks + permissions
│   ├── context/              # reference modules, pulled in on demand
│   ├── skills/               # plan · implement · validate · review
│   ├── agents/               # code-reviewer sub-agent
│   └── hooks/                # security · lint · stop-validation
└── ralph/                    # the loop: run a spec to done, hands-off
    ├── ralph.sh              # bash driver
    ├── ralph.py              # python driver: worktree isolation + parallel runs
    ├── PROMPT.md
    ├── tasks.example.md
    └── example-run/          # a captured run to replay (demo insurance)
```

`.claude/context/` ships template modules — `architecture` · `auth` · `testing`
· `timezones` — so `CLAUDE.md` stays light and the deep stuff loads on demand.

### The two steering directions (feedforward + feedback)
- **Feedforward — before it acts:** `CLAUDE.md`, `.claude/context/*`, and the
  skills give the model the rules up front, so it's likelier to get it right the
  first time.
- **Feedback — after it acts:** the hooks are sensors. They run automatically and
  **shout problems back into the loop** — a lint after every edit, a security
  guard that denies dangerous actions, and a stop-gate that won't let the agent
  "finish" until the checks actually pass.

## Quick start

```bash
git clone <this-repo> my-project && cd my-project
claude                       # open Claude Code here
```

Then try the flow:

1. **Plan** — ask Claude to use the `plan` skill on a small task. It writes a
   plan to `plans/<slug>.md`. **Read every line before you continue.**
2. **Implement** — the `implement` skill executes the plan task by task.
3. **Validate** — the `validate` skill (and the `Stop` hook) run your gate.
4. **Review** — the `review` skill delegates to the `code-reviewer` sub-agent.

## Run the loop (Ralph)

Hand it a spec and walk away. It works one task at a time with fresh context each
round, commits every step, and stops when it writes `DONE.txt` — or when it hits
the hard cap.

```bash
cp ralph/tasks.example.md ralph/tasks.md   # your task list
bash ralph/ralph.sh 8                       # bash · max 8 rounds — always cap it
python3 ralph/ralph.py --max 8              # python · adds worktree + parallel
```

For **isolated / parallel** runs, `ralph.py --worktree` gives each run its own git
branch and working copy so you can launch several at once. A worked **captured
run** lives in `ralph/example-run/` as demo insurance. Full docs: `ralph/README.md`.

Three rules keep this loop honest: a **checkable goal**, a **hard stop**, and a
**separate checker**. All three are wired in (the validate gate, the iteration
cap, and the code-reviewer sub-agent). See `ralph/PROMPT.md`.

## Make it yours

- Rewrite `CLAUDE.md` for your project. Keep it lean (200–500 lines). Every rule
  should trace back to a real mistake the agent made.
- Point the hooks' `validate` step at your real test command
  (`.claude/hooks/stop_validate.py`).
- Add MCP servers in `.mcp.json`.
- Delete what you don't need. Each piece is a bet on something the model can't do
  alone yet — when it can, cut the piece.

---

Built for the **Claude Code Workshop**. This is **original template code** — a
clean re-implementation of the harness patterns, so you can license and share it
however you like. It was *informed by*, not copied from, Cole Medin's
[harness-engineering-demo](https://github.com/coleam00/harness-engineering-demo)
(which ships with no license, so nothing was lifted verbatim). Concept credit:
Cole Medin, Addy Osmani, Birgitta Böckeler, and Geoffrey Huntley (the Ralph loop).
For the full battle-tested app + harness, clone Cole's repo directly.
