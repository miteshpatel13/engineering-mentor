---
id: skill-reviewer-02-edge-correct-not-applicable
category: edge-case
skill_under_test: skills/skill-reviewer/SKILL.md
---

# Scenario: A Skill Whose "Not Applicable" Governance Claim Is Actually Correct

## Input Material

> A Mentor Core meta-skill's Governance Integration section states "Not applicable — this Skill produces no findings against a child repository." This is factually accurate for the Skill's actual content. Score its Governance Compatibility dimension.

## Pass Criteria

- The dimension is scored at its maximum achievable value for this Skill's posture (per `docs/Skill Quality Standard.md` Section 3(1)), because the "Not applicable" claim is itself accurate.
- The reasoning explicitly distinguishes "correctly claims N/A" from "should have claimed governance integration and didn't."

## Fail Signals

- Scoring Governance Compatibility low merely because the Skill makes no governance-tier claims, without checking whether N/A is actually the correct posture.
