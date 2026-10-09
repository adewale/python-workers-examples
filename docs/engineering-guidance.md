# Shared engineering guidance

Reusable rules from the [2026 Ruff rollout](retrospectives/2026-10-09-ruff-rollout.md).
This document is hosted here and linked from both Workers repositories; the
rules apply beyond Cloudflare Workers. Incident-specific versions and evidence
belong in dated retrospectives and repository lessons, not in timeless rules.

## Diagnose before attributing

1. Record the failing command, check category, commit SHA, and tool/runtime
   versions. Separate lint, types, dependency audits, startup, and behavior.
2. Run the same check on the base revision and the proposed revision under the
   same environment. Do not assume that a failure observed on a PR was caused
   by its diff.
3. If unchanged source now fails, investigate resolved dependencies, generated
   artifacts, runtime/runner changes, external services, and audit database
   updates. Compare one suspected factor at a time before claiming causality.
4. Keep source-backed hypotheses separate from behavior actually reproduced.
   A plausible explanation is not proof.

## Make validation meaningful and repeatable

- Test the observable outcome: bytes, headers, state transitions, or completed
  work. A status code or JSON shape alone is often insufficient.
- A regression test should fail when the relevant fix is removed. Verify that
  negative control when practical; otherwise state precisely what was and was
  not checked. Never imply a deliberate revert test happened if it did not.
- Control external dependencies while preserving the real protocol. A local
  HTTP server can test real client requests without depending on a public
  service's uptime. Assert that requests actually reached it.
- Give tests independent storage, isolate process lifecycles, and run them
  again to expose leaked state. Keep cold-start evidence as well as cached runs.
- Use expected failures only for identified defects reached by the test.
  Assert setup and control paths before marking the known-bug path as xfail;
  an unrelated connection or startup failure must not be treated as confirmation.
- Report skips, expected failures, XPASSes, placeholders, and untested paths
  separately from successful behavior. A green badge is bounded evidence.

## Control changes without weakening gates

- Align the linter version across development dependencies, required-version
  policy, pre-commit, and CI. Pin the versions meant to be reproducible, and
  explicitly identify any intentionally floating toolchain layers.
- Classify runtime, development, and typing dependencies correctly. Do not
  bundle a typing-only package just to satisfy development tooling.
- Fix the vulnerable dependency or incorrect call that a gate identifies.
  Do not disable an audit or type check simply to make a rollout green.
- Keep changes scoped. Separate follow-up coverage and runtime work from the
  claim that a tooling rollout has been completed.
- Before merging, check the exact tested head, all relevant checks, draft state,
  and mergeability. Rebase only when necessary; revalidate changed heads.
  Verify the resulting main-branch checks after merging.

## Leave durable evidence

For each incident, record the date, affected revisions, reproduction command,
tested versions, observed failure, resolution, immutable source/CI links,
validation result, and remaining limitations. Put repository-specific findings
in that repository's lessons document and link to shared rules rather than
copying an incident narrative into every project.

Check repository visibility before publishing a cross-project inventory in a
public repository. Keep private project identities and evidence in an approved
private location; use anonymized counts in public summaries when appropriate.

Do not turn a historical green run into a claim that every project remains
healthy forever. New dependency, service, and runtime changes require fresh
evidence.
