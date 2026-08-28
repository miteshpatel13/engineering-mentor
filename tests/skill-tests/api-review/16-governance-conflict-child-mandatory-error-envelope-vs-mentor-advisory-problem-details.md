---
id: api-review-16-governance-conflict-child-mandatory-error-envelope-vs-mentor-advisory-problem-details
category: governance-sensitive
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: Genuine Conflict Between Child Mandatory Convention and Mentor Advisory Guidance (Category 4 — Conflict)

## Input Material

> Context discovery reports Mentor Advisory guidance: "Prefer a machine-readable `type` field (per RFC 7807 Problem Details) in error responses, to support programmatic client handling." A declared Child Mandatory rule (`classification: mandatory` in its own frontmatter, `status: active` — mandatory for this child project, not a Mentor Mandatory requirement) states: "All error responses in this API must use this project's existing fixed error envelope (`{ code, message }`), with no additional fields — mandated because the shared client library already deployed across every consuming service parses exactly this two-field shape, and adding fields risks breaking strict client-side schema validation in older SDK versions still in production." The endpoint under review returns an error using the child's fixed two-field envelope, with no `type` field, consistent with the child rule. The HTTP status code and error semantics are otherwise correct (Rules → Validation and Error Semantics).

## Pass Criteria

- Recognizes this is genuinely a Conflict (`docs/Governance Precedence Model.md` Section 10 category 4), not an Override: the child rule is Child Mandatory, a different tier than the Child-Advisory Override case, and it disagrees with Mentor's Advisory `type`-field preference rather than merely narrowing it.
- States both sides explicitly: Mentor Advisory prefers a `type` field; the Child Mandatory rule requires the fixed two-field envelope with no additions; the two disagree — surfaced, not silently resolved.
- Recognizes Child Mandatory outranks Mentor Advisory in the precedence order (`docs/Governance Precedence Model.md` Section 4), so the fixed envelope is what the project actually follows here — reported as the outcome of a surfaced conflict, not as if Mentor's guidance never existed.
- Does not treat this as a Prohibited Override — the superseded Mentor requirement is Advisory, not Mandatory, so Section 9's prohibited-override treatment does not apply.

## Fail Signals

- Reporting a finding that the error response "should" include a `type` field, phrased as a defect, with no acknowledgment that the child's Mandatory envelope rule legitimately governs here.
- Silently applying the child's envelope with no surfaced conflict at all, as if this were an ordinary Override (fixture 15) rather than a genuine, stated disagreement.
- Misclassifying the child rule as a Prohibited Override merely because it disagrees with Mentor Advisory guidance.
