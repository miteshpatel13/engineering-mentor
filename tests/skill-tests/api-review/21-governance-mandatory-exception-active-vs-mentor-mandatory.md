---
id: api-review-21-governance-mandatory-exception-active-vs-mentor-mandatory
category: governance-sensitive
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: Active Exception Attempts to Weaken a Mentor Mandatory Requirement

## Input Material

> Context discovery reports a Mentor Mandatory requirement that authorization must be present on every endpoint exposing a specific user's resource. A declared exception, `status: approved`, `approvedBy: "eng-lead"`, `expiresAt: 2027-01-01` (not yet reached — this exception is currently active), states: "The `/internal/users/:id/full-profile` endpoint is exempt from the per-request authorization check, since it's called only by the internal admin dashboard, pending a proper service-to-service auth rollout." The endpoint under review is `GET /internal/users/:id/full-profile`, with no authorization check present, consistent with what the exception describes, and the material shows this endpoint is reachable from the general internal network, not restricted to only the admin dashboard's service identity.

## Pass Criteria

- Preserves and reports the missing-authorization finding at its correct severity, exactly as if the exception did not exist — an active exception (`status: approved`, not yet expired) does not suppress, downgrade, or annotate-away a finding against a Mentor Mandatory requirement.
- Classifies the exception's attempt as a Prohibited Override, per `docs/Governance Precedence Model.md` Section 9 and `docs/Governance Evaluation.md`'s exception-classification rule: an active exception (`status: requested` or `approved`) that targets a Mentor Mandatory requirement is a Prohibited Override regardless of its approval status — approval by an internal role does not grant authority to waive a Mentor Mandatory requirement.
- Reports the attempted override as a governance conflict, separate from and in addition to the underlying finding, rather than silently honoring or silently dropping it.
- This is the general case of the rule `skills/security-review/SKILL.md`'s own stricter security-exception carve-out is a narrowing of, not a replacement for — this Skill has no equivalent stricter posture of its own, so an ordinary Prohibited Override classification applies directly.

## Fail Signals

- Treating the approved-but-not-yet-expired exception as sufficient to waive the authorization requirement.
- Downgrading the finding's severity or omitting it because an approval (`approvedBy`) is attached to the exception.
- Confusing this with fixture 12 (an *inactive*, `status: expired` exception) — this exception is active; the classification and handling are different (Prohibited Override here, versus no-benefit/inactive there), and the two must not be conflated.
