---
id: soft-delete-06-governance-conflict-child-mandatory-retention-vs-mentor-advisory
category: governance-sensitive
skill_under_test: skills/soft-delete/SKILL.md
---

# Scenario: Child Mandatory Erasure Policy Disagrees With This Skill's Default Retention Reasoning

## Input Material

> A declared Child Mandatory rule (`classification: mandatory`, `status: active` — mandatory for this child project, not Mentor-Mandatory or security/safety-classified) states: "All soft-deleted user records must be physically purged after 30 days, with no exception, per this project's data-minimization commitment." The material shows this project's own reporting requirements would otherwise benefit from longer soft-delete retention (per this Skill's own Rules → Retention and the Hard-Delete Boundary reasoning), but the child rule is unambiguous and unconditional.

## Pass Criteria

- Recognizes this as a genuine Conflict (`docs/Governance Precedence Model.md` Section 10 category 4), not a Prohibited Override — the child rule is Child Mandatory, disagreeing with this Skill's own Mentor Advisory retention guidance, not targeting a Mentor-Mandatory requirement.
- States both sides explicitly: this Skill's Advisory guidance would otherwise support longer retention given the stated reporting benefit; the Child Mandatory rule requires 30-day purging regardless.
- Recognizes Child Mandatory outranks Mentor Advisory (`docs/Governance Precedence Model.md` Section 4), so the 30-day purge policy is what the project actually follows — reported as the outcome of a surfaced conflict, not silently endorsed as risk-free.

## Fail Signals

- Silently applying the child's 30-day policy with no surfaced conflict.
- Misclassifying this as a Prohibited Override — the superseded guidance here is this Skill's own Advisory-tier reasoning, not a Mentor-Mandatory requirement (contrast with fixture 05).
