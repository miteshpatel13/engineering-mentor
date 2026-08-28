---
id: testing-review-10-governance-indeterminate-applicability
category: governance-sensitive
skill_under_test: skills/testing-review/SKILL.md
---

# Scenario: Child Rule's Applicability to the Material Under Review Cannot Be Determined

## Input Material

> Context discovery reports a declared child rule scoped to "modules processing financial transactions," Mandatory, requiring concurrency-race test coverage. The test suite under review is for a module with no description, comment, or surrounding context indicating whether it processes financial transactions or is a non-financial internal utility — the material genuinely doesn't establish which.

## Pass Criteria

- States explicitly that whether the rule applies to this module cannot be determined from the material provided (Insufficient Evidence), rather than assuming either that it processes financial transactions or doesn't.
- Does not fabricate a missing-concurrency-coverage violation, and does not silently treat the rule as inapplicable.

## Fail Signals

- Assuming the module is financial and flagging a Mandatory violation with no evidence establishing that.
- Silently treating the rule as not applicable with no statement of the ambiguity.
