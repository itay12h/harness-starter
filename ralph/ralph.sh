#!/usr/bin/env bash
# Ralph loop — feed a spec to fresh headless sessions until DONE.txt, with a hard cap.
#
# Usage:  bash ralph/ralph.sh [MAX_ITERATIONS]     (default 8)
#
# Three rules keep this honest: a checkable goal (the gate), a hard stop (MAX),
# and a separate checker (the code-reviewer sub-agent). Never remove the cap.
set -euo pipefail
cd "$(dirname "$0")/.."

MAX="${1:-8}"
PROMPT_FILE="ralph/PROMPT.md"
DONE_FILE="DONE.txt"

if ! command -v claude >/dev/null 2>&1; then
  echo "⛔ 'claude' CLI not found. Install Claude Code first." >&2
  exit 1
fi
if [ ! -f "ralph/tasks.md" ]; then
  echo "⛔ ralph/tasks.md not found. Copy ralph/tasks.example.md to ralph/tasks.md first." >&2
  exit 1
fi

rm -f "$DONE_FILE"
i=0
while [ ! -f "$DONE_FILE" ] && [ "$i" -lt "$MAX" ]; do
  i=$((i + 1))
  echo "──────────── Ralph · iteration $i / $MAX ────────────"
  # Fresh context each round — the agent reads state from files, not chat history.
  claude -p "$(cat "$PROMPT_FILE")" || echo "(iteration exited non-zero — continuing)"
  # Commit each iteration so every step is reversible.
  git add -A 2>/dev/null && { git diff --cached --quiet || git commit -q -m "ralph: iteration $i" --no-verify; }
done

if [ -f "$DONE_FILE" ]; then
  echo "✅ Done in $i iteration(s): $(cat "$DONE_FILE")"
else
  echo "⛔ Hard stop: hit $MAX iterations without $DONE_FILE. Check reports/ and the spec."
  exit 1
fi
