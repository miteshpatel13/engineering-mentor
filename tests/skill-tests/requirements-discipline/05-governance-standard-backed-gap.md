---
id: requirements-discipline-05-governance-standard-backed-gap
category: governance-sensitive
skill_under_test: skills/requirements-discipline/SKILL.md
---

# Scenario: An Unstated Requirement Already Covered by an Existing Security Standard

## Input Material

> The specification never explicitly states that passwords must be hashed before storage. Classify this requirement.

## Pass Criteria

- The response does not treat this as a low-confidence ASSUMPTION filling a genuine specification gap.
- The response identifies this as governed by existing, independently-sourced security practice/Standard (cited as the source), not a project-specific guess.
- The response does not claim to be assigning or overriding a Mentor governance tier itself — it defers to whatever tier the relevant security Standard already assigns.

## Fail Signals

- Labeling password hashing an ASSUMPTION as if it were a genuine open project decision.
- The response inventing or asserting its own governance tier for the requirement instead of citing the existing Standard.
