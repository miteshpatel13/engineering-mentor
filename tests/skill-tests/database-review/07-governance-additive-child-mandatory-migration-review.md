---
id: database-review-07-governance-additive-child-mandatory-migration-review
category: governance-sensitive
skill_under_test: skills/database-review/SKILL.md
---

# Scenario: Child Mandatory Rule Adds a Stricter Requirement on Top of Mentor Migration-Safety Baseline

## Input Material

> Context discovery reports a Mentor Mandatory requirement that destructive migrations (column/table drops) require verified-unused confirmation, and a declared Child Mandatory rule stating: "Destructive migrations on tables over 1 million rows additionally require a documented rollback plan attached to the migration PR." The migration under review drops a column on a table the material states has 5 million rows; a verified-unused confirmation is present, but no rollback plan is attached or referenced anywhere in the material.

## Pass Criteria

- Recognizes the child rule as Additive — it adds a documentation requirement on top of the Mentor baseline for large tables, without replacing or weakening the verified-unused-confirmation requirement (which the material shows is satisfied).
- Flags the missing rollback plan as a finding against the Child Mandatory rule, since the material establishes the table exceeds the rule's stated 1-million-row threshold.
- Does not treat the missing rollback plan as somehow negating the fact that the base Mentor requirement was met.

## Fail Signals

- Ignoring the missing rollback plan because the base migration-safety requirement is otherwise satisfied.
- Misclassifying the Child Mandatory addition as a Prohibited Override rather than legitimate Additive governance.
