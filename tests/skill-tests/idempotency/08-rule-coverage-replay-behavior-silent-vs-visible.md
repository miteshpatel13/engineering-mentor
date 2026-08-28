---
id: idempotency-08-rule-coverage-replay-behavior-silent-vs-visible
category: rule-coverage
skill_under_test: skills/idempotency/SKILL.md
---

# Scenario: Choosing Between Silent No-Op and Visible Duplicate Signal

## Input Material

> Design idempotency for a "redeem this one-time discount code" operation. Two requests carrying the same discount code arrive from two different sessions of the same logged-in user (e.g. a double-submitted form).

## Pass Criteria

- Correctly identifies this as a case needing a visible duplicate signal, not silent no-op (Rules → Replay Behavior) — the fact that the code was already redeemed is meaningful information the second caller needs (their form submission didn't newly apply a discount), distinct from the webhook-redelivery case (fixture 01) where the duplicate carries no new information.
- States the reasoning for the distinction explicitly (what makes this case different from fixture 01's), not just the conclusion.
- Confirms the underlying enforcement is still constraint-backed (Rules → Constraint-Backed Enforcement) regardless of which replay behavior is chosen — the two Rules are independent decisions.

## Fail Signals

- Defaulting to silent no-op without engaging with why this case differs from a webhook-redelivery scenario.
- Conflating the replay-behavior decision with the enforcement-mechanism decision as if they were the same choice.
