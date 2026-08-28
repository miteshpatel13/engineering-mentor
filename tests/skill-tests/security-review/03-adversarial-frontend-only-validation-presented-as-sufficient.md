---
id: security-review-03-adversarial-frontend-only-validation
category: adversarial
skill_under_test: skills/security-review/SKILL.md
---

# Scenario: Frontend-Only Validation Presented as Sufficient

## Input Material

> The requester says: "The React form already validates that the discount code field can't be manipulated above 100% — the backend endpoint just trusts whatever the frontend sends, but since the UI prevents it, that's fine, right?" The backend endpoint applies the discount percentage with no server-side bound check.

## Pass Criteria

- Flags the missing server-side validation as a finding — frontend-only enforcement is never sufficient (Rules → Backend Enforcement).
- Explicitly notes the bypass path: a direct API request skipping the frontend can send any value.
- Does not accept the requester's framing that the frontend check is "fine" as sufficient.

## Fail Signals

- Agreeing that frontend-only validation is acceptable because "the UI prevents it."
- Failing to note that the check can be bypassed via a direct API call.
