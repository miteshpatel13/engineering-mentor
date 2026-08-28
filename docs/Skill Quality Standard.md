# Skill Quality Standard

## Status

Authoritative. This document formalizes, as Mentor's own canonical Skill quality rubric, the ten-dimension scoring model first applied ad hoc in the `mentor-skills-source` audit (`SKILL_QUALITY_REPORT.md`, dated 2026-08-27, in that source repository) when auditing an external 30-skill candidate collection against this repository. That audit's scoring produced consistent, defensible, non-inflated results using this exact rubric; this document promotes the rubric itself to a standing Mentor Standard rather than a one-off audit methodology, so every future Skill — imported, generalized, or newly authored — is scored the same way.

This rubric also supersedes, for scoring purposes, the shorter "Evaluation should check" list in `context/skills/Skill Testing & Evaluation Standard.md` — not by redefining that document, but by replacing its flat seven-item checklist with ten independently-scored dimensions for anyone actually scoring a Skill. Concretely: that list's Correctness and Consistency map onto this rubric's Correctness; False positives and False negatives map onto False-Positive Resistance; Unintended side effects maps onto Safety; Compatibility with repository conventions maps onto Context Awareness; and Clarity of output maps onto Clarity. A reviewer scoring a Skill uses this document's ten dimensions, not that shorter list, as the operative rubric.

## 1. The Ten Dimensions

| Dimension | What it measures |
|---|---|
| Correctness | Are the Skill's technical claims actually true, for the technologies/scenarios it addresses? |
| Completeness | Does the Skill cover its stated Scope fully, including the sections `docs/Skill Standard.md` requires? |
| Clarity | Can a reader apply the Skill correctly without re-reading it, or asking a clarifying question the Skill should have answered itself? |
| Scope Isolation | Does the Skill stay inside its declared Scope, and is its boundary against sibling Skills explicit and accurate (see `docs/Skill Taxonomy.md` Section 5, Overlap/Duplication Rules)? |
| Context Awareness | Does the Skill correctly identify and declare what context/other Skills it depends on (`docs/Skill Standard.md` Section 3), and does it behave correctly whether that context is present, absent, or invalid? |
| Governance Compatibility | Does the Skill correctly implement `docs/Skill Standard.md` Section 4 — accurate tier claims (or an accurate disclaimer of none), correct Severity Taxonomy usage where applicable, correct Context Discovery / Governance Evaluation integration where claimed? |
| Safety | Does applying the Skill's guidance avoid introducing security, data-integrity, or safety risk — and does the Skill itself avoid instructing anything `context/standards/Security Standards.md` would flag? |
| False-Positive Resistance | For a Review-type Skill (or any Skill that generates findings): does it avoid flagging correct code/configuration as a defect? Marked `N/A`, not scored, for a Skill that does not generate findings — see Section 2. |
| Examples | Are the Skill's worked examples concrete and realistic, and — per `docs/Skill Standard.md` Section 2 — does at least one negative example exist wherever the Scope/Edge Cases boundary isn't otherwise obvious? |
| Test Coverage | Per `docs/Skill Testing Standard.md`: does test evidence exist, of the appropriate tier, covering the required scenario categories? |

## 2. Scoring Scale

Every evaluable dimension is scored 0–5. Two special values exist and must be used honestly rather than converted to a number by guessing:

- **`N/A`** — the dimension does not apply to this Skill's type or content (e.g. False-Positive Resistance for a pure-reference Domain Pattern Skill that makes no findings; Safety for a Skill with no implementation-affecting claims).
- **`U` (Unknown)** — the dimension is potentially applicable but cannot be reasonably evaluated from the Skill's own material (e.g. Correctness for a claim about a technology the reviewer has no way to verify from the text alone). `U` is a statement about the limits of the current review, not a low score, and must not silently become `0`.

| Score | Meaning |
|---|---|
| 5 | Exemplary. No credible reviewer would ask for more on this dimension. |
| 4 | Strong, with a minor, specifically-named gap that doesn't undermine the Skill's usefulness. |
| 3 | Adequate. Functions correctly but has a real, specifically-named limitation a reader should know about. |
| 2 | Weak. The gap materially reduces the Skill's reliability or usefulness on this dimension. |
| 1 | Present but minimal — the dimension is nominally addressed with little real substance. |
| 0 | Absent. No evidence the dimension was considered at all. |

A score is never assigned without a one-clause reason in the same review — "4/5, N/A, or U" alone, with no stated basis, is not a completed quality review. This mirrors `docs/Skill Standard.md`'s own no-silent-omission rule applied to scoring rather than section presence.

**Do not inflate.** A dimension scored 5 by default because "the Skill looks fine" rather than because a specific strength was identified is a scoring error, not a compliment to the Skill's author. The `mentor-skills-source` audit's own baseline scoring (`SKILL_QUALITY_REPORT.md` there) is the worked reference for what a defensible, non-inflated score set looks like at collection scale — including its explicit uniform 0/5 for Test Coverage and 1/5 for Governance Compatibility across all 30 skills evaluated, where the evidence genuinely supported those low, uniform scores rather than a generous curve.

## 3. Certification Threshold

A Skill is eligible for certification (`docs/Skill Taxonomy.md` Section 7, Lifecycle stage 5) — the gate a Skill must clear before it reaches Production — only when:

1. No dimension scores below 3, **except** Test Coverage and Governance Compatibility, which must score at their respective *maximum achievable* value given the Skill's actual required posture — a Skill whose Governance Integration section correctly states "Not applicable" is not penalized for scoring low on Governance Compatibility's tier-classification criteria, but a Skill that claims Review-type governance integration and doesn't correctly implement it scores low and is blocked.
2. Test Coverage specifically meets `docs/Skill Testing Standard.md` Section 3's minimum fixture bar — this is a hard gate, not merely a scored dimension a strong showing elsewhere can offset. A Skill with excellent Correctness/Clarity/Examples and zero tests does not clear certification; it cannot even reach Tested (`docs/Skill Taxonomy.md` Section 7, stage 3) — let alone Reviewed (stage 4) or Certified (stage 5) — until fixtures exist, since Tested is a precondition for Reviewed under this lifecycle's ordering.
3. Every `U` (Unknown) dimension has been either resolved (re-scored with evidence) or explicitly accepted as a known limitation by whoever approves certification — a `U` silently carried into a Production Skill's record is not acceptable; the certification decision must address it one way or the other.

**Proposed clarification (Phase 15, not yet adopted by any actual certification):** clearing the three conditions above establishes *eligibility* for certification — it is a necessary, not sufficient, condition. `docs/Skill Taxonomy.md` Section 7 stage 5 additionally requires sign-off by an independent party, which this document does not itself define; `docs/Skill Certification Process.md` proposes that definition. A Skill scoring highly on every dimension here, with a met Test Coverage gate, is not thereby Certified — see that document before treating a high score as a certification. **Policy clarification (Phase 19):** this Section 3 threshold governs eligibility for the *optional* Certified gate specifically (`docs/Skill Certification Process.md`'s policy clarification) — an ordinary internal Skill reaching Reviewed (`docs/Skill Taxonomy.md` Section 7, stage 4) and Production (stage 6) is not required to clear this threshold or to have Tier E evidence; only a Skill actually pursuing the optional Certified gate is held to it.

A Skill may be merged, deferred, or improved-then-reconsidered instead of certified — see `docs/Skill Taxonomy.md` Section 7 for the full lifecycle and `SKILL_QUALITY_REPORT.md` (in the `mentor-skills-source` audit) for a worked example of exactly this outcome applied to 30 real candidate skills, none of which cleared certification as-is, several of which were recommended for exactly this improve-then-reconsider path.

## 4. Re-Scoring

A Production Skill is re-scored whenever it changes materially (not for a typo fix) — governed by the same regression discipline `docs/Skill Testing Standard.md` Section 4 already states for test fixtures: a Skill's quality score is not assumed stable across a change, it's re-verified.

## Related

- `docs/Skill Standard.md` — defines the structural contract several dimensions above are scored against (Completeness, Governance Compatibility, Context Awareness).
- `docs/Skill Testing Standard.md` — defines what counts as evidence for the Test Coverage dimension and Section 3's certification gate.
- `docs/Skill Taxonomy.md` — Section 7 (Lifecycle) is where a quality score is actually consumed as a certification decision.
- `context/standards/Severity Taxonomy.md` — the reference example, elsewhere in this repository, of a single canonical scoring vocabulary used consistently by every consumer rather than redefined per-consumer; this Standard follows the same discipline for Skill quality.
