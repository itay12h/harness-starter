---
name: review
description: Get an independent review of the current diff by delegating to the code-reviewer sub-agent. Use before merging or calling a change done.
---

# Review

The maker never grades its own work. Delegate to a fresh reviewer.

## Steps

1. Gather the diff (`git diff` against the base branch).
2. Hand it to the `code-reviewer` sub-agent.
3. Relay its findings ranked by severity. Treat blockers as blocking — fix them
   before you call the change done.
