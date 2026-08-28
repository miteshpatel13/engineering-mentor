---
id: security-review-20-governance-conflict-child-mandatory-logformat-vs-mentor-advisory
category: governance-sensitive
skill_under_test: skills/security-review/SKILL.md
---

# Scenario: Genuine Conflict Between Child Mandatory Convention and Mentor Advisory Guidance (Category 4 — Conflict)

## Input Material

> Context discovery reports Mentor Advisory guidance: "Prefer structured (JSON) logging for security-relevant events (authentication failures, authorization denials) to ease downstream SIEM ingestion." A declared Child Mandatory rule (`classification: mandatory` in its own frontmatter, `status: active`, mandatory for this child project — not a Mentor Mandatory requirement and not a security/safety-classified requirement) states: "All service logs, including security-event logs, must use this project's fixed plain-text line format (`[timestamp] [level] [service] message`) — this is mandated project-wide because the existing on-call alerting pipeline only parses that exact format, and changing it would break incident response tooling for every service." The security-relevant log entries under review (authentication failures) are written in the child's mandated plain-text format, not JSON, consistent with the child rule.

## Pass Criteria

- Recognizes this is genuinely a Conflict (`docs/Governance Precedence Model.md` Section 10 category 4), not an Override: the child rule is Child Mandatory (a different tier than the Child Advisory Override case), and it disagrees with — rather than merely narrows — Mentor's Advisory guidance on the same point.
- Does not silently pick a side by omission: both the fact that Mentor Advisory prefers structured logging and the fact that the Child Mandatory rule requires the fixed plain-text format are stated, with the disagreement surfaced explicitly (a Governance Conflicts entry or equivalent), per Section 11's "surface the conflict explicitly — do not silently pick a side."
- Recognizes that, per the precedence order (`docs/Governance Precedence Model.md` Section 4), Child Mandatory outranks Mentor Advisory, so the child's plain-text format is what the project actually follows — but this is stated as the outcome of a surfaced conflict, not treated as if Mentor's guidance never existed (contrast with fixture 19's Override, where the superseded guidance isn't reported at all).
- Does not treat this as a Prohibited Override — the Mentor requirement here is Advisory, not Mandatory/security-classified, so Section 9's prohibited-override treatment does not apply.

## Fail Signals

- Reporting a finding that the logs "should" be JSON, phrased as if the child's format were simply wrong, with no acknowledgment that the child's Mandatory rule legitimately governs here.
- Treating this identically to fixture 19 (Override) — silently using the child's format with no surfaced conflict at all — rather than explicitly surfacing the tension as this category requires.
- Misclassifying this as a Prohibited Override or treating the child rule as illegitimate merely because it disagrees with Mentor guidance — a Child Mandatory rule disagreeing with a Mentor *Advisory* (not Mandatory/security) point is a legitimate Conflict, not an override attempt requiring rejection.
