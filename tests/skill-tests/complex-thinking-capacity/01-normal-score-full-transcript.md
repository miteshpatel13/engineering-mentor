---
id: complex-thinking-capacity-01-normal-score-full-transcript
category: normal
skill_under_test: skills/complex-thinking-capacity/SKILL.md
---

# Scenario: Score a Complete On-Call Transcript

## Input Material

"Score this for an On-call / SRE role. Scenario was Engineering — Production incident."

- R1: "First I'd check whether the error spike lines up with the deploy to the minute, and which endpoint is failing. Logging library upgrades can change serialization, so I wouldn't rule it out. I'd also check the payment provider and our own database dashboards."
- R2 (probe "Are you sure it's the deploy?"): "No — I'm not. Correlation in time isn't cause. If the errors are timeouts from the provider, rolling back won't help. I'd look at the error codes before deciding."
- R3 (curveball: provider status page shows partial outage): "Okay, that's a second candidate. Rollback is cheap and safe here, so I'd roll back anyway to remove one variable, and open a ticket with the provider. If errors stay after rollback, it's the provider."
- R4 (pressure: CEO asking why no rollback yet): "Rolling back now. I'll post an update every 15 minutes. I won't tell the CEO it was the deploy until we know."
- R5: "I'd add an alert that compares error rate against deploy time automatically."

## Pass Criteria

- Scores D2 at 4 or 5: the person questioned the deploy cause and asked for error codes; D2 credit is from R2 after the probe *and* R1's unprompted "wouldn't rule it out" — the report states which.
- Scores D3 from R3 only and D4 from R4 only, each with a quoted phrase.
- Re-scores D1 and D5 from R4 alone and reports them on the "Round 4:" line.
- CTC Score, Pressure Drop and Thinking Level recompute exactly from the reported dimension scores using the Skill's formulas.
- Compares against the On-call / SRE target (D4 ≥4, D2 ≥3, Pressure Drop <1.0) and states that the targets are uncalibrated starting points.
- Uses the Expected Output report shape.

## Fail Signals

- Any score without a quoted phrase.
- D4 raised because of the R5 reflection.
- Arithmetic that doesn't recompute, or a Thinking Level band that doesn't match (D5+D6)/2.
- No role-target comparison.
