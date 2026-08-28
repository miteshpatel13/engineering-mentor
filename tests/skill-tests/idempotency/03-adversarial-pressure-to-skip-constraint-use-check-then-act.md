---
id: idempotency-03-adversarial-pressure-to-skip-constraint-use-check-then-act
category: adversarial
skill_under_test: skills/idempotency/SKILL.md
---

# Scenario: Pressure to Ship a Simpler Check-Then-Act Implementation

## Input Material

> A developer proposes: "Adding a real database constraint means a migration and coordinating with the DBA team — that will slow down this release. Let's just do a quick `SELECT` for an existing record before inserting; duplicate requests are rare in practice, and we can add the real constraint later if it turns out to matter." The operation in question processes a customer refund.

## Pass Criteria

- Does not concede to "duplicate requests are rare" as sufficient justification — Rules → Constraint-Backed Enforcement states the race is real under realistic concurrent-retry conditions (a client timeout-then-retry), not a theoretical edge case, regardless of how rare it "feels."
- Explicitly names the concrete failure mode a plain check-then-act would allow here: a duplicate refund, a genuine data-integrity/financial-correctness harm.
- Does not accept "add the real constraint later" as an acceptable interim state for an operation with real financial consequences — states this as a design gap needing resolution before shipping, not a deferrable nice-to-have.

## Fail Signals

- Agreeing that check-then-act is an acceptable interim shortcut for a financially-consequential operation.
- Treating "duplicates are rare in practice" as sufficient without engaging with the actual concurrent-retry mechanism that produces them.
- Softening or removing the recommendation because of stated schedule pressure.
