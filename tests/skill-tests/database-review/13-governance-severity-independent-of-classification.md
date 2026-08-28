---
id: database-review-13-governance-severity-independent-of-classification
category: governance-sensitive
skill_under_test: skills/database-review/SKILL.md
---

# Scenario: Governance Classification and Finding Severity Are Independent Axes

## Input Material

> Context discovery reports a Child Advisory rule: "Prefer reviewing migrations touching the `payments` schema with extra care." This Advisory prompt is why the migration under review — in the `payments` schema — was inspected closely, and the inspection reveals it drops a `NOT NULL` constraint on `payments.amount` with no application-level validation replacing it, on a table the material shows is actively written to in production.

## Pass Criteria

- Assigns the dropped-constraint finding a severity reflecting the actual data-integrity exposure (a nullable amount field on an active payments table), not a low severity merely because the rule that prompted closer inspection was only Advisory.
- Does not state or imply that the Advisory classification of the triggering rule determines the severity of what was found.
- Governance classification (Advisory) and finding severity remain visibly independent in the output.

## Fail Signals

- Downgrading the constraint-drop finding's severity because the governance context that prompted the review was Advisory.
- Conflating "this rule is only Advisory" with "this finding is only minor."
