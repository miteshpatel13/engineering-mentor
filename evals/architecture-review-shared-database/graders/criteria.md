---
type: llm
---

PASS if the response flags (1) both services writing the same tables as a data-ownership / coupling problem and (2) the synchronous Orders<->Billing call cycle as a coupling and failure-mode (cascading failure / availability) risk, and proposes a concrete alternative for at least one of them (e.g. a single owner per table exposed via an API or events).
FAIL if either risk is missed, or if the response endorses the design as-is.
