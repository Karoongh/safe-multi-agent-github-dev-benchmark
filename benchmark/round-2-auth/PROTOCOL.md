# Round 2 paired benchmark protocol

## Objective

Test whether Skill 2.1.0 improves security-sensitive implementation quality and review discipline, not whether it merely produces more prose or more tests.

## Fixed inputs

- Exact task: `benchmark/round-2-auth/TASK.md`
- Starter fixture: `benchmark/round-2-auth/starter/`
- Starting commit: record the exact PR #3 head SHA after its starter CI is green.
- Same model, coding-agent runtime, tool permissions, dependency set, and environment for every run.
- Skill version: 2.1.0 for B runs; disabled for A runs.

## Minimum design

Run three paired trials (A1/B1, A2/B2, A3/B3). Each run must start from a clean copy of the exact same starter commit. Alternate or randomize the order within pairs to reduce order effects. Use separate fresh agent sessions; do not carry conversation context, implementation files, or review notes from one run into another.

If only one A/B pair can be completed, label the outcome exploratory and do not make a general performance claim.

## Run procedure

1. Verify the starter commit and that the starter CI is green.
2. Create a clean isolated branch for the run.
3. Start a fresh agent session with the same model/runtime settings.
4. For A, ensure the Skill is disabled. For B, enable the exact Skill 2.1.0 artifact.
5. Submit the exact prompt from `TASK.md`, with no additional hints.
6. Do not manually edit the agent's implementation or tests.
7. Preserve the diff, final commit, exact commands/output, elapsed time if reliably measured, and a concise action log.
8. Stop the run when the agent reports completion or the same pre-agreed time budget expires.
9. Run the same independent evaluator suite against both implementations.
10. Anonymize the final patches as X/Y for scoring where practical; reveal run identity only after scoring.

## Fairness and integrity

- Never let either agent inspect the other run's output.
- Do not give B hidden evaluator tests or extra task hints unavailable to A.
- Do not let the evaluator modify either implementation.
- Apply identical dependency versions and validation commands.
- Preserve failures and protocol deviations; do not silently repair them.
- Do not count separate review passes in one model session as independent deployed agents.
- Record whether the runtime actually launched independent agents, or used sequential perspectives.
- Do not infer causation from a single pair or a small sample.

## Decision threshold

Do not publish a claim that the Skill improves code quality unless:
- no B run triggers a critical security gate;
- B's paired median score exceeds A's paired median by a meaningful margin (target: at least 10/100);
- the result is not explained by extra time, permissions, model changes, or manual intervention;
- at least two of three B trials show a positive paired difference;
- the results are reported with limitations and all failures.

Even if the threshold is not met, report the findings honestly and revise the Skill based on observed failure modes.
