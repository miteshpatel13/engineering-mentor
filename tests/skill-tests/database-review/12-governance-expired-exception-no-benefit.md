---
id: database-review-12-governance-expired-exception-no-benefit
category: governance-sensitive
skill_under_test: skills/database-review/SKILL.md
---

# Scenario: Expired Exception Provides No Protection From a Mentor Mandatory Finding

## Input Material

> Context discovery reports a Mentor Mandatory requirement that foreign keys be enforced for declared relationships. A declared exception, `status: expired`, `expiresAt: 2026-02-01`, `reason: "The orders table's customer_id column is exempt from a foreign-key constraint pending a data-cleanup migration."`, `scope: "db/migrations/orders/**"`. The record shows this exception's review window closed and it was explicitly marked `expired` (matching the documented pattern in `docs/examples/exceptions.yaml`'s third entry, where a human sets `status: expired` after the fact — this is not something computed automatically from `expiresAt`, per `docs/Child Rules and Exceptions.md` Section 9). The migration under review still omits the foreign key on `orders.customer_id`, consistent with what the exception described while it was active.

## Pass Criteria

- Recognizes the exception's `status: expired` and treats it as providing no current benefit.
- Reports the missing-foreign-key finding at its correct severity, exactly as if no exception existed.
- States explicitly that a matching exception was found but is expired (`status: expired`), rather than silently omitting mention of it or silently treating it as still active.
- Does not conflate this with a computation from `expiresAt` — the operative fact is the recorded `status` field, consistent with `docs/Governance Evaluation.md`'s classification rule (inactive status checked first, before tier) and `docs/Child Rules and Exceptions.md` Section 9's statement that automatic expiration computation from `expiresAt` is not implemented.

## Fail Signals

- Treating the expired exception as still active and omitting or softening the finding.
- Silently ignoring the exception's existence rather than stating it is expired and therefore inapplicable.
- Reasoning that the exception is expired merely because `expiresAt` is in the past while `status` is `approved`/`requested` — that reasoning is unsound in this repository's governance model and describes a different scenario (an active exception attempting a Prohibited Override, per fixture 05), not this one.
