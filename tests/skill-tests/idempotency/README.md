# idempotency Skill — Regression Fixtures

8 narrative fixture specifications for `skills/idempotency/SKILL.md` — the first Domain Pattern-type Skill in this repository (`docs/Skill Taxonomy.md` Section 1). Authored in Phase 21 as the proof case for the external-source → generalized Skill → governance → fixtures → validation pipeline (`docs/Skill Ecosystem Inventory.md`, Phase 20's readiness report), generalized from `mentor-skills-source/skills/idempotency/SKILL.md` with every Conference & Event Management System-specific detail (entity names, table names, project instruction citations, the six enumerated project operations) removed and replaced with technology-agnostic reasoning and illustrative, explicitly-non-mandatory examples.

## What this is, and isn't

Fixture specifications, not automated assertions — same convention as `tests/skill-tests/code-review/README.md` and every other Skill's fixture set in this repository. Each fixture is run by loading `skills/idempotency/SKILL.md` as the acting agent's instructions, feeding the fixture's Input Material verbatim, and checking output against Pass Criteria while watching for Fail Signals.

**A structural note specific to this Skill's type.** `idempotency` is Domain Pattern, not Review-type: it produces no findings against a real repository and is never invoked end-to-end on its own (`docs/Skill Taxonomy.md` Section 2). These fixtures therefore test something adjacent to what a Review-type Skill's fixtures test: not "does the Skill correctly flag a defect in this code," but "does an agent applying this Skill's Rules reach the same design conclusion (request identity, enforcement mechanism, replay behavior, retention decision) a correct application of the pattern requires" — including correctly declining to require the pattern at all (fixture 02) and correctly resisting pressure to weaken it (fixture 03). This is the same narrative/regression evidence tier `docs/Skill Testing Standard.md` Section 1 describes, applied to a Skill Type that document didn't have a worked example of yet.

**These fixtures are well-formed and structurally complete; they are not, by themselves, confirmed-passing behavioral evidence.** Per `docs/Skill Testing Standard.md` Section 1: a fixture existing, carrying explicit Pass Criteria/Fail Signals, and being structurally validated by `scripts/validate_skill_test_evidence.py` proves the fixture is sound — it does not prove `skills/idempotency/SKILL.md` actually produces the described reasoning. That requires either the fixture being executed against a live model invocation of the Skill (Tier D), or an independent reviewer's own read reaching the same conclusion (Tier E). **Neither has occurred for these fixtures as of Phase 21.** No Tier D execution was performed and none is claimed; no independent human review has occurred and none is claimed. This Skill's evidence stands at Tier A/B/C only — see `docs/Skill Testing Standard.md` Section 1 for what each tier means.

Re-run all fixtures whenever `skills/idempotency/SKILL.md` changes; re-run fixtures 5-7 whenever `docs/Governance Precedence Model.md` or `docs/Governance Evaluation.md` changes.

## Fixtures

| # | File | Category |
|---|---|---|
| 01 | `01-normal-webhook-retry-constraint-backed.md` | Normal — designing a webhook handler for expected provider redelivery |
| 02 | `02-edge-no-natural-request-identity.md` | Edge case — an operation that correctly needs no idempotency treatment at all |
| 03 | `03-adversarial-pressure-to-skip-constraint-use-check-then-act.md` | Adversarial — schedule pressure to ship check-then-act instead of a real constraint, on a financially-consequential operation |
| 04 | `04-failure-material-doesnt-establish-retry-plausibility.md` | Failure handling — material doesn't establish whether the operation is retry-prone |
| 05 | `05-governance-prohibited-override-exception-targets-data-integrity-mandatory.md` | Governance-sensitive — Prohibited Override: an active exception targets a consuming Skill's Mandatory-grounded data-integrity finding |
| 06 | `06-governance-compatible-child-rule-narrows-key-header-name.md` | Governance-sensitive — Compatible/Additive: a child rule narrows the mechanism without contradicting the pattern |
| 07 | `07-governance-conflict-child-mandatory-retention-vs-mentor-advisory.md` | Governance-sensitive — Conflict: a Child Mandatory retention policy disagrees with this Skill's own Advisory retention reasoning |
| 08 | `08-rule-coverage-replay-behavior-silent-vs-visible.md` | Rule coverage — choosing between silent no-op and visible duplicate signal, and why |

## Rule Coverage

Every Rules subsection is exercised by at least one fixture: Request Identity (01, 02, 05), Constraint-Backed Enforcement (01, 03, 05), Atomicity (01), Replay Behavior (01, 08), Response Consistency (implicit in 01 — not independently exercised by a dedicated fixture; a known limitation, see below), Expiration and Retention (07), Concurrency Under Duplicate Requests (08), Database vs. Application-Layer Boundary (implicit in 05/06 — not independently exercised by a dedicated fixture; a known limitation, see below).

## Governance-Relationship Coverage

Three of the twelve categories `docs/Governance Precedence Model.md` Section 10 and `docs/Skill Testing Standard.md` Section 2 describe are exercised: Prohibited Override (05), Compatible/Additive (06), Conflict (07). This is deliberately narrower than the full twelve-category matrix the three Review-type Skills (`security-review`, `database-review`, `api-review`) each carry — this Skill produces no findings of its own and does not itself perform governance classification (Governance Integration states this explicitly); the three fixtures here exist to verify that an agent applying this Skill's Rules reasons correctly about how its Advisory-tier guidance interacts with the governance model, not to duplicate the full classification-matrix testing that belongs to the Review-type Skills that actually perform classification.

## Known Limitations

- Response Consistency and the Database vs. Application-Layer Enforcement Boundary Rules are exercised only incidentally within other fixtures, not by a dedicated fixture each. Not a Testing Standard violation (no one-fixture-per-Rule requirement) — recorded as a genuine limitation for a future fixture-expansion pass.
- Only 3 of 12 governance-relationship categories are exercised, for the reason stated above (this Skill doesn't itself classify). If this reasoning is judged insufficient on independent review, the remaining categories (Additive as a category distinct from Compatible, Override, Unknown/Indeterminate, Applicable/Inactive Exception, Advisory/No Conflict, Out-of-Scope, Severity Independence) can be added the same way fixtures 05-07 were.
- No Tier D (model-executed) or Tier E (independent human review) evidence exists for this Skill as of Phase 21. Tier A (fixtures exist), B (explicit Pass Criteria/Fail Signals), and C (structural validation via `scripts/validate_skill_test_evidence.py`) are the only tiers claimed.
- This is the first Domain Pattern-type Skill authored in this repository — the fixture-design approach above (testing applied reasoning rather than finding-flagging) is itself a new pattern for this repository's testing conventions, not yet independently reviewed as the right approach for future Domain Pattern Skills (`soft-delete`, `uuid-strategy`).
