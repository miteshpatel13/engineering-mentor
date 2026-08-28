# code-review Skill — Regression Fixtures

Ten permanent behavioral test scenarios for `skills/code-review/SKILL.md`, originating from the Skill Tester's independent evaluation (7 scenario passes, several hardening gaps identified) plus three additional scenarios added when the Skill was hardened. A 27th fixture was added in Phase 13 (Certification Blocker Remediation, part of the independent-certification-pilot follow-up work) to close a gap the Phase 12 pilot identified: fixtures 11-26 included a genuine Override scenario (24) but no genuine Conflict scenario (`docs/Governance Precedence Model.md` Section 10 category 4) — see fixture 27.

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
| 11 | `11-child-mandatory-additive-rule.md` | Governance: Child Mandatory additive rule |
| 12 | `12-child-mandatory-prohibited-override.md` | Governance: Child Mandatory prohibited override |
| 13 | `13-child-advisory-rule.md` | Governance: Child Advisory rule, no conflict |
| 14 | `14-child-rule-scoped-applicability.md` | Governance: rule not applicable outside its declared scope |
| 15 | `15-child-rule-insufficient-evidence.md` | Governance: rule applicability can't be determined (missing evidence) |
| 16 | `16-applicable-exception.md` | Governance: applicable, approved exception (no suppression) |
| 17 | `17-expired-exception.md` | Governance: expired/non-matching exception provides no benefit |
| 18 | `18-exception-prohibited-security-downgrade.md` | Governance: exception attempting a Mandatory security downgrade |
| 19 | `19-child-and-mentor-both-violated.md` | Governance: Additive — both Mentor and child rule violated |
| 20 | `20-classification-vs-severity-independence.md` | Governance: classification and severity stay independent axes |
| 21 | `21-no-mentor-configuration.md` | Governance: no `.mentor/` configuration (backward compatibility) |
| 22 | `22-invalid-child-context.md` | Governance: invalid `project.yaml` and invalid child rule file |
| 23 | `23-child-configurable-boundary-violation.md` | Governance: Configurable value outside Mentor's boundary |
| 24 | `24-child-advisory-overrides-mentor-advisory.md` | Governance: valid Child Advisory override of Mentor Advisory |
| 25 | `25-unknown-applicability.md` | Governance: genuinely ambiguous (Unknown) applicability |
| 26 | `26-mandatory-security-test-authorization-override.md` | Governance: mandatory security regression — authorization override |
| 27 | `27-child-mandatory-conflicts-mentor-advisory.md` | Governance: genuine Conflict — Child Mandatory rule disagrees with Mentor Advisory guidance (Phase 13) |

## Governance Fixtures (11–26)

Fixtures 11 through 26 were added for the First Enforcement Phase (code-review as the reference implementation of `docs/Governance Precedence Model.md`). They follow the same fixture convention as 1–10 above — narrative, LLM-judged, no automated assertion harness — with one addition: because `skills/code-review/SKILL.md`'s Workflow step 0 now runs `context-discovery` and, when declared, `scripts/validate_child_rule.py`/`scripts/validate_exceptions_yaml.py` before reviewing, each governance fixture's Input Material states the Normalized Project Context and parsed rule/exception data *as if those steps had already run*, rather than requiring the evaluating agent to actually execute the scripts. This keeps these fixtures consistent with the narrative, no-execution-harness convention already established for 1–10, while still exercising the Skill's actual governance-reasoning rules (Child Governance, Progressive Context Loading, Output Format for Child-Derived Findings) against realistic discovery/validator output shapes.

Re-run fixtures 11–27 whenever `skills/code-review/SKILL.md`'s Child Governance rules, `docs/Governance Precedence Model.md`, or `docs/Child Rules and Exceptions.md` changes, in addition to the existing re-run triggers above.

Note: this Phase 13 addition is scoped narrowly to the reference governance-fixture model per `docs/Skill Testing Standard.md` Section 2 (now updated to explicitly name Override and Conflict as required categories). It does not address `skills/code-review/SKILL.md`'s separate, pre-existing structural validity issue (missing `category`/`skillType` frontmatter fields and missing `## When to Use`/`## Governance Integration` sections, per `scripts/validate_skill.py`), which remains out of scope for this phase.
