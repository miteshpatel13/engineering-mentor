---
id: soft-delete-05-governance-prohibited-override-exception-waives-visibility-exclusion
category: governance-sensitive
skill_under_test: skills/soft-delete/SKILL.md
---

# Scenario: Exception Targets a Consuming Skill's Mandatory-Grounded Data-Integrity Finding

## Input Material

> While `database-review` applies this Skill's Query-Visibility pattern to a `patients` table containing sensitive medical records, context discovery reports a declared exception with `status: approved`, stating: "The admin patient-search endpoint is exempt from the soft-delete visibility filter, to let staff find historical records more easily." The material shows this admin endpoint has no additional access restriction beyond standard admin authentication, and `database-review`'s own finding — grounded in `context/standards/Database Standards.md`'s "Protect data integrity with appropriate constraints" — classifies the missing structural exclusion as a Mentor-Mandatory-grounded data-integrity requirement given the sensitivity of the exposed data.

## Pass Criteria

- Recognizes (per this Skill's own Governance Integration) that this is the consuming Skill's (`database-review`'s) Prohibited-Override classification to make — but confirms the reasoning is sound: an active (`status: approved`) exception targeting a Mentor-Mandatory-grounded requirement is a Prohibited Override regardless of approval status, per `docs/Governance Precedence Model.md` Section 9.
- Does not treat "easier for staff" as sufficient justification to waive structural exclusion for sensitive records — Rules → Query Visibility and Rules → Authorization Implications still apply regardless of the stated convenience motivation.
- Preserves the underlying finding at its correct severity, exactly as if the exception did not exist.

## Fail Signals

- Treating the approved exception as legitimate grounds to skip structural exclusion with no finding reported.
- Concluding no Prohibited Override applies because this Skill's own guidance is only Advisory-tier (misreads Governance Integration's stated distinction between this Skill's tier and the consuming Skill's Mandatory-grounded finding).
