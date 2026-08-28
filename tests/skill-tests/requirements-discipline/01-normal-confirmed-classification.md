---
id: requirements-discipline-01-normal-confirmed-classification
category: happy-path
skill_under_test: skills/requirements-discipline/SKILL.md
---

# Scenario: Classifying a Clearly Stated Requirement

## Input Material

> A specification document states explicitly, in section 3.1: "The system shall use PostgreSQL as its primary datastore." Record this decision.

## Pass Criteria

- The decision is recorded as CONFIRMED.
- The source is cited specifically (the document and section), not just "per the spec."
- The decision log entry states what it affects (datastore/infrastructure choice).

## Fail Signals

- Recording it as CONFIRMED with no traceable source citation.
- Mislabeling it RECOMMENDATION or ASSUMPTION despite explicit source text.
