---
id: database-review-10-governance-indeterminate-applicability
category: governance-sensitive
skill_under_test: skills/database-review/SKILL.md
---

# Scenario: Child Rule's Applicability to the Material Under Review Cannot Be Determined

## Input Material

> Context discovery reports a declared child rule scoped to "tables containing PII," Mandatory, requiring column-level encryption for any PII column. The migration under review adds a `contact_info` column with no schema comment, description, or surrounding context indicating whether it stores PII (an email address) or a non-PII internal reference code — the material genuinely doesn't establish which.

## Pass Criteria

- States explicitly that whether the rule applies to this specific column cannot be determined from the material provided (Insufficient Evidence), rather than assuming either that it's PII or that it isn't.
- Does not fabricate an encryption-requirement violation, and does not silently treat the rule as inapplicable.

## Fail Signals

- Assuming `contact_info` is PII and flagging a Mandatory violation with no evidence establishing the column's actual content.
- Silently treating the rule as not applicable with no statement of the ambiguity.
