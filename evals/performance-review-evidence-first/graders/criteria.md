---
type: llm
---

PASS if the response (1) identifies the per-project Task/Member queries as an N+1 pattern and proposes batching/eager loading, (2) asks for or defines a measurable baseline and target (e.g. latency percentiles, query counts) before choosing a fix, and (3) says the improvement must be verified with measurements after the change, rather than presenting caching as the default fix.
FAIL if the N+1 pattern is missed, or if caching is endorsed without any measurement discipline.
