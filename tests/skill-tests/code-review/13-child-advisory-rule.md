---
id: code-review-13-child-advisory-rule
category: governance-advisory
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: Child Advisory Rule (No Conflict)

## Input Material

Reviewing a change in a child repository. `context-discovery` reports `mentorConfigured: true`, `projectProfile.valid: true`, `childRules: {declared: true, files: [{"path": "03-testing-requirements.md", "sizeBytes": 1600}]}`, `exceptions: {declared: false}`.

Running `python3 scripts/validate_child_rule.py --dir .mentor/rules --json` returns one valid rule:

```json
{
  "id": "03-testing-requirements",
  "title": "Prefer integration tests over deep mocking for service-layer code",
  "classification": "advisory",
  "scope": "src/services/** test coverage",
  "category": "testing",
  "status": "active"
}
```

Diff under review — a new service method plus its test:

```js
// src/services/orderService.js
async function cancel(orderId) {
  return prisma.order.update({ where: { id: orderId }, data: { status: 'cancelled' } });
}

// src/services/orderService.test.js
test('cancel updates order status', async () => {
  const mockUpdate = jest.fn().mockResolvedValue({ id: 1, status: 'cancelled' });
  prisma.order.update = mockUpdate;
  await cancel(1);
  expect(mockUpdate).toHaveBeenCalledWith({ where: { id: 1 }, data: { status: 'cancelled' } });
});
```

## Pass Criteria

- The review does not report a Blocking or CRITICAL/HIGH finding merely because the test mocks the Prisma client deeply.
- The review may note, at INFO or LOW, that the child's Advisory testing rule (`03-testing-requirements`) prefers an integration-test approach here, citing the rule — framed as a preference/recommendation, not a defect.
- The finding (if any) is Non-Blocking and does not claim the code is non-compliant with a Mandatory requirement — Advisory-tier guidance never produces a Blocking finding on its own.
- No exception mechanism is invoked or requested — Child Advisory guidance can be followed or deviated from without one.

## Fail Signals

- The deep-mocking test is reported as a Blocking, CRITICAL, or HIGH finding.
- The review claims the code "violates" a Mandatory rule when the underlying rule is Advisory.
- The review demands an exception entry before accepting the deviation from the child's Advisory preference.
