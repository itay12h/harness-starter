# CLAUDE.md — Project DNA

> Loaded into the top of every session, before the first message. This is the
> steering. Keep it lean (aim 200–500 lines). Every rule below should trace back
> to a real mistake — earn each line, don't guess it.

## Project

<!-- One paragraph: what this is, the stack, the shape. Replace this. -->
A working template. Swap this section for your real project overview: what it
does, the language/framework, where the important code lives.

## Rules

- Prefer the simplest thing that works. No new dependency without asking.
- Never touch production URLs, credentials, or `.env` files.
- Never run destructive commands (`rm -rf`, force-push, dropping data) without an
  explicit go-ahead.
- Match the surrounding code — its style, naming, and structure — over your own
  defaults.
- If you make the same mistake twice, that's a signal: propose a new rule for
  this file.

## How we work here

- **Plan before you build.** For anything non-trivial, use the `plan` skill and
  write the plan to `plans/` first. Small change? Skip it.
- **Validate before you call it done.** Run the gate (`validate` skill / the Stop
  hook). "Looks done" is not done.
- **A separate checker.** Use the `code-reviewer` sub-agent on diffs — you are
  too optimistic about your own code.

## Commands

<!-- Replace with your real commands so the agent and the hooks can run them. -->
- Install: `<your install command>`
- Test / gate: `<your test command>`   <!-- also wired in stop_validate.py -->
- Lint: `<your lint command>`

## Reference modules (read on demand, not always)

Deeper context lives in `.claude/context/` so this file stays light:

- `.claude/context/architecture.md` — how the pieces fit together.
- Add more as needed (auth, testing, data model, gotchas). Link them here.
