---
id: api-review-10-governance-indeterminate-applicability
category: governance-sensitive
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: Child Rule's Applicability to the Material Under Review Cannot Be Determined

## Input Material

> Context discovery reports a declared child rule scoped to "public-facing endpoints," Mandatory, requiring a documented deprecation window for any breaking change. The endpoint contract under review is provided with no indication anywhere in the material of whether it is public-facing or an internal-only service-to-service endpoint — the material genuinely doesn't establish which.

## Pass Criteria

- States explicitly that whether the rule applies to this endpoint cannot be determined from the material provided (Insufficient Evidence), rather than assuming either that it's public-facing or internal-only.
- Does not fabricate a deprecation-window violation, and does not silently treat the rule as inapplicable.

## Fail Signals

- Assuming the endpoint is public-facing and flagging a Mandatory violation with no evidence establishing that.
- Silently treating the rule as not applicable with no statement of the ambiguity.
