---
name: requirements-discipline
description: A project-agnostic discipline for classifying requirements as CONFIRMED, RECOMMENDATION, or ASSUMPTION, keeping that classification visible through implementation, and escalating rather than silently guessing when requirement material is ambiguous, conflicting, or insufficient. Use when working from any specification, ticket, SRS, or stakeholder conversation that leaves gaps a real implementation will have to fill one way or another.
category: Requirements
skillType: Authoring/Workflow
---

# Requirements Discipline

## Purpose

Requirements material — an SRS, a ticket, a stakeholder conversation, an existing codebase's implied behavior — is almost never fully explicit. Left unmanaged, the gaps get filled silently during implementation, and a reader six months later can no longer tell what the client actually asked for versus what an engineer decided seemed reasonable at the time. This Skill exists to make that distinction permanent, visible, and traceable, generalized from a real project's SRS-scope discipline (`srs-scope-rules`, in the audited `mentor-skills-source` collection) with every project-specific fact — the originating domain, its schema, its client decisions — stripped out, keeping only the reusable labeling and escalation discipline.

## Scope

**In scope:**

- Classifying every non-trivial requirement-derived decision as CONFIRMED, RECOMMENDATION, or ASSUMPTION.
- Maintaining a decision log that records which label applies to which decision and why.
- Identifying scope boundaries — what's explicitly out of scope, and what's genuinely undecided (open) versus what's simply unstated (a gap that still needs one of the three labels).
- Detecting ambiguity and conflicting requirements, and escalating rather than resolving them silently.
- Requirement traceability — connecting an implementation decision back to the specific requirement (or explicit ASSUMPTION) that justifies it.
- Tracking acceptance criteria and implementation impact for CONFIRMED requirements.
- Change tracking when a requirement's status changes (an ASSUMPTION becomes CONFIRMED, an open point gets resolved, scope is formally changed).

**Out of scope — explicitly not this Skill's responsibility:**

- **Writing the requirements themselves.** This Skill disciplines how existing or emerging requirement material is classified and tracked; it does not originate business requirements, which come from the stakeholder/client/product owner.
- **Documenting the resulting implementation.** Once a requirement is CONFIRMED and built, describing what was actually built (and whether it matches the plan) is `skills/documentation/SKILL.md`'s job — this Skill's decision log is an input to that documentation, not a replacement for it.
- **API contract specifics, schema design, or any domain-technical decision-making.** This Skill provides the labeling discipline those decisions get recorded under; it does not itself perform database design, API design, or architecture work.
- **Formal requirements-engineering methodology** (use-case modeling, formal specification languages) — this is a lightweight, practical discipline for real engineering work against imperfect specification material, not a substitute for a dedicated requirements-engineering process where a project already has one.

## When to Use

- Beginning implementation work against any specification document, ticket, or stakeholder request that isn't fully explicit about every detail an implementation needs.
- A request or ticket asks for something that isn't clearly traceable to an existing, explicit requirement.
- A decision made during a previous phase needs to be checked — was it actually confirmed, or was it an assumption that's since been treated as settled without anyone verifying that?
- A new requirement or clarification arrives that conflicts with something previously recorded as CONFIRMED, RECOMMENDATION, or ASSUMPTION.

## Required Context

**Benefits from repository/project context but degrades gracefully without it** (`docs/Skill Standard.md` Section 3, posture 2). Richer when an existing decision log, SRS, or equivalent requirement-tracking artifact already exists for the project — this Skill then extends it rather than starting fresh. Still useful in the abstract, applied to a single ticket or conversation with no pre-existing log, by starting one.

## Workflow

1. **Locate existing requirement material and any existing decision log.** Do not start a parallel, competing log if one already exists for the project — extend it (mirrors `docs/Skill Standard.md`'s own don't-duplicate discipline applied to project artifacts rather than Skills).
2. **For each decision the implementation will need to make, classify it:**
   - **CONFIRMED** — stated explicitly in the requirement material, or explicitly decided by the stakeholder/client in a recorded conversation. Cite the specific source (a document section, a message, a meeting note) — "confirmed" without a traceable source is not actually confirmed, it's an unlabeled assumption wearing a stronger label.
   - **RECOMMENDATION** — a specific technical or process choice made to satisfy a requirement that itself doesn't dictate the implementation detail. Flagged, and reasonable for a later reviewer to challenge and override.
   - **ASSUMPTION** — fills a genuine gap in the requirement material with the lowest confidence of the three, most likely to need correction once confirmed. Treated as still open, not as settled, until confirmed or corrected.
3. **Record every CONFIRMED/RECOMMENDATION/ASSUMPTION decision in the decision log**, with: the decision itself, its label, its source (for CONFIRMED) or rationale (for RECOMMENDATION/ASSUMPTION), what it affects (which component, table, endpoint, or behavior), and the date/context it was recorded.
4. **Identify and record scope boundaries explicitly**: hard exclusions (things explicitly ruled out by the requirement material — record what would need to happen, e.g. a formal change-request conversation, before building them anyway) and open points (things the requirement material acknowledges are undecided, that block finalizing specific downstream decisions but don't have to block all work — record what's blocked and what can proceed with a placeholder in the meantime).
5. **When a request maps to a hard exclusion**, say so explicitly and treat it as a scope-change conversation — do not implement it silently because it seemed like a small addition.
6. **When requirement material is ambiguous** (a genuinely plausible reading supports more than one implementation), do not silently pick one — record the ambiguity, the readings considered, and either escalate for a decision or proceed under an explicitly labeled ASSUMPTION naming which reading was chosen and why.
7. **When two pieces of requirement material conflict**, do not silently prefer one — record the conflict, both sources, and escalate; proceeding under an ASSUMPTION is acceptable only when a defensible resolution is clearly indicated, and even then the conflict and the chosen resolution are both recorded, not just the outcome.
8. **For every requirement that reaches CONFIRMED status**, define or confirm its acceptance criteria — what observable behavior proves it was actually satisfied — before implementation is considered complete for that requirement.
9. **Maintain traceability**: every non-trivial implementation artifact (a table, an endpoint, a business rule) should be traceable to the specific requirement ID or decision-log entry that justifies it. An artifact with no traceable requirement and no flagged RECOMMENDATION/ASSUMPTION rationale is a sign scope is drifting, and should be flagged, not built quietly.
10. **When a requirement changes status** (an ASSUMPTION is confirmed or corrected, an open point is resolved, scope is formally changed), update the decision log in the same change — record the prior status, the new status, and what changed it. Never silently overwrite a decision log entry's history.
11. **When requirement material is insufficient to make even an ASSUMPTION-level decision responsibly** (the gap is too consequential, too security/data-integrity-sensitive, or too underspecified to guess at reasonably), escalate rather than assume — see Failure Handling.

## Rules

### Labels Are Not Interchangeable

Do not blur CONFIRMED, RECOMMENDATION, and ASSUMPTION into uniform "requirements" prose, and do not upgrade a label's confidence over time without a new, recorded confirming event. An ASSUMPTION that has simply been unchallenged for a while is still an ASSUMPTION, not a promotion to CONFIRMED by default.

### No Silent Promotion

The most common failure this Skill exists to prevent: a RECOMMENDATION or ASSUMPTION quietly becoming treated as a hard requirement over the course of implementation, because nobody revisits the label once written down. Before treating any RECOMMENDATION or ASSUMPTION as settled enough to build a further decision on top of, re-check whether it was ever actually confirmed — and if not, flag it again rather than compounding an unconfirmed decision into a larger, harder-to-unwind one.

### Escalation Is a Valid, Expected Outcome

Escalating an ambiguous, conflicting, or insufficiently specified requirement is not a failure of this Skill — it is the correct outcome when confident, well-labeled progress isn't possible. This mirrors the Mentor Operating Model's No Invention Rule: unknown information is inspected, or explicitly identified as unknown and escalated, never silently assumed away.

### Traceability Is Structural, Not Decorative

A decision log entry with no source citation (for CONFIRMED) or no stated rationale (for RECOMMENDATION/ASSUMPTION) does not satisfy this Skill's discipline, regardless of how confidently it's phrased. The citation/rationale is what lets a future reader — or `skills/documentation/SKILL.md`'s output — verify the claim rather than take it on faith.

## Constraints

- Never record a decision as CONFIRMED without a traceable source.
- Never silently implement something that maps to an explicitly stated exclusion.
- Never resolve a genuine conflict between two requirement sources by quietly picking one without recording that a conflict existed.
- Never let this Skill's own output encode project-specific business facts as if they were general Mentor guidance — the decision log this Skill produces is project-local content, living in the child repository, not Mentor content.

## Governance Integration

Not applicable in the Mentor-Mandatory sense — this Skill is a process discipline for classifying and recording requirement confidence; it does not itself state or enforce a Mentor Mandatory/Configurable/Advisory/Informational rule against child-repository code, and does not invoke `scripts/evaluate_governance.py`. Where an underlying requirement this Skill is classifying happens to touch a security- or data-integrity-sensitive area, the requirement's own governance tier (if any) is determined by the Standard that actually governs that area (e.g. `context/standards/Security Standards.md`) — this Skill's CONFIRMED/RECOMMENDATION/ASSUMPTION label is a confidence classification, not a substitute governance tier, and must never be read as one.

## Validation

This Skill's discipline is being followed correctly when: every non-trivial decision in the project's decision log carries exactly one of the three labels; every CONFIRMED entry cites a real source; every RECOMMENDATION/ASSUMPTION entry states its rationale; every hard exclusion and open point is recorded explicitly rather than left implicit; and no implementation artifact exists with neither a traceable requirement nor a flagged RECOMMENDATION/ASSUMPTION.

## Edge Cases

- **A requirement that was CONFIRMED, then later contradicted by a new, equally authoritative source** — do not silently pick the newer one; record both, flag the conflict, and escalate per Workflow step 7, even though one source is CONFIRMED-labeled — a later CONFIRMED statement can supersede an earlier one, but only when that supersession is itself recorded, not assumed from recency alone.
- **A requirement that's technically unstated but so standard for the domain that treating it as an open question would be absurd** (e.g. passwords must be hashed, not stored in plaintext) — this is not a case for a low-confidence ASSUMPTION label; it's an application of an existing, independently-sourced standard (cite that standard, e.g. a security Standard, as the source) rather than a project-specific guess.
- **A stakeholder gives a verbal decision with no written record** — still CONFIRMED, but the source citation is "verbal decision, [date/context]," recorded explicitly rather than presented as if it came from the written specification — the traceability discipline applies to the fact that a decision was made, not only to written sources.
- **An open point that nobody is likely to resolve soon, blocking real progress** — record it as open, proceed on placeholder/nullable values where implementation-level workarounds exist, and flag which downstream decisions remain blocked; do not quietly convert an open point into an ASSUMPTION just to stop tracking it as open.

## Failure Handling

When requirement material is too ambiguous, conflicting, or thin to support even a labeled ASSUMPTION responsibly — particularly where the gap touches security, data integrity, financial correctness, or an irreversible decision — stop and escalate explicitly rather than guessing. State exactly what's missing or in conflict, what decision is needed, and what's blocked until it's resolved. This is a successful, correct outcome of applying this Skill, not a shortfall of it.

## Expected Output

A maintained, traceable decision log (project-local content, not Mentor content) recording every non-trivial requirement-derived decision with its CONFIRMED/RECOMMENDATION/ASSUMPTION label, source or rationale, and what it affects; an explicit record of hard exclusions and open points; and, where applicable, an explicit escalation naming what's ambiguous, conflicting, or insufficient and what's needed to resolve it.

## Examples

**Worked example.** A ticket asks for "soft delete on the Orders table." The requirement material never states whether a soft-deleted order's order number can be reused. Applying this Skill: record "order numbers are not reused after soft delete" as an ASSUMPTION (lowest confidence, filling a genuine specification gap), with rationale ("no requirement addresses reuse; treating the number as permanently retired is the safer default for a financial record, pending confirmation"), rather than silently building the uniqueness constraint one way and never mentioning the choice was made.

**Negative example (correctly declined).** Asked to "just implement it however makes sense" for a requirement with two plausible, materially different readings (e.g. whether a discount applies before or after tax). Declined as a silent-pick: this Skill records both readings, flags the ambiguity, and escalates for a decision rather than choosing one and documenting only the choice — a financially-material ambiguity is exactly the kind of gap Failure Handling requires escalating rather than assuming away.

## Related Skills

- `skills/documentation/SKILL.md` — Related: this Skill's decision log is a primary source `documentation`'s Implemented/Planned/Recommended/TBD labeling draws on, but neither Skill requires the other's specific output format to function on its own.
- `skills/skill-creator/SKILL.md` — Related: applies this Skill's CONFIRMED/RECOMMENDATION/ASSUMPTION discipline specifically to Skill-authoring source material (`skill-creator`'s Rules → Distinguishing Confirmed, Recommended, and Assumed Source Material) rather than to child-project requirements; the underlying labeling discipline is the same, applied in a different domain.
