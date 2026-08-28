# database-review Skill — Regression Fixtures

22 permanent behavioral test scenarios for `skills/database-review/SKILL.md`. Fixtures 1-5 cover the normal/edge/adversarial/failure/governance-sensitive categories from the original retrofit phase. Fixtures 6-15 were added in Phase 11 (Review Skill Governance Evidence) to close a gap Phase 10 identified: the single governance-sensitive fixture (5) exercised only one governance relationship, while `docs/Skill Testing Standard.md` Section 2's second paragraph requires the full governance-relationship series for any Review-type Skill. Fixtures 16-22 were added in Phase 13 (Certification Blocker Remediation) to close concrete defects and coverage gaps the Phase 12 independent certification pilot identified: a tier-conflation defect in fixture 6 (rewritten), a thin fixture 8 (rewritten), an overdetermined fixture 9 (rewritten), genuine Override/Conflict governance coverage (16-17), and the 3 named Edge Cases (18-20) and 2 named Failure Handling triggers (21-22) that had no exercising fixture. See "Governance-Relationship Coverage" and "Named Edge Case / Failure Handling Coverage" below for the mapping.

## What this is, and isn't

Fixture specifications, not automated assertions — same convention as `tests/skill-tests/code-review/README.md`. Each fixture is run by loading `skills/database-review/SKILL.md` as the acting agent's instructions, feeding the fixture's Input Material verbatim, and checking output against Pass Criteria while watching for Fail Signals.

**These fixtures are well-formed and structurally complete; they are not, by themselves, confirmed-passing behavioral evidence.** Per `docs/Skill Testing Standard.md` Section 1's evidence-strength distinction: a fixture existing, carrying explicit Pass Criteria/Fail Signals, and being structurally validated by `scripts/validate_skill_test_evidence.py` proves the fixture is sound — it does not prove `skills/database-review/SKILL.md` actually produces the described behavior. That requires either the fixture being executed against a live model invocation of the Skill, or an independent reviewer's own read reaching the same conclusion. Neither has occurred for these fixtures as of Phase 13; this gap is stated here explicitly rather than left implicit — see `docs/Independent Certification Report.md` for the Phase 12 pilot's full evidence-tier analysis, which this phase's remediation does not itself close.

Re-run all fixtures whenever `skills/database-review/SKILL.md` changes; re-run fixtures 6 onward whenever `docs/Governance Precedence Model.md` or `docs/Governance Evaluation.md` changes.

## Fixtures

| # | File | Category |
|---|---|---|
| 1 | `01-normal-not-null-no-default-migration.md` | Happy path — a migration that will fail against existing rows |
| 2 | `02-edge-small-config-table-no-index.md` | Edge case — an unindexed filter on a table with no scale evidence, correctly not flagged |
| 3 | `03-adversarial-pressure-to-approve-destructive-drop.md` | Adversarial — pressure to approve a destructive column drop with no usage verification |
| 4 | `04-failure-no-visibility-into-current-schema.md` | Failure handling — migration reviewed with no visibility into current schema/data |
| 5 | `05-governance-exception-targets-mandatory-integrity-rule.md` | Governance-sensitive — an exception attempts to waive a Mentor Mandatory data-integrity requirement |
| 06 | `06-governance-compatible-child-configurable-pool-size.md` | Governance-sensitive — Compatible: Child Configurable lock-duration threshold within a Mentor Mandatory Migration Safety bound (rewritten Phase 13: clarified as two distinct linked requirements, not one requirement with two tiers; connection-pool framing removed as unsupported by any Rule) |
| 07 | `07-governance-additive-child-mandatory-migration-review.md` | Governance-sensitive — Additive: Child Mandatory rollback-plan requirement stacked on Mentor migration-safety baseline |
| 08 | `08-governance-advisory-no-conflict-naming-convention.md` | Governance-sensitive — Child Advisory optimistic-concurrency preference, no conflict (rewritten Phase 13: now grounded in Rules → Transactions and Concurrency, requiring the model to verify the actual mechanism, not just the rule's existence) |
| 09 | `09-governance-out-of-scope-child-rule.md` | Governance-sensitive — a declared rule that is data-layer-relevant in topic but whose scope glob excludes the reviewed material (rewritten Phase 13: no longer overdetermined by an unrelated topic) |
| 10 | `10-governance-indeterminate-applicability.md` | Governance-sensitive — rule applicability can't be determined from available evidence |
| 11 | `11-governance-applicable-exception-advisory-deviation.md` | Governance-sensitive — an approved, scoped, unexpired exception legitimately deviating from Advisory guidance |
| 12 | `12-governance-expired-exception-no-benefit.md` | Governance-sensitive — an exception with `status: expired` provides no protection from a Mandatory finding (rewritten Phase 13: uses `status: expired` directly, per `docs/Child Rules and Exceptions.md` §9, rather than an `approved` status with a past `expiresAt`) |
| 13 | `13-governance-severity-independent-of-classification.md` | Governance-sensitive — classification and severity stay independent axes |
| 14 | `14-rule-coverage-query-plan-verification.md` | Rule coverage — Query-Plan Verification (Phase 10) |
| 15 | `15-rule-coverage-over-fetching.md` | Rule coverage — Over-Fetching (Phase 10) |
| 16 | `16-governance-override-child-advisory-primary-key-convention.md` | Governance-sensitive — genuine Override: Child Advisory primary-key convention legitimately replaces Mentor Advisory guidance |
| 17 | `17-governance-conflict-child-mandatory-hard-delete-vs-mentor-advisory-soft-delete.md` | Governance-sensitive — genuine Conflict: Child Mandatory hard-delete policy disagrees with Mentor Advisory soft-delete guidance |
| 18 | `18-edge-query-pattern-isolated-no-call-frequency.md` | Edge case — N+1 pattern reviewed with no visibility into call frequency (named Edge Case) |
| 19 | `19-edge-new-table-no-existing-data.md` | Edge case — brand-new table, existing-data migration concerns don't apply (named Edge Case) |
| 20 | `20-edge-orm-generated-migration-reviewed-as-hand-written.md` | Edge case — auto-generated migration reviewed with full rigor (named Edge Case) |
| 21 | `21-failure-declared-engine-orm-undeterminable.md` | Failure handling — declared engine/ORM can't be determined (named Failure Handling trigger) |
| 22 | `22-failure-table-scale-undeterminable.md` | Failure handling — table's actual scale can't be determined and the finding depends on it (named Failure Handling trigger) |

## Governance-Relationship Coverage (Phase 11-13)

Mapping of `docs/Skill Testing Standard.md` Section 2's required governance-relationship categories to the fixture that exercises each:

| Relationship | Fixture |
|---|---|
| Compatible | #06 |
| Additive | #07 |
| Prohibited Override | #05 |
| Override (genuine — Child Advisory replaces Mentor Advisory) | #16 |
| Conflict (genuine — Child Mandatory disagrees with Mentor Advisory) | #17 |
| Advisory, no conflict | #08 |
| Out-of-scope | #09 |
| Indeterminate applicability | #10 |
| Applicable exception | #11 |
| Expired exception | #12 |
| Security-Mandatory downgrade | N/A — see Note below |
| Severity independent of classification | #13 |

**Note on "Security-Mandatory downgrade":** this category is `skills/security-review/SKILL.md`'s own stricter carve-out (its Governance Integration section states this is "the one case where this Skill's Governance Integration is stricter than the general Child Governance mechanism"). `skills/database-review/SKILL.md`'s Governance Integration section claims no equivalent stricter posture, so an ordinary Prohibited Override (fixture #05) already covers the applicable requirement here — a dedicated security-downgrade fixture would test a claim this Skill doesn't make.

## Named Edge Case / Failure Handling Coverage (Phase 13)

Per `docs/Skill Testing Standard.md` Section 2: "an edge case named in the Skill but never exercised in a fixture is a gap in the fixtures, not an acceptable omission" — same rule for Failure Handling triggers. `skills/database-review/SKILL.md` names 4 Edge Cases and 3 Failure Handling triggers.

| Named scenario (from `skills/database-review/SKILL.md`) | Fixture |
|---|---|
| Edge Case — migration reviewed with no visibility into current production data volume | #04 |
| Edge Case — query pattern reviewed in isolation, no visibility into actual call frequency | #18 |
| Edge Case — new table with no existing data at all | #19 |
| Edge Case — ORM-generated migration reviewed automatically | #20 |
| Failure Handling — current schema state can't be determined | #04 |
| Failure Handling — declared engine/ORM can't be determined | #21 |
| Failure Handling — table's actual scale can't be determined and the finding depends on it | #22 |
