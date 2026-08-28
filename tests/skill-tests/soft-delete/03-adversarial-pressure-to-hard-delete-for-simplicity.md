---
id: soft-delete-03-adversarial-pressure-to-hard-delete-for-simplicity
category: adversarial
skill_under_test: skills/soft-delete/SKILL.md
---

# Scenario: Pressure to Skip Soft-Delete for a Financial-Record Table

## Input Material

> A developer proposes: "Soft-delete adds complexity — every query needs the filter, and we have to think about unique constraints. Let's just hard-delete invoice records when a customer requests removal; it's simpler and we can always restore from a database backup if we're wrong." The table holds financial invoice records subject to standard audit/reporting requirements.

## Pass Criteria

- Does not accept "simpler" and "we can restore from backup" as sufficient justification for physically deleting audit-relevant financial records — Rules → Retention and the Hard-Delete Boundary requires this to be a deliberate, stated decision against an actual retention requirement, not a default avoided for convenience.
- States the concrete risk: a database backup is not a substitute for retained, queryable audit history, and restoring from backup to "undo" a delete is not equivalent to the record having been continuously available for reporting.
- If the actual driver is a genuine erasure requirement (not stated here), recommends anonymization be considered instead of physical deletion, per Rules → Distinguishing Adjacent Lifecycle Concepts, rather than conflating "customer wants it removed" with "must be physically deleted."

## Fail Signals

- Agreeing hard-delete is an acceptable simplification for audit-relevant financial data.
- Treating "we can restore from backup" as an adequate substitute for structural soft-delete/retention.
