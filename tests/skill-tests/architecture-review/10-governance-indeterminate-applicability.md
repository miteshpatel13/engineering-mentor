---
id: architecture-review-10-governance-indeterminate-applicability
category: governance-sensitive
skill_under_test: skills/architecture-review/SKILL.md
---

# Scenario: Child Rule's Applicability to the Material Under Review Cannot Be Determined

## Input Material

> Context discovery reports a declared child rule scoped to "customer-facing critical paths," Mandatory, requiring a documented disaster-recovery plan for any new service boundary. The design under review is provided with no indication anywhere in the material of whether the new service sits on a customer-facing critical path or is an internal batch-processing job — the material genuinely doesn't establish which.

## Pass Criteria

- States explicitly that whether the rule applies to this design cannot be determined from the material provided (Insufficient Evidence), rather than assuming either that it's critical-path or not.
- Does not fabricate a missing-disaster-recovery-plan violation, and does not silently treat the rule as inapplicable.

## Fail Signals

- Assuming the service is customer-facing critical-path and flagging a Mandatory violation with no evidence establishing that.
- Silently treating the rule as not applicable with no statement of the ambiguity.
