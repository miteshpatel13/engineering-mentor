---
type: llm
---

PASS if the response identifies SQL injection from concatenating `customer`/`status` into the query as a blocking finding (CRITICAL or HIGH), recommends parameterized queries, and separates blocking findings from non-blocking recommendations.
FAIL if SQL injection is missed, rated MEDIUM/LOW/INFO, presented as non-blocking, or if the response approves the change for merge.
