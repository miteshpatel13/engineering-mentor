---
type: llm
---

PASS if the response (1) treats committing `.env` with a database password as a blocking CRITICAL or HIGH finding and says the credential must be rotated and removed from history, not just deleted in a later commit, (2) flags that unrelated changes (billing calculation fix, theme color, lockfile churn) are mixed in one commit and recommends splitting them, and (3) flags the "misc" commit message as not meaningful.
FAIL if the committed secret is missed or rated below HIGH, or if the change is approved for push.
