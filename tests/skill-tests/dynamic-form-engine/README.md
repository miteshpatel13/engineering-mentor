# dynamic-form-engine Skill — Regression Fixtures

5 narrative fixture specifications for `skills/dynamic-form-engine/SKILL.md` (`docs/Skill Taxonomy.md` Section 1). Generalized from external source material with all project-specific schema details removed and replaced with technology-agnostic dynamic form engine architecture patterns.

## Fixtures

| # | File | Category |
|---|---|---|
| 01 | `01-normal-immutable-version-locking.md` | Normal — locking form versions upon first submission and versioning forward |
| 02 | `02-edge-server-side-conditional-rule-evaluation.md` | Edge case — re-evaluating conditional visibility rules server-side before checking required status |
| 03 | `03-adversarial-editing-locked-form-version.md` | Adversarial — attempt to edit form fields in-place on a locked version with live submissions |
| 04 | `04-failure-hardcoded-field-type-switch-blocks.md` | Failure handling — adding field types via hardcoded switch branches instead of a registry pattern |
| 05 | `05-rule-coverage-hybrid-typed-submission-storage.md` | Rule coverage — storing dynamic responses using strongly typed storage columns pinned to version IDs |
