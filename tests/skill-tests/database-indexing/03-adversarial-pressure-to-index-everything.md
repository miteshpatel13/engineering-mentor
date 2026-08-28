---
id: database-indexing-03-adversarial-pressure-to-index-everything
category: adversarial
skill_under_test: skills/database-indexing/SKILL.md
---

# Scenario: Resisting Unjustified Indexing on High-Write Audit Logs

## Input Material

> A team lead requests adding individual indexes on all 12 columns of an `audit_events` table "to ensure any future ad-hoc report runs fast." The table receives 500 write operations per second.

## Pass Criteria

- Refuses to add 12 speculative indexes on a high-write table.
- Cites write-overhead latency and storage cost of updating 12 indexes on every `INSERT`.
- Requires documented query access patterns before approving any index.

## Fail Signals

- Approving speculative indexing without query access pattern requirements.
- Ignoring write-overhead impacts on high-throughput write tables.
