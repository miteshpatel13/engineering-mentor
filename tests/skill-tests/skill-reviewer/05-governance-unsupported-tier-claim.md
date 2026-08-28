---
id: skill-reviewer-05-governance-unsupported-tier-claim
category: governance-sensitive
skill_under_test: skills/skill-reviewer/SKILL.md
---

# Scenario: A Rule Phrased as Absolute With No Cited Standard

## Input Material

> A drafted Skill's Rules section states: "Passwords must always be hashed before storage — non-negotiable" with no citation to any `context/standards/*.md` file. Review this Rule's governance correctness.

## Pass Criteria

- The response flags this as a Governance defect: the Mandatory-sounding phrasing is not, by itself, evidence of Mandatory tier per `docs/Skill Standard.md` Section 4's opening rule.
- The response requires either a citation to an existing Standard (if one already covers this — likely true for password hashing) or an explicit downgrade to a stated tier pending that citation.
- The response does not accept the claim as correctly classified merely because the underlying advice (hash passwords) is itself good practice — good advice and correct governance-tier sourcing are treated as separate questions.

## Fail Signals

- Accepting the Rule's Mandatory framing without requiring a citation.
- Conflating "this is good advice" with "this is correctly governance-classified."
