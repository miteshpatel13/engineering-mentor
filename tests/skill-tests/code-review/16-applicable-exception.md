---
id: code-review-16-applicable-exception
category: governance-exception-applicable
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: Applicable, Approved Exception on a Non-Security Finding

## Input Material

Reviewing a change in a child repository. `context-discovery` reports `mentorConfigured: true`, `projectProfile.valid: true`, `childRules: {declared: false}`, `exceptions: {declared: true, path: ".mentor/exceptions.yaml", parsed: true, entryCount: 1}`.

Running `python3 scripts/validate_exceptions_yaml.py .mentor/exceptions.yaml --json` returns one valid entry:

```json
{
  "id": "legacy-report-no-pagination",
  "rule": "pagination-required",
  "reason": "/v1/legacy-report is a deprecated endpoint scheduled for removal; adding pagination now would require client changes we don't want to make for a route being deleted next quarter.",
  "scope": "GET /v1/legacy-report only",
  "owner": "api-team",
  "status": "approved",
  "approvedBy": "jane.doe",
  "approvedAt": "2026-01-15",
  "expiresAt": "2026-09-01"
}
```

Diff under review:

```js
router.get('/v1/legacy-report', requireAuth, async (req, res) => {
  const rows = await Report.find({}); // unbounded, no pagination
  res.json(rows);
});
```

## Pass Criteria

- The unbounded query / missing pagination is still reported as a real finding (MEDIUM by default per Severity for Availability/Resource-Exhaustion Findings, absent further scale evidence) — the exception's existence does not remove it from the Findings section.
- Verification (or an equivalent explicit note) states that an approved, scoped exception (`legacy-report-no-pagination`) exists for exactly this endpoint and rule, and that this Skill does not implement exception-aware suppression or downgrading of findings in this phase.
- The finding's severity is not altered because an approved exception exists — it is assessed purely on the evidence bar in Severity for Availability/Resource-Exhaustion Findings, independent of the exception.

## Fail Signals

- The finding is omitted or removed from Findings because an approved exception exists.
- The finding's severity is silently downgraded because of the exception.
- The exception is not mentioned at all, leaving the reader unaware that a relevant, approved deviation is on record.
