---
id: skill-reviewer-04-failure-conflicting-dependency-labels
category: failure-handling
skill_under_test: skills/skill-reviewer/SKILL.md
---

# Scenario: Two Sibling Skills Disagree on a Relationship's Nature

## Input Material

> `skills/database-review/SKILL.md`'s Related Skills section lists `identifier-strategy` as a Dependency. `skills/identifier-strategy/SKILL.md`'s Related Skills section lists `database-review` as merely Related. Review this batch for cross-Skill consistency.

## Pass Criteria

- The response flags this as a Taxonomy defect requiring resolution — the two Skills disagree about the same edge.
- The response does not silently pick one Skill's label as authoritative without stating why.
- The response applies the true-dependency test (does `database-review`'s actual Rules/Workflow require `identifier-strategy`'s established output?) to determine which label is actually correct, and recommends the specific correction needed.

## Fail Signals

- Averaging or ignoring the disagreement.
- Picking a side with no stated reasoning tied to the actual dependency test.
