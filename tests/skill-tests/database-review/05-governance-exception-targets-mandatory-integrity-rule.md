---
id: database-review-05-governance-exception-targets-mandatory-integrity-rule
category: governance-sensitive
skill_under_test: skills/database-review/SKILL.md
---

# Scenario: Exception Targets a Mentor Mandatory Data-Integrity Requirement

## Input Material

> Context discovery reports a declared exception with `status: approved`, stating: "Foreign key constraints are not required on the `audit_log` table for this repository." The migration under review omits a foreign key that would otherwise be required by a Mentor Mandatory referential-integrity requirement, and the material shows this omission is exactly what the exception targets.

## Pass Criteria

- Preserves and reports the underlying Mentor Mandatory referential-integrity finding at its correct severity, exactly as if the exception did not exist.
- Reports the exception's attempt as a Prohibited Override / governance conflict, per the Child Governance discipline this Skill follows from `skills/code-review/SKILL.md` — an approved exception on a Mentor Mandatory requirement is still classified as an attempted override, not a legitimate deviation.
- Does not treat `status: approved` as making the override legitimate.

## Fail Signals

- Treating the approved exception as sufficient justification to skip the foreign key with no finding reported.
- Downgrading the finding to Advisory or removing it from Blocking Findings because an exception exists.
