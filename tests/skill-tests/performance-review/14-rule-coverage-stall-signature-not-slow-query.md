---
id: performance-review-14-rule-coverage-stall-signature-not-slow-query
category: rule-coverage
skill_under_test: skills/performance-review/SKILL.md
---

# Scenario: A Config Read With a 10 ms Median and a 1.6 s Average

## Input Material

> APM over 23 days: `GET /version` (two reads of tiny config tables) has a median of 10.8 ms, an average of 1.6 s, and a max of exactly 10 minutes. Eleven other unrelated endpoints also show a max of exactly 10 minutes. The config-table select averages 884 ms with a max of 16 minutes. Separately, `POST /otp/send` max is 6 minutes on days the SMS provider was slow; its HTTP client has no timeout. The team proposes adding an index to the config table and caching the version response.

## Pass Criteria

- Applies Rules → Stall Signatures Point at Shared Resources: the median/average gap and the identical cross-endpoint maxima indicate waiting for a shared resource (connection pool, leaked or deadlocked connections), not query cost; recommends correlating stall times with scheduled jobs and deploys and diagnosing per `skills/data-access-reliability/SKILL.md`.
- Says the index will not address the diagnosed cause (Rules → Optimization Relevance); caching may help the endpoint but not the shared stall.
- Applies Rules → External Calls Bound the Request to the OTP endpoint: add a timeout and return a quick retryable error.
- States re-measurement targets (e.g. max config read under 1 s, OTP max near the timeout) per Post-Change Verification Required.

## Fail Signals

- Accepting the index as the fix.
- Diagnosing from the average alone.
