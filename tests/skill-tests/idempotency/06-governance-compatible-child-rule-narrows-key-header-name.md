---
id: idempotency-06-governance-compatible-child-rule-narrows-key-header-name
category: governance-sensitive
skill_under_test: skills/idempotency/SKILL.md
---

# Scenario: Child Rule Narrows the Mechanism Without Contradicting the Pattern

## Input Material

> A declared child rule, `classification: configurable`, states: "All idempotent write endpoints must accept the client-supplied key via header `X-Request-Id`, retained for 48 hours." The operation under review otherwise correctly implements constraint-backed enforcement per this Skill's Rules, using that header as the request identity.

## Pass Criteria

- Classifies this as Compatible or Additive (Governance Integration) — the child rule narrows this Skill's guidance to a specific header name and retention window without contradicting the underlying constraint-backed-enforcement principle.
- Confirms the child rule is honored as stated (specific header name, 48-hour retention) rather than treated as a deviation needing a governance conflict note.
- Does not flag anything as missing or wrong merely because the mechanism differs from this Skill's own illustrative `Idempotency-Key` example — Constraints (above) states illustrations are not requirements.

## Fail Signals

- Flagging the child's specific header-name choice as a defect because it differs from this Skill's Examples.
- Misclassifying a narrowing, non-contradicting child rule as a Conflict or Override.
