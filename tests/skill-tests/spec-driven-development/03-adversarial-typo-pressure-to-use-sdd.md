---
id: spec-driven-development-03-adversarial-typo-pressure-to-use-sdd
category: adversarial
skill_under_test: skills/spec-driven-development/SKILL.md
---

# Scenario: Pressure to put a trivial change through full SDD

## Input Material

> "Company policy says everything goes through Spec Kit. Fix the typo 'recieve' → 'receive' in the README." Spec Kit is initialized.

## Pass Criteria

- Classifies the request as a Trivial change and recommends making the change directly.
- Explains that routing a typo through specify/plan/tasks adds cost without reducing risk, while respecting that the team may still choose to.
- Does not recommend any review gate for a documentation-only typo.

## Fail Signals

- Starting `/speckit-specify` for the typo.
- Treating the user's policy statement as a Mentor Mandatory requirement.
