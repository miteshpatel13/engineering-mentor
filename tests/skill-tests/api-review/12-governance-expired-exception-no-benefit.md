---
id: api-review-12-governance-expired-exception-no-benefit
category: governance-sensitive
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: Expired Exception Provides No Protection From a Mentor Mandatory Finding

## Input Material

> Context discovery reports a Mentor Mandatory requirement that breaking changes to an existing contract require a versioning accommodation. A declared exception, `status: expired`, `expiresAt: 2026-01-15`, `reason: "The /reports endpoint's field removal is exempt from the versioning requirement pending client migration."`, `scope: "endpoints/reports/**"`. The record shows this exception's review window closed and it was explicitly marked `expired` (matching the documented pattern in `docs/examples/exceptions.yaml`'s third entry, where a human sets `status: expired` after the fact — this is not something computed automatically from `expiresAt`, per `docs/Child Rules and Exceptions.md` Section 9). The change under review still removes the field with no versioning accommodation, consistent with what the exception described while it was active.

## Pass Criteria

- Recognizes the exception's `status: expired` and treats it as providing no current benefit.
- Reports the breaking-change finding at its correct severity (HIGH, per the existing positive example's pattern), exactly as if no exception existed.
- States explicitly that a matching exception was found but is expired (`status: expired`), rather than silently omitting mention of it or silently treating it as still active.
- Does not conflate this with a computation from `expiresAt` — the operative fact is the recorded `status` field, consistent with `docs/Governance Evaluation.md`'s classification rule and `docs/Child Rules and Exceptions.md` Section 9.

## Fail Signals

- Treating the expired exception as still active and omitting or softening the finding.
- Silently ignoring the exception's existence rather than stating it is expired and therefore inapplicable.
- Reasoning that the exception is expired merely because `expiresAt` is in the past while `status` is `approved`/`requested` — that describes a different scenario (an active exception attempting a Prohibited Override against a Mandatory requirement, see the new fixture 21), not this one.
