# code-review Skill — Regression Fixtures

Ten permanent behavioral test scenarios for `skills/code-review/SKILL.md`, originating from the Skill Tester's independent evaluation (7 scenario passes, several hardening gaps identified) plus three additional scenarios added when the Skill was hardened.

## What this is, and isn't

These are **fixture specifications**, not automated assertions. There is currently no execution harness in this repository that runs a Skill and checks its output programmatically — `context/skills/Skill Testing & Evaluation Standard.md` calls for behavioral evaluation, and a Markdown-text-matching script would not verify that; it would only prove the Skill's *file* didn't change. Pretending otherwise would be a fake automated assertion, which the Mentor's own standards reject.

Until a real execution harness exists (tracked as future `scripts/` work), each fixture is run by:

1. Loading `skills/code-review/SKILL.md` (and the files it references: `context/sop/Code Review SOP.md`, `context/standards/Code Review Standard.md`, `context/standards/Severity Taxonomy.md`, `context/templates/Review Template.md`, and the relevant checklist) as the acting agent's instructions — e.g. via the `skill-tester` Skill, or a subagent given the same material.
2. Feeding that agent the fixture's **Input Material** verbatim, as if it were the user's actual review request.
3. Checking the agent's output against the fixture's **Pass Criteria**, and specifically watching for its **Fail Signals**.

Re-run all ten fixtures whenever `skills/code-review/SKILL.md`, `context/standards/Code Review Standard.md`, `context/standards/Severity Taxonomy.md`, or `context/templates/Review Template.md` changes.

## Fixtures

| # | File | Category |
|---|---|---|
| 1 | `01-clean-authenticated-endpoint.md` | Happy path / false-positive resistance |
| 2 | `02-sql-injection.md` | Security detection |
| 3 | `03-bola-idor.md` | Security detection |
| 4 | `04-missing-context.md` | Input-requirement guarantee |
| 5 | `05-performance-anti-pattern.md` | Performance detection |
| 6 | `06-false-positive-resistance.md` | False-positive discipline |
| 7 | `07-conflicting-requirement.md` | Constraint handling (legitimate constraint) |
| 8 | `08-severity-taxonomy-consistency.md` | Severity taxonomy compliance |
| 9 | `09-security-control-bypass-request.md` | Constraint handling (bypass request) |
| 10 | `10-partial-missing-artifact-context.md` | Partial-context handling |
