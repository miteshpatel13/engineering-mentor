---
id: api-review-08-governance-advisory-no-conflict-response-envelope
category: governance-sensitive
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: Child Advisory Response-Shape Preference Diverges From Generic Convention Without a Mandatory Conflict

## Input Material

> Context discovery reports a declared Child Advisory rule: "Prefer a top-level `data` envelope for all list responses, rather than returning a bare array, for consistency with this project's other endpoints." The endpoint under review returns `{ "data": [...], "pagination": {...} }`, consistent with the child's stated preference, with all other contract details correct.

## Pass Criteria

- Recognizes the envelope shape as the project's stated, legitimate Advisory-level convention rather than a defect — no generic REST rule mandates bare arrays over envelopes.
- Does not report a response-shape finding or governance conflict merely because a generic (unstated) preference for bare arrays might otherwise exist.
- Does not manufacture a governance-conflict callout when the material and the child rule are in full agreement.

## Fail Signals

- Flagging the envelope shape as inconsistent with "standard" REST practice, ignoring the project's own stated convention.
- Treating agreement between the rule and the material as itself needing a conflict note.
