---
id: complex-thinking-capacity-02-edge-missing-pressure-round
category: edge-case
skill_under_test: skills/complex-thinking-capacity/SKILL.md
---

# Scenario: Transcript Missing the Pressure Round

## Input Material

"The recording cut off after the curveball. Can you still score it? Role: Software engineer. Scenario: QA — Release night."

- R1: "Duplicates could hit stock and invoices. I'd check how many users are on bad networks."
- R2 (probe): "The one-line fix might not cover retries. I'd check idempotency on the order endpoint."
- R3 (curveball): "Reconciliation shares the path, so I'd add its regression tests before shipping."

## Pass Criteria

- Scores D1, D2, D3, D5, D6 from the available rounds with quoted evidence.
- Marks D4 "not observed" (not a low score) and does not compute the Pressure Drop, saying round 4 is missing.
- Reports the CTC Score as "based on 5/6 dimensions", computed as the average of the five observed scores × 20.
- Suggests re-running the pressure round (same scripted pressure) before any decision.

## Fail Signals

- Scoring D4 as 1 or any number.
- Computing a Pressure Drop.
- Dividing by 6 with a missing dimension, or omitting "based on 5/6 dimensions".
