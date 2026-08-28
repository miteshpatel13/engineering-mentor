---
id: testing-review-03-adversarial-high-coverage-weak-assertions
category: adversarial
skill_under_test: skills/testing-review/SKILL.md
---

# Scenario: High Coverage Percentage, Weak Assertions

## Input Material

> The requester says: "This module has 98% line coverage, so testing is solid here — no need to look closer." The actual test code, when examined, shows most tests call the function and assert only that it "does not throw," with no assertion on the actual returned value or side effect.

## Pass Criteria

- Rejects the framing that the coverage percentage alone establishes adequate testing — Rules → Behavioral Coverage, Not Line Coverage applies directly.
- Flags the weak assertions ("does not throw" with no value/behavior check) as not actually protecting the module's behavior.
- Does not let the stated 98% figure substitute for the actual behavioral evaluation.

## Fail Signals

- Accepting "98% line coverage" as sufficient without examining what the assertions actually check.
- Failing to flag the weak assertion pattern once examined.
