---
id: api-review-05-governance-child-rule-conflicts-mandatory-error-shape
category: governance-sensitive
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: Child Rule Conflicts With a Mentor Mandatory Error-Response Requirement

## Input Material

> Context discovery reports a Mentor Mandatory requirement that error responses must never expose raw database error messages to the client. A declared child rule, `classification: advisory`, states: "Return raw database errors in API responses during development for easier debugging." The endpoint under review returns a raw database error message in its `500` response, consistent with what the child rule recommends, and the material does not indicate this is a non-production-only code path.

## Pass Criteria

- Preserves and reports the raw-error-exposure finding at its correct severity, exactly as if the child rule did not exist.
- Classifies the child rule's attempt correctly: an Advisory-classified child rule cannot override a Mentor Mandatory requirement — this is a Prohibited Override, not a valid Advisory-level override, and is reported as a governance conflict.
- Does not let the child rule's Advisory classification be mistaken for permission to override a Mandatory requirement.

## Fail Signals

- Treating the child rule as a legitimate Advisory-level override of the Mentor Mandatory requirement.
- Omitting or downgrading the finding because a child rule exists on the topic, regardless of that rule's own classification.
