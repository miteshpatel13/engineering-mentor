# soft-delete Skill — Regression Fixtures

7 narrative fixture specifications for `skills/soft-delete/SKILL.md`, a Domain Pattern-type Skill (`docs/Skill Taxonomy.md` Section 1). Authored in Phase 22, generalized from `mentor-skills-source/skills/soft-delete/SKILL.md` with every Conference & Event Management System-specific detail (entity names, table names, the project's specific generated-column MySQL syntax as a stated requirement, its specific `IsActive`/`Status`/`IsAnonymized` field names) removed and replaced with technology-agnostic reasoning and illustrative, explicitly-non-mandatory examples.

## What this is, and isn't

Fixture specifications, not automated assertions — same convention as every other Skill's fixture set in this repository. Each fixture is run by loading `skills/soft-delete/SKILL.md` as the acting agent's instructions, feeding the fixture's Input Material verbatim, and checking output against Pass Criteria while watching for Fail Signals.

As with `skills/idempotency/SKILL.md` (`tests/skill-tests/idempotency/README.md`), `soft-delete` is Domain Pattern, not Review-type — it produces no findings against a real repository. These fixtures test whether an agent applying this Skill's Rules reaches the correct design conclusion (visibility mechanism, uniqueness handling, cascading decision, retention decision), including correctly declining to apply deletion-specific reasoning where it doesn't belong (fixture 02) and correctly resisting pressure to weaken retention for convenience (fixture 03).

**These fixtures are well-formed and structurally complete; they are not, by themselves, confirmed-passing behavioral evidence.** Per `docs/Skill Testing Standard.md` Section 1, that requires either Tier D (execution against a live model invocation) or Tier E (an independent reviewer's own read). **Neither has occurred for these fixtures as of Phase 22.** No Tier D execution was performed and none is claimed; no independent human review has occurred and none is claimed. Evidence stands at Tier A/B/C only.

Re-run all fixtures whenever `skills/soft-delete/SKILL.md` changes; re-run fixtures 5-6 whenever `docs/Governance Precedence Model.md` or `docs/Governance Evaluation.md` changes.

## Fixtures

| # | File | Category |
|---|---|---|
| 01 | `01-normal-structural-visibility-and-conditional-uniqueness.md` | Normal — structural query-visibility exclusion plus conditional uniqueness for a customer table |
| 02 | `02-edge-reference-table-deactivation-not-deletion.md` | Edge case — correctly recognizing Deactivation as distinct from soft-delete |
| 03 | `03-adversarial-pressure-to-hard-delete-for-simplicity.md` | Adversarial — schedule/simplicity pressure to hard-delete audit-relevant financial records |
| 04 | `04-failure-material-doesnt-establish-retention-need.md` | Failure handling — material doesn't establish whether retention is needed at all |
| 05 | `05-governance-prohibited-override-exception-waives-visibility-exclusion.md` | Governance-sensitive — Prohibited Override: an active exception targets a consuming Skill's Mandatory-grounded finding |
| 06 | `06-governance-conflict-child-mandatory-retention-vs-mentor-advisory.md` | Governance-sensitive — Conflict: a Child Mandatory erasure policy disagrees with this Skill's own Advisory retention reasoning |
| 07 | `07-rule-coverage-cascading-relationship-decision.md` | Rule coverage — two contrasting cascading decisions in one scenario |

## Rule Coverage

Logical vs. Physical Deletion (01, 03), Query Visibility (01, 05), Distinguishing Adjacent Lifecycle Concepts (02, 03), Natural-Key Uniqueness (01), Restoration (not independently exercised — known limitation, see below), Cascading and Relationship Considerations (07), Authorization Implications (05), Retention and the Hard-Delete Boundary (03, 04, 06), Auditability (not independently exercised — known limitation).

## Governance-Relationship Coverage

Two of the twelve categories in `docs/Governance Precedence Model.md` Section 10 are exercised: Prohibited Override (05), Conflict (06) — deliberately narrower than the full matrix the three Review-type Skills carry, for the same reason stated in `tests/skill-tests/idempotency/README.md`: this Skill doesn't itself classify governance relationships; these fixtures verify it reasons correctly about the handoff to a consuming Skill, not that it performs classification itself.

## Known Limitations

- Restoration and Auditability Rules are not independently exercised by a dedicated fixture. Not a Testing Standard violation — recorded as a genuine limitation for a future fixture-expansion pass.
- Only 2 of 12 governance-relationship categories are exercised, for the reason stated above.
- No Tier D or Tier E evidence exists for this Skill as of Phase 22. Tier A/B/C only.
