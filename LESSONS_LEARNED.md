# Lessons learned

## 2026-10-09 — Ruff rollout exposed Workers runtime and test-harness failures

The Ruff upgrade was not sufficient to explain the red integration checks:
the failures also reproduced without the Ruff changes. Treat a lint upgrade
and a runtime repair as separate hypotheses, even when they share a PR.

### Evidence and resolution

[PR #2](https://github.com/adewale/python-workers-examples/pull/2) contains the
fixes. The merged revision is
[`a3192a8`](https://github.com/adewale/python-workers-examples/commit/a3192a8bdae07b8b699a5dfb9eba24d7854e94e5).
Both the [PR CI run](https://github.com/adewale/python-workers-examples/actions/runs/37918860898)
and the [post-merge CI run](https://github.com/adewale/python-workers-examples/actions/runs/37919180915)
passed the integration suite and Ruff.

- **Runtime dependencies are not typing dependencies.** Remove typing-only
  `webtypy` from the runtime dependency lists. The previous toolchain's legacy
  Pyodide package-installation path failed with newer pip/urllib3. Update the
  Workers CLI as part of the runtime repair rather than merely increasing a
  server-startup timeout.
- **Worker import time is not request time.** FastAPI's telemetry initialization
  needed entropy unavailable during Worker startup. Keep the application and
  routes in `src/app.py`, and import that module inside `Default.fetch` so the
  existing app is initialized in request context.
- **Unused bindings can have side effects.** D1's unused AI binding made the
  tested Wrangler version request Cloudflare credentials even for local
  development. Remove the binding that the example does not use; do not add
  production credentials to make an otherwise local test pass.
- **Compatibility flags are part of the runtime contract.** Add
  `python_workflows` alongside `python_workers`. Keep awaiting the workflow
  binding calls, and test that the DAG reaches `complete`, not just that its
  status endpoint returns JSON.
- **State and processes must be isolated.** A repeated Durable Objects run
  inherited a message left by an earlier run. Give each test temporary storage,
  use that same path when initializing its D1 database, and terminate the
  entire dev-server process group rather than only the parent `uv` process.
- **Cold startup differs from a cached run.** Allow dependency downloads for
  every example in CI, and notice when the startup process exits. Timeout and
  diagnostic handling should not hide an immediate startup failure.

### Tested environment and commands

These are the versions used for the repair, not a promise that every layer is
locked indefinitely:

| Layer | Version / policy |
| --- | --- |
| Ruff / pre-commit hook | 0.16.0, aligned with `required-version` |
| uv | 0.12.3, pinned in CI |
| workers-py | 1.17.7, pinned in the example development groups |
| Python | 3.13 selected in CI; local Docker used 3.13.14 and PR CI used 3.13.15 |
| Wrangler | 4.149.0 observed during local verification; not pinned by this repair |
| Runner | Linux Docker locally; GitHub's clean `ubuntu-latest` runner for CI |

```sh
uv sync --dev
UV_PYTHON=3.13 CI=true uv run pytest -vv
uv run ruff check .
```

The PR CI result was **8 passed, 1 xfailed, 1 xpassed**; Ruff passed.
No production deployment was performed.

### What green CI does not establish

- `test_05_langchain` is a placeholder containing `pass`. Its XPASS is not
  evidence that LangChain works.
- The dev-server fixture does not start Workers for tests marked `xfail`.
  Consequently, the Workers AI expected failure does not verify the AI path.
- The suite exercises selected local examples, not every directory, remote
  deployment, or platform capability. The Cron test checks the fetch response,
  not a scheduled invocation.
- Floating Wrangler/runtime versions and the runner image can still change.
  Future toolchain upgrades need their own recorded compatibility run.

Follow-ups are real LangChain and Workers AI coverage, explicit toolchain
version policy, and tests for capabilities outside the current local suite.
They are not unfinished Ruff merges.

See the [shared engineering guidance](docs/engineering-guidance.md),
[cross-project retrospective](docs/retrospectives/2026-10-09-ruff-rollout.md),
and [Workers issues lessons](https://github.com/adewale/python-workers-issues/blob/main/LESSONS_LEARNED.md)
for the reusable rules and companion findings.
