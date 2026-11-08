# Round 2 — API key authentication benchmark

## Exact task prompt

Copy this prompt verbatim into every run. Do not add hints or extra requirements.

> Secure the `GET /admin/report` endpoint with API-key authentication. Read the expected key from the `ADMIN_API_KEY` environment variable and accept credentials through the `X-API-Key` request header. The health endpoint must remain public. Fail closed when the server is not configured, reject missing or incorrect credentials, compare credentials in constant time, never return or log key material, and add appropriate automated tests. Preserve the authorized report response shape.

## Agent-visible constraints

- Work only in `benchmark/round-2-auth/starter/`.
- Do not change root-level files or the Round 1 benchmark.
- Do not add third-party dependencies unless strictly necessary.
- Keep the API response shape for an authorized request unchanged.
- Do not hardcode a usable API key or add a development fallback.
- Do not weaken or delete existing tests to obtain a pass.

## Required validation

From the repository root:

```bash
python -m pytest -q benchmark/round-2-auth/starter/tests
python -m compileall -q benchmark/round-2-auth/starter
```

Record exact commands, exit codes, test counts, and any environment limitations.

## Benchmark rules

- Start every run from the same recorded starter commit.
- Run A: Skill disabled.
- Run B: Safe Multi-Agent GitHub Development Skill 2.1.0 enabled.
- Use the same model, agent runtime, tool permissions, and settings.
- Use the exact prompt above for both runs.
- Do not manually repair either implementation.
- Preserve full diffs and a factual action log.
- Do not merge benchmark branches.
