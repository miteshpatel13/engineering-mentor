---
name: Invalid_Name!
description: Fixture Skill with a name that does not match the required kebab-case pattern, for regression testing scripts/validate_skill.py.
category: Testing
skillType: Domain Pattern
---

# Invalid Name Value Fixture

## Purpose

Confirms a malformed `name` value is reported, independent of the (not-applicable, since this fixture has no real skills/<name>/ location) directory-match check.

## Scope

In scope: this one case. Out of scope: everything else.

## When to Use

Only by scripts/run_skill_standard_tests.py.

## Required Context

Context-independent.

## Workflow

1. Validate this file.
2. Confirm exactly one `E_INVALID_VALUE` error.

## Rules

Makes no claim on any child repository's behavior.

## Constraints

None beyond being a fixture.

## Governance Integration

Not applicable — this is a fixture.

## Validation

Passes when `scripts/validate_skill.py` reports `valid: false` with exactly one error.

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
