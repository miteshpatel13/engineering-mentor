# Context Discovery Tests

Regression fixtures and an automated runner for `scripts/discover_project_context.py`, under `fixtures/`.

Like `tests/schema-tests/` (and unlike `tests/skill-tests/`, which are narrative behavioral specs for LLM-judged Skill behavior with no execution harness), context discovery is fully deterministic and mechanical — so this suite is a real, automated test harness, not a narrative fixture set.

## Running the suite

```bash
python3 scripts/run_context_discovery_tests.py
```

The runner imports `discover()` directly from `scripts/discover_project_context.py` and asserts specific, named properties of its output against each fixture — not full-dict equality against a golden file. Full-dict equality was rejected deliberately: `projectRoot` is an absolute path that varies by machine/checkout location, and pinning every field (including ones a given scenario isn't actually testing) would make the suite brittle to unrelated, correct changes. Each assertion instead targets the specific field(s) that scenario exists to verify.

## Fixtures and scenarios

Each directory under `fixtures/` is a **synthetic child repository** — never a real one, and never `engineering-mentor` itself (this repository intentionally has no `.mentor/` directory of its own; see `docs/Child Repository Integration.md`'s Design Principles).

| Fixture | Scenario(s) covered |
|---|---|
| `fully-configured-child/` | 1 — fully configured child (`project.yaml`, `architecture.md`, `rules/`, `exceptions.yaml` all present and valid) |
| `no-mentor-directory/` | 2 — no `.mentor/` directory at all |
| `missing-project-yaml/` | 3 — `.mentor/` exists, `project.yaml` missing |
| `invalid-project-yaml/` | 4 — `project.yaml` present but fails schema validation (generic: missing required fields) |
| `missing-architecture-md/` | 5 — valid `project.yaml`, `architecture.md` missing |
| `with-rules-dir/` | 6 — valid `project.yaml`, non-empty `rules/` |
| `with-exceptions/` | 7 — valid `project.yaml`, non-empty `exceptions.yaml` |
| `malformed-architecture-md/` | 8 — `architecture.md` exists as a directory instead of a file |
| `empty-rules-dir/` | 9 — `rules/` exists but is empty |
| `empty-exceptions-file/` | 10 — `exceptions.yaml` exists but is empty |
| `unsupported-schema-version/` | 11 — `project.yaml` declares an unsupported `schemaVersion` |
| `invalid-mentor-version-range/` | 12 — `project.yaml` declares a self-contradictory `mentor.version` range |
| `progressive-artifacts/` | 13 — progressive repository-artifact discovery (some present, some absent); 14 — no repository-wide blind loading (a deep, unrelated file tree with a sentinel file must never appear in discovery output, and the inspected-artifact list must stay fixed-length) |

Scenario 15 (read-only behavior) is cross-cutting rather than fixture-specific: the runner hashes every file across **every** fixture before running discovery against all of them, then re-hashes and asserts an exact match — proving discovery never wrote to any fixture, regardless of what it found or didn't find.

## Adding a new fixture

1. Create `fixtures/<scenario-name>/` as a synthetic repository root exercising the one behavior the scenario is about — keep other pieces minimal/valid so the assertion isn't muddied by unrelated noise.
2. Add scenario-specific `check(...)` calls to `scripts/run_context_discovery_tests.py`, targeting the exact fields the new scenario is meant to verify.
3. Re-run the suite and confirm the new checks (and every existing one) pass.

## What this suite does not test

Whether a consuming Mentor Skill (e.g. `code-review`) correctly *uses* the Normalized Project Context once handed to it is an LLM-behavioral question, not a deterministic one — that belongs in `tests/skill-tests/`'s narrative convention if and when such coverage is added, not here.
