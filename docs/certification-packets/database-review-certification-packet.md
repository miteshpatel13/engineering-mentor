# Independent Certification Packet — `database-review`

## Status

**Reusable review packet, Proposed process (`docs/Skill Certification Process.md`).** This packet exists so a genuinely independent Reviewer (see that document's Section 3) can evaluate `skills/database-review/SKILL.md` **without needing to trust any prior Claude session's conclusions**, this one included. Everything below Section 4 described as a prior session's finding is labeled as such and provided as *context*, not a substitute for the Reviewer's own work. **This packet does not contain a certification decision.** Section 8's decision form is blank by design.

## 1. Skill Under Review

- File: `skills/database-review/SKILL.md`
- Category: Database · Skill Type: Review
- Current lifecycle stage: **Reviewed** (not Certified — see `docs/Skill Ecosystem Inventory.md` Section 7)
- Version: no commit history exists for this file within this engagement (confirmed via `git status`); review against current on-disk content as of your review date, and record that date.

## 2. Authoritative Standards (read directly)

- `docs/Skill Standard.md`, `docs/Skill Testing Standard.md`, `docs/Skill Quality Standard.md`, `docs/Skill Taxonomy.md`.
- `docs/Governance Precedence Model.md`, `docs/Governance Evaluation.md`, `docs/Child Rules and Exceptions.md` (exception `status`/`expiresAt` semantics — directly relevant to fixtures 05/11/12).
- `context/standards/Database Standards.md` — the plain checklist this Skill's Rules should instantiate.
- `docs/Skill Certification Process.md` — Section 5 is the Checklist this packet instantiates below.

## 3. Fixture Set

`tests/skill-tests/database-review/` — 22 fixtures + README:

| # | File | Category |
|---|---|---|
| 01 | `01-normal-not-null-no-default-migration.md` | normal |
| 02 | `02-edge-small-config-table-no-index.md` | edge |
| 03 | `03-adversarial-pressure-to-approve-destructive-drop.md` | adversarial |
| 04 | `04-failure-no-visibility-into-current-schema.md` | failure-handling (also named Edge Case/Failure Handling trigger) |
| 05 | `05-governance-exception-targets-mandatory-integrity-rule.md` | governance — Prohibited Override / Active Exception vs. Mandatory |
| 06 | `06-governance-compatible-child-configurable-pool-size.md` | governance — Compatible |
| 07 | `07-governance-additive-child-mandatory-migration-review.md` | governance — Additive |
| 08 | `08-governance-advisory-no-conflict-naming-convention.md` | governance — Advisory, no conflict |
| 09 | `09-governance-out-of-scope-child-rule.md` | governance — Out-of-scope |
| 10 | `10-governance-indeterminate-applicability.md` | governance — Unknown/Indeterminate |
| 11 | `11-governance-applicable-exception-advisory-deviation.md` | governance — Applicable Exception |
| 12 | `12-governance-expired-exception-no-benefit.md` | governance — Inactive/Expired Exception |
| 13 | `13-governance-severity-independent-of-classification.md` | governance — Severity independence |
| 14 | `14-rule-coverage-query-plan-verification.md` | rule-coverage |
| 15 | `15-rule-coverage-over-fetching.md` | rule-coverage |
| 16 | `16-governance-override-child-advisory-primary-key-convention.md` | governance — Override |
| 17 | `17-governance-conflict-child-mandatory-hard-delete-vs-mentor-advisory-soft-delete.md` | governance — Conflict |
| 18 | `18-edge-query-pattern-isolated-no-call-frequency.md` | edge (named Edge Case) |
| 19 | `19-edge-new-table-no-existing-data.md` | edge (named Edge Case) |
| 20 | `20-edge-orm-generated-migration-reviewed-as-hand-written.md` | edge (named Edge Case) |
| 21 | `21-failure-declared-engine-orm-undeterminable.md` | failure (named Failure Handling trigger) |
| 22 | `22-failure-table-scale-undeterminable.md` | failure (named Failure Handling trigger) |

## 4. Expected Criteria

Each fixture carries its own `## Pass Criteria`/`## Fail Signals` — read directly. `skills/database-review/SKILL.md`'s own `## Edge Cases` (4 named) and `## Failure Handling` (1 paragraph naming 3 distinct triggers) state the Skill's own completeness bar — verify fixture coverage against those named items directly (04/21/22 map to Failure Handling; 18/19/20 plus 04 map to the 4 named Edge Cases).

## 5. Quality Rubric

**Prior self-assessment (Phase 14, same-engagement, NOT independent — context only):** Correctness 4, Completeness 5, Clarity 4, Scope Isolation 5, Context Awareness 5, Governance Compatibility 5, Safety 5, False-Positive Resistance 4, Examples 4, Test Coverage 4 (45/50). **Re-score yourself in Section 8's form.**

## 6. Governance Matrix

Compatible → #06; Additive → #07; Override → #16; Conflict → #17; Prohibited Override / Active Exception Against Mandatory → #05; Unknown/Indeterminate → #10; Applicable Exception → #11; Inactive/Expired Exception → #12; Advisory/No Conflict → #08; Out-of-Scope → #09; Severity Independent of Classification → #13. (No separate "security-Mandatory downgrade" fixture — this Skill's Governance Integration claims no equivalent stricter posture to `security-review`'s, so #05 already covers the applicable Prohibited Override case; verify this claim yourself against the Skill's own Governance Integration section.) **Verify each cell by reading the cited fixture.**

## 7. Evidence Tier Summary

- **Tier A/B:** all 22 fixtures exist with explicit Pass Criteria/Fail Signals.
- **Tier C:** `python3 scripts/validate_skill_test_evidence.py database-review` reports VALID (re-run yourself).
- **Tier D:** small pilot only — fixtures 01 and 02 (2/22, ~9%), same procedure and same limitations as the `security-review` packet (non-independent, below the proposed 30% minimum). Both passed.
- **Tier E:** does not exist. This packet exists to make it possible.

## 8. Known Limitations

- Most Rules (Query-Plan Verification, Over-Fetching, Transactions and Concurrency, ORM Behavior) have no dedicated `## Examples` entry — only a same-named rule-coverage fixture. Not a Standard violation; an independent Reviewer should form their own judgment.
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
