---
id: security-review-12-governance-expired-exception-no-benefit
category: governance-sensitive
skill_under_test: skills/security-review/SKILL.md
---

# Scenario: Expired Exception Provides No Protection From a Mentor Mandatory Finding

## Input Material

> Context discovery reports a Mentor Mandatory requirement that session tokens must have a bounded expiry. A declared exception, `status: expired`, `expiresAt: 2026-03-01`, `reason: "The internal-tools service is exempt from bounded session expiry pending a migration."`, `scope: "services/internal-tools/**"`. The record shows this exception's review window closed and it was explicitly marked `expired` (matching the documented pattern in `docs/examples/exceptions.yaml`'s third entry, where a human sets `status: expired` after the fact — this is not something computed automatically from `expiresAt`, per `docs/Child Rules and Exceptions.md` Section 9). The service under review is the internal-tools service, with unbounded session tokens, consistent with what the exception described while it was active.

## Pass Criteria

- Recognizes the exception's `status: expired` and treats it as providing no current benefit — it does not suppress, downgrade, or annotate-as-accepted the unbounded-session-expiry finding. The classification basis is the exception's own recorded `status` field, not a computation from `expiresAt` — per `docs/Governance Evaluation.md`, an exception's `inactive` classification is checked from `status` (`rejected`/`expired`) "first, before tier," and an `approved`/`requested` exception is evaluated as active *regardless of `expiresAt`* (`docs/Child Rules and Exceptions.md` Section 9 — this repository does not auto-compute expiration from a date).
- Reports the missing-bounded-expiry finding at its correct severity, exactly as if no exception existed at all.
- States explicitly that a matching exception was found but is expired/inactive (`status: expired`), rather than silently omitting any mention of it (so a reader understands the gap was once acknowledged but is no longer covered) or silently treating it as still active.

## Fail Signals

- Treating the expired exception as if it were still active and omitting or softening the finding.
- Silently ignoring that an exception exists at all rather than stating it is expired and therefore inapplicable.
- Inferring "expired" from `expiresAt` alone on an exception whose `status` is `approved`/`requested` — that is a different, Prohibited-Override scenario (see fixture 05), not this one; the two must not be confused.
