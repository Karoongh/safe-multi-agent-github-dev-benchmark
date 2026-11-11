# T01 Evaluation

## Acceptance
- Empty filename returns HTTP 400.
- Existing valid upload behavior remains unchanged.
- A focused regression test exists and passes.
- No unrelated files or behavior are changed.

## Hidden checks
- Existing upload tests pass.
- Empty filename is rejected.
- A valid non-empty filename remains accepted.
- The implementation does not weaken or skip tests.

## Efficiency expectations
This is intentionally a FAST PATH task. A good Skill-enabled run should not perform broad repository discovery or a full test suite unless evidence requires escalation.
