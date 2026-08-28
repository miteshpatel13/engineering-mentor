---
id: requirements-discipline-02-edge-partial-open-point
category: edge-case
skill_under_test: skills/requirements-discipline/SKILL.md
---

# Scenario: An Open Point That Blocks Only Some Downstream Work

## Input Material

> The specification defers the final list of user roles to a future client decision. Several features (permission checks on two endpoints) depend on knowing the final role list; most of the system does not.

## Pass Criteria

- The role-list decision is recorded as an open point, not silently treated as resolved.
- The response identifies specifically which downstream work is blocked (the two permission-checked endpoints) versus what can proceed using a placeholder/nullable role concept.
- The response does not block all development pending this one open point.

## Fail Signals

- Treating the entire feature set as blocked.
- Silently picking a placeholder role list and treating it as settled without recording it as open.
