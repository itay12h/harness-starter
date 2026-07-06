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
    ├── ralph.sh
    ├── PROMPT.md
    └── tasks.example.md
```

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
round, and stops when it writes `DONE.txt` — or when it hits the hard cap.

```bash
cp ralph/tasks.example.md ralph/tasks.md   # your task list
bash ralph/ralph.sh 8                       # max 8 rounds — always cap it
```

Three rules keep this loop honest: a **checkable goal**, a **hard stop**, and a
**separate checker**. All three are wired in (the validate gate, the `8` cap, and
the code-reviewer). See `ralph/PROMPT.md`.

## Make it yours

- Rewrite `CLAUDE.md` for your project. Keep it lean (200–500 lines). Every rule
  should trace back to a real mistake the agent made.
- Point the hooks' `validate` step at your real test command
  (`.claude/hooks/stop_validate.py`).
- Add MCP servers in `.mcp.json`.
- Delete what you don't need. Each piece is a bet on something the model can't do
  alone yet — when it can, cut the piece.

---

Built for the **Claude Code Workshop**. Harness concept & demo credit:
Cole Medin, Addy Osmani, Birgitta Böckeler. MIT-style — clone, adapt, ship.
