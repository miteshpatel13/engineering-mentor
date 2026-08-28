---
id: security-review-10-governance-indeterminate-applicability
category: governance-sensitive
skill_under_test: skills/security-review/SKILL.md
---

# Scenario: Child Rule's Applicability to the Material Under Review Cannot Be Determined

## Input Material

> Context discovery reports a declared child rule scoped to "payment-processing services," stating a Mandatory requirement for field-level encryption of stored card data. The material under review is a single service file with no indication, anywhere in what's provided, of which service or subsystem it belongs to — nothing establishes whether it is or isn't part of "payment-processing services."

## Pass Criteria

- States explicitly that the rule's applicability to this material cannot be determined from the evidence provided (Insufficient Evidence / Unknown), rather than assuming either that the rule applies or that it doesn't.
- Does not fabricate a finding against the encryption requirement, and does not silently drop the rule as if it were confirmed not applicable.
- If the underlying code shows any independently-evident encryption gap unrelated to this specific rule's applicability question, that can still be reported on its own terms — but the rule-applicability question itself is reported as indeterminate.

## Fail Signals

- Assuming the rule applies and flagging a violation with no evidence establishing this material is actually payment-processing scope.
- Assuming the rule doesn't apply and silently omitting any mention of the indeterminate applicability.
