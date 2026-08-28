# Skill Certification Process

## Status

**Proposed.** This document does not exist in any prior form in this repository. It fills a gap this and the prior phase (`docs/Skill Ecosystem Inventory.md` Section 2's Independence Flag, Section 7) found and named but did not resolve: `docs/Skill Taxonomy.md` Section 7 stage 5 requires a Certified Skill be "formally signed off by whoever approves the change," and `docs/Skill Quality Standard.md` Section 3 defines the quality threshold that gates eligibility — but neither document, nor any other document in this repository, defines *who* "whoever approves the change" is, what independence that person or process must have from a Skill's Author, or what evidence proves that independence was real. This document proposes that missing definition. It does not redefine anything `docs/Skill Taxonomy.md`, `docs/Skill Standard.md`, `docs/Skill Testing Standard.md`, or `docs/Skill Quality Standard.md` already states — where this document restates something from one of those, it is citing, not superseding. Everything in this document that is new is marked **Proposed** in its own right below, so a future reader can tell at a glance what is settled Mentor policy and what is this phase's design proposal, not yet adopted by any act of actually certifying a Skill against it.

**What adopting this document would mean, and what it does not mean today.** Nothing in this phase changes any Skill's lifecycle stage. `security-review`, `database-review`, and `api-review` remain at Reviewed. This document makes it *possible* for a future phase to reach Certified defensibly; it does not itself certify anything, and being well-designed is not the same as being executed.

**Policy clarification (Phase 19).** `docs/Skill Taxonomy.md` Section 7's normal internal production path is Draft → Implemented → Tested → Reviewed → Production → Deprecated; Certified is an *optional* high-assurance gate, not a required step for an ordinary internal Skill, reserved for cases such as: security-critical Skills, externally distributed Skills, regulated/compliance use, major architectural Skills, or a Skill an owner explicitly designates as requiring formal independent sign-off. An ordinary internal Skill may reach Production directly from Reviewed; the absence of Tier E evidence (Section 7, below) does not block that path — it only blocks *this* document's Certified gate specifically. This section does not weaken the Certified gate itself, which remains exactly as demanding as defined below for any Skill that does pursue it; it only states that pursuing it is a choice, not a universal requirement. The certification records already produced under this process (`docs/certification-records/`) remain valid historical evidence of the review work actually performed, regardless of whether the Skills they describe are ever certified.

## 1. What the Repository Currently Requires — Restated, Not Redefined

Precisely what exists today, cited by section, before this document adds anything:

- **`docs/Skill Taxonomy.md` Section 7** defines seven lifecycle stages (Draft → Implemented → Tested → Reviewed → Certified → Production → Deprecated). Stage 4 (Reviewed) requires review "using `skills/skill-reviewer/SKILL.md`" and scoring against the Quality Standard. Stage 5 (Certified) requires "`docs/Skill Quality Standard.md` Section 3's certification threshold is met **and formally signed off by whoever approves the change**." No role named "Reviewer," "Certifier," or "Approver" is defined anywhere in that document beyond this one clause; no independence requirement is stated; no evidence format for the sign-off is specified.
- **`docs/Skill Quality Standard.md` Section 3** defines a purely evidentiary/numeric threshold (no dimension below 3 except Test Coverage/Governance Compatibility at their maximum achievable value; Test Coverage meets the Testing Standard's hard fixture-count/diversity gate; every `U` resolved or explicitly accepted). It says nothing about *who* scores a Skill, whether that person may be its Author, or what independence a "certification" sign-off requires — it defines eligibility, not authority.
- **`docs/Skill Testing Standard.md` Section 1** defines the Tier A–E evidence-strength model (fixture exists / expected result exists / structurally validates / executed against a live model invocation and checked against Pass Criteria / an independent reviewer's own read reaching the same conclusion). It defines what Tier D and Tier E *are*, in one sentence each. It does not define a minimum Tier D fixture count, a Pass-Criteria-withholding procedure, an evidence-recording format, or what "independent" means for Tier E.
- **`docs/Skill Ecosystem Inventory.md` Section 2** records an "Independence flag" as a fact about the current 15 Skills (none has an independent Reviewer or Certifier) and states the consequence ("none is eligible to be marked Certified regardless of any other score or gate it passes") — but this is a *recorded observation*, not a *defined process*. It does not say what would need to be true for the flag to change.
- **No document in this repository defines an "Approver" role, a "Certifier" role's permitted/prohibited actions, an independence test, or a certification record schema.** A targeted search (`grep -rniE "certifier|sign.?off|independent review|approv(ed|al) by|reviewer role"` across `docs/` and `context/`) confirms this — the only hits are the Inventory's own observations quoted above and one unrelated `exceptions.yaml` field description.

**Conclusion:** the repository has a quality gate (Quality Standard Section 3) and names a governance gate in one clause (Taxonomy Section 7 stage 5) without ever defining the mechanism that clause presupposes. This is the process gap this document exists to close.

## 2. Roles

Five roles, four of which the repository already implies (Author, Tester, Reviewer, Certifier — `docs/Skill Ecosystem Inventory.md` Section 2's table header) and one this document adds because Taxonomy stage 5's "sign-off" and "certification" are not the same act (Section 2.5, below).

### 2.1 Author

**Responsibility:** Writes or materially edits a Skill's `SKILL.md` content — Rules, Scope, Examples, Edge Cases, Failure Handling, Governance Integration.

**Independence requirement:** None — the Author is definitionally not independent of their own work.

**Required evidence:** Identity recorded in the Certification Record (Section 4). For this engagement, "This engagement (session/account lineage), Phase N" is an honest, sufficient identity record — inventing a named individual where none exists would violate the No Invention Rule.

**Permitted actions:** Write, edit, self-review informally, run structural validators against their own work, propose the Skill for Tested/Reviewed stage.

**Prohibited actions:** Cannot act as Reviewer or Certifier for their own work (Section 3 defines why). Cannot mark their own Skill Certified under any circumstance, regardless of quality score.

**Sign-off responsibility:** None — the Author does not sign off on their own certification.

### 2.2 Tester

**Responsibility:** Produces test evidence — fixtures per `docs/Skill Testing Standard.md`, and, where a Tier D pilot is performed (Section 6, below), actually executing it and recording raw output.

**Independence requirement:** **Existing repository practice does not require the Tester to be independent of the Author** (`docs/Skill Ecosystem Inventory.md` Section 2's table records the same engagement as both, for every Skill, without treating that as itself disqualifying — only Reviewer/Certifier independence is flagged as the blocker). This document does not change that: a Skill's fixtures being authored by the same person who wrote the Skill is normal, expected, and not itself a certification blocker, provided the fixtures are later checked (Reviewer role) against evidence, not merely against the Author's own intent.

**Required evidence:** Fixture set location, count, category coverage, and (if a Tier D pilot occurred) which fixtures were executed, by what mechanism, and the raw output — not just a pass/fail claim.

**Permitted actions:** Write fixtures, run structural/deterministic validators, execute a Tier D pilot per Section 6's procedure.

**Prohibited actions:** Cannot withhold or selectively report Tier D pilot results — a failing pilot result is recorded exactly as a passing one is (Section 6.5).

**Sign-off responsibility:** Attests the recorded fixture count/category coverage and any Tier D pilot results are accurate and complete, not cherry-picked.

### 2.3 Reviewer

**Responsibility:** Independently executes the Certification Checklist (Section 5) against the Skill and its evidence, using the Independent Review Packet (Section 6 of the companion packets, one per Skill) rather than any prior session's or report's conclusions. Produces findings in their own words.

**Independence requirement:** **This is the load-bearing requirement of this entire document.** See Section 3 for the full definition. Summary: a Reviewer must not be the same session/account/engagement lineage as the Author, must work from the packet and the repository's actual current state (not from a prior report's summary of them), and must reach their own conclusion rather than ratify one presented to them.

**Required evidence:** Reviewer identity (a real name, role, or account distinguishable from the Author's), the date, the exact Skill file version/commit reviewed, which checklist items were checked and how, and specific findings (not merely a checklist with boxes ticked and no reasoning).

**Permitted actions:** Request changes, flag a Rule as unclear or incorrect, disagree with a prior quality score and re-score with reasons, decline to proceed to Certifier sign-off.

**Prohibited actions:** Cannot certify (that is the Certifier's distinct act — Section 2.5). Cannot be the Skill's Author or Tester for the same Skill. Cannot be a Claude subagent spawned within the same session as the Author (Section 3 addresses this explicitly, per this phase's explicit instruction).

**Sign-off responsibility:** Signs the Certification Record's Reviewer field with their identity, date, and a findings summary — this is a Reviewed-stage sign-off, distinct from and prior to Certifier sign-off.

### 2.4 Certifier

**Responsibility:** Makes the final Certified/Not-Certified decision, on the basis of the Reviewer's findings and the full evidence record — not by re-doing the Reviewer's work, but by confirming the Reviewer's process was itself sound (used the right packet/checklist, was actually independent, addressed every mandatory gate) before signing.

**Independence requirement:** Same bar as Reviewer (Section 3) with respect to the Author. **May be the same person as the Reviewer** when a single independent party reasonably performs both roles (this document does not require artificial role-splitting between two different independent people when one genuinely independent reviewer is already a meaningful, real improvement over today's zero) — but if Reviewer and Certifier are the same person, the Certification Record states this explicitly rather than implying two separate checks occurred.

**Required evidence:** Same fields as Reviewer, plus the explicit Certified/Not-Certified decision and its rationale, plus confirmation that every mandatory gate in Section 5's Final Gate was individually checked (not inferred from a high total score — `docs/Skill Testing Standard.md`'s and this engagement's own repeated instruction that total score never substitutes for a gate).

**Permitted actions:** Certify, decline to certify with stated reasons, certify with explicitly recorded known limitations (a Certified Skill can still carry a documented, accepted limitation — certification is not a claim of perfection, it is a claim that the process and evidence were genuinely checked by someone independent).

**Prohibited actions:** Cannot certify based on total score alone. Cannot certify a Skill whose Test Coverage or Governance Compatibility dimension is below its maximum achievable value for its required posture. Cannot certify without a Reviewer sign-off already on record (Certifier confirms the Reviewer's work; it does not substitute for it, even when one person holds both roles — the packet's checklist must actually have been executed).

**Sign-off responsibility:** The binding one — this is the signature that actually changes a Skill's lifecycle stage from Reviewed to Certified.

### 2.5 Approver (new role this document adds)

**Why this role is added, not merely implied by "Certifier."** Taxonomy Section 7 stage 5 conflates two different questions under one clause: *is this Skill technically correct, complete, and evidenced well enough to trust* (a quality/engineering judgment — the Certifier's job) and *should Engineering Mentor actually adopt and ship it as live governance content, given business priorities, timing, and risk appetite* (a product/ownership decision, distinct from technical quality — e.g. a Skill can be technically Certified and still deliberately held back from Production for unrelated reasons). Conflating these means a purely technical sign-off could be read as also being a shipping decision, which overstates what a Certifier's expertise or mandate actually covers.

**Responsibility:** Decides whether a Certified Skill actually advances to Production (Taxonomy stage 6) and when — a distinct, later act from Certification itself.

**Independence requirement:** None — the Approver is expected to be the project owner or whoever has standing authority over what ships, and is not required to be independent of the Author in the same sense a Reviewer/Certifier is, because this is not a technical-correctness check.

**Required evidence:** A dated decision recorded in the Certification Record's Production field, referencing which Certification Record it acts on.

**Permitted actions:** Approve for Production, hold at Certified without advancing, request the Certifier revisit a specific concern before advancing (this can send the Skill back to Reviewer/Certifier, but the Approver does not re-open the technical certification decision themselves).

**Prohibited actions:** Cannot certify (only a Certifier can). Cannot advance a Skill to Production that is not yet Certified.

**Sign-off responsibility:** The Production-advancement decision only.

## 3. Independence, Defined (Proposed — the repository is silent, so this section answers directly rather than leaving the question open)

**Definition.** A Reviewer or Certifier is independent of a Skill's Author when three conditions all hold: (a) **no shared session/context** — the Reviewer did not participate, as Claude or as a human, in authoring, drafting, or directing the specific content of the Skill under review; (b) **no shared incentive/account lineage** — the Reviewer is not the same account, engagement, or continuous working relationship that produced the Skill and every prior report about it, such that the Reviewer has no institutional stake in the prior work being found sound; (c) **genuine, own-conclusion work** — the Reviewer executes the checklist against the Skill's actual current file content and evidence, using the Independent Review Packet, and reaches their own documented conclusion, rather than reading a prior session's report and agreeing with it.

Answering each question this phase posed directly, because guessing quietly would be worse than answering plainly and marking the answer Proposed:

- **Can the same Claude session review its own work? NO.** Fails (a) and (c) definitionally — it is the same context that authored the content.
- **Can a new Claude session under the same account qualify? NO, not alone.** A fresh session lacks (a)'s shared-context problem in the narrow sense (no conversational memory of authoring the Skill), but fails (b): the same account/engagement relationship — the same person prompting it, the same incentive for the engagement's own prior work to be validated, the same practical ability for the person operating that account to simply re-run until a favorable result appears — is still present. This document proposes that account-lineage independence, not session-lineage independence, is the meaningful bar, because session boundaries are trivially resettable by the same operator and therefore cannot be the thing independence actually rests on.
- **Can a subagent qualify? NO — settled, not merely proposed**, per this phase's and Phase 14's explicit instruction, and for the same substantive reason: a subagent spawned within the same session inherits condition (a)'s failure directly (it was given the task, and often the material, by the very session that did the authoring) and cannot supply condition (b) or (c) independently of it. **A subagent can still supply genuine Tier D evidence** (Section 6) — a live model invocation actually occurred, and that is an empirical/behavioral fact, not a judgment-authority claim — but Tier D and Tier E are different questions (`docs/Skill Testing Standard.md` Section 1's own either/or framing), and a subagent's output must never be recorded as, or mistaken for, Tier E.
- **Can the project owner qualify? CONDITIONALLY YES — this is a real, currently-available path.** The project owner has directed this entire engagement and is not independent of it in an organizational sense, but independence here is about who does the *review work*, not about title. If the project owner personally, directly executes the Certification Checklist (Section 5) against the Skill's actual current files using the Independent Review Packet — reading the Rules, the fixtures, the governance matrix themselves, and reaching their own findings, rather than reading this session's report and stamping it — that satisfies (c), and satisfies (a)/(b) in the sense that matters: a human's own independent judgment, applied firsthand, is not the same act as the Claude session that authored the content checking its own output. This is explicitly recorded as the most practically available path to a genuine first Tier E data point, and is not equivalent to a rubber-stamp reading of this or any prior report.
- **Can another human developer qualify? YES**, provided they were not involved in directing or authoring this Skill's specific content and genuinely execute the checklist themselves.
- **Can another team member qualify? CONDITIONALLY**, same test as the developer case — independence turns on whether they authored/directed this Skill's content and whether they do the work themselves, not on title or team membership.
- **Can a different repository/account qualify? For Tier D, yes — a differently-provisioned Claude account/session with no shared history can supply additional, more clearly independent Tier D behavioral evidence.** For Tier E specifically, a different AI account still does not resolve the requirement, because Taxonomy stage 5 requires "sign-off," which this document interprets as requiring a human decision-maker's accountable judgment, not an unaccountable model's — an AI reviewer, however differently provisioned, is not "whoever approves the change" in the sense that clause implies. This interpretation is itself Proposed, since the original clause does not say "human" explicitly; it is the most defensible reading available without inventing an unstated requirement.
- **What evidence proves independence?** The Certification Record (Section 4) must state: Reviewer identity distinguishable from the Author's; an explicit statement they were not involved in authoring/directing this Skill's content; confirmation they worked from the Independent Review Packet and the repository's current files, not from a prior report's conclusions; and findings written in their own words, not copied from any prior report (including this one).

## 4. Certification Record — Schema

One record per Skill per certification attempt, stored alongside the Skill (proposed location: `docs/certification-records/<skill-name>-certification-record.md`, not created for any Skill in this phase — see Section 12). Fields:

```text
Skill:                  <skills/<name>/SKILL.md>
Version:                <git commit hash or, absent commits in this repo's current
                         history, a content hash / explicit "as of <date>, uncommitted">
Author:                  <identity + phase/date>
Tester:                  <identity + phase/date; fixture count/location>
Reviewer:                <identity, distinguishable from Author; date; independence
                         statement per Section 3; "N/A — not yet performed" if absent>
Certifier:               <identity; date; "N/A — not yet performed" if absent>
Review date:             <date the Reviewer's checklist pass was performed>
Certification date:      <date, only if Certified>
Quality score:           <all 10 dimensions, individually, with reasons — never a bare total>
Evidence tiers:          <A/B/C confirmed how; D — exact fixtures executed, by whom/what,
                         raw output location; E — "absent" until a genuine independent
                         Reviewer record exists>
Fixture coverage:        <count, category diversity, governance-matrix completeness>
Known limitations:       <stated explicitly, never silently omitted — e.g. "Tier D
                         evidence covers 2/20 fixtures," "Examples section has no
                         dedicated entry for Rule X">
Governance verification: <confirmation the Governance Integration section's claims were
                         checked against the actual code-review reference implementation
                         and evaluate_governance.py, not merely read>
Decision:                <Reviewed | Certified | Not Certified | Blocked by Evidence |
                         Blocked by Governance | Blocked by Structure>
Decision rationale:      <specific, citable reasons — never "score was high enough">
```

**This schema exists specifically so "Reviewed" and "Certified" cannot be confused**: a record with a populated Reviewer field, dated, with findings, and a Decision of `Reviewed` or `Blocked by Evidence` is visibly and structurally different from one with a populated Certifier field and a Decision of `Certified` — the schema has no field that can be silently left blank and mistaken for having been satisfied, because every field states "N/A — not yet performed" explicitly rather than being omitted.

## 5. Certification Checklist

Executed by the Reviewer, using a Skill's Independent Review Packet. Every item requires a specific citation (a file, a line, a fixture) as evidence, not a bare checkbox.

### Structure
- [ ] Frontmatter parses; `name` matches directory; `category` and `skillType` are valid enum values (`scripts/validate_skill.py` reports VALID).
- [ ] Every required `##` section from `docs/Skill Standard.md` Section 1 is present.
- [ ] `Related Skills` paths all resolve to real files.
- [ ] Naming matches `docs/Skill Taxonomy.md` Section 4's pattern for the Skill's type.
- [ ] Scope's In/Out-of-scope lists are both present and each Out-of-scope item names where that responsibility actually lives.

### Content
- [ ] Correctness — spot-check at least 3 Rule claims against independent domain knowledge; note any inaccuracy found.
- [ ] Completeness — every Scope item maps to a Rule or an explicit statement of why not.
- [ ] Clarity — could you apply this Rule correctly without asking the Author a clarifying question? Note any Rule where the answer is no.
- [ ] Scope Isolation — check Related Skills' boundary claims bidirectionally (does the other Skill's file actually agree with the boundary stated here?).
- [ ] Context Awareness — Required Context names specific NPC fields (not "context discovery output" generically); Failure Handling names what happens when that context is missing.
- [ ] Safety — Constraints forbid the specific unsafe shortcuts this Skill's domain makes tempting.
- [ ] False-Positive Resistance — at least one Edge Case or fixture demonstrates the Skill correctly declining to flag something.
- [ ] Examples — at least one worked positive example; a negative example wherever a Scope/Edge Case boundary isn't otherwise obvious.

### Governance
- [ ] Compatible, Additive, Override, Conflict, Prohibited Override, Unknown/Indeterminate, Applicable Exception, Inactive/Expired Exception, Active Exception Against Mandatory, Advisory/No Conflict, Out-of-Scope, Severity Independent of Classification — each has a genuine, distinct fixture (read the fixture; do not count a category because a README table names it).
- [ ] Governance Integration's claims (invokes context-discovery first; routes classification through `scripts/evaluate_governance.py`; follows `skills/code-review/SKILL.md`'s Child Governance mechanism) are checked against that mechanism's actual current text, not assumed accurate because previously reported so.

### Evidence
- [ ] Tier A — fixtures exist (count, location).
- [ ] Tier B — every fixture carries explicit Pass Criteria/Fail Signals.
- [ ] Tier C — `scripts/validate_skill_test_evidence.py` reports VALID.
- [ ] Tier D — state exactly which fixtures (if any) were executed against a live model invocation, by what mechanism, with Pass Criteria withheld from the executor, and whether output matched. State the exact coverage fraction (e.g. "2/20") — never imply full coverage from a partial pilot.
- [ ] Tier E — this Reviewer's own independent pass is what supplies it. Confirm your own independence per Section 3 before treating your own review as Tier E evidence.

### Final Gate
- [ ] Every item above is individually checked — not inferred from a high total score.
- [ ] No dimension scores below 3 (Quality Standard Section 3.1).
- [ ] Test Coverage and Governance Compatibility are at their maximum achievable value for this Skill's required posture.
- [ ] No `U` (Unknown) dimension remains unresolved and unacknowledged.
- [ ] Reviewer independence (Section 3) is confirmed and stated, not assumed.
- [ ] If every condition above holds: recommend Certifier sign-off. **If any condition does not hold, certification remains blocked regardless of how many other conditions passed** — this is a gate, not a score to average.

## 6. Tier D Requirements

**Definition** (restated from `docs/Skill Testing Standard.md` Section 1, not redefined): a fixture is Tier D evidence when it was actually executed against a live model invocation of the Skill, and the resulting output was checked against that fixture's own Pass Criteria.

**Minimum number/diversity proposed for a Tier D pass to be treated as meaningfully representative** (Proposed — the Testing Standard states the tier exists but not a minimum): at least one fixture from each present category (normal, edge, adversarial, failure-handling, governance-sensitive, rule-coverage) per Skill, and at least 30% of the Skill's total fixture count. Phase 14's 6-fixture pilot (2 per Skill, normal + edge only, ~9% coverage) falls short of this proposed bar and should be described as exactly what it is — a small, real, but partial pilot — never as "Tier D coverage achieved."

**How Pass Criteria are withheld:** the executing model (subagent, separate session, or external harness) receives only the Skill's literal `SKILL.md` text and the fixture's Input Material section. It must not receive the fixture's Pass Criteria or Fail Signals. The evaluator (a different party than the executor, wherever practical) then compares the executor's actual output against the fixture's real Pass Criteria after the fact.

**How outputs are evaluated:** each Pass Criterion is checked individually against the actual output (not summarized as an overall vibe); each Fail Signal is checked for presence; the result is recorded as PASS/FAIL per fixture, with the actual output preserved (not just the verdict) so a later reviewer can re-check the grading.

**How evidence is recorded:** in the Certification Record's Evidence Tiers field — exact fixtures, exact executing mechanism (model/session identity, date), and either the raw output inline or a stable pointer to where it's preserved.

**Reproducibility requirement:** a second party must be able to re-run the same fixture against the same Skill text and reach the same PASS/FAIL determination independently — this is why raw output, not just a verdict, must be preserved.

**Current harness status:** `scripts/` contains no execution-harness script (confirmed by directory listing and repo-wide grep, Phase 14). **TIER D HARNESS: NOT AVAILABLE.** The only Tier D evidence that exists is Phase 14's manual, small, explicitly-bounded pilot (6 fixtures via `Agent`-tool subagent dispatch, output compared by that session against real Pass Criteria) — a real, valid, but narrow instance of the procedure above, not an automated harness, and not sufficient coverage on its own per the minimum this section proposes.

## 7. Tier E Requirements

**Definition** (restated, not redefined): an independent reviewer's own read of the Skill's material against its fixtures/criteria, reaching a conclusion — see Section 3 for what "independent" requires.

**Minimum evidence for genuine Tier E**, all required, none optional:
- Independent Reviewer identity (distinguishable from Author; see Section 3's independence test).
- Review date.
- Exact reviewed Skill version (file content/commit hash, or an explicit "as of `<date>`, uncommitted" statement given this repository's current state — see Section 4).
- The exact evidence set the Reviewer worked from (which packet, which fixtures, which validator output).
- Findings — specific, in the Reviewer's own words, citing file/fixture/line where relevant.
- Disposition — what the Reviewer concluded on each Checklist item, not only a final verdict.
- Sign-off — the Reviewer's explicit statement that they performed this review themselves, independently, per Section 3.

**No genuine Tier E evidence exists for any of the three target Skills as of this phase.** This document does not, and cannot, create one — per this phase's explicit instruction not to fabricate a Reviewer identity, this section states the requirement precisely so a future, real independent Reviewer can satisfy it, rather than approximating it now.

## Related

- `docs/Skill Taxonomy.md` Section 7 — the lifecycle stages this process gates entry to, particularly stage 5's sign-off clause this document proposes a concrete mechanism for.
- `docs/Skill Quality Standard.md` Section 3 — the numeric/structural threshold this process's Reviewer/Certifier confirm before signing; this document does not alter that threshold.
- `docs/Skill Testing Standard.md` Section 1 — the Tier A–E model Sections 6–7 above give minimum, concrete requirements for.
- `docs/Skill Ecosystem Inventory.md` Section 2 (Independence flag) and Section 7 (Phase 14's findings) — the recorded facts this document's process is designed to eventually change, honestly, not paper over.
- `docs/certification-packets/` — the reusable per-Skill packets (Section 6 of each) instantiating this document's Checklist and Record schema for `security-review`, `database-review`, and `api-review`.
