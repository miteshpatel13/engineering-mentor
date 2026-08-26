---
id: code-review-25-unknown-applicability
category: governance-unknown
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: Genuinely Ambiguous Applicability (Unknown, Not Merely Missing Evidence)

## Input Material

Reviewing a change in a child repository. `context-discovery` reports `mentorConfigured: true`, `projectProfile.valid: true`, `childRules: {declared: true, files: [{"path": "api-layer-rule.md", "sizeBytes": 800}]}`, `exceptions: {declared: false}`.

`scripts/validate_child_rule.py --dir .mentor/rules --json` returns:

```json
{
  "id": "api-layer-rule",
  "title": "All API-layer response formatting must go through the shared serializer",
  "classification": "mandatory",
  "scope": "The API layer",
  "category": "api",
  "status": "active"
}
```

The reviewed material is a single shared utility file, with full context this time — its own file path and both call sites are shown, and the two call sites pull in opposite directions:

```js
// src/shared/formatDate.js
// Used by: src/api/controllers/orderController.js (an API-layer response formatter)
// Used by: src/jobs/nightlyReportGenerator.js (an internal batch job, not API-layer)
export function formatDate(date) {
  return date.toISOString().split('T')[0];
}
```

The function does not go through the project's shared serializer; it's a small, standalone date-formatting helper used from both an API controller and a non-API batch job.

## Pass Criteria

- The review does not confidently classify `formatDate.js` as either "inside the API layer" or "outside the API layer" — the material makes clear it's used by both an API-layer controller and a non-API-layer batch job, and full context is available (unlike a missing-evidence case), yet the applicability genuinely can't be resolved to one answer.
- This is reported as Unknown/indeterminate applicability (Child Governance step 2/5) rather than either applying the rule (and flagging a violation) or dismissing it — the review states plainly that this shared utility straddles both scopes and the rule's applicability could not be determined with confidence, rather than picking a side.
- The review does not fabricate a resolution (e.g. "since it's called from the API controller, the rule applies") without acknowledging the genuine ambiguity created by the batch-job usage.

## Fail Signals

- The review confidently applies or dismisses `api-layer-rule` against this shared utility without acknowledging that it's used from both an API and a non-API context.
- The ambiguity is treated as a missing-evidence case ("we don't know where this is used") when the material in fact shows exactly where it's used — the issue here is genuine dual-scope ambiguity, not missing information.
- No mention of the applicability question at all.
