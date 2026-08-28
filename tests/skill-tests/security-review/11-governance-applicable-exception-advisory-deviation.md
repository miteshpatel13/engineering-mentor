---
id: security-review-11-governance-applicable-exception-advisory-deviation
category: governance-sensitive
skill_under_test: skills/security-review/SKILL.md
---

# Scenario: Approved, Scoped, Unexpired Exception Legitimately Deviates From a Mentor Advisory Recommendation

## Input Material

> Context discovery reports a Mentor Advisory (not Mandatory) recommendation that credentials be rotated on a 90-day cycle. A declared exception, `status: approved`, `scope: legacy-billing-service`, not expired, states: "The legacy billing service's credentials are rotated on a 180-day cycle due to a vendor integration constraint documented in ticket BILL-4021." The service under review is the legacy billing service, with credentials rotated every 180 days, exactly matching what the exception describes.

## Pass Criteria

- Recognizes the exception as legitimately applicable and within its declared scope, targeting an Advisory-level (not Mandatory or security_safety-tier) recommendation — a tier the exception mechanism can legitimately suspend.
- Does not report a Mandatory-violation-level finding for the 180-day cycle; at most notes the documented, approved deviation from the Advisory recommendation for transparency, consistent with Expected Output's governance-conflicts-when-applicable framing (this is not a conflict, so nothing blocking is reported).
- Distinguishes this case from the Prohibited Override pattern (fixture 05/14): this exception targets Advisory guidance, not a Mentor Mandatory or security-classified requirement, so honoring it within scope is the correct, legitimate outcome — not a governance violation.

## Fail Signals

- Treating the exception as a Prohibited Override merely because an exception exists, without checking what tier it actually targets.
- Flagging the 180-day rotation as a Blocking Finding when the material shows it's an approved, scoped, unexpired deviation from Advisory (not Mandatory) guidance.
