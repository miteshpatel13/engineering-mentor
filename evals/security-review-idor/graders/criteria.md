---
type: llm
---

PASS if the response identifies (1) broken object-level authorization / IDOR because `user_id` comes from the request body instead of the authenticated session, (2) privilege escalation via the client-controlled `role` field (mass assignment), and (3) sensitive data (passwords) written to logs; with (1) and (2) rated CRITICAL or HIGH.
FAIL if the IDOR or the role escalation is missed or rated below HIGH.
