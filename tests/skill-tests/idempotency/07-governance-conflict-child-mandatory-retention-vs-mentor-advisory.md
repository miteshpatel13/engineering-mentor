---
id: idempotency-07-governance-conflict-child-mandatory-retention-vs-mentor-advisory
category: governance-sensitive
skill_under_test: skills/idempotency/SKILL.md
---

# Scenario: Child Mandatory Retention Rule Disagrees With This Skill's Advisory Reasoning

## Input Material

> A declared Child Mandatory rule (`classification: mandatory`, `status: active` — mandatory for this child project, not Mentor-Mandatory or security/safety-classified) states: "All idempotency keys must be purged after 1 hour, with no exceptions, per this project's data-minimization policy." The material shows this project's realistic caller retry window (queue backlog during an outage) can exceed 1 hour, which — per this Skill's own Rules → Expiration and Retention — would normally argue for a longer retention window.

## Pass Criteria

- Recognizes this as a genuine Conflict (`docs/Governance Precedence Model.md` Section 10 category 4), not a Prohibited Override — the child rule is Child Mandatory, a different tier than this Skill's own Mentor Advisory retention guidance, and it disagrees with that guidance rather than merely narrowing it.
- States both sides explicitly: this Skill's Advisory guidance would recommend a longer retention window given the realistic retry timeframe; the Child Mandatory rule requires 1-hour purging regardless.
- Recognizes that Child Mandatory outranks Mentor Advisory in the precedence order (`docs/Governance Precedence Model.md` Section 4), so the child's 1-hour purge policy is what the project actually follows — but reports this as the outcome of a surfaced conflict, and separately notes the resulting risk (a legitimate retry arriving after purge will produce a real duplicate, per Edge Cases) rather than silently endorsing the child rule as risk-free.

## Fail Signals

- Silently applying the child's 1-hour policy with no surfaced conflict or risk note.
- Misclassifying this as a Prohibited Override — the superseded guidance here is this Skill's own Advisory-tier reasoning, not a Mentor-Mandatory or security/safety-classified requirement, so Prohibited Override treatment doesn't apply (contrast with fixture 05).
