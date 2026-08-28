---
name: valid-unknown-field
description: Fixture Skill with one recognized-but-extra frontmatter field, for regression testing scripts/validate_skill.py.
category: Testing
skillType: Domain Pattern
author: someone
---

# Valid Unknown Field Fixture

## Purpose

Confirms an unrecognized frontmatter field produces a warning, not an error.

## Scope

In scope: this one case. Out of scope: everything else.

## When to Use

Only by scripts/run_skill_standard_tests.py.

## Required Context

Context-independent.

## Workflow

1. Validate this file.
2. Confirm zero errors and exactly one `W_UNKNOWN_FRONTMATTER_FIELD` warning.

## Rules

Makes no claim on any child repository's behavior.

## Constraints

None beyond being a fixture.

## Governance Integration

Not applicable — this is a fixture.

## Validation

Passes when `scripts/validate_skill.py` reports `valid: true` with exactly one warning.

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
