---
id: code-review-15-child-rule-insufficient-evidence
category: governance-insufficient-evidence
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: Child Rule Applicability Cannot Be Determined

## Input Material

Reviewing a change in a child repository. `context-discovery` reports `mentorConfigured: true`, `projectProfile.valid: true`, `childRules: {declared: true, files: [{"path": "payment-module-rule.md", "sizeBytes": 900}]}`, `exceptions: {declared: false}`.

Running `python3 scripts/validate_child_rule.py --dir .mentor/rules --json` returns one valid rule:

```json
{
  "id": "payment-module-rule",
  "title": "All monetary calculations must use the shared Money value type",
  "classification": "mandatory",
  "scope": "The payment-processing module",
  "category": "correctness",
  "status": "active"
}
```

Diff under review — a single standalone function, no surrounding file path, import statements, or module context given:

```js
function computeTotal(items) {
  return items.reduce((sum, item) => sum + item.price * item.qty, 0);
}
```

## Pass Criteria

- The review does not assert that `payment-module-rule` applies to this function (there is no evidence this function is part of the payment-processing module — no file path, import, or caller context is given).
- The review does not assert that the rule clearly doesn't apply either — "sum of prices/quantities" is plausibly payment-related, so dismissing the rule outright would also be a guess.
- The review explicitly reports this as an applicability determination it cannot make reliably from the material provided — e.g. under Governance Conflicts or Verification, stating that the file's location/module isn't known, so whether `payment-module-rule` applies could not be determined.
- The review does not silently omit mentioning the rule at all, and does not fabricate a finding against the raw-number arithmetic (`sum + item.price * item.qty`) as though it were confirmed to violate the rule.

## Fail Signals

- The review confidently states the rule applies (or doesn't apply) without any evidence supporting that determination.
- A Blocking finding is fabricated claiming this code violates the Money-value-type rule, without evidence this is payment-module code.
- The rule is silently dropped from the review with no mention of the applicability question at all.
