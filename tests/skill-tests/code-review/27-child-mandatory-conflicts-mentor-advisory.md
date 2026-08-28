---
id: code-review-27-child-mandatory-conflicts-mentor-advisory
category: governance-conflict
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: Child Mandatory Rule Genuinely Conflicts With Mentor Advisory Guidance (Category 4 — Conflict, Not Override)

## Input Material

Reviewing a change in a child repository. `context-discovery` reports `mentorConfigured: true`, `projectProfile.valid: true`, `childRules: {declared: true, files: [{"path": "log-format.md", "sizeBytes": 550}]}`, `exceptions: {declared: false}`.

Mentor's own generic Advisory guidance (non-security, style/pattern-level) recommends structured (JSON) logging for application log output, as a general default absent a project-specific reason to prefer something else.

`scripts/validate_child_rule.py --dir .mentor/rules --json` returns:

```json
{
  "id": "log-format",
  "title": "All service logs must use the fixed plain-text line format",
  "classification": "mandatory",
  "scope": "All application logging across every service in this repository",
  "category": "observability",
  "status": "active"
}
```

The rule's own body (summarized in the material) states this is mandated project-wide because the existing on-call alerting pipeline parses only this exact plain-text format, and changing it would break incident-response tooling.

Diff under review — a new log statement using the project's mandated plain-text format, not JSON:

```js
logger.write(`[${new Date().toISOString()}] [INFO] [billing-service] payment processed for order ${orderId}`);
```

Running `python3 scripts/evaluate_governance.py <repo-root> --assertions <file> --json` with this rule's `ruleId`, `mentorRequirementTier: mentor_advisory`, `applicability: applies`, `relationship: replaces` returns `classification: conflict`, `handling: surface_conflict_child_favored` — matching `docs/Governance Evaluation.md`'s own deterministic test scenario `05-child-mandatory-vs-mentor-advisory`, which this fixture's assertions are deliberately modeled on.

## Pass Criteria

- The review does **not** treat this identically to fixture 24 (a silent, unremarked Override) — the child rule here is Child Mandatory, a different tier than fixture 24's Child Advisory, and `scripts/evaluate_governance.py` classifies this relationship as `conflict`, not `override`.
- A Governance Conflicts entry is included, stating: Mentor's generic Advisory guidance prefers structured (JSON) logging; the Child Mandatory `log-format` rule requires the fixed plain-text format; the two disagree — surfaced explicitly, per `docs/Governance Precedence Model.md` Section 11's "surface the conflict explicitly — do not silently pick a side" handling for a true Conflict.
- The review does not report a Findings-section defect recommending JSON logging as if the plain-text format were simply wrong — the Child Mandatory rule outranks Mentor Advisory in the precedence order (`docs/Governance Precedence Model.md` Section 4), so the plain-text format is what the project actually follows; this is stated as the resolution of a surfaced conflict (`handling: surface_conflict_child_favored`), not reported as a silent Override (contrast with fixture 24) and not reported as a Prohibited Override (contrast with fixture 12/18 — the underlying Mentor requirement here is Advisory, not Mandatory, so Section 9's prohibited-override treatment does not apply).

## Fail Signals

- Treating this exactly like fixture 24 — silently accepting the child's format with no Governance Conflicts entry at all, as though it were an ordinary, unremarkable Override.
- Reporting a Findings-section finding that the log format "should" be JSON, phrased as an unresolved defect, with no acknowledgment that the Child Mandatory rule legitimately governs here.
- Misclassifying this as a Prohibited Override (rejecting the child's rule outright) — the superseded Mentor requirement is Advisory, not Mandatory, so this is a legitimate Conflict outcome favoring the child, not an override attempt to be rejected.
