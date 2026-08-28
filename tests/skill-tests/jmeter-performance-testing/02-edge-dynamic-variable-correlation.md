---
id: jmeter-performance-testing-02-edge-dynamic-variable-correlation
category: edge
skill_under_test: skills/jmeter-performance-testing/SKILL.md
---

# Scenario: Dynamic Variable Correlation Across Test Steps

## Input Material

> A load test plan logs in a user in Step 1 and receives a JWT token `eyJhbGci...`. In Step 2 (Create Post), the developer hardcodes a single static JWT token string into the header for all 200 virtual user threads.

## Pass Criteria

- Identifies static hardcoded tokens across threads as a correlation failure.
- Mandates dynamic token extraction (JSON Path Extractor) from Step 1 response payloads to pass dynamically into Step 2 headers.

## Fail Signals

- Hardcoding dynamic session IDs, JWT tokens, or resource UUIDs across virtual user threads.
