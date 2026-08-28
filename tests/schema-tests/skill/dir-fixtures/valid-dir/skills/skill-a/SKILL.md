---
name: skill-a
description: Fixture Skill A, for dir-fixture cross-reference testing of scripts/validate_skill.py --dir.
category: Domain Patterns
skillType: Domain Pattern
---

# Skill A

## Purpose

Fixture only — exercises a correct `skills/<name>/` directory match and a Related Skills reference that resolves.

## Scope

In scope: being a valid fixture that references `skill-b`. Out of scope: everything else.

## When to Use

Only by scripts/run_skill_standard_tests.py.

## Required Context

Context-independent.

## Workflow

1. Validate this directory with `--dir`.
2. Confirm zero errors and zero warnings across both files.

## Rules

Makes no claim on any child repository's behavior.

## Constraints

None beyond being a fixture.

## Governance Integration

Not applicable — this is a fixture.

## Validation

Passes when `scripts/validate_skill.py --dir` reports `valid: true` for the whole directory.

## Edge Cases

None.

## Failure Handling

Not applicable.

## Expected Output

No output of its own — it is test input.

## Examples

This file is its own example.

## Related Skills

- `skills/skill-b/SKILL.md` — sibling fixture Skill; this reference must resolve without a `W_RELATED_SKILL_NOT_FOUND` warning.
