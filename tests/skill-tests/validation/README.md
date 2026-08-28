# validation Skill — Regression Fixtures

5 narrative fixture specifications for `skills/validation/SKILL.md` (`docs/Skill Taxonomy.md` Section 1). Generalized from external source material with all project-specific schema details removed and replaced with technology-agnostic validation architecture patterns.

## Fixtures

| # | File | Category |
|---|---|---|
| 01 | `01-normal-two-layer-validation-architecture.md` | Normal — separating DTO structural validation from service-layer business rules |
| 02 | `02-edge-cross-field-dependency-validation.md` | Edge case — enforcing multi-field logical dependencies (e.g. date ordering, conditional inputs) |
| 03 | `03-adversarial-client-submitted-price-tampering.md` | Adversarial — parameter tampering where client submits financial totals |
| 04 | `04-failure-relying-on-frontend-validation-only.md` | Failure handling — bypassing backend validation due to assumed frontend checks |
| 05 | `05-rule-coverage-server-authoritative-recalculation.md` | Rule coverage — server-side authoritative recalculation of prices and permissions |
