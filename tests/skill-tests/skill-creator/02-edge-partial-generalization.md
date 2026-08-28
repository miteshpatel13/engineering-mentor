---
id: skill-creator-02-edge-partial-generalization
category: edge-case
skill_under_test: skills/skill-creator/SKILL.md
---

# Scenario: Source Material Mixing Principle and Project Fact

## Input Material

> Source material for a candidate `soft-delete-and-lifecycle` Skill includes both a reusable principle (a generated-column pattern that collapses a soft-deleted row's unique value to NULL so it can be reused) and project-specific detail (the exact table names `Registration`, `Doctor`, and a specific client's confirmed decision to exempt `AuditLog`). Draft the Skill.

## Pass Criteria

- The reusable generated-column-uniqueness principle is retained, described generically (not tied to `Registration`/`Doctor`).
- The specific table names, client identity, and the specific "AuditLog is exempted" decision are NOT carried into the drafted Skill's Rules or Examples as if they were general Mentor guidance.
- If an example is needed, it uses a generic or clearly-fictional stand-in, per the Generalization, Not Copying rule.
- The response explicitly names what was left out and why (project-specific fact vs. reusable principle), rather than silently dropping it with no explanation.

## Fail Signals

- The drafted Skill's Examples or Rules reference `Registration`, `Doctor`, or the specific client's `AuditLog` exemption decision as if they were general facts.
- No explicit statement of what was generalized away and why.
