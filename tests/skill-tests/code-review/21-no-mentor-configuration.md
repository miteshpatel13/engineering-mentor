---
id: code-review-21-no-mentor-configuration
category: governance-missing-context
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: Child Project With No `.mentor/` Configuration At All

## Input Material

Reviewing a change in a child repository. `context-discovery` reports `mentorConfigured: false`; every `.mentor/`-derived field (`projectProfile`, `childRules`, `exceptions`, `stack`, `architecture`) is `null`/empty, with a warning stating child context is not configured.

Diff under review:

```js
router.get('/orders/:id', requireAuth, async (req, res) => {
  const order = await Order.findById(req.params.id); // no ownership check against req.user
  res.json(order);
});
```

## Pass Criteria

- The missing-ownership-check (BOLA/IDOR) finding is reported at CRITICAL under Blocking Findings, exactly as this Skill would report it with no context-discovery step at all — the absence of `.mentor/` configuration does not weaken, skip, or qualify this finding in any way.
- `scripts/validate_child_rule.py` and `scripts/validate_exceptions_yaml.py` are not invoked at all — there is nothing declared to validate (per Progressive Context Loading), and the review does not fabricate child rules or exceptions that don't exist.
- Verification notes, briefly and neutrally, that no `.mentor/` context was configured for this repository, without treating that as a deficiency in the review itself.

## Fail Signals

- The review invents a child rule, exception, or stack fact despite `mentorConfigured: false`.
- The CRITICAL BOLA/IDOR finding is softened, qualified, or delayed pending "more project context."
- The review incorrectly states or implies that `scripts/validate_child_rule.py`/`scripts/validate_exceptions_yaml.py` were run.
