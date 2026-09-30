---
type: llm
---

PASS if the response concludes the suite is NOT adequate to ship, explains that line coverage does not demonstrate behavioral protection, and names missing tests for at least three of: insufficient balance, negative/zero amount, caller not owning the source account (authorization), transaction rollback when credit fails, and concurrent transfers.
FAIL if the response calls the suite adequate or only suggests cosmetic improvements.
