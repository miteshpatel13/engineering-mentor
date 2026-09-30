---
type: llm
---

PASS if the proposed contract includes all of: (1) an idempotency mechanism for refund creation (e.g. an Idempotency-Key header or client request id) so retries cannot double-refund, (2) server-side validation that the refund amount does not exceed the remaining refundable amount, (3) an asynchronous or pending status for refunds that settle later, and (4) explicit error responses with status codes for at least invalid amount and not-found/not-refundable cases.
FAIL if idempotency is absent, if over-refund validation is absent, or if there is no error contract.
