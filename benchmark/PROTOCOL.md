# Benchmark protocol

## Purpose

Compare two workflows under controlled, repeatable conditions. This is a small case study, not a statistically powered experiment.

## Before either run

1. Clone this repository.
2. Check out the same starter commit for each run (record its SHA).
3. Create a separate working copy or reset to that exact commit before the second run.
4. Use the same coding agent, model, runtime version, permissions, and relevant settings.
5. Install dependencies and confirm the starter test passes.
6. Record the agent/model/runtime and date in `benchmark/RESULTS.md`.

## Run A — without the Skill

1. Ensure the Safe Multi-Agent GitHub Development Skill is not active for this session.
2. Submit the exact prompt from `TASK.md`, without additions.
3. Allow the agent to complete its work.
4. Do not manually edit its implementation.
5. Save the final diff and transcript or a concise, factual record of the agent's actions.
6. Run the validation commands and record their exact output.

## Reset

Discard the Run A working copy. Recreate it from the recorded starter commit. Do not carry implementation files, tests, or agent context from Run A into Run B.

## Run B — with the Skill

1. Enable the published Skill version being evaluated.
2. Use the same agent/model/runtime and settings as Run A.
3. Submit the exact same prompt from `TASK.md`.
4. Allow the agent to complete its work without manual implementation edits.
5. Save the final diff and transcript or a concise, factual record of the agent's actions.
6. Run the same validation commands and record their exact output.

## Evidence to preserve

For each run, preserve:

- starter commit SHA;
- agent, model, runtime, Skill state/version;
- final commit SHA or patch/diff;
- exact validation commands and exit codes;
- test count and pass/fail summary;
- any security-relevant design decisions;
- incomplete work, failures, and manual intervention;
- elapsed time, if measured consistently.

Do not publish API keys, tokens, private prompts, personal data, or other secrets in logs or screenshots.

## Comparison discipline

- Compare the actual code and test behavior, not just agent explanations.
- A larger diff or more tests is not automatically better.
- Note whether a concern was found, fixed, tested, and independently verified.
- Distinguish observed facts from subjective judgments.
- If either run is interrupted or materially deviates from the protocol, disclose that limitation.
- Do not claim the Skill caused an outcome unless the evidence supports the claim; this two-run exercise only provides a limited comparison.
