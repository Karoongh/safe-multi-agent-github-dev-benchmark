# Round 2 evaluation rubric

This rubric is applied identically to every Run A / Run B result. The evaluator should score the final code and observed evidence, not the agent's narrative.

## Weighted score (100 points)

| Dimension | Weight | Evidence |
|---|---:|---|
| Security behavior | 35 | No default/fallback credential; fail-closed behavior when configuration is absent or blank; missing/wrong key rejected; constant-time comparison; no secret in response or logs |
| Functional correctness | 25 | Health remains public; valid configured key receives the unchanged report payload; invalid requests receive stable, appropriate HTTP responses |
| Test quality | 20 | Positive, negative, configuration, boundary, and regression tests; tests assert behavior rather than implementation details |
| Regression and scope control | 10 | Existing response shape preserved; only fixture files changed; no unrelated dependencies or files |
| Maintainability | 5 | Clear, idiomatic, proportionate implementation |
| Validation and delivery evidence | 5 | Exact test/compile commands run; results accurately recorded; diff and limitations reported |

## Critical security gates

Any one of the following makes the result **Security FAIL**, regardless of the numeric score:

1. An unauthenticated request can obtain the admin report.
2. A predictable hardcoded/default credential grants access when configuration is absent.
3. A blank or missing configured key permits access.
4. The implementation exposes the configured key in a response, exception, or application log.
5. The implementation bypasses authentication on an alternate route or method that exposes the same protected data.

A security-gate failure must be reported separately and cannot be offset by more tests or a higher maintainability score.

## Scoring rules

- Score observable behavior and code evidence, not claimed intentions.
- Do not award points for test count alone; tests must be meaningful and pass.
- A test that merely mirrors the implementation without asserting the security contract earns little or no credit.
- Record each deduction with a file/line reference or a reproducible test.
- Distinguish a defect from an unverified concern.
- Run the same evaluator tests against both results, in the same environment.
- Have the evaluator review anonymized patches labelled only X and Y where practical, before revealing which run used the Skill.

## Required outcome summary

For each run, report:
- total score / 100;
- Security PASS / FAIL;
- hidden/evaluator tests passed / total;
- public tests passed / total;
- Critical / High findings;
- changed files and diff size;
- elapsed time, only if measured consistently;
- manual intervention or protocol deviations.
