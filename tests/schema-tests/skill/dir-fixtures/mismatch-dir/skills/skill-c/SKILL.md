---
name: wrong-name
description: Fixture Skill whose frontmatter name deliberately does not match its directory, for regression testing scripts/validate_skill.py --dir.
category: Domain Patterns
skillType: Domain Pattern
---

# Mismatched Name Fixture

## Purpose

Confirms `E_NAME_DIRECTORY_MISMATCH` fires when frontmatter `name` disagrees with the `skills/<name>/` directory, and `W_RELATED_SKILL_NOT_FOUND` fires for a reference that doesn't resolve.

## Scope

In scope: this one case. Out of scope: everything else.

## When to Use

Only by scripts/run_skill_standard_tests.py.

## Required Context

Context-independent.

## Workflow

1. Validate this directory with `--dir`.
2. Confirm exactly one `E_NAME_DIRECTORY_MISMATCH` error and one `W_RELATED_SKILL_NOT_FOUND` warning.

## Rules

Makes no claim on any child repository's behavior.

## Constraints

None beyond being a fixture.

## Governance Integration

Not applicable — this is a fixture.

## Validation

Passes when `scripts/validate_skill.py --dir` reports exactly this error and this warning.

## Edge Cases

None.

## Failure Handling

Not applicable.

## Expected Output

No output of its own — it is test input.

## Examples

This file is its own example.

## Related Skills

- `skills/nonexistent/SKILL.md` — deliberately does not exist, to exercise `W_RELATED_SKILL_NOT_FOUND`.
