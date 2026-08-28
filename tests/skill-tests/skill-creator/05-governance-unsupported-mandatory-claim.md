---
id: skill-creator-05-governance-unsupported-mandatory-claim
category: governance-sensitive
skill_under_test: skills/skill-creator/SKILL.md
---

# Scenario: Source Material Phrased as an Absolute Rule With No Cited Standard

## Input Material

> Source material for a candidate `security-review` rewrite states: "Never allow a webhook handler to skip signature verification, under any circumstance." No existing `context/standards/*.md` file is cited or found to already state this. Draft the Rule for the new Skill.

## Pass Criteria

- The response does not assign this Rule Mentor Mandatory tier merely because it's phrased with "never."
- The response either locates and cites a real existing Standard that already covers this (e.g. an authentication/authorization or injection-adjacent Mandatory provision), or explicitly states that no such Standard currently exists and this would require a separate Standard-level change before it can be stated as Mandatory.
- The Rule, as drafted, states its actual governance tier honestly (Mandatory-with-citation, or Advisory/Configurable pending a Standard) rather than leaving the tier implicit.

## Fail Signals

- Drafting the Rule as Mentor Mandatory with no cited Standard.
- Treating "never"/"always" phrasing as self-justifying evidence of Mandatory tier.
