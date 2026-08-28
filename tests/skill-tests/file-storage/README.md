# file-storage Skill — Regression Fixtures

5 narrative fixture specifications for `skills/file-storage/SKILL.md` (`docs/Skill Taxonomy.md` Section 1). Generalized from external source material with all project-specific schema details removed and replaced with technology-agnostic file storage patterns.

## Fixtures

| # | File | Category |
|---|---|---|
| 01 | `01-normal-server-key-generation.md` | Normal — generating unguessable server-side storage keys and unified metadata registry |
| 02 | `02-edge-content-magic-byte-mime-validation.md` | Edge case — validating file types by inspecting magic byte content instead of headers |
| 03 | `03-adversarial-path-traversal-via-client-filename.md` | Adversarial — attempt to execute path traversal using client-supplied filenames |
| 04 | `04-failure-unguessable-url-as-only-authorization.md` | Failure handling — relying on unguessable UUID paths instead of explicit authorization checks |
| 05 | `05-rule-coverage-storage-provider-adapter.md` | Rule coverage — isolating storage driver SDKs behind generic adapter interfaces |
