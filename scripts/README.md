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
- `skills/*/SKILL.md` structural validation against `docs/Skill Standard.md` -- frontmatter (`name`/`description`/`category`/`skillType`) and required-section presence (`validate_skill.py`, `run_skill_standard_tests.py` -- see `docs/Skill Standard.md` and `docs/Skill Taxonomy.md`). Structural only; does not score Skill quality (`docs/Skill Quality Standard.md`, a human/review judgment) and does not run a Skill's own narrative test fixtures (`docs/Skill Testing Standard.md`).
- On-disk narrative test-evidence check for a Skill claiming the Tested lifecycle stage -- existence, README presence, non-zero fixture count, and category diversity only (never fixture quality/correctness) against `docs/Skill Testing Standard.md` Section 3's two named hard blockers (`validate_skill_test_evidence.py`, `run_skill_test_evidence_tests.py` -- see `docs/Skill Testing Standard.md` and `docs/Skill Taxonomy.md` Section 7). A missing test-evidence directory is a warning, not an error, since some Skills are legitimately deterministic-only or explicitly exempted meta-guidance; judging fixture quality itself remains `skill-tester`'s and `skill-reviewer`'s narrative job.
- Claude Code plugin packaging validation -- the Claude counterpart of `validate_antigravity.py` (`validate_claude_plugin.py`, `run_claude_plugin_tests.py`): manifest fields and HTTPS repository URL, nothing but `plugin.json` inside `.claude-plugin/`, manifest component paths, version/metadata parity with the Antigravity `plugin.json`, skill and agent frontmatter as Claude Code reads it (names, descriptions, the 1,536-character listing cap, duplicates), `hooks/hooks.json` and `.mcp.json` shape when present, the `${CLAUDE_PLUGIN_ROOT}` Resource paths note and existence of every concrete Mentor path a Skill or Agent references, and a distribution hygiene scan for machine-specific paths, committed secrets, and `.env` files. Does not re-check the Skill Standard (that stays with `validate_skill.py`); `--with-cli` also runs the authoritative `claude plugin validate --strict`. Its fixtures are generated at run time rather than committed, because several must contain exactly what the hygiene scan forbids.
- Behavioral evaluation lives outside `scripts/`: `evals/` holds `claude plugin eval` cases (see `evals/README.md`). Those runs call the model and are billed, so they are not part of the deterministic suite above.

Automation should be safe, reproducible, and documented.
