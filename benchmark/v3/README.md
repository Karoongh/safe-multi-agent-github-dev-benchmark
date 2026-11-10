# V3 Efficiency Task Fixture

This branch is a controlled fixture for the Efficient Coding Agent 3.0.0 benchmark.

## T01 — Isolated bug fix

Prompt:

> Fix the bug in `app/main.py` so that the upload endpoint rejects empty filenames with HTTP 400 while preserving all existing valid upload behavior. Add a focused regression test. Do not refactor unrelated code.

Risk class: FAST

Expected surface:
- `app/main.py`
- `tests/test_upload.py`

Validation:
- targeted upload tests
- final diff inspection

The benchmark runner must execute this exact prompt once with the skill disabled (A) and once with Efficient Coding Agent 3.0.0 enabled (B), from the same starter commit, in fresh isolated sessions. No manual repair is permitted.
