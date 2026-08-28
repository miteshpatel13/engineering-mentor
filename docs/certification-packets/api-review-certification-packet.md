# Independent Certification Packet — `api-review`

## Status

**Reusable review packet, Proposed process (`docs/Skill Certification Process.md`).** This packet exists so a genuinely independent Reviewer (see that document's Section 3) can evaluate `skills/api-review/SKILL.md` **without needing to trust any prior Claude session's conclusions**, this one included. Everything below Section 4 described as a prior session's finding is labeled as such and provided as *context*, not a substitute for the Reviewer's own work. **This packet does not contain a certification decision.** Section 8's decision form is blank by design.

## 1. Skill Under Review

- File: `skills/api-review/SKILL.md`
- Category: API · Skill Type: Review
- Current lifecycle stage: **Reviewed** (not Certified — see `docs/Skill Ecosystem Inventory.md` Section 7)
- Version: no commit history exists for this file within this engagement (confirmed via `git status`); review against current on-disk content as of your review date, and record that date.

## 2. Authoritative Standards (read directly)

- `docs/Skill Standard.md`, `docs/Skill Testing Standard.md`, `docs/Skill Quality Standard.md`, `docs/Skill Taxonomy.md`.
- `docs/Governance Precedence Model.md`, `docs/Governance Evaluation.md`, `docs/Child Rules and Exceptions.md` (exception `status`/`expiresAt` semantics — directly relevant to fixtures 05/11/12/21).
- `context/standards/API & Backend Standards.md` — the plain checklist this Skill's Rules should instantiate (note: this Skill deliberately does not own every item on that list — see its own Scope "Out of scope" bullet for the explicit timeout/N+1 delegations).
- `docs/Skill Certification Process.md` — Section 5 is the Checklist this packet instantiates below.

## 3. Fixture Set

`tests/skill-tests/api-review/` — 22 fixtures + README:

| # | File | Category |
|---|---|---|
| 01 | `01-normal-breaking-field-removal-no-versioning.md` | normal |
| 02 | `02-edge-internal-endpoint-different-error-shape.md` | edge |
| 03 | `03-adversarial-pressure-to-skip-idempotency.md` | adversarial |
| 04 | `04-failure-vague-intent-no-concrete-contract.md` | failure-handling (named Failure Handling trigger) |
| 05 | `05-governance-child-rule-conflicts-mandatory-error-shape.md` | governance — Prohibited Override (rule) |
| 06 | `06-governance-compatible-child-configurable-page-size.md` | governance — Compatible |
| 07 | `07-governance-additive-child-mandatory-rate-limit-header.md` | governance — Additive |
| 08 | `08-governance-advisory-no-conflict-response-envelope.md` | governance — Advisory, no conflict |
| 09 | `09-governance-out-of-scope-child-rule.md` | governance — Out-of-scope |
| 10 | `10-governance-indeterminate-applicability.md` | governance — Unknown/Indeterminate |
| 11 | `11-governance-applicable-exception-advisory-deviation.md` | governance — Applicable Exception |
| 12 | `12-governance-expired-exception-no-benefit.md` | governance — Inactive/Expired Exception |
| 13 | `13-governance-severity-independent-of-classification.md` | governance — Severity independence |
| 14 | `14-rule-coverage-pagination.md` | rule-coverage |
| 15 | `15-governance-override-child-advisory-pagination-link-header.md` | governance — Override |
| 16 | `16-governance-conflict-child-mandatory-error-envelope-vs-mentor-advisory-problem-details.md` | governance — Conflict |
| 17 | `17-edge-brand-new-api-no-existing-conventions.md` | edge (named Edge Case) |
| 18 | `18-edge-breaking-change-internal-only-no-external-consumers.md` | edge (named Edge Case) |
| 19 | `19-edge-graphql-contract-reviewed-with-rest-expectations.md` | edge (named Edge Case) |
| 20 | `20-failure-conventions-undeterminable-from-context-discovery.md` | failure (named Failure Handling trigger) |
| 21 | `21-governance-mandatory-exception-active-vs-mentor-mandatory.md` | governance — Prohibited Override / Active Exception Against Mandatory |
| 22 | `22-rule-coverage-http-method-semantics.md` | rule-coverage (Rule added Phase 13) |

## 4. Expected Criteria

Each fixture carries its own `## Pass Criteria`/`## Fail Signals` — read directly. `skills/api-review/SKILL.md`'s own `## Edge Cases` (3 named) and `## Failure Handling` (2 named triggers) state the Skill's own completeness bar — verify 17/18/19 against the 3 Edge Cases and 04/20 against the 2 Failure Handling triggers directly.

## 5. Quality Rubric

**Prior self-assessment (Phase 14, same-engagement, NOT independent — context only):** Correctness 4, Completeness 5, Clarity 4, Scope Isolation 5, Context Awareness 5, Governance Compatibility 5, Safety 5, False-Positive Resistance 4, Examples 4, Test Coverage 4 (45/50). **Re-score yourself in Section 8's form.**

## 6. Governance Matrix

Compatible → #06; Additive → #07; Override → #15; Conflict → #16; Prohibited Override (rule) → #05; Prohibited Override / Active Exception Against Mandatory (exception) → #21; Unknown/Indeterminate → #10; Applicable Exception → #11; Inactive/Expired Exception → #12; Advisory/No Conflict → #08; Out-of-Scope → #09; Severity Independent of Classification → #13. Note: fixture 21 replaced a Phase-11-era README entry that had mischaracterized this category as "N/A" — verify this correction is actually sound by reading fixture 21 directly, not by trusting this note. **Verify each cell by reading the cited fixture.**

## 7. Evidence Tier Summary

- **Tier A/B:** all 22 fixtures exist with explicit Pass Criteria/Fail Signals.
- **Tier C:** `python3 scripts/validate_skill_test_evidence.py api-review` reports VALID (re-run yourself).
- **Tier D:** small pilot only — fixtures 01 and 02 (2/22, ~9%), same procedure and limitations as the other two packets (non-independent, below the proposed 30% minimum). Both passed.
- **Tier E:** does not exist. This packet exists to make it possible.

## 8. Known Limitations

- Most Rules (Idempotency, Documentation and Observability) have no dedicated `## Examples` entry — only a same-named rule-coverage fixture. Not a Standard violation; form your own judgment.
- External-dependency timeout ownership is explicitly delegated to `skills/code-review/SKILL.md` (Scope, "Out of scope") rather than owned here — confirm this delegation is actually reasonable, not merely stated, as part of your Scope Isolation check.
- Tier D coverage is 2/22 fixtures, non-independent. Tier E entirely absent.
- No commit history exists for this file within this engagement.

## 9. Reviewer Checklist

Use `docs/Skill Certification Process.md` Section 5 verbatim.

## 10. Certification Decision Form (BLANK)

```text
Reviewer identity:            ____________________  (must be distinguishable from Author)
Independence statement:       ____________________
Review date:                  ____________________
Skill version reviewed:       ____________________
Checklist result (Section 5): [ ] Structure   [ ] Content   [ ] Governance   [ ] Evidence
Quality scores (own):
  Correctness ___  Completeness ___  Clarity ___  Scope Isolation ___
  Context Awareness ___  Governance Compatibility ___  Safety ___
  False-Positive Resistance ___  Examples ___  Test Coverage ___
Final Gate — all conditions individually confirmed?  [ ] YES   [ ] NO
Decision:  [ ] Certified   [ ] Not Certified   [ ] Blocked by Evidence
           [ ] Blocked by Governance   [ ] Blocked by Structure
Decision rationale:            ____________________
Certifier identity (if different from Reviewer): ____________________
Certifier sign-off date:      ____________________
```

This form is intentionally blank. No box above is pre-checked.
