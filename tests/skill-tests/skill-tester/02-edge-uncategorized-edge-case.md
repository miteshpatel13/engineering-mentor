---
id: skill-tester-02-edge-uncategorized-edge-case
category: edge-case
skill_under_test: skills/skill-tester/SKILL.md
---

# Scenario: An Edge Case Not Covered by the Fixed Category List

## Input Material

> The Skill under test has an Edge Cases entry describing behavior when two source Skills being merged give contradictory guidance on the same point — a scenario that doesn't map cleanly onto any of `docs/Skill Testing Standard.md` Section 2's fixed category names (happy path, invalid input, missing context, etc.).

## Pass Criteria

- A fixture is written for this named edge case anyway, because `docs/Skill Testing Standard.md` Section 2 requires covering every edge case the Skill itself names, independent of the fixed category list.
- The fixture is filed under a sensible category label (e.g. "edge-case") even though no fixed category name matches exactly.

## Fail Signals

- Concluding no fixture is needed because the scenario doesn't match one of the fixed category names.
