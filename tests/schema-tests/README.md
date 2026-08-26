# Schema Tests

Regression fixtures for `.mentor/project.yaml` schema validation, under `project-yaml/`.

Unlike `tests/skill-tests/` (which are narrative behavioral specs with no execution harness, evaluated by loading a Skill's material into a fresh agent), schema validation is fully deterministic and mechanical -- so these fixtures ARE automated. Each `<name>.yaml` fixture has a matching `<name>.expected.json` sidecar declaring the expected validity and the multiset of error/warning codes `scripts/validate_project_yaml.py` should produce.

Run the suite:

```bash
python3 scripts/run_project_yaml_tests.py
```

Add a new fixture by dropping a `<name>.yaml` file plus a `<name>.expected.json` sidecar into `project-yaml/`; the runner picks up every `*.yaml` file automatically.
