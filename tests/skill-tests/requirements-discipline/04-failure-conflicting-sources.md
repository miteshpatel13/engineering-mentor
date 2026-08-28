---
id: requirements-discipline-04-failure-conflicting-sources
category: failure-handling
skill_under_test: skills/requirements-discipline/SKILL.md
---

# Scenario: Two Authoritative Sources Conflict

## Input Material

> The original SRS (v1.0) states cancellations are non-refundable. A later client email states "refunds should be allowed within 24 hours." Both are treated as authoritative sources within the project. Record the requirement for refund handling.

## Pass Criteria

- The response records both sources and the conflict explicitly, rather than silently preferring the more recent one.
- The response escalates for an explicit resolution, or, if proceeding under an ASSUMPTION that the newer statement supersedes the SRS, states that reasoning explicitly as a recorded ASSUMPTION rather than as settled CONFIRMED fact.

## Fail Signals

- Silently implementing the 24-hour refund rule as CONFIRMED without recording that it conflicts with the SRS.
- Silently keeping the non-refundable rule without acknowledging the later client statement at all.
