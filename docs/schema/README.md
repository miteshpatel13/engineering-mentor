# Schema

Machine-readable schemas for Engineering Mentor / child-repository integration artifacts.

## project.yaml

- `project.schema.v1.json` -- the JSON Schema (draft 2020-12) for `.mentor/project.yaml`, schema generation 1.
- See `docs/Project Profile Schema.md` for the full field-by-field reference, validation expectations, and compatibility policy.
- See `docs/examples/project.yaml` (fully populated) and `docs/examples/project.minimal.yaml` (minimum valid) for reference examples.
- Validate a file with `python3 scripts/validate_project_yaml.py <path>` (requires PyYAML; no other dependency).
- Regression suite: `python3 scripts/run_project_yaml_tests.py`, backed by fixtures under `tests/schema-tests/project-yaml/`.

A new schema generation (breaking change) gets its own `project.schema.v2.json` alongside this one -- generations are added, not replaced in place, so existing `schemaVersion: 1` files and their validator keep working.

## exceptions.yaml

- `exceptions.schema.v1.json` -- the JSON Schema (draft 2020-12) for `.mentor/exceptions.yaml`, schema generation 1. Every entry sets `additionalProperties: false` -- a deliberate, stricter departure from `project.yaml`'s open-schema philosophy, explained in `docs/Child Rules and Exceptions.md` Section 11 (Security Boundaries).
- See `docs/Child Rules and Exceptions.md` for the full field-by-field reference, lifecycle semantics, and the security boundary this schema enforces.
- See `docs/examples/exceptions.yaml` for a reference example covering a temporary, a permanent, an expired, and a rejected exception.
- Validate a file with `python3 scripts/validate_exceptions_yaml.py <path>` (requires PyYAML; no other dependency).
- Regression suite: `python3 scripts/run_rules_and_exceptions_tests.py`, backed by fixtures under `tests/schema-tests/exceptions/`.

## .mentor/rules/ frontmatter

`.mentor/rules/<id>.md` files use a small YAML frontmatter contract, not a JSON Schema file -- see `docs/Child Rules and Exceptions.md` Section 5 for why a second schema file was judged unnecessary for a six-field contract. `scripts/validate_child_rule.py` is the sole authoritative enforcement of that contract; regression suite in the same `run_rules_and_exceptions_tests.py` command above, backed by fixtures under `tests/schema-tests/child-rules/`.
