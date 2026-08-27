# Scripts

Reserved for deterministic repository automation such as:

- Skill validation
- Link/reference validation
- Markdown checks
- Structure checks
- Skill test runners
- Release validation
- `.mentor/project.yaml` schema validation (`validate_project_yaml.py`, `run_project_yaml_tests.py` -- see `docs/Project Profile Schema.md`)
- Mentor Context Discovery (`discover_project_context.py`, `run_context_discovery_tests.py` -- see `docs/Context Discovery.md` and `skills/context-discovery/SKILL.md`)
- `.mentor/rules/` and `.mentor/exceptions.yaml` validation (`validate_child_rule.py`, `validate_exceptions_yaml.py`, `run_rules_and_exceptions_tests.py` -- see `docs/Child Rules and Exceptions.md`)
- Governance Evaluation -- deterministic classification of a child rule/exception's relationship to a Mentor governance requirement (`evaluate_governance.py`, `run_governance_evaluation_tests.py` -- see `docs/Governance Evaluation.md`). Read-only; does not parse `.mentor/` itself (reuses `discover_project_context.py`, `validate_child_rule.py`, `validate_exceptions_yaml.py`) and does not determine finding severity.

Automation should be safe, reproducible, and documented.
