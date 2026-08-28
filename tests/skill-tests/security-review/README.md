# security-review Skill — Regression Fixtures

20 permanent behavioral test scenarios for `skills/security-review/SKILL.md`. Fixtures 1-5 cover the normal/edge/adversarial/failure/governance-sensitive categories from the original retrofit phase. Fixtures 6-17 were added in Phase 11 (Review Skill Governance Evidence) to close a gap Phase 10 identified: the single governance-sensitive fixture (5) exercised only one governance relationship, while `docs/Skill Testing Standard.md` Section 2's second paragraph requires the full governance-relationship series for any Review-type Skill. Fixtures 18-20 were added in Phase 13 (Certification Blocker Remediation): fixture 13 was rewritten (it previously mislabeled an unauthenticated-access scenario as "IDOR," conflating Authentication with Authorization contrary to this Skill's own Rules — identified by the Phase 12 independent certification pilot), fixture 18 was added to directly test the AuthN/AuthZ distinction that error was about, and fixtures 19-20 close the genuine Override/Conflict governance-relationship gap the pilot identified.

## What this is, and isn't

Fixture specifications, not automated assertions — same convention as `tests/skill-tests/code-review/README.md`. Each fixture is run by loading `skills/security-review/SKILL.md` as the acting agent's instructions, feeding the fixture's Input Material verbatim, and checking output against Pass Criteria while watching for Fail Signals.

**These fixtures are well-formed and structurally complete; they are not, by themselves, confirmed-passing behavioral evidence.** Per `docs/Skill Testing Standard.md` Section 1's evidence-strength distinction: a fixture existing, carrying explicit Pass Criteria/Fail Signals, and being structurally validated by `scripts/validate_skill_test_evidence.py` proves the fixture is sound — it does not prove `skills/security-review/SKILL.md` actually produces the described behavior. That requires either the fixture being executed against a live model invocation of the Skill, or an independent reviewer's own read reaching the same conclusion. Neither has occurred for these fixtures as of Phase 13; this gap is stated here explicitly rather than left implicit — see `docs/Independent Certification Report.md` for the Phase 12 pilot's full evidence-tier analysis, which this phase's remediation does not itself close.

Re-run all fixtures whenever `skills/security-review/SKILL.md` changes; re-run fixtures 6 onward whenever `docs/Governance Precedence Model.md` or `docs/Governance Evaluation.md` changes.

## Fixtures

| # | File | Category |
|---|---|---|
| 1 | `01-normal-idor-missing-ownership-check.md` | Happy path — an endpoint missing an object-ownership authorization check (IDOR) |
| 2 | `02-edge-parameterized-query-no-injection-risk.md` | Edge case — a fully parameterized query, correctly not flagged for SQL injection |
| 3 | `03-adversarial-frontend-only-validation-presented-as-sufficient.md` | Adversarial — pressure to accept frontend-only validation as the security control |
| 4 | `04-failure-no-visibility-into-caller.md` | Failure handling — code reviewed with no visibility into what calls it |
| 5 | `05-governance-exception-targets-security-mandatory.md` | Governance-sensitive — an approved exception targets a Mentor Mandatory security requirement |
| 06 | `06-governance-compatible-child-configurable-rate-limit.md` | Governance-sensitive — Compatible: Child Configurable rate-limit value alongside Mentor Mandatory rate-limiting requirement |
| 07 | `07-governance-additive-child-mandatory-mfa.md` | Governance-sensitive — Additive: Child Mandatory MFA requirement stacked on Mentor Mandatory authentication |
| 08 | `08-governance-advisory-no-conflict-logging-library.md` | Governance-sensitive — Child Advisory logging-library preference, no conflict |
| 09 | `09-governance-out-of-scope-child-rule.md` | Governance-sensitive — a declared child rule outside this Skill's security scope |
| 10 | `10-governance-indeterminate-applicability.md` | Governance-sensitive — rule applicability can't be determined from available evidence |
| 11 | `11-governance-applicable-exception-advisory-deviation.md` | Governance-sensitive — an approved, scoped, unexpired exception legitimately deviating from Advisory guidance |
| 12 | `12-governance-expired-exception-no-benefit.md` | Governance-sensitive — an exception with `status: expired` provides no protection from a Mandatory finding (rewritten Phase 13: uses `status: expired` directly, per `docs/Child Rules and Exceptions.md` §9, rather than an `approved` status with a past `expiresAt`) |
| 13 | `13-governance-severity-independent-of-classification.md` | Governance-sensitive — classification and severity stay independent axes (rewritten Phase 13: the vehicle scenario is now a genuine AuthZ/IDOR finding — authenticated caller, missing ownership check — rather than a mislabeled unauthenticated-access scenario) |
| 14 | `14-governance-prohibited-override-plain-child-rule.md` | Governance-sensitive — an ordinary child rule (not an exception) attempts a Prohibited Override of a Mandatory authorization requirement |
| 15 | `15-rule-coverage-file-upload-safety.md` | Rule coverage — File-Upload Safety (Phase 10) |
| 16 | `16-rule-coverage-dependency-risk.md` | Rule coverage — Dependency Risk (Phase 10) |
| 17 | `17-rule-coverage-secure-logging.md` | Rule coverage — Secure Logging (Phase 10) |
| 18 | `18-rule-coverage-authn-vs-authz-distinction.md` | Rule coverage — Authentication vs. Authorization (Phase 13, added to directly test the distinction fixture 13 previously got wrong) |
| 19 | `19-governance-override-child-advisory-session-token-format.md` | Governance-sensitive — genuine Override: Child Advisory session-token-format convention legitimately replaces Mentor Advisory guidance |
| 20 | `20-governance-conflict-child-mandatory-logformat-vs-mentor-advisory.md` | Governance-sensitive — genuine Conflict: Child Mandatory log-format convention disagrees with Mentor Advisory structured-logging guidance |

## Governance-Relationship Coverage (Phase 11-13)

| Relationship | Fixture |
|---|---|
| Compatible | #06 |
| Additive | #07 |
| Prohibited Override (child rule) | #14 |
| Override (genuine — Child Advisory replaces Mentor Advisory) | #19 |
| Conflict (genuine — Child Mandatory disagrees with Mentor Advisory) | #20 |
| Advisory, no conflict | #08 |
| Out-of-scope | #09 |
| Indeterminate applicability | #10 |
| Applicable exception | #11 |
| Expired exception | #12 |
| Security-Mandatory downgrade (exception) | #05 |
| Severity independent of classification | #13 |

## Note on Fixture 13's Phase 13 Rewrite

The original fixture 13 described "a direct, unauthenticated read of another user's private data" and labeled it "an IDOR" — but this Skill's own Rules (Authentication vs. Authorization) require IDOR to describe an *authenticated* caller acting outside their authorization; an unauthenticated read is a missing-authentication (AuthN) finding, not an AuthZ/IDOR finding. The rewritten fixture 13 keeps its original governance point (severity is independent of the classification of the rule that prompted inspection) but uses a genuinely authenticated-caller, ownership-check-missing scenario as the vehicle, so a response that correctly follows this Skill's own AuthN/AuthZ distinction is never at odds with the fixture's own Pass Criteria. Fixture 18 was added separately to test the AuthN/AuthZ distinction directly, with two endpoints in one scenario (one AuthN failure, one AuthZ/IDOR failure), so a regression of this specific error is caught even if a future edit to fixture 13 drifts again.
