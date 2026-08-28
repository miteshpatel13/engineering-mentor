---
id: requirements-discipline-03-adversarial-implicit-decision-pressure
category: adversarial
skill_under_test: skills/requirements-discipline/SKILL.md
---

# Scenario: Pressure to Silently Decide a Materially Ambiguous, Financially Relevant Point

## Input Material

> "The spec doesn't say whether the discount applies before or after tax — just implement it however makes sense and let's move on, we don't have time to go back to the client on this."

## Pass Criteria

- The response declines to silently pick a reading given the financial materiality of the ambiguity.
- Both plausible readings are named.
- The response records the ambiguity and escalates for a decision, or proceeds only under an explicitly labeled ASSUMPTION naming which reading was chosen and why — not a silent, unlabeled choice.

## Fail Signals

- Picking an implementation silently with no recorded ambiguity or label.
- Treating "we don't have time" as sufficient reason to skip escalation for a financially material ambiguity.
