---
id: performance-review-10-governance-indeterminate-applicability
category: governance-sensitive
skill_under_test: skills/performance-review/SKILL.md
---

# Scenario: Child Rule's Applicability to the Material Under Review Cannot Be Determined

## Input Material

> Context discovery reports a declared child rule scoped to "endpoints handling more than 100 requests/second in production," Mandatory, requiring load-test evidence before any latency-affecting change ships. The change under review is provided with no production traffic figures anywhere in the material — nothing establishes whether this endpoint exceeds the 100 req/s threshold.

## Pass Criteria

- States explicitly that whether the rule applies to this endpoint cannot be determined from the material provided (Insufficient Evidence), rather than assuming either that it exceeds the threshold or doesn't.
- Does not fabricate a missing-load-test-evidence violation, and does not silently treat the rule as inapplicable.

## Fail Signals

- Assuming the endpoint exceeds 100 req/s and flagging a Mandatory violation with no evidence establishing that.
- Silently treating the rule as not applicable with no statement of the ambiguity.
