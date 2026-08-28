---
id: enum-management-03-adversarial-renumbering-existing-enum
category: adversarial
skill_under_test: skills/enum-management/SKILL.md
---

# Scenario: Resisting Renumbering of Persisted Enum Values

## Input Material

> During a code cleanup PR, a developer reorganizes an existing `UserRole` enum alphabetically:
> `BEFORE: ADMIN = 1, USER = 2, GUEST = 3`
> `AFTER: ADMIN = 1, GUEST = 2, USER = 3`
> Millions of historical user database rows carry `user_role = 2`.

## Pass Criteria

- Strongly rejects renumbering existing enum members.
- Identifies that renumbering corrupts historical persisted data in production databases.
- Mandates the Freeze Principle: once persisted, integer-to-concept mappings are permanent.

## Fail Signals

- Approving renumbering of existing enum values for aesthetic or alphabetical reasons.
