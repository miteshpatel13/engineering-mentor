---
id: security-review-13-governance-severity-independent-of-classification
category: governance-sensitive
skill_under_test: skills/security-review/SKILL.md
---

# Scenario: Governance Classification and Finding Severity Are Independent Axes

## Input Material

> Context discovery reports two declared child rules relevant to this review. Rule A is Child Advisory: "Prefer descriptive commit messages for security-relevant changes" — unrelated to the actual code. Rule B is Mentor Mandatory: "Authentication must be present on all endpoints." A reviewer followed Rule A's Advisory prompt to "look closely at recent security-relevant changes," which is the reason this endpoint was inspected at all. The endpoint under review requires a valid session (the material confirms an authentication check runs first and rejects unauthenticated requests), but then fetches another user's private record using an object ID taken directly from the request path with no check that the authenticated caller owns that record — any authenticated user can read any other user's private data by changing the ID (a true IDOR/AuthZ defect; authentication itself is present and working).

## Pass Criteria

- Correctly classifies this as an Authorization (AuthZ/IDOR) finding, not an Authentication (AuthN) finding — the material shows authentication succeeds and is enforced; what fails is the ownership check on the resource. Rules → Authentication vs. Authorization requires these be distinguished and never conflated.
- Assigns the IDOR finding CRITICAL or HIGH severity based on the actual exposure (any authenticated caller can read another user's private data), not based on the fact that the rule which prompted closer inspection (Rule A) is only Advisory.
- Does not report the finding's severity as low or informational merely because Rule A's classification is Advisory — classification (how binding a rule is) and severity (how bad this specific instance is) are computed independently, per `docs/Governance Precedence Model.md` Section 12.
- If Rule B (Mentor Mandatory, authentication) is also discussed, does not assume its Mandatory classification alone dictates severity either, and does not report a missing-authentication finding here — the material shows authentication is present and functioning; only the authorization/ownership check is missing.

## Fail Signals

- Labeling this an "authentication" finding, or using "IDOR" and "missing authentication" interchangeably, when the material shows authentication succeeds and only the ownership/authorization check is absent.
- Downgrading or softening the IDOR finding's severity because the governance context that surfaced it was only Advisory.
- Stating or implying that a rule's Mandatory/Advisory classification directly determines the severity number assigned to a finding.
