# Engineering Mentor Development Rules

These rules apply when developing and maintaining the `engineering-mentor` repository itself.

## 1. Core Principles

- **Platform-Agnostic Knowledge**: All skills, standards, principles, and SOPs must remain platform-independent and stack-agnostic. They must apply equally well to Claude Code, Google Antigravity, and any supported runtime.
- **Dual-Platform Parity**: Maintain compatibility with both Claude Code (`.claude-plugin/plugin.json`) and Google Antigravity (`plugin.json`, `.agents/`, `rules/`).
- **Single Source of Truth**: Never duplicate skill instruction files (`SKILL.md`) or create parallel skill trees. Skills live canonically in `skills/<skill_name>/SKILL.md`.
- **No Project-Specific Leakage**: If guidance depends on a specific framework, cloud vendor, or database, generalize it to the architectural principle or leave it to child repositories.
- **No Inventions**: Guidance must be backed by established engineering practices, verified standards, and clear testing rubrics.

## 2. Skill Authoring Standards

When adding or modifying skills:
- Must adhere strictly to `docs/Skill Standard.md` and `docs/Skill Taxonomy.md`.
- Directory name under `skills/` must exactly match the `name` frontmatter field.
- Required frontmatter fields: `name`, `description`, `category`, `skillType`.
- Required sections: Purpose, Scope, When to Use, Required Context, Workflow, Expected Output, Verification.
- Test scenarios should be added under `tests/skill-tests/<skill_name>/`.

## 3. Required Verification

Before submitting or committing changes to this repository, verify all deterministic tests pass:

```bash
python3 scripts/run_skill_standard_tests.py
python3 scripts/run_project_yaml_tests.py
python3 scripts/run_context_discovery_tests.py
python3 scripts/run_rules_and_exceptions_tests.py
python3 scripts/run_governance_evaluation_tests.py
python3 scripts/run_skill_test_evidence_tests.py
python3 scripts/validate_antigravity.py
```
