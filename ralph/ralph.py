#!/usr/bin/env python3
"""ralph.py — the Ralph loop, cross-platform Python driver.

Feeds PROMPT.md to a fresh headless `claude -p` process each iteration until a
`DONE.txt` sentinel appears or the hard cap is hit. Commits after every
iteration, so every step is reversible.

Two modes:

  In-place (default) — runs on the CURRENT branch, in this directory.
      python ralph/ralph.py
  Simple, but it commits onto whatever branch you're on. Only do this in a
  throwaway checkout.

  Self-isolating worktree (opt-in) — Ralph makes its OWN git worktree on a fresh
  branch, runs the whole loop there, and commits to that branch. Your main tree
  never moves. This is the unit you scale horizontally.
      python ralph/ralph.py --worktree
      # launch several at once, each an isolated agent on its own branch:
      python ralph/ralph.py --worktree --branch ralph/feature-a &
      python ralph/ralph.py --worktree --branch ralph/feature-b &
      wait

Flags / env:
    --max <n>        RALPH_MAX_ITER=10      hard iteration cap (ALWAYS on)
    --timeout <s>    RALPH_ITER_TIMEOUT=1800  per-iteration wall-clock limit
    --worktree       RALPH_WORKTREE=1       run in a fresh worktree + branch
    --branch <name>  RALPH_BRANCH=<name>    branch name (default ralph/run-<ts>)
    --cleanup        RALPH_CLEANUP=1        remove the worktree on success (branch kept)
    --setup <cmd>    RALPH_SETUP=<cmd>      shell command to run once before the loop
                                            (e.g. spin up an isolated DB / install deps)
                     RALPH_WORKTREE_DIR     base dir for worktrees (default ../ralph-worktrees)
                     RALPH_CLAUDE_BIN       override the claude binary

WARNING: --dangerously-skip-permissions bypasses file-write confirmations.
Use only in a sandbox or a dedicated --worktree.

The Ralph loop is a public technique (Geoffrey Huntley et al.); this is a clean
generic driver. Concept & the worktree/parallel pattern credit: Cole Medin's
harness-engineering-demo.
"""
from __future__ import annotations

import datetime
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
LOG_FILE: Path = REPO_ROOT / "ralph" / "ralph.log"


def _ts() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg: str) -> None:
    line = f"[{_ts()}] {msg}"
    print(line, flush=True)
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def _bin(name: str, override: str | None = None) -> str:
    return override or shutil.which(name) or name


def parse_config() -> dict:
    argv = sys.argv[1:]

    def flag(name: str, env: str) -> bool:
        return (name in argv) or os.environ.get(env, "").lower() in ("1", "true", "yes")

    def opt(name: str, env: str, default):
        if name in argv:
            i = argv.index(name)
            if i + 1 < len(argv):
                return argv[i + 1]
        return os.environ.get(env, default)

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    return {
        "max_iter": int(opt("--max", "RALPH_MAX_ITER", 10)),
        "timeout": int(opt("--timeout", "RALPH_ITER_TIMEOUT", 1800)),
        "worktree": flag("--worktree", "RALPH_WORKTREE"),
        "branch": opt("--branch", "RALPH_BRANCH", f"ralph/run-{ts}"),
        "cleanup": flag("--cleanup", "RALPH_CLEANUP"),
        "setup": opt("--setup", "RALPH_SETUP", None),
        "wt_base": Path(os.environ.get("RALPH_WORKTREE_DIR", str(REPO_ROOT.parent / "ralph-worktrees"))),
        "claude_bin": os.environ.get("RALPH_CLAUDE_BIN"),
    }


def create_worktree(branch: str, wt_base: Path) -> Path:
    wt_base.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", branch).strip("-")
    wt_path = wt_base / slug
    if wt_path.exists():
        wt_path = wt_base / f"{slug}-{datetime.datetime.now().strftime('%H%M%S')}"
    git = _bin("git")
    r = subprocess.run([git, "worktree", "add", str(wt_path), "-b", branch],
                       cwd=str(REPO_ROOT), capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git worktree add failed: {(r.stderr or r.stdout).strip()}")
    return wt_path


def git_commit(work_root: Path, iteration: int) -> None:
    git = _bin("git")
    subprocess.run([git, "add", "-A"], cwd=str(work_root), check=False)
    staged = subprocess.run([git, "diff", "--cached", "--quiet"], cwd=str(work_root))
    if staged.returncode != 0:
        subprocess.run([git, "commit", "-m", f"ralph: iteration {iteration}", "--no-verify"],
                       cwd=str(work_root), check=False)
        log(f"git commit: iteration {iteration}")
    else:
        log("git: nothing to commit this iteration")


def run_claude(spec: str, work_root: Path, claude_bin: str | None, timeout: int) -> None:
    claude = _bin("claude", claude_bin)
    result = subprocess.run(
        [claude, "-p", "--output-format", "json",
         "--dangerously-skip-permissions", "--max-turns", "40"],
        input=spec, capture_output=True, text=True, encoding="utf-8",
        timeout=timeout, cwd=str(work_root),
    )
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(result.stdout or "")
        if result.stderr:
            f.write(result.stderr)


def _default_base() -> str:
    git = _bin("git")
    r = subprocess.run([git, "symbolic-ref", "--short", "HEAD"], cwd=str(REPO_ROOT),
                       capture_output=True, text=True)
    return (r.stdout.strip() or "main")


def summary(cfg: dict, work_root: Path, branch: str, done: bool) -> None:
    if not cfg["worktree"]:
        return
    line = "=" * 64
    print("\n" + line + "\nRalph worktree run summary\n" + line)
    print(f"  Result:   {'DONE (spec complete)' if done else 'stopped (cap/timeout)'}")
    print(f"  Branch:   {branch}")
    print(f"  Worktree: {work_root}")
    print(f"  Log:      {LOG_FILE}")
    print(f'  Review:   git -C "{REPO_ROOT}" diff {_default_base()}..{branch}')
    print(f'  Merge:    git -C "{REPO_ROOT}" merge {branch}   (or open a PR)')
    print(f'  Discard:  git -C "{REPO_ROOT}" worktree remove "{work_root}" --force '
          f'&& git -C "{REPO_ROOT}" branch -D {branch}')
    print(line)


def main() -> None:
    global LOG_FILE
    cfg = parse_config()
    branch = cfg["branch"]

    if cfg["worktree"]:
        try:
            work_root = create_worktree(branch, cfg["wt_base"])
        except RuntimeError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            sys.exit(1)
        LOG_FILE = work_root / "ralph" / "ralph.log"
        log(f"=== worktree mode: branch '{branch}' at {work_root} ===")
    else:
        work_root = REPO_ROOT
        LOG_FILE = REPO_ROOT / "ralph" / "ralph.log"

    if cfg["setup"]:
        log(f"setup: {cfg['setup']}")
        subprocess.run(cfg["setup"], shell=True, cwd=str(work_root), check=False)

    prompt_file = work_root / "ralph" / "PROMPT.md"
    tasks_file = work_root / "ralph" / "tasks.md"
    done_file = work_root / "DONE.txt"

    if not prompt_file.exists():
        print(f"ERROR: PROMPT.md not found at {prompt_file}", file=sys.stderr)
        sys.exit(1)
    if not tasks_file.exists():
        print("ERROR: ralph/tasks.md not found. Copy ralph/tasks.example.md first.", file=sys.stderr)
        sys.exit(1)
    if not shutil.which(_bin("claude", cfg["claude_bin"])):
        print("ERROR: 'claude' CLI not found. Install Claude Code first.", file=sys.stderr)
        sys.exit(1)

    spec = prompt_file.read_text(encoding="utf-8")
    if done_file.exists():
        done_file.unlink()

    log("=== Ralph loop started ===")
    log(f"max_iter={cfg['max_iter']} | timeout={cfg['timeout']}s per iteration")

    done = False
    iteration = 0
    while iteration < cfg["max_iter"]:
        iteration += 1
        log(f"--- Iteration {iteration} / {cfg['max_iter']} ---")
        try:
            run_claude(spec, work_root, cfg["claude_bin"], cfg["timeout"])
            log(f"claude finished iteration {iteration}")
        except subprocess.TimeoutExpired:
            log(f"iteration {iteration} timed out after {cfg['timeout']}s")
        except Exception as exc:
            log(f"iteration {iteration} error: {exc}")

        git_commit(work_root, iteration)

        if done_file.exists():
            log(f"DONE.txt found — spec complete after {iteration} iteration(s).")
            done = True
            break
        log(f"iteration {iteration} complete — not done yet.")

    if not done:
        log(f"HARD STOP: hit {cfg['max_iter']} iterations without DONE.txt. Review ralph/ralph.log.")

    if cfg["worktree"] and cfg["cleanup"] and done:
        git = _bin("git")
        subprocess.run([git, "worktree", "remove", str(work_root), "--force"],
                       cwd=str(REPO_ROOT), check=False)
        log(f"cleanup: removed worktree (branch '{branch}' kept)")

    summary(cfg, work_root, branch, done)
    sys.exit(0 if done else 1)


if __name__ == "__main__":
    main()
