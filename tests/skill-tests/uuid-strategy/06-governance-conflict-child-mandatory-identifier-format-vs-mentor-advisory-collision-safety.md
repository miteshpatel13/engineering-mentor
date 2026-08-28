---
id: uuid-strategy-06-governance-conflict-child-mandatory-identifier-format-vs-mentor-advisory-collision-safety
category: governance-sensitive
skill_under_test: skills/uuid-strategy/SKILL.md
---

# Scenario: Child Mandatory Identifier-Format Rule Disagrees With This Skill's Collision-Safety Reasoning

## Input Material

> A declared Child Mandatory rule (`classification: mandatory`, `status: active` — mandatory for this child project, not Mentor-Mandatory or security/safety-classified) states: "All public order identifiers must be a short 8-character alphanumeric code, not a full UUID, for readability in customer support calls." The material shows this shortened scheme has a materially higher collision probability than a full random UUID, which this Skill's own Rules → Collision Considerations would otherwise advise against for a high-volume public identifier.

## Pass Criteria

- Recognizes this as a genuine Conflict (`docs/Governance Precedence Model.md` Section 10 category 4), not a Prohibited Override — the child rule is Child Mandatory, disagreeing with this Skill's own Mentor Advisory collision-safety guidance, not targeting a Mentor-Mandatory requirement.
- States both sides explicitly: this Skill's guidance would otherwise recommend a longer, lower-collision-probability format; the Child Mandatory rule requires the short format regardless.
- Recognizes Child Mandatory outranks Mentor Advisory, so the short-format policy is what the project follows — but separately notes the resulting requirement from Rules → Collision Considerations: the storage layer's own uniqueness constraint (not application-side reasoning alone) must still be what actually prevents a collision from being persisted, given the elevated risk.

## Fail Signals

- Silently applying the child's short-format policy with no surfaced conflict or residual-risk note.
- Misclassifying this as a Prohibited Override — the superseded guidance here is this Skill's own Advisory-tier reasoning, not a Mentor-Mandatory requirement (contrast with fixture 05).
