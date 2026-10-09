# Ruff 0.16.0 rollout retrospective

Recorded: 2026-10-09. Rollout merges span 2026-07-26 to 2026-10-09.

## Outcome and scope

All **29** PRs on the rollout branch `agent/upgrade-ruff-0.16` were merged.
Autowiki was explicitly excluded. GitHub's PR inventory was checked on the
recorded date; the public links below preserve the shareable scope independently
of this chat. One private-repository PR is included only as an anonymized count.
This is a completed tooling rollout, not a claim that every repository's
current application behavior has been exhaustively tested.

The last two merges were
[python-workers-issues #2](https://github.com/adewale/python-workers-issues/pull/2)
and [python-workers-examples #2](https://github.com/adewale/python-workers-examples/pull/2).
Their PR and post-merge checks passed. No production Workers deployment was
performed during those repairs.

## What blocked progress

Red checks were not all Ruff failures. The rollout also encountered dependency
audits, type-checker errors, and integration failures:

| Project / evidence | Failing check encountered |
| --- | --- |
| [pythonbyexample #12](https://github.com/adewale/pythonbyexample/pull/12) | npm audit: high-severity sharp advisories through the Miniflare/Wrangler dependency path |
| [claude-history-explorer #12](https://github.com/adewale/claude-history-explorer/pull/12) | Production dependency audit: high-severity Hono advisories |
| [planet_cf #16](https://github.com/adewale/planet_cf/pull/16) | ty: invalid argument types |
| [xampler #1](https://github.com/adewale/xampler/pull/1) | ty: redundant cast reported as a failure |
| [olsen #9](https://github.com/adewale/olsen/pull/9) | govulncheck: reachable TIFF vulnerabilities in golang.org/x/image |
| [Workers examples #2](https://github.com/adewale/python-workers-examples/pull/2) | Legacy package installation, startup/runtime contracts, and persistent test state |
| [Workers issues #2](https://github.com/adewale/python-workers-issues/pull/2) | External header-echo availability and startup/runtime contracts |

The Workers failures also reproduced without the Ruff changes. Comparing the
base and PR behavior prevented us from treating the linter upgrade as the
automatic explanation. The eventual repairs changed the toolchain and runtime
configuration as well as test infrastructure; see the repository-specific
evidence rather than attributing every symptom to one dependency.

## Lessons we will reuse

- Compare base and head in a controlled environment before assigning blame.
- Treat lint, types, audits, startup, and behavioral failures as distinct gates.
- Align tool versions, and document which other layers still float.
- Exercise real protocols against controlled services: local echoing removed
  public-service uptime from CI without mocking away HTTP behavior.
- Validate work actually completed: the workflow test now waits for `complete`.
- Isolate storage and terminate complete server process groups between tests.
- Read the test and fixture before interpreting a green badge, xfail, or XPASS.
- Keep evidence and limitations beside the code, not solely in chat history.

The operational checklist is [shared engineering guidance](../engineering-guidance.md).
Detailed findings are in the [examples lessons](../../LESSONS_LEARNED.md) and
[issues lessons](https://github.com/adewale/python-workers-issues/blob/main/LESSONS_LEARNED.md).

## Final Workers verification

The repair pinned Ruff 0.16.0, uv 0.12.3 in CI, and workers-py 1.17.7 in the
example development groups. CI selected Python 3.13. Local Docker verification
observed Wrangler 4.149.0; Wrangler was not pinned by this repair.

| Repository | PR CI | Post-merge CI | Integration result in PR CI |
| --- | --- | --- | --- |
| python-workers-examples | [successful run](https://github.com/adewale/python-workers-examples/actions/runs/37918860898) | [successful run](https://github.com/adewale/python-workers-examples/actions/runs/37919180915) | 8 passed, 1 xfailed, 1 xpassed; Ruff passed |
| python-workers-issues | [successful run](https://github.com/adewale/python-workers-issues/actions/runs/37918858835) | [successful run](https://github.com/adewale/python-workers-issues/actions/runs/37919064552) | 2 passed, 3 skipped, 1 xfailed; Ruff passed |

Merged revisions:
[examples `a3192a8`](https://github.com/adewale/python-workers-examples/commit/a3192a8bdae07b8b699a5dfb9eba24d7854e94e5),
[issues `17e2a28`](https://github.com/adewale/python-workers-issues/commit/17e2a28d4ac2d5439aaf8470866c5e7a94ededf0).
These links are dated receipts, not continuously updated health indicators.

## Remaining work, separate from the rollout

- Replace the LangChain placeholder test; its XPASS proves nothing about a
  running LangChain Worker.
- Exercise Workers AI in a supported environment. The current xfail fixture
  prevents its server from starting, so the expected failure is not validation.
- Run the three deployment-only R2 tests with explicit authorization for a
  suitable deployment; they were skipped in this verification.
- Continue tracking the reproduced httpx User-Agent stripping bug. In the
  issues suite, real-request assertions now run before its expected failure.
- Decide the remaining floating toolchain/version policy and validate future
  upgrades, including runner-image changes.

These are coverage or platform follow-ups, not outstanding Ruff rebases.

## Rollout inventory

Each of the 28 public PRs below was merged when this retrospective was recorded.
One additional private-repository PR was also merged; its identity and link are
omitted from this public document. Together they account for all 29 merges.

- [agentic-mermaid #229](https://github.com/adewale/agentic-mermaid/pull/229)
- [aha #20](https://github.com/adewale/aha/pull/20)
- [anti-slop-writing #16](https://github.com/adewale/anti-slop-writing/pull/16)
- [atlas #35](https://github.com/adewale/atlas/pull/35)
- [audit-skill #9](https://github.com/adewale/audit-skill/pull/9)
- [cfboundary #1](https://github.com/adewale/cfboundary/pull/1)
- [cfdoctor #18](https://github.com/adewale/cfdoctor/pull/18)
- [claude-history-explorer #12](https://github.com/adewale/claude-history-explorer/pull/12)
- [geist_fabrik #82](https://github.com/adewale/geist_fabrik/pull/82)
- [good-pr #13](https://github.com/adewale/good-pr/pull/13)
- [good-readme #9](https://github.com/adewale/good-readme/pull/9)
- [good-repo #10](https://github.com/adewale/good-repo/pull/10)
- [guardrails-skill #12](https://github.com/adewale/guardrails-skill/pull/12)
- [keyboardia #72](https://github.com/adewale/keyboardia/pull/72)
- [olsen #9](https://github.com/adewale/olsen/pull/9)
- [oshineye-dev #2](https://github.com/adewale/oshineye-dev/pull/2)
- [planet_cf #16](https://github.com/adewale/planet_cf/pull/16)
- [python-workers-examples #2](https://github.com/adewale/python-workers-examples/pull/2)
- [python-workers-issues #2](https://github.com/adewale/python-workers-issues/pull/2)
- [python-workers-skill #9](https://github.com/adewale/python-workers-skill/pull/9)
- [pythonbyexample #12](https://github.com/adewale/pythonbyexample/pull/12)
- [skill-eval-harness #50](https://github.com/adewale/skill-eval-harness/pull/50)
- [skill_scanner #11](https://github.com/adewale/skill_scanner/pull/11)
- [slide-maker #13](https://github.com/adewale/slide-maker/pull/13)
- [swiss-poster-skill #17](https://github.com/adewale/swiss-poster-skill/pull/17)
- [tasche #14](https://github.com/adewale/tasche/pull/14)
- [testing-best-practices #23](https://github.com/adewale/testing-best-practices/pull/23)
- [xampler #1](https://github.com/adewale/xampler/pull/1)
