---
id: api-review-22-rule-coverage-http-method-semantics
category: rule-coverage
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: HTTP Method Semantics — State-Changing Operation Exposed via a Safe Method

## Input Material

> An endpoint `GET /api/reports/:id/regenerate` triggers a full regeneration of a report (a expensive, side-effecting server operation that overwrites the existing report content and increments an internal `regenerationCount` field) whenever it is called — including when called by a link crawler, browser prefetch, or any automated tool that follows `GET` links assuming they are safe and side-effect-free, which the material confirms has already happened at least once (a monitoring/uptime-check bot that periodically issues `GET` requests to all known endpoint paths inadvertently triggered several regenerations).

## Pass Criteria

- Flags this as an HTTP Method Semantics finding: `GET` is defined as a safe method with no expected side effects, and this endpoint's actual behavior (triggering expensive, state-changing regeneration) violates that expectation — this is a Real Defect, not merely a style preference, since the material shows it has already caused an actual incident (unintended regenerations triggered by a monitoring bot).
- Recommends changing the operation to a non-safe method appropriate to its semantics (`POST`, since regeneration is not idempotent in the sense of "safe to repeat with identical effect" per the material — each call increments a counter and overwrites content) rather than merely recommending caution.
- Assigns a severity reflecting that this is a confirmed, materially-evidenced defect (the monitoring-bot incident is concrete evidence in the material), not a hypothetical risk.

## Fail Signals

- Treating this as a minor style/convention preference (e.g. INFO/LOW) when the material provides concrete evidence of an actual incident caused by the method-semantics violation.
- Failing to flag it at all because the endpoint "works" in the sense of returning a response — the defect is that a safe-method contract is violated, not that the endpoint is non-functional.
- Recommending a fix that doesn't address the actual method-semantics mismatch (e.g. "add authentication" or "add rate limiting" without addressing that `GET` should not perform this side effect at all).
