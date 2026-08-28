# enum-management Skill — Regression Fixtures

5 narrative fixture specifications for `skills/enum-management/SKILL.md` (`docs/Skill Taxonomy.md` Section 1). Generalized from external source material with all project-specific schema details removed and replaced with technology-agnostic enum management patterns.

## Fixtures

| # | File | Category |
|---|---|---|
| 01 | `01-normal-explicit-integer-assignment.md` | Normal — designing a code enum with explicit, fixed integer assignments |
| 02 | `02-edge-master-data-vs-enum-decision.md` | Edge case — distinguishing static code enums from dynamic admin-managed lookup tables |
| 03 | `03-adversarial-renumbering-existing-enum.md` | Adversarial — refactoring request to reorder/renumber existing enum members |
| 04 | `04-failure-missing-dto-validation.md` | Failure handling — API endpoint accepting arbitrary integers without enum boundary validation |
| 05 | `05-rule-coverage-api-boundary-validation.md` | Rule coverage — validating incoming enum payload parameters at DTO boundary |
