# Independent Certification Packet — `security-review`

## Status

**Reusable review packet, Proposed process (`docs/Skill Certification Process.md`).** This packet exists so a genuinely independent Reviewer (see that document's Section 3) can evaluate `skills/security-review/SKILL.md` **without needing to trust any prior Claude session's conclusions**, this one included. Everything below Section 4 that is described as a prior session's finding is labeled as such explicitly and is provided as *context*, not as a substitute for the Reviewer's own work. **This packet does not contain a certification decision.** Section 8's decision form is blank by design — an independent Reviewer/Certifier fills it in, not this document's author.

## 1. Skill Under Review

- File: `skills/security-review/SKILL.md`
- Category: Security · Skill Type: Review
- Current lifecycle stage: **Reviewed** (not Certified — see `docs/Skill Ecosystem Inventory.md` Section 7)
- Version: this repository has no commit history for this file within this engagement (confirmed via `git status` — untracked/uncommitted throughout); review against the file's current on-disk content as of the date you perform this review, and record that date in your Certification Record (Section 4 of the Process document).

## 2. Authoritative Standards (read these directly — do not rely on this packet's summaries of them)

- `docs/Skill Standard.md` — structural contract.
- `docs/Skill Testing Standard.md` — evidence-tier model and fixture-category requirements.
- `docs/Skill Quality Standard.md` — the ten-dimension scoring rubric and certification threshold.
- `docs/Skill Taxonomy.md` — lifecycle stages.
- `docs/Governance Precedence Model.md` — the six-category conflict model (Compatible/Additive/Override/Conflict/Prohibited Override/Unknown) this Skill's Governance Integration must correctly implement.
- `docs/Governance Evaluation.md` — `scripts/evaluate_governance.py`'s responsibility boundary.
- `docs/Child Rules and Exceptions.md` — exception lifecycle semantics (`status` vs. `expiresAt`), directly relevant to fixtures 05/11/12.
- `context/checklists/Security Checklist.md`, a plain ten-item checklist this Skill's Rules should instantiate, not merely gesture at.
- `docs/Skill Certification Process.md` — this packet's own process document; Section 5 is the Checklist this packet instantiates below.

## 3. Fixture Set

`tests/skill-tests/security-review/` — 20 fixtures + README. Full list (read each fixture directly; do not evaluate from this table alone):

| # | File | Category |
|---|---|---|
| 01 | `01-normal-idor-missing-ownership-check.md` | normal |
| 02 | `02-edge-parameterized-query-no-injection-risk.md` | edge |
| 03 | `03-adversarial-frontend-only-validation-presented-as-sufficient.md` | adversarial |
| 04 | `04-failure-no-visibility-into-caller.md` | failure-handling |
| 05 | `05-governance-exception-targets-security-mandatory.md` | governance — Prohibited Override (exception) |
| 06 | `06-governance-compatible-child-configurable-rate-limit.md` | governance — Compatible |
| 07 | `07-governance-additive-child-mandatory-mfa.md` | governance — Additive |
| 08 | `08-governance-advisory-no-conflict-logging-library.md` | governance — Advisory, no conflict |
| 09 | `09-governance-out-of-scope-child-rule.md` | governance — Out-of-scope |
| 10 | `10-governance-indeterminate-applicability.md` | governance — Unknown/Indeterminate |
| 11 | `11-governance-applicable-exception-advisory-deviation.md` | governance — Applicable Exception |
| 12 | `12-governance-expired-exception-no-benefit.md` | governance — Inactive/Expired Exception |
| 13 | `13-governance-severity-independent-of-classification.md` | governance — Severity independence |
| 14 | `14-governance-prohibited-override-plain-child-rule.md` | governance — Prohibited Override (rule) |
| 15 | `15-rule-coverage-file-upload-safety.md` | rule-coverage |
| 16 | `16-rule-coverage-dependency-risk.md` | rule-coverage |
| 17 | `17-rule-coverage-secure-logging.md` | rule-coverage |
| 18 | `18-rule-coverage-authn-vs-authz-distinction.md` | rule-coverage |
| 19 | `19-governance-override-child-advisory-session-token-format.md` | governance — Override |
| 20 | `20-governance-conflict-child-mandatory-logformat-vs-mentor-advisory.md` | governance — Conflict |

## 4. Expected Criteria

Do not re-derive from prose memory. Each fixture above carries its own explicit `## Pass Criteria` and `## Fail Signals` — read each fixture directly for its own criteria. `skills/security-review/SKILL.md`'s own `## Edge Cases` (4 named), `## Failure Handling` (1 paragraph), and `## Validation` sections state the Skill's own self-described completeness bar — check fixture coverage against those named items directly, not against this packet's characterization of them.

## 5. Quality Rubric (Section 1 of `docs/Skill Quality Standard.md`)

Ten dimensions, 0–5 or N/A/U, each requiring a stated reason: Correctness, Completeness, Clarity, Scope Isolation, Context Awareness, Governance Compatibility, Safety, False-Positive Resistance, Examples, Test Coverage. **Prior self-assessment (Phase 14, same-engagement, NOT independent — provided for context only, do not adopt without independently re-deriving):** Correctness 4, Completeness 5, Clarity 4, Scope Isolation 5, Context Awareness 5, Governance Compatibility 5, Safety 5, False-Positive Resistance 4, Examples 4, Test Coverage 4 (45/50). **Re-score these yourself in Section 8's form; do not copy these values forward without doing the evaluation.**

## 6. Governance Matrix

The 12-category relationship model this Skill's fixture set must genuinely, distinctly cover (`docs/Governance Precedence Model.md` Section 10, plus exception-lifecycle and severity-independence categories `docs/Skill Testing Standard.md` Section 2 requires): Compatible → #06; Additive → #07; Override → #19; Conflict → #20; Prohibited Override (rule) → #14; Prohibited Override / Active Exception Against Mandatory → #05; Unknown/Indeterminate → #10; Applicable Exception → #11; Inactive/Expired Exception → #12; Advisory/No Conflict → #08; Out-of-Scope → #09; Severity Independent of Classification → #13. **Verify each cell yourself by reading the cited fixture — a prior session's table (including this one) is a claim to check, not a fact to accept.**

## 7. Evidence Tier Summary

- **Tier A/B:** all 20 fixtures exist with explicit Pass Criteria/Fail Signals.
- **Tier C:** `python3 scripts/validate_skill_test_evidence.py security-review` reports VALID (confirm this yourself — re-run it).
- **Tier D:** a small pilot exists — fixtures 01 and 02 only (2/20, ~10%), executed via an `Agent`-tool subagent given only the Skill's literal text and the fixture's Input Material (Pass Criteria withheld), output checked against real Pass Criteria by the same session that ran it. Both passed. **This falls short of `docs/Skill Certification Process.md` Section 6's proposed minimum coverage bar (≥30%, all present categories) and was performed by the same engagement, not an independent party** — treat it as a real but partial and non-independent data point, not as satisfying Tier D at scale.
- **Tier E:** does not exist. No independent Reviewer has ever evaluated this Skill. **This packet exists to make that possible.**

## 8. Known Limitations (stated explicitly, not hidden)

- Most Rules (File-Upload Safety, Dependency Risk, Secure Logging, Abuse and Resource Exhaustion) have no dedicated `## Examples` entry — their only worked material is a same-named rule-coverage fixture, not an Examples-section walkthrough. Not a Standard violation (at least one worked example + negative example where needed is the actual bar), but worth an independent Reviewer's own judgment on whether it's sufficient.
- Tier D coverage is 2/20 fixtures, non-independent.
- Tier E is entirely absent.
- No commit history exists for this file within this engagement — version identification for the Certification Record must use file content/date, not a commit hash.

## 9. Reviewer Checklist

Use `docs/Skill Certification Process.md` Section 5 verbatim (Structure / Content / Governance / Evidence / Final Gate). Check every item against this Skill's actual current files — do not check a box because this packet asserts something is true.

## 10. Certification Decision Form (BLANK — to be completed by the independent Reviewer/Certifier only)

```text
Reviewer identity:            ____________________  (must be distinguishable from Author)
Independence statement:       ____________________  (per Process doc Section 3 — state how
                               each of the 3 conditions is satisfied)
Review date:                  ____________________
Skill version reviewed:       ____________________
Checklist result (Section 5): [ ] Structure   [ ] Content   [ ] Governance   [ ] Evidence
Quality scores (own, not copied from Section 5 above):
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
