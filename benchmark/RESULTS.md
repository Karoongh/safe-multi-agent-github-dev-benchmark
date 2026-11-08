# Benchmark results

**Status: Run A completed locally; Run B not run.**

This is an interim evidence record. No comparison or Skill-effect conclusion is possible until Run B is completed under the same conditions.

## Run metadata

| Field | Run A — without Skill | Run B — with Skill |
|---|---|---|
| Date | 2026-11-08 | Not run |
| Starter commit SHA | `4d487e7466f940f74d52d6a053ee0d188f110863` | Same starter required |
| Agent / model | ChatGPT coding run / GPT-6 | Pending |
| Runtime | Local execution environment | Pending |
| Python | 3.13.5 | Pending |
| Skill version | None | Safe Multi-Agent GitHub Development 2.1.0 (planned) |
| Final implementation commit | `a6e7208c7d45fa5f8a103c2b0c9a146636c02fb0` | — |
| Duration | Not measured | — |

## Validation

| Check | Run A | Run B |
|---|---|---|
| Dependency installation command | `python -m pip install -r requirements.txt` could not reach PyPI because DNS/network access was unavailable; required packages were already installed | Not run |
| Installed versions | FastAPI 0.128.2; pytest 9.0.2; httpx 0.28.1; python-multipart 0.0.29 | — |
| `pytest -q` | **9 passed** | Not run |
| `python -m compileall -q app tests` | Passed | Not run |
| GitHub Actions | Pending PR workflow result | Not run |

## Findings

### Run A — without Skill

Implemented and tested:
- 10 MiB application-level file-size limit, checked while reading in 64 KiB chunks.
- Extension allowlist for TXT, PDF, PNG, JPG, and JPEG.
- Content checks: UTF-8 validation for TXT and basic file-signature checks for PDF/PNG/JPEG; client MIME type is not trusted.
- Filename normalization, path-component removal, restricted characters, and Windows reserved-name checks.
- Exclusive file creation to avoid overwriting an existing upload; collision fallback uses a random suffix.
- Partial-file cleanup on validation or write errors.
- Nine tests covering valid upload, unsupported extension, mismatched signature, invalid text encoding, path traversal, duplicate names, oversize cleanup, PDF signature, and invalid filename.

Observed limitations:
- PDF/image validation checks signatures only; it does not fully parse or scan files for malware.
- FastAPI/Starlette parses multipart input before this endpoint receives the UploadFile. The endpoint bounds its own copy/write operation, but a reverse proxy or ASGI-level request-body limit is still recommended for production.
- The dependency installation command could not be completed in this environment because external DNS/network access was unavailable; tests used already-installed packages.

### Run B — with Skill

Not run.

## Side-by-side assessment

| Dimension | Run A evidence | Run B evidence | Assessment |
|---|---|---|---|
| Bounded upload handling | 10 MiB limit; 64 KiB reads; oversize test passes | Pending | Pending |
| File-type validation | Extension allowlist; basic signatures / UTF-8; negative tests pass | Pending | Pending |
| Filename/path safety | Normalization and traversal test pass | Pending | Pending |
| Collision handling | Exclusive create and duplicate-name test pass | Pending | Pending |
| Negative and boundary tests | 9 tests pass | Pending | Pending |
| Error handling | 400 / 413 / 415 paths tested | Pending | Pending |
| Scope control and maintainability | Small FastAPI implementation; limitations documented | Pending | Pending |
| Validation and delivery evidence | Local pytest and compileall passed; dependency install blocked by network | Pending | Pending |

## Limitations

This is one small task and one run per condition. It is not statistically significant, a security certification, or proof of general agent performance. The Run A execution was performed in ChatGPT using GPT-6; Run B must use the same model/runtime and starting commit for the comparison to be meaningful.

## Conclusion

**No comparative conclusion yet.** Run A is recorded. Complete Run B from the exact starter commit before drawing any conclusion about the Skill.
