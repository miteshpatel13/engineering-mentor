# complex-thinking-capacity Skill — Regression Fixtures

6 narrative fixture specifications for `skills/complex-thinking-capacity/SKILL.md` (Authoring/Workflow), covering the scenario categories in `docs/Skill Testing Standard.md` Section 2 that apply to a context-independent Skill that assesses people rather than repositories.

## What this is, and isn't

Fixture specifications, not automated assertions — the same convention as every other Skill's fixture set. Each fixture is run by loading the Skill as the acting agent's instructions, feeding the Input Material verbatim, and checking output against Pass Criteria while watching for Fail Signals.

**Structurally complete, not confirmed-passing behavioral evidence.** No live model execution (Tier D) or independent human review (Tier E) has occurred; evidence stands at Tier A/B/C (`docs/Skill Testing Standard.md` Section 1).

Governance-relationship fixtures are not applicable: the Skill's Governance Integration is "Not applicable" (it never invokes Context Discovery or Governance Evaluation). Fixture 06 covers the security-sensitive category instead — the Skill handles personal data and can be pushed toward discriminatory or covert assessment.

Re-run all fixtures whenever the Skill changes; re-run fixture 01 whenever the Calibration Anchor in the Skill's Examples changes.

## Fixtures

| # | File | Category |
|---|---|---|
| 01 | `01-normal-score-full-transcript.md` | Normal — scores a complete 5-round transcript with correct round attribution and arithmetic |
| 02 | `02-edge-missing-pressure-round.md` | Edge case — round 4 missing; D4 and Pressure Drop not observed, score based on 5/6 |
| 03 | `03-adversarial-confidence-not-thinking.md` | Adversarial — fluent, confident answer with little reasoning must not score high |
| 04 | `04-failure-impression-notes-and-diagnosis.md` | Failure handling — impression-only notes plus a diagnosis request |
| 05 | `05-rule-coverage-plan-stress-test.md` | Rule coverage — Mode D scores D2, D5, D6 only on a written plan |
| 06 | `06-security-covert-biased-assessment.md` | Security-sensitive — covert assessment, humiliating pressure, and a protected-characteristic adjustment |

## Rule Coverage

Which Round Counts (01, 02), Scoring Rubric (01, 03, 05), Computed Outputs (01, 02, 05), Role Targets (01), Running a Live Session (06), Constraints (04, 06), Failure Handling (04), Edge Cases — missing round (02), written plan (05). Known limitation: Two Raters reconciliation and Mode C scenario building have no dedicated fixture.
