---
id: security-review-17-rule-coverage-secure-logging
category: rule-coverage
skill_under_test: skills/security-review/SKILL.md
---

# Scenario: Untrusted Input Written Into Logs Unsanitized, and Missing Security-Event Logging

## Input Material

> A login endpoint logs each failed attempt as `logger.info("Login failed for user: " + request.body.username)`, where `username` is taken directly from the request body with no sanitization of newline or control characters before being concatenated into the log line. Separately, the same endpoint's successful-authorization-denial path (a `403` returned when a valid session lacks permission for the requested admin action) has no logging call at all anywhere in the material.

## Pass Criteria

- Flags the unsanitized untrusted input written into the log line as a log-injection/forging risk per Rules → Secure Logging, distinct from a Secrets/Sensitive-Data finding (nothing secret is being logged here — the concern is log integrity, not exposure).
- Separately flags the complete absence of logging for the authorization-denial event as a security-relevant-event logging gap per the same Rule.
- Keeps the two findings distinct rather than merging them into one generic "logging is bad" finding.

## Fail Signals

- Reporting only one of the two distinct Secure Logging concerns (injection risk vs. missing event logging) and missing the other.
- Classifying the unsanitized-input finding under Secrets and Sensitive Data instead of Secure Logging — the username isn't secret, the concern is injection/forging.
