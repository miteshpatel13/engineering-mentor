---
name: valid-minimal
description: Fixture Skill with only the required sections, omitting both recommended ones, for regression testing scripts/validate_skill.py.
category: Testing
skillType: Domain Pattern
---

# Valid Minimal Fixture

## Purpose

Exists to confirm required-only coverage still validates, with warnings for the omitted recommended sections.

## Scope

In scope: being a minimal valid fixture. Out of scope: everything else.

## When to Use

Only by scripts/run_skill_standard_tests.py.

## Required Context

Context-independent.

## Workflow

1. Validate this file.
2. Confirm zero errors and exactly two warnings.

## Rules

Makes no claim on any child repository's behavior.

## Governance Integration

Not applicable — this is a fixture.

## Validation

Passes when `scripts/validate_skill.py` reports `valid: true` with two `W_MISSING_RECOMMENDED_SECTION` warnings.

## Edge Cases

None.

## Failure Handling

Not applicable.

## Expected Output

No output of its own — it is test input.

## Examples

This file is its own example.
