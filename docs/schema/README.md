# Schema

Machine-readable schemas for Engineering Mentor / child-repository integration artifacts.

## project.yaml

- `project.schema.v1.json` -- the JSON Schema (draft 2020-12) for `.mentor/project.yaml`, schema generation 1.
- See `docs/Project Profile Schema.md` for the full field-by-field reference, validation expectations, and compatibility policy.
- See `docs/examples/project.yaml` (fully populated) and `docs/examples/project.minimal.yaml` (minimum valid) for reference examples.
- Validate a file with `python3 scripts/validate_project_yaml.py <path>` (requires PyYAML; no other dependency).
- Regression suite: `python3 scripts/run_project_yaml_tests.py`, backed by fixtures under `tests/schema-tests/project-yaml/`.

A new schema generation (breaking change) gets its own `project.schema.v2.json` alongside this one -- generations are added, not replaced in place, so existing `schemaVersion: 1` files and their validator keep working.
