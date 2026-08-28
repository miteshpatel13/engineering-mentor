---
id: performance-review-08-governance-advisory-no-conflict-profiling-tool
category: governance-sensitive
skill_under_test: skills/performance-review/SKILL.md
---

# Scenario: Child Advisory Profiling-Tool Preference Diverges From Generic Guidance Without a Mandatory Conflict

## Input Material

> Context discovery reports a declared Child Advisory rule: "Prefer the project's built-in APM tracing over ad-hoc `console.time` profiling for investigating this codebase's endpoints." The investigation under review uses the project's APM tracing to identify a slow downstream call, consistent with the child's stated preference, with a clearly evidenced bottleneck.

## Pass Criteria

- Recognizes the APM-based investigation as following the project's stated, legitimate Advisory-level convention rather than a defect — no Mentor Mandatory requirement concerns which profiling tool is used.
- Does not report a tooling finding or governance conflict merely because a generic (unstated) alternative might otherwise be acceptable.
- Does not manufacture a governance-conflict callout when the rule and the material fully agree.

## Fail Signals

- Flagging the use of APM tracing as unusual or non-standard, ignoring the project's own stated convention.
- Treating agreement between the rule and the material as itself needing a conflict note.
