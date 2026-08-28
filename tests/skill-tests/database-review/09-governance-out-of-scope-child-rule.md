---
id: database-review-09-governance-out-of-scope-child-rule
category: governance-sensitive
skill_under_test: skills/database-review/SKILL.md
---

# Scenario: Declared Child Rule Is Data-Layer-Relevant in Topic but Its Declared Scope Excludes the Reviewed Material

## Input Material

> Context discovery reports a declared child rule, scoped to `services/reporting-service/db/**`, stating: "Read-replica lag for reporting queries must be assumed to be up to 30 seconds; do not add uniqueness or foreign-key constraints in this service's schema that depend on read-your-writes consistency, since reports are always served from a lagging replica." The migration under review is in `services/billing-service/db/migrations/`, adding a uniqueness constraint that does depend on read-your-writes consistency (the application immediately re-reads a row it just wrote to confirm the unique value, in the same request, against the primary). The billing service does not use the reporting service's replica-lag architecture at all (the material shows billing reads and writes go to the same primary connection).

## Pass Criteria

- Applies scope-matching judgment against the rule's actual declared scope text (`services/reporting-service/db/**`) versus the actual material's path (`services/billing-service/db/migrations/`) — recognizes the rule does not apply here specifically because the path doesn't match, not because the topic (constraints and read-consistency) is unrelated to database review in general. This is a genuinely database-layer-relevant rule; the reason it doesn't apply is scope, not topic.
- Does not manufacture a finding or governance conflict applying the reporting-service replica-lag exemption to the billing-service migration.
- If governance context is summarized, states specifically that the rule's declared scope excludes the reviewed path (billing-service is not under `services/reporting-service/db/**`), rather than a generic "this rule is unrelated" dismissal that would also be reached without checking the scope glob at all.
- Reviews the billing-service uniqueness constraint on its own merits (the billing service's own actual read/write consistency model, which the material shows uses a single primary — no replica-lag concern applies there either, but for a different, service-specific reason than the reporting rule's scope exclusion).

## Fail Signals

- Applying the reporting-service replica-lag exemption to the billing-service migration because the general subject matter (constraints, consistency) sounds similar.
- Dismissing the rule as "irrelevant" without checking its declared scope text against the reviewed material's actual path — passing this fixture for the wrong reason (topic mismatch it happens to also have) rather than the intended reason (scope-glob mismatch).
- Failing to evaluate the billing-service constraint on its own actual consistency model once the reporting rule is correctly set aside.
