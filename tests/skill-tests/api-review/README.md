# api-review Skill — Regression Fixtures

22 permanent behavioral test scenarios for `skills/api-review/SKILL.md`. Fixtures 1-5 cover the normal/edge/adversarial/failure/governance-sensitive categories from the original retrofit phase. Fixtures 6-14 were added in Phase 11 (Review Skill Governance Evidence) to close a gap Phase 10 identified: the single governance-sensitive fixture (5) exercised only one governance relationship, while `docs/Skill Testing Standard.md` Section 2's second paragraph requires the full governance-relationship series for any Review-type Skill. Fixtures 15-22 were added in Phase 13 (Certification Blocker Remediation) to close concrete gaps the Phase 12 independent certification pilot identified: genuine Override/Conflict governance coverage (15-16), the 3 named Edge Cases (17-19) and 1 named Failure Handling trigger (20) that had no exercising fixture, a genuine active-exception-vs-Mentor-Mandatory fixture (21, replacing a previously-mischaracterized "N/A" README entry), and coverage for the new HTTP Method Semantics Rule (22, added this phase — see `skills/api-review/SKILL.md`'s Rules section and Section "Completeness Remediation" below). See "Governance-Relationship Coverage" and "Named Edge Case / Failure Handling Coverage" below for the mapping.

## What this is, and isn't

Fixture specifications, not automated assertions — same convention as `tests/skill-tests/code-review/README.md`. Each fixture is run by loading `skills/api-review/SKILL.md` as the acting agent's instructions, feeding the fixture's Input Material verbatim, and checking output against Pass Criteria while watching for Fail Signals.

**These fixtures are well-formed and structurally complete; they are not, by themselves, confirmed-passing behavioral evidence.** Per `docs/Skill Testing Standard.md` Section 1's evidence-strength distinction: a fixture existing, carrying explicit Pass Criteria/Fail Signals, and being structurally validated by `scripts/validate_skill_test_evidence.py` proves the fixture is sound — it does not prove `skills/api-review/SKILL.md` actually produces the described behavior. That requires either the fixture being executed against a live model invocation of the Skill, or an independent reviewer's own read reaching the same conclusion. Neither has occurred for these fixtures as of Phase 13; this gap is stated here explicitly rather than left implicit — see `docs/Independent Certification Report.md` for the Phase 12 pilot's full evidence-tier analysis, which this phase's remediation does not itself close.

Re-run all fixtures whenever `skills/api-review/SKILL.md` changes; re-run fixtures 6 onward whenever `docs/Governance Precedence Model.md` or `docs/Governance Evaluation.md` changes.

## Fixtures

| # | File | Category |
|---|---|---|
| 1 | `01-normal-breaking-field-removal-no-versioning.md` | Happy path — a field removed from a public API with no deprecation/versioning |
| 2 | `02-edge-internal-endpoint-different-error-shape.md` | Edge case — internal endpoint deliberately uses a different, already-established error shape |
| 3 | `03-adversarial-pressure-to-skip-idempotency.md` | Adversarial — pressure to skip an idempotency mechanism for a retryable payment operation |
| 4 | `04-failure-vague-intent-no-concrete-contract.md` | Failure handling — a request describes intent with no concrete contract to review |
| 5 | `05-governance-child-rule-conflicts-mandatory-error-shape.md` | Governance-sensitive — a child rule conflicts with a Mentor Mandatory error-response requirement |
| 06 | `06-governance-compatible-child-configurable-page-size.md` | Governance-sensitive — Compatible: Child Configurable default page size alongside Mentor Mandatory pagination requirement |
| 07 | `07-governance-additive-child-mandatory-rate-limit-header.md` | Governance-sensitive — Additive: Child Mandatory rate-limit headers stacked on Mentor error-shape baseline |
| 08 | `08-governance-advisory-no-conflict-response-envelope.md` | Governance-sensitive — Child Advisory response-envelope preference, no conflict |
| 09 | `09-governance-out-of-scope-child-rule.md` | Governance-sensitive — a declared child rule outside this Skill's contract scope |
| 10 | `10-governance-indeterminate-applicability.md` | Governance-sensitive — rule applicability can't be determined from available evidence |
| 11 | `11-governance-applicable-exception-advisory-deviation.md` | Governance-sensitive — an approved, scoped, unexpired exception legitimately deviating from Advisory guidance |
| 12 | `12-governance-expired-exception-no-benefit.md` | Governance-sensitive — an exception with `status: expired` provides no protection from a Mandatory finding (rewritten Phase 13: uses `status: expired` directly, per `docs/Child Rules and Exceptions.md` §9) |
| 13 | `13-governance-severity-independent-of-classification.md` | Governance-sensitive — classification and severity stay independent axes |
| 14 | `14-rule-coverage-pagination.md` | Rule coverage — Pagination (Phase 10) |
| 15 | `15-governance-override-child-advisory-pagination-link-header.md` | Governance-sensitive — genuine Override: Child Advisory pagination-header convention legitimately replaces Mentor Advisory guidance |
| 16 | `16-governance-conflict-child-mandatory-error-envelope-vs-mentor-advisory-problem-details.md` | Governance-sensitive — genuine Conflict: Child Mandatory error envelope disagrees with Mentor Advisory Problem-Details guidance |
| 17 | `17-edge-brand-new-api-no-existing-conventions.md` | Edge case — brand-new API, no existing conventions (named Edge Case) |
| 18 | `18-edge-breaking-change-internal-only-no-external-consumers.md` | Edge case — breaking change on a genuinely internal-only API (named Edge Case) |
| 19 | `19-edge-graphql-contract-reviewed-with-rest-expectations.md` | Edge case — GraphQL contract, don't apply REST versioning expectations (named Edge Case) |
| 20 | `20-failure-conventions-undeterminable-from-context-discovery.md` | Failure handling — existing conventions can't be determined (named Failure Handling trigger) |
| 21 | `21-governance-mandatory-exception-active-vs-mentor-mandatory.md` | Governance-sensitive — an active exception attempts to weaken a Mentor Mandatory requirement (general case; replaces the previous "N/A" README entry) |
| 22 | `22-rule-coverage-http-method-semantics.md` | Rule coverage — HTTP Method Semantics (Rule added Phase 13) |

## Governance-Relationship Coverage (Phase 11-13)

| Relationship | Fixture |
|---|---|
| Compatible | #06 |
| Additive | #07 |
| Prohibited Override (child rule) | #05 |
| Prohibited Override (active exception vs. Mentor Mandatory) | #21 |
| Override (genuine — Child Advisory replaces Mentor Advisory) | #15 |
| Conflict (genuine — Child Mandatory disagrees with Mentor Advisory) | #16 |
| Advisory, no conflict | #08 |
| Out-of-scope | #09 |
| Indeterminate applicability | #10 |
| Applicable exception | #11 |
| Expired exception | #12 |
| Severity independent of classification | #13 |

**Correction (Phase 13) — "Security-Mandatory downgrade" / active-exception coverage:** Phase 11's README previously recorded this category as "N/A — see Note below," reasoning that `skills/security-review/SKILL.md`'s stricter security-exception carve-out doesn't apply to this Skill. The Phase 12 independent certification pilot found this reasoning conflated two different things: `docs/Skill Testing Standard.md` Section 2's actual requirement is the *general* category — any active exception attempting to touch a Mentor Mandatory requirement (matching `tests/skill-tests/code-review/18-exception-prohibited-security-downgrade.md`) — not specifically the security-classified narrow carve-out. No prior fixture in this set tested an active exception against a Mentor Mandatory requirement at all (fixture 5 is a rule, not an exception; fixture 12 is an inactive exception). Fixture 21 closes this gap directly; the category is no longer N/A.

## Named Edge Case / Failure Handling Coverage (Phase 13)

Per `docs/Skill Testing Standard.md` Section 2. `skills/api-review/SKILL.md` names 3 Edge Cases and 2 Failure Handling triggers.

| Named scenario (from `skills/api-review/SKILL.md`) | Fixture |
|---|---|
| Edge Case — brand-new API with no existing conventions | #17 |
| Edge Case — breaking change on a genuinely internal-only API with no external consumers | #18 |
| Edge Case — GraphQL contract reviewed with REST-shaped expectations | #19 |
| Failure Handling — material describes intent with no concrete contract | #04 |
| Failure Handling — repository's existing conventions can't be determined | #20 |

## Completeness Remediation (Phase 13)

Per the Phase 12 pilot's Completeness finding: `context/standards/API & Backend Standards.md` names "use appropriate HTTP semantics where REST is used" and "use timeouts for external dependencies" as API/backend standards items, neither of which previously had a Rule or an explicit delegation in `skills/api-review/SKILL.md`. This phase resolved both, on the evidence, rather than leaving ownership ambiguous:

- **HTTP method semantics** — genuinely belongs to this Skill (it is a contract-shape/correctness concern, not an implementation-reliability concern). Added as a new Rule subsection (`### HTTP Method Semantics`), with fixture #22 (rule coverage) and a new worked Example in `## Examples`.
- **External-dependency timeouts** — does not belong to this Skill; it is implementation-level reliability logic, not contract shape. Explicitly delegated to `skills/code-review/SKILL.md`'s general reliability review via this Skill's Scope "Out of scope" bullet — no new Rule was added here, and no duplicate fixture was created, since `skills/code-review/SKILL.md` already reviews reliability concerns (its own Availability/Resource-Exhaustion severity guidance covers timeout-adjacent concerns) and adding a second, narrower copy of that concern here would duplicate rather than clarify ownership.

Also per the pilot's Scope finding: `skills/database-review/SKILL.md` was added to this Skill's `## Related Skills`, with an explicit boundary for N+1 (this Skill flags contract-shape signals that make N+1 likely; `database-review` owns confirming the actual query pattern).
