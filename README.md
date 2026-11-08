# Safe Multi-Agent GitHub Development — Benchmark

A reproducible, public benchmark for comparing an AI coding workflow **with and without** the Safe Multi-Agent GitHub Development Skill.

> **Status:** Benchmark setup published. No comparative result has been measured yet.

## Objective

Use the same task, starter repository, agent/runtime, and validation commands for two sequential runs:

- **Run A — Baseline:** the coding agent works without the Skill.
- **Run B — Skill-assisted:** the same agent works with the Skill enabled.

The purpose is to observe differences in implementation quality, security reasoning, scope control, testing, validation, and delivery evidence. This repository does not assume that either run will win.

## Benchmark task

See [benchmark/TASK.md](benchmark/TASK.md). Use its task statement verbatim for both runs.

## Repository layout

- `app/main.py` — intentionally minimal starter upload endpoint.
- `tests/test_upload.py` — starter test for valid uploads.
- `benchmark/TASK.md` — fixed task and acceptance criteria.
- `benchmark/PROTOCOL.md` — repeatable run procedure.
- `benchmark/RESULTS.md` — evidence-based results record.

## Quick start

Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

python -m pip install -r requirements.txt
pytest -q
```

The starter test should pass before either run. The initial implementation is deliberately incomplete; it is a benchmark fixture, not production-ready upload handling.

## Fairness rules

1. Start both runs from the exact same starter commit.
2. Use the exact task prompt in `benchmark/TASK.md`.
3. Keep the agent, model, runtime, and relevant settings the same.
4. Do not manually repair the code between runs.
5. Record the actual diff, commands, test output, and agent-reported limitations.
6. Do not treat an agent's claims as proof; inspect the repository and run the checks.
7. Report failures and regressions as well as successes.

See [benchmark/PROTOCOL.md](benchmark/PROTOCOL.md) before starting.

## Results

The results file is intentionally a blank evidence record until both runs have been completed. No performance, security, or quality advantage is claimed in advance.

## Scope and limitations

This is a small, controlled software-engineering exercise focused on file-upload handling. It is not a statistically significant study, a security certification, or proof that the Skill works equally well across every coding agent. Any compatibility statement must be limited to runtimes actually tested.

## Related project

The Skill under evaluation: [safe-multi-agent-github-dev-skill](https://github.com/Karoongh/safe-multi-agent-github-dev-skill)
