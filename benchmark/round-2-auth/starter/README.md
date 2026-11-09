# Round 2 starter — API key authentication

This isolated FastAPI fixture is intentionally vulnerable. The task is defined in
[`../TASK.md`](../TASK.md).

The starter currently uses a predictable fallback credential when
`ADMIN_API_KEY` is unset. This is an insecure behavior that the benchmark task
requires the agent to remove.

Run the starter tests from the repository root:

```bash
python -m pytest -q benchmark/round-2-auth/starter/tests
```

Do not edit files outside this fixture during the benchmark.
