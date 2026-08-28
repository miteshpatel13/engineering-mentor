---
id: database-review-06-governance-compatible-child-configurable-pool-size
category: governance-sensitive
skill_under_test: skills/database-review/SKILL.md
---

# Scenario: Child Configurable Value Compatible With a Mentor Mandatory Bound (Two Distinct Requirements, Not One Requirement Wearing Two Tiers)

## Input Material

> Context discovery reports two distinct, related governance facts about this migration's target table, which must be kept separate rather than treated as one requirement with two labels:
>
> - **Requirement A (Mentor Mandatory):** "A migration that adds or modifies a table must not hold a lock for an unacceptable duration" (Rules → Migration Safety). This requirement's *existence* — that some acceptable-duration bound must be respected — is fixed by Mentor and is not something a child project can opt out of.
> - **Requirement B (Mentor Configurable boundary on Requirement A):** the *specific numeric threshold* that counts as "unacceptable" for this project is left to the child to select, within Mentor's defined outer bound of "no more than 60 seconds under any circumstance." A declared Child Configurable rule sets this project's specific threshold at 500 milliseconds — well inside Mentor's 60-second outer bound.
>
> The migration under review adds a column to a large, frequently-written table using a technique documented (in the material) to hold its lock for approximately 200 milliseconds — within both the child's 500ms threshold and Mentor's 60-second outer bound.

## Pass Criteria

- Recognizes Requirement A (the Mandatory existence of *some* acceptable-duration bound) and Requirement B (the Configurable *specific value* the child selected within Mentor's boundary) as two distinct parts of the same Configurable-rule structure (`docs/Governance Precedence Model.md` Section 7) — never as one single requirement that is simultaneously and contradictorily "Mandatory" and "Configurable."
- Recognizes both are satisfied simultaneously by the migration's ~200ms lock duration (well under both the child's 500ms threshold and Mentor's 60-second outer bound) — Compatible, no tension.
- Does not flag the child's specific 500ms threshold itself as a finding — Mentor's boundary only requires that *some* bound exists and that the child's selected value stays within Mentor's outer bound; the child's specific number is exactly what Section 7 says is negotiable.
- States the classification explicitly (Compatible) rather than omitting governance reasoning because nothing is wrong.

## Fail Signals

- Describing Requirement A and Requirement B as if they were one requirement that is both "Mandatory" and "Configurable" at once — this conflates two distinct classification tiers, which `docs/Governance Precedence Model.md` Section 2 identifies as the most common failure mode. Always describe them as two linked parts: a Mentor-fixed existence/outer-bound, and a child-selected value within it.
- Flagging the child's specific 500ms threshold as itself requiring justification, or treating the child's Configurable value as if it could convert Requirement A into something Advisory or optional (`docs/Governance Precedence Model.md` Section 7 explicitly prohibits a child configuration from reclassifying a Mandatory requirement).
- Failing to recognize the migration as satisfying both requirements.
