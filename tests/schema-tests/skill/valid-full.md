---
name: valid-full
description: Fixture Skill exercising every required and recommended section, for regression testing scripts/validate_skill.py.
category: Domain Patterns
skillType: Domain Pattern
---

# Valid Full Fixture

## Purpose

Exists only to exercise the validator's happy path.

## Scope

**In scope:** being a complete, valid fixture.
**Out of scope:** everything else.

## When to Use

Only by scripts/run_skill_standard_tests.py.

## Required Context

Context-independent.

## Workflow

1. Validate this file.
2. Confirm zero errors and zero warnings.

## Rules

Makes no claim on any child repository's behavior.

## Constraints

None beyond being a fixture.

## Governance Integration

Not applicable — this is a fixture, not a real Skill; it produces no findings and evaluates no repository.

## Validation

Passes when `scripts/validate_skill.py` reports `valid: true` with no warnings.

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
