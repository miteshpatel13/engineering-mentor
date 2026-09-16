# third-party-integration Skill — Regression Fixtures

5 narrative fixture specifications for `skills/third-party-integration/SKILL.md` (`docs/Skill Taxonomy.md` Section 1, `Authoring/Workflow` type). Tests the complete third-party integration lifecycle across normal adapter isolation, rate limiting backoff edge cases, adversarial webhook spoofing/replays, circuit breaker failure recovery, and OAuth 2.0 token lifecycle rule coverage.

## Fixtures

| # | File | Category |
|---|---|---|
| 01 | `01-normal-rest-webhook-adapter.md` | Normal — asynchronous webhook ingestion, HMAC signature verification, and Anti-Corruption Layer adapter isolation |
| 02 | `02-edge-rate-limiting-and-exponential-backoff.md` | Edge case — handling HTTP 429 rate limits, `Retry-After` header parsing with full jitter, and client-side throttling |
| 03 | `03-adversarial-unverified-webhook-replay.md` | Adversarial — rejecting spoofed webhook signatures, expired timestamps, and duplicate event replays |
| 04 | `04-failure-circuit-breaker-third-party-downtime.md` | Failure handling — tripping circuit breaker on prolonged 503 outage, graceful degradation, and dead-letter queue routing |
| 05 | `05-rule-coverage-oauth-token-refresh-lifecycle.md` | Rule coverage — OAuth 2.0 Authorization Code flow with PKCE, concurrent token refresh lock, and secure token caching |
