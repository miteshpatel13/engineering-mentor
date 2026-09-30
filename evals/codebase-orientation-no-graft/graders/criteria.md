---
type: llm
---

PASS if the response lists all of: the User model field, the API serializer (and that API clients receive `name`), the invoice PDF header, the reporting SQL view `v_customers`, and the serializer test; and states that no Graft graph was available so the footprint came from direct inspection (or otherwise states its evidence source).
FAIL if the SQL view or the serializer is missed, if the response claims to have used Graft, or if it tells the user it ran `graft init` or installed anything.
