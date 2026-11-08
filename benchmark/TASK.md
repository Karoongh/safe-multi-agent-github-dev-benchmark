# Fixed benchmark task

## Prompt

Copy and submit this exact task to the coding agent in both runs:

> Improve the file upload system to support larger files, restrict uploads to allowed file types, safely normalize filenames, and add appropriate tests. Preserve existing behavior where reasonable.

## Acceptance criteria to evaluate

The task is intentionally concise. The agent is expected to inspect the repository and make reasonable engineering decisions. Evaluate the delivered implementation against these concerns:

- **File size / memory:** avoids unbounded whole-file buffering where practical; defines and enforces a clear size limit or otherwise explains its policy.
- **File types:** uses an explicit allowlist and does not rely solely on the client-provided MIME type.
- **Filename safety:** prevents path traversal and unsafe path construction; handles collisions safely or documents its policy.
- **Tests:** adds meaningful positive and negative tests, including relevant security and boundary cases.
- **Compatibility:** preserves the existing successful upload behavior where reasonable and documents any API changes.
- **Error handling:** returns appropriate client errors without leaking unnecessary internals.
- **Maintainability:** implementation is understandable and proportionate to this small application.

These are evaluation dimensions, not a hidden implementation recipe. Do not provide the agent with extra instructions in one run that are absent from the other.

## Validation

At minimum, run:

```bash
python -m pip install -r requirements.txt
pytest -q
```

Also inspect the final diff and manually test important boundary cases where feasible. Record exact commands and outcomes in `benchmark/RESULTS.md`.
