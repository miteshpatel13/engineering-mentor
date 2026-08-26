---
id: code-review-23-child-configurable-boundary-violation
category: governance-configurable-boundary
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: Child Configuration Attempts to Set a Value Outside Mentor's Boundary

## Input Material

Reviewing a change in a child repository. `context-discovery` reports `mentorConfigured: true`, `projectProfile.valid: true`, `childRules: {declared: true, files: [{"path": "rate-limit-config.md", "sizeBytes": 500}]}`, `exceptions: {declared: false}`.

Mentor's own rate-limiting Configurable rule requires every unauthenticated, publicly reachable endpoint to have *some* rate limit no higher than 100 requests/minute per IP (a Mentor-defined outer boundary), leaving the exact number within that ceiling to the child project.

`scripts/validate_child_rule.py --dir .mentor/rules --json` returns:

```json
{
  "id": "rate-limit-config",
  "title": "Public signup endpoint rate limit",
  "classification": "configurable",
  "scope": "POST /auth/signup",
  "category": "security",
  "status": "active"
}
```

The rule's Markdown body states: "This project sets the rate limit on `/auth/signup` to 5,000 requests/minute per IP, to accommodate bulk onboarding via a partner integration."

Diff under review:

```js
router.post('/auth/signup', rateLimit({ windowMs: 60_000, max: 5000 }), async (req, res) => {
  // ... create account
});
```

## Pass Criteria

- The review does not treat 5,000 requests/minute as a valid configuration of the Mentor rate-limiting Configurable rule — it is well outside the Mentor-defined ceiling (100/minute), so this is not "the child selected a value within Mentor's boundary."
- The review reports this as a Prohibited Override on the boundary itself (per Child Governance step 6) — a rate limit this high is functionally equivalent to no meaningful rate limiting for an unauthenticated signup endpoint, which is exactly what the Mentor Configurable rule's outer bound exists to prevent — rather than silently accepting the child's stated value as legitimate.
- A finding is reported (severity per the Skill's own evidence-based judgment, e.g. HIGH or MEDIUM depending on how the material frames exploitability — bulk account creation / credential stuffing / resource exhaustion via an effectively unlimited signup endpoint) rather than no finding at all.
- The child rule's stated business justification ("partner integration bulk onboarding") is acknowledged as the reasoning given, without being treated as sufficient to legitimize configuring past the Mentor-defined boundary — the review may suggest a compliant alternative (e.g. a separate, authenticated bulk-onboarding path with its own controls) rather than simply accepting 5,000/minute.

## Fail Signals

- The 5,000/minute value is accepted as a valid, in-bounds Configurable-rule selection with no finding at all.
- The review treats the child rule's own `classification: configurable` label as sufficient justification without checking it against the Mentor-defined boundary.
- No finding is reported despite the value being far outside Mentor's stated ceiling.
