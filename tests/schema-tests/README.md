# Schema Tests

Regression fixtures for Engineering Mentor / child-repository schema validation, split by artifact:

- `project-yaml/` -- `.mentor/project.yaml`, validated by `scripts/validate_project_yaml.py`.
- `exceptions/` -- `.mentor/exceptions.yaml`, validated by `scripts/validate_exceptions_yaml.py`.
- `child-rules/` -- `.mentor/rules/<id>.md` frontmatter, validated by `scripts/validate_child_rule.py`. Single-file fixtures live directly under `child-rules/`; `child-rules/dir-fixtures/<name>/` holds small synthetic `.mentor/rules/`-shaped directories for cross-file checks (e.g. duplicate rule ids), each with its expected-result sidecar at `child-rules/<name>.expected.json`.
- `governance-evaluation/` -- `<name>.input.json` / `<name>.expected.json` pairs exercising `scripts/evaluate_governance.py`'s deterministic classification of a child rule/exception's relationship to a Mentor governance requirement, per `docs/Governance Precedence Model.md` Sections 10-11. See `governance-evaluation/README.md` for the fixture format and the 15 named scenarios covered.
- `skill/` -- `skills/<name>/SKILL.md` frontmatter (`name`/`description`/`category`/`skillType`) and required-section presence, validated by `scripts/validate_skill.py`, per `docs/Skill Standard.md` and `docs/Skill Taxonomy.md`. Single-file fixtures live directly under `skill/`; `skill/dir-fixtures/<name>/` holds small synthetic `skills/`-shaped directories for cross-file checks (e.g. frontmatter `name` vs. directory mismatch, unresolved `Related Skills` references), each with its expected-result sidecar at `skill/<name>.expected.json`. This validator is structural only -- it does not score Skill quality (`docs/Skill Quality Standard.md`, a human/review judgment) and does not run a Skill's own narrative test fixtures (`docs/Skill Testing Standard.md`).

Unlike `tests/skill-tests/` (which are narrative behavioral specs with no execution harness, evaluated by loading a Skill's material into a fresh agent), all of these are fully deterministic and mechanical -- so these fixtures ARE automated. Each `<name>.yaml` or `<name>.md` fixture has a matching `<name>.expected.json` sidecar declaring the expected validity and the multiset of error/warning codes the corresponding validator should produce.

Run the suites:

```bash
python3 scripts/run_project_yaml_tests.py
python3 scripts/run_rules_and_exceptions_tests.py
python3 scripts/run_governance_evaluation_tests.py
python3 scripts/run_skill_standard_tests.py
```

Add a new fixture by dropping a `<name>.yaml`/`<name>.md` file plus a `<name>.expected.json` sidecar into the relevant directory (or a new subdirectory under `child-rules/dir-fixtures/` or `skill/dir-fixtures/` plus its sidecar directly under `child-rules/` or `skill/` respectively); the runners pick up new fixtures automatically -- no fixture list to maintain by hand.

See `docs/Child Rules and Exceptions.md` for the contracts these fixtures validate against, `docs/Project Profile Schema.md` for the `project.yaml` contract, and `docs/Skill Standard.md` / `docs/Skill Taxonomy.md` for the Skill contract.
