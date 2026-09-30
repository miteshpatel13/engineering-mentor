---
description: A happy-path-only, mock-interaction test suite must trigger testing-review and be judged inadequate despite high line coverage.
tags: [review, testing]
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

Is this test suite good enough to ship the transfer feature? Coverage report says 92%.

```ts
describe('TransferService.transfer', () => {
  it('transfers money', async () => {
    const repo = { debit: jest.fn(), credit: jest.fn() };
    const svc = new TransferService(repo as any);
    await svc.transfer('acc-1', 'acc-2', 100);
    expect(repo.debit).toHaveBeenCalled();
    expect(repo.credit).toHaveBeenCalled();
  });
});
```

`transfer` checks the balance, rejects negative amounts, requires the caller to own `acc-1`, and runs debit+credit in a transaction.
