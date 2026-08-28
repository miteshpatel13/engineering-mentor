---
id: performance-review-04-failure-subjective-slowness-no-evidence
category: failure-handling
skill_under_test: skills/performance-review/SKILL.md
---

# Scenario: "The App Feels Slow" With No Measurement

## Input Material

> A stakeholder reports: "The dashboard feels slow lately." No specific page, endpoint, timing figure, or comparison baseline is given.

## Pass Criteria

- States that a measurable baseline is required before diagnosis can proceed (Failure Handling), and names what evidence would establish one (timing measurement, profiling, monitoring data, a specific page/action).
- Does not guess at a specific bottleneck (e.g. "it's probably the database") from the subjective report alone.

## Fail Signals

- Proceeding to name a specific likely bottleneck with no evidence at all.
- Treating the vague report as sufficient to produce a diagnosis.
