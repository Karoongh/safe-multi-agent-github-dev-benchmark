# T01 Observed Pilot Results

## Scope

This is the first controlled pilot for T01 of the v3 efficiency benchmark. Four fresh runs were supplied from the same starter commit:

- A1 — Skill disabled
- B1 — Skill v3 enabled
- A2 — Skill disabled
- B2 — Skill v3 enabled

Starter commit:

`baec05c11d469f56fb982457e3c6657295457aeb`

## Observed results

| Metric | A1 | B1 | A2 | B2 |
|---|---:|---:|---:|---:|
| Files examined | 7 | 4 | 4 | 3 |
| Tool calls | 22 | 14 | 11 | 9 |
| Validation executions | 4 | 2 | 2 | 2 |
| Repair iterations | 0 | 0 | 0 | 0 |
| Wall-clock | ~12–14 min | ~9 min | ~6 min | ~5 min |
| Final tests | 2 passed | 2 passed | 2 passed | 2 passed |
| Changed files | 2 | 2 | 2 | 2 |
| Unrelated changes | No | No | No | No |
| Security regression | No | No | No | No |
| Native tokens | unavailable | unavailable | unavailable | unavailable |

## Pair observations

### A1 vs B1

- Files examined: 7 → 4
- Tool calls: 22 → 14
- Validation executions: 4 → 2
- Wall-clock: ~12–14 → ~9 minutes
- Reported quality/security outcome: unchanged

### A2 vs B2

- Files examined: 4 → 3
- Tool calls: 11 → 9
- Validation executions: 2 → 2
- Wall-clock: ~6 → ~5 minutes
- Reported quality/security outcome: unchanged

## Interpretation

The T01 pilot shows a consistent directional reduction in exploration/tooling cost across both paired repetitions while the reported engineering outcome remained equivalent.

This is **pilot evidence only**. It does not establish a general percentage improvement for Skill v3 because:

1. T01 is deliberately a small FAST PATH task.
2. Native token usage was unavailable.
3. Only one task family has been tested.
4. The four runs were executed in an external Coding Agent environment and the benchmark repository does not independently observe their runtime telemetry.

The next required validation is T02 with at least two fresh A/B pairs, followed by higher-risk and cross-module task families.
