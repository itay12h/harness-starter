# Testing (reference module)

> How to run and write tests here. The `validate` gate and the Stop hook depend
> on this. Replace with your project's real commands.

- **Run all** — `<your test command>`.
- **Run one** — `<how to target a single test/file>`.
- **Where they live** — `<path>`.
- **Conventions** — one behavior per test; arrange / act / assert; no network in
  unit tests.
- **The gate** — a change is not done until the full suite is green. The Stop
  hook (`stop_validate.py`) enforces this, so "looks done" won't slip through.
