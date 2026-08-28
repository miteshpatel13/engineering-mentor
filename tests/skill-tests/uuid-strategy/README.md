# uuid-strategy Skill — Regression Fixtures

7 narrative fixture specifications for `skills/uuid-strategy/SKILL.md`, a Domain Pattern-type Skill (`docs/Skill Taxonomy.md` Section 1). Authored in Phase 22, generalized from `mentor-skills-source/skills/uuid-strategy/SKILL.md` with every Conference & Event Management System-specific detail (entity/table names, the project's specific `<Table>ID`/`<Table>UUID`/`QRToken` column-naming convention, its specific NestJS-pipe resolution mechanism) removed and replaced with technology-agnostic reasoning and illustrative, explicitly-non-mandatory examples.

## What this is, and isn't

Fixture specifications, not automated assertions — same convention as every other Skill's fixture set in this repository. Each fixture is run by loading `skills/uuid-strategy/SKILL.md` as the acting agent's instructions, feeding the fixture's Input Material verbatim, and checking output against Pass Criteria while watching for Fail Signals.

As with `skills/idempotency/SKILL.md` and `skills/soft-delete/SKILL.md`, `uuid-strategy` is Domain Pattern, not Review-type — it produces no findings against a real repository. These fixtures test whether an agent applying this Skill's Rules reaches the correct design conclusion, including correctly declining to recommend an opaque identifier where it isn't warranted (fixture 02) and — the sharpest test of this Skill's single most important boundary — correctly rejecting opacity as a substitute for authorization when explicitly pressured to (fixtures 03 and 05).

**These fixtures are well-formed and structurally complete; they are not, by themselves, confirmed-passing behavioral evidence.** Per `docs/Skill Testing Standard.md` Section 1, that requires either Tier D (execution against a live model invocation) or Tier E (an independent reviewer's own read). **Neither has occurred for these fixtures as of Phase 22.** No Tier D execution was performed and none is claimed; no independent human review has occurred and none is claimed. Evidence stands at Tier A/B/C only.

Re-run all fixtures whenever `skills/uuid-strategy/SKILL.md` changes; re-run fixtures 5-6 whenever `docs/Governance Precedence Model.md` or `docs/Governance Evaluation.md` changes.

## Fixtures

| # | File | Category |
|---|---|---|
| 01 | `01-normal-public-resource-opaque-identifier-warranted.md` | Normal — designing identifiers for a public-facing order resource |
| 02 | `02-edge-internal-only-table-no-benefit.md` | Edge case — correctly declining to recommend an opaque identifier where it isn't warranted |
| 03 | `03-adversarial-opacity-presented-as-sufficient-security.md` | Adversarial — opacity proposed as a substitute for an authorization check |
| 04 | `04-failure-audience-not-established.md` | Failure handling — material doesn't establish the identifier's audience |
| 05 | `05-governance-prohibited-override-exception-waives-authorization.md` | Governance-sensitive — Prohibited Override: an exception misuses this Skill's guidance to justify waiving a consuming Skill's authorization finding |
| 06 | `06-governance-conflict-child-mandatory-identifier-format-vs-mentor-advisory-collision-safety.md` | Governance-sensitive — Conflict: a Child Mandatory format rule disagrees with this Skill's own Advisory collision-safety reasoning |
| 07 | `07-rule-coverage-generation-strategy-tradeoff.md` | Rule coverage — store-generated vs. application-generated tradeoff given a concrete constraint |

## Rule Coverage

Identifier Purpose and Audience (01, 02, 04), When an Opaque Identifier Is Warranted (01, 02), Generation Strategy (07), Collision Considerations (06), Storage/Indexing/Ordering (01, 02), Resolution Boundary (01), Exposure and Security Considerations (03, 05), Migration Concerns (not independently exercised — known limitation, see below).

## Governance-Relationship Coverage

Two of the twelve categories in `docs/Governance Precedence Model.md` Section 10 are exercised: Prohibited Override (05), Conflict (06) — deliberately narrower than the full matrix the three Review-type Skills carry, for the same reason stated in the `idempotency` and `soft-delete` READMEs: this Skill doesn't itself classify governance relationships; these fixtures verify it reasons correctly about the handoff, including the sharpest case (05) where an exception specifically misuses this Skill's own guidance as false justification.

## Known Limitations

- Migration Concerns is not independently exercised by a dedicated fixture. Not a Testing Standard violation — recorded as a genuine limitation for a future fixture-expansion pass.
- Only 2 of 12 governance-relationship categories are exercised, for the reason stated above.
- No Tier D or Tier E evidence exists for this Skill as of Phase 22. Tier A/B/C only.
