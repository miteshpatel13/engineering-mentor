---
id: third-party-integration-03-adversarial-unverified-webhook-replay
category: adversarial
skill_under_test: skills/third-party-integration/SKILL.md
---

# Scenario: Webhook Spoofing, Signature Bypass, and Replay Attack

## Input Material

> Review an inbound webhook implementation receiving payment notifications from a third-party gateway:
> ```python
> @app.post("/webhooks/payments")
> async def handle_payment_webhook(request: Request):
>     data = await request.json()
>     if request.headers.get("X-Signature") == "test-key":
>         order_id = data["order_id"]
>         db.orders.update(order_id, status="PAID")
>         return {"status": "ok"}
>     return {"error": "invalid signature"}, 400
> ```

## Pass Criteria

- **Identifies Security Vulnerabilities**: Flags the hardcoded signature check (`"test-key"`) as a CRITICAL security flaw that allows attackers to forge payment completions.
- **HMAC Verification with Constant-Time Comparison**: Mandates computing HMAC SHA-256 over raw unparsed request bytes using the secret key from a secure store, evaluated via constant-time comparison (`timingSafeEqual`) to prevent timing attacks.
- **Replay Attack Defense**: Requires verifying a timestamp header (e.g., `X-Timestamp`) within a strict tolerance window (e.g., $\le 300$ seconds) to reject replayed historical payloads.
- **Deduplication / Idempotency**: Requires recording `event_id` in an idempotency table backed by a database unique constraint to prevent duplicate processing of re-sent webhooks.

## Fail Signals

- Accepting simple equality string checks (`==`) for HMAC signature validation.
- Verifying the signature over parsed JSON or re-serialized strings rather than raw request bytes.
- Failing to detect the replay vulnerability when timestamp verification or idempotency deduplication is omitted.
- Leaving payment status mutation directly in the synchronous HTTP request handler.
