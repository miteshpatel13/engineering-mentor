---
id: dynamic-form-engine-05-rule-coverage-hybrid-typed-submission-storage
category: rule-coverage
skill_under_test: skills/dynamic-form-engine/SKILL.md
---

# Scenario: Persisting Submissions in Hybrid Typed Columns

## Input Material

> A dynamic submission engine stores all submission answers (numbers, dates, text, multi-selects) as unformatted raw strings in a single `value_string VARCHAR(255)` column.

## Pass Criteria

- Rejects storing all response types as unformatted strings.
- Mandates a hybrid storage model using strongly typed columns (`value_text`, `value_number`, `value_date`, `value_json`) keyed to `form_field_id`.

## Fail Signals

- Storing numeric or date submission values exclusively as untyped string blobs.
