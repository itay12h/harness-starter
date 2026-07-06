# Fix plan — running log across iterations

The agent maintains this file itself, appending one entry per iteration. This is
its memory between fresh-context runs.

## Iteration 1
- Picked: "Add a `/health` endpoint that returns 200 and `{"status":"ok"}`".
- Added `GET /health` returning `{"status":"ok"}` (200), plus an inline test.
- Validation: `pytest tests/test_health.py` → 1 passed.
- Next: input validation on create-user.

## Iteration 2
- Picked: "Add input validation to the create-user handler".
- Reject empty email and passwords shorter than 8 chars with a 400.
- Validation: `pytest` → 2 passed.
- Next: prove invalid input is rejected.

## Iteration 3
- Picked: "Write a test proving invalid input is rejected with a 400".
- Added `test_create_user_invalid` asserting 400 on a bad payload.
- Validation: full gate (`ruff check` + `pytest`) → all green.
- All tasks checked and gate passes → `touch DONE.txt`.
