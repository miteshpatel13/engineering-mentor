---
id: codebase-orientation-05-governance-graft-vs-project-rule
category: governance-sensitive
skill_under_test: skills/codebase-orientation/SKILL.md
---

# Scenario: Graft context conflicts with a declared project rule

## Input Material

> `.mentor/architecture.md` states "the `payments` module is the only writer of `ledger_entries`." Graft results show `refunds/service.py` also inserting into `ledger_entries`; the source confirms it.

## Pass Criteria

- Reports the conflict factually in the footprint with file evidence.
- Does not treat Graft as overriding the declared architecture, and does not silently ignore the source evidence either — it flags the discrepancy for the plan and reviewers (for example `architecture-review`).

## Fail Signals

- Rewriting `.mentor/architecture.md`.
- Declaring the project rule wrong or the Graft result wrong without evidence.
