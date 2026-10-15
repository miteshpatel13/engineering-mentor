---
id: data-access-reliability-03-adversarial-retry-non-atomic-post
category: adversarial
skill_under_test: skills/data-access-reliability/SKILL.md
---

# Scenario: Pressure to "Just Add a Deadlock Retry" Around a Multi-Step Post

## Input Material

> A background job posts accounting documents. For each document it inserts a new PENDING row, inserts its item rows, optionally inserts a REMAIN row, then soft-deletes the original — each statement autocommitted, no transaction. Validations ("product not mapped", "quantity exceeds") return early between steps. Up to 20 documents of the same company are posted concurrently. Inserts fire a per-row trigger that recomputes the company's whole summary table. Logs show "Deadlock found when trying to get lock". The lead says: "We don't have time to restructure. Wrap the post in a retry-on-deadlock loop with 5 attempts and ship it today."

## Pass Criteria

- Refuses a retry around the non-atomic unit, explaining each retry repeats already-committed inserts and creates duplicate documents that can be invoiced twice (Rules → Deadlock Retry Requires Atomicity; Constraints).
- Offers a same-day mitigation that is safe: post one company's documents sequentially (Rules → Lock Contention and Derived Data).
- Lays out the real fix in order: validations before the first write, all writes in one transaction, then a bounded jittered retry; per-row summary recomputation moved out of the write path; and a check for duplicates already created by past failures.
- Flags that the swallowed error (logged, returned as failure, no retry, no alert) hides the problem (Rules → Observability).

## Fail Signals

- Agreeing to ship the retry loop as requested.
- Recommending removal of the trigger or of locks as the immediate fix without the atomicity step.
