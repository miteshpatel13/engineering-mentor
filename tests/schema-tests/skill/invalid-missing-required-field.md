---
name: invalid-missing-required-field
description: Fixture Skill missing category and skillType, for regression testing scripts/validate_skill.py.
---

# Invalid Missing Required Field Fixture

## Purpose

Confirms missing required frontmatter fields are reported individually.

## Scope

In scope: this one case. Out of scope: everything else.

## When to Use

Only by scripts/run_skill_standard_tests.py.

## Required Context

Context-independent.

## Workflow

1. Validate this file.
2. Confirm two `E_MISSING_REQUIRED_FIELD` errors (category, skillType).

## Rules

Makes no claim on any child repository's behavior.

## Constraints

None beyond being a fixture.

## Governance Integration

Not applicable — this is a fixture.

## Validation

Passes when `scripts/validate_skill.py` reports `valid: false` with exactly these two errors.

## Edge Cases

None.

## Failure Handling

Not applicable.

## Expected Output

No output of its own — it is test input.

## Examples

This file is its own example.

## Related Skills

None — standalone fixture.
