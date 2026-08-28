---
id: uuid-strategy-07-rule-coverage-generation-strategy-tradeoff
category: rule-coverage
skill_under_test: skills/uuid-strategy/SKILL.md
---

# Scenario: Choosing Between Store-Generated and Application-Generated Identifiers

## Input Material

> A team is deciding how to generate the opaque public identifier for a new resource. One engineer wants a database default-expression value (generated automatically on insert); another wants the application layer to generate it before insert, citing an existing bulk-import script that writes directly to the database, bypassing the application entirely.

## Pass Criteria

- States the tradeoff explicitly per Rules → Generation Strategy: store-generated guarantees a value on any insert path, including the bulk-import script, at the cost of engine coupling; application-generated is portable but requires every insert path (including that same bulk-import script) to remember to set it.
- Given the stated bulk-import script that bypasses the application, correctly weighs this as a concrete point favoring store-generated for this specific case, rather than declaring one approach universally correct (Constraints).
- Does not present either option as a requirement — states it as a reasoned recommendation given the stated constraint.

## Fail Signals

- Declaring one generation approach "the standard" without engaging with the tradeoff or the stated bulk-import detail.
- Ignoring the bulk-import script's implication for whether application-generated identifiers would actually be reliably set.
