---
type: llm
---

PASS if the response says the plan is NOT ready for /speckit-tasks and, as blocking (CRITICAL or HIGH) findings, identifies both (1) trusting a client-supplied unit_price instead of calculating the price on the server and (2) adding a NOT NULL column with no default or backfill to a 30-million-row live table; and mentions at least one of: no unique constraint on (customer_id, sku), no rollback plan, deploying migration and code together.
FAIL if the plan is approved, if either (1) or (2) is missed or rated below HIGH, or if the response edits the plan instead of reviewing it.
