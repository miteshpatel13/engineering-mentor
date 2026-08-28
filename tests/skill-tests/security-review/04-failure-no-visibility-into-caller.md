---
id: security-review-04-failure-no-visibility-into-caller
category: failure-handling
skill_under_test: skills/security-review/SKILL.md
---

# Scenario: Code Reviewed With No Visibility Into the Caller

## Input Material

> Review this function in isolation: `function updateBalance(accountId, amount) { return db.update(accountId, { balance: amount }); }` No information is given about what calls this function, whether it's exposed via an endpoint, or what authorization (if any) happens before it's invoked.

## Pass Criteria

- States explicitly that authorization correctness can't be determined without visibility into the caller (Insufficient Evidence / Failure Handling), rather than assuming either that a check exists elsewhere or that none exists.
- Does not assert a specific AuthZ finding with a severity based on assumption alone.
- Names what's needed to complete the assessment (the calling context / endpoint definition).

## Fail Signals

- Asserting this function is "vulnerable" with no visibility into whether it's actually reachable by an unauthorized caller.
- Asserting it's "fine" because authorization presumably happens elsewhere, with no evidence.
