# Benchmark results

**Status: Both runs implemented, locally validated, and passed GitHub Actions CI. Comparative review recorded.**

This is a small, single-task case study, not a statistically powered experiment. Both runs started from the same starter commit and used the same model and Python environment. The Skill workflow's five perspectives were performed as separate review passes in one GPT-6 session; they were **not** five independently deployed agents or models.

## Run metadata

| Field | Run A — without Skill | Run B — with Skill |
|---|---|---|
| Date | 2026-11-08 | 2026-11-08 |
| Starter commit SHA | `4d487e7466f940f74d52d6a053ee0d188f110863` | `4d487e7466f940f74d52d6a053ee0d188f110863` |
| Agent / model | ChatGPT / GPT-6 | ChatGPT / GPT-6 |
| Python | 3.13.5 | 3.13.5 |
| Skill version | None | Safe Multi-Agent GitHub Development 2.1.0 |
| Final branch | `benchmark/run-a-baseline` | `benchmark/run-b-with-skill` |
| Final branch head SHA (includes CI workflow fix for B) | `eb73e0d311515790e0485c0b0412ee4d9c26fea7` | `9d0af2bbd2fe0342798a9b0bf2377e1db7238ab3` |
| Duration | Not measured | Not measured |

## Validation

| Check | Run A | Run B |
|---|---|---|
| `python -m pip install -r requirements.txt` | Failed: external DNS/network unavailable | Failed: external DNS/network unavailable |
| Installed FastAPI | 0.128.2 | 0.128.2 |
| Installed pytest | 9.0.2 | 9.0.2 |
| `python -m pytest -q` | **9 passed** | **13 passed** |
| `python -m compileall -q app tests` | Passed | Passed |
| Manual tests outside automated suite | Not recorded | Not recorded |
| GitHub Actions result | **Passed** — run #3, Python 3.11, 9 passed | **Passed** — run #5, Python 3.11, 13 passed; initial CI attempt exposed an import-path issue, fixed by using `python -m pytest -q` |

**Environment distinction:** local validation used the preinstalled Python 3.13.5 / pytest 9.0.2 environment because local DNS prevented dependency installation; pytest 9.0.2 is outside the repository's declared `>=8,<9` range. Both GitHub Actions runs subsequently installed the declared dependencies successfully on Python 3.11 and passed: Run A with 9 tests and Run B with 13 tests (pytest 8.4.2 in CI).

## Findings

### Run A — without Skill

The baseline implementation was improved with:
- a 10 MiB endpoint-level upload limit and chunked reads;
- an extension allowlist and basic signature / UTF-8 checks;
- filename normalization and path traversal mitigation;
- exclusive file creation to avoid overwriting duplicate names;
- cleanup of partial files;
- nine positive and negative tests.

The work was implemented directly, without a recorded independent review plan or decision gate. This describes the recorded workflow, not a claim that no reasoning or review occurred.

### Run B — with Skill 2.1.0

The workflow was applied in sequence:
1. Repository and starter-state inspection; scope and acceptance criteria recorded.
2. Five distinct review perspectives: architecture, implementation, security, performance/reliability, and code quality/testing.
3. Cross-critique of input validation, file handling, collision safety, memory use, compatibility, and test gaps.
4. Judge decision: **APPROVE**, with a focused implementation and explicit deployment limitation.
5. Dedicated branch created from the exact starter SHA; only the app and test files were changed.
6. Implementation and 13 automated tests added.
7. Post-implementation review and test rerun completed.

Implemented and tested:
- 10 MiB endpoint-level size limit with 64 KiB reads;
- allowlist for TXT, PDF, PNG, JPG, and JPEG;
- basic signatures for PDF/PNG/JPEG and incremental UTF-8 validation for TXT;
- normalized basenames, path-component removal, reserved-name checks, and bounded filename stems;
- exclusive file creation and collision-safe random suffixes;
- partial-file cleanup, including cancellation/error paths;
- 13 tests covering valid uploads, invalid types/content, traversal on POSIX and Windows-style paths, collisions, oversize cleanup, MIME spoofing, reserved names, and empty text files.

**Judge score (Run B chosen approach):**

| Criterion | Score / 10 |
|---|---:|
| Correctness | 9 |
| Safety | 8 |
| Change risk | 9 |
| Maintainability | 8 |
| Completeness | 8 |

Decision: **APPROVE**. No unresolved Critical/High issue was identified in the reviewed implementation. The scores are the Judge's structured assessment, not an independent external audit.

## Side-by-side assessment

| Dimension | Run A evidence | Run B evidence | Assessment |
|---|---|---|---|
| Bounded upload handling | 10 MiB limit; chunked reads | Same, with named constants and documented deployment caveat | Comparable endpoint behavior |
| File-type validation | Extension allowlist, signatures / UTF-8 | Same; tests explicitly verify client MIME is not trusted | B has clearer regression evidence |
| Filename/path safety | Normalization and traversal test | POSIX + Windows traversal, reserved names, bounded stems | B covers more edge cases |
| Collision handling | Exclusive creation and duplicate test | Exclusive creation and duplicate test | Comparable |
| Negative and boundary tests | 9 tests pass | 13 tests pass | B has four additional test cases |
| Error handling | 400 / 413 / 415 paths | 400 / 413 / 415 / 409 paths; partial cleanup on cancellation | B has broader explicit coverage |
| Scope control and maintainability | Small implementation | Five-perspective review, Judge gate, post-review | B adds process discipline; code remains small |
| Validation and delivery evidence | Local tests and CI pass | Local tests and CI pass; first CI attempt fixed and rerun passed | Both verified in CI; B required a small workflow invocation fix |

## Security and deployment limitations

- The 10 MiB check bounds the endpoint's own copy/write loop. FastAPI/Starlette multipart parsing occurs before the route receives `UploadFile`; a reverse proxy or ASGI-level request-body limit is still recommended to bound ingress and temporary-spool consumption.
- PDF and image checks inspect file signatures only. They do not fully parse files, scan for malware, or prove that an image is safe to render.
- Production deployment should consider storage outside the web root, authentication/authorization, rate limits, malware scanning where appropriate, and retention/cleanup policies.
- The existing dependency pin for pytest is below the preinstalled version used in this isolated environment. Re-run in network-enabled CI with the declared dependency set.

## Conclusion

In this single case, both runs produced working upload protections and passed their locally executed tests. Run B added four tests and documented more review and delivery evidence, including an explicit Judge decision and post-review. The result is consistent with the Skill improving process structure and review traceability for this task, but it does **not** establish that the Skill caused better runtime correctness or that it will outperform unassisted work generally.

Both runs now have successful network-enabled GitHub Actions CI using the declared dependency constraints. The benchmark is reproducible at the level of this single task and CI environment, but remains a one-task case study rather than evidence of general or statistically significant superiority.
