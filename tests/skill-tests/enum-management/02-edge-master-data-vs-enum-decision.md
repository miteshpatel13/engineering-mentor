---
id: enum-management-02-edge-master-data-vs-enum-decision
category: edge
skill_under_test: skills/enum-management/SKILL.md
---

# Scenario: Enum vs. Master Data Lookup Table Decision

## Input Material

> A product owner asks to store `ProductCategory` as a code enum. Admins will frequently add, rename, and deactivate categories via an admin web dashboard without deploying code.

## Pass Criteria

- Rejects hardcoding `ProductCategory` as a code enum.
- Explains that runtime user-managed lists require a relational Master Data table (`categories` table with `id`, `name`, `is_active`).
- Reserves code enums strictly for static, code-controlled domain concepts.

## Fail Signals

- Recommending code-compiled enums for user-configurable dynamic data.
