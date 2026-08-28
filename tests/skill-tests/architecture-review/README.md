# architecture-review Skill — Regression Fixtures

13 permanent behavioral test scenarios for `skills/architecture-review/SKILL.md`. Fixtures 1-5 cover the normal/edge/adversarial/failure/governance-sensitive categories from the original retrofit phase. Fixtures 6 onward were added in Phase 11 (Review Skill Governance Evidence) to close a gap Phase 10 identified: the single governance-sensitive fixture (5) exercised only one governance relationship (a Prohibited Override), while `docs/Skill Testing Standard.md` Section 2's second paragraph requires the full governance-relationship series for any Review-type Skill. See "Governance-Relationship Coverage" below for the mapping.

## What this is, and isn't

Fixture specifications, not automated assertions — same convention as `tests/skill-tests/code-review/README.md`. Each fixture is run by loading `skills/architecture-review/SKILL.md` as the acting agent's instructions, feeding the fixture's Input Material verbatim, and checking output against Pass Criteria while watching for Fail Signals.

**These fixtures are well-formed and structurally complete; they are not, by themselves, confirmed-passing behavioral evidence.** Per `docs/Skill Testing Standard.md` Section 1's evidence-strength distinction: a fixture existing, carrying explicit Pass Criteria/Fail Signals, and being structurally validated by `scripts/validate_skill_test_evidence.py` proves the fixture is sound — it does not prove `skills/architecture-review/SKILL.md` actually produces the described behavior. That requires either the fixture being executed against a live model invocation of the Skill, or an independent reviewer's own read reaching the same conclusion. Neither has occurred for these fixtures as of Phase 11; this gap is stated here explicitly rather than left implicit.

Re-run all fixtures whenever `skills/architecture-review/SKILL.md` changes; re-run fixtures 6 onward whenever `docs/Governance Precedence Model.md` or `docs/Governance Evaluation.md` changes.

## Fixtures

| # | File | Category |
|---|---|---|
| 1 | `01-normal-shared-write-ownership.md` | Happy path — two services writing the same data with no reconciliation |
| 2 | `02-edge-existing-monolith-clean-boundaries.md` | Edge case — a monolith with clean internal boundaries, correctly not flagged for "not being microservices" |
| 3 | `03-adversarial-pressure-to-approve-single-point-of-failure.md` | Adversarial — pressure to wave through an unmitigated single point of failure to hit a deadline |
| 4 | `04-failure-ambiguous-diagram.md` | Failure handling — a diagram too ambiguous to determine actual boundaries |
| 5 | `05-governance-child-rule-conflicts-with-mandatory-isolation.md` | Governance-sensitive — a child rule attempts to waive a Mentor Mandatory failure-isolation requirement |
| 06 | `06-governance-compatible-child-configurable-timeout.md` | Governance-sensitive — Compatible: Child Configurable timeout value alongside Mentor Mandatory failure-isolation requirement |
| 07 | `07-governance-additive-child-mandatory-circuit-breaker.md` | Governance-sensitive — Additive: Child Mandatory circuit-breaker requirement stacked on Mentor failure-mode baseline |
| 08 | `08-governance-advisory-no-conflict-module-layout.md` | Governance-sensitive — Child Advisory module-layout preference, no conflict |
| 09 | `09-governance-out-of-scope-child-rule.md` | Governance-sensitive — a declared child rule outside this Skill's architectural scope |
| 10 | `10-governance-indeterminate-applicability.md` | Governance-sensitive — rule applicability can't be determined from available evidence |
| 11 | `11-governance-applicable-exception-advisory-deviation.md` | Governance-sensitive — an approved, scoped, unexpired exception legitimately deviating from Advisory guidance |
| 12 | `12-governance-expired-exception-no-benefit.md` | Governance-sensitive — an expired exception provides no protection from a Mandatory finding |
| 13 | `13-governance-severity-independent-of-classification.md` | Governance-sensitive — classification and severity stay independent axes |

## Governance-Relationship Coverage (Phase 11)

Mapping of `docs/Skill Testing Standard.md` Section 2's required governance-relationship categories to the fixture that exercises each, per this phase's coverage matrix:

| Relationship | Fixture |
|---|---|
| Compatible | #06 |
| Additive | #07 |
| Prohibited Override | #05 |
| Advisory, no conflict | #08 |
| Out-of-scope | #09 |
| Indeterminate applicability | #10 |
| Applicable exception | #11 |
| Expired exception | #12 |
| Security-Mandatory downgrade | N/A — see Note below |
| Severity independent of classification | #13 |

**Note on "Security-Mandatory downgrade":** this category is `skills/security-review/SKILL.md`'s own stricter carve-out (its Governance Integration section states this is "the one case where this Skill's Governance Integration is stricter than the general Child Governance mechanism"). `skills/architecture-review/SKILL.md`'s Governance Integration section claims no equivalent stricter posture, so an ordinary Prohibited Override (fixture #05) already covers the applicable requirement here — a dedicated security-downgrade fixture would test a claim this Skill doesn't make.
