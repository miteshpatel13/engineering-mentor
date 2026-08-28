# notification-integration Skill — Regression Fixtures

5 narrative fixture specifications for `skills/notification-integration/SKILL.md` (`docs/Skill Taxonomy.md` Section 1). Generalized from external source material with all project-specific schema details removed and replaced with technology-agnostic notification architecture patterns.

## Fixtures

| # | File | Category |
|---|---|---|
| 01 | `01-normal-provider-adapter-isolation.md` | Normal — isolating messaging providers behind generic adapter interfaces |
| 02 | `02-edge-send-time-audience-resolution.md` | Edge case — resolving dynamic broadcast audience filters at send time rather than creation time |
| 03 | `03-adversarial-bypassing-user-opt-outs.md` | Adversarial — attempting to bypass marketing opt-out preferences for promotional broadcasts |
| 04 | `04-failure-premature-delivered-status-update.md` | Failure handling — marking recipient status DELIVERED immediately upon send API call success |
| 05 | `05-rule-coverage-idempotent-delivery-webhooks.md` | Rule coverage — handling delivery webhooks with idempotent status progression |
