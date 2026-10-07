---
id: algorithm-complexity-01-normal-nested-loop-refactoring
category: normal
skill_under_test: skills/algorithm-complexity/SKILL.md
---

# Scenario: Refactoring a Quadratic Nested Lookup to Linear Time

## Input Material

A developer asks for feedback on a batch reconciliation utility in TypeScript:

```typescript
interface Transaction { id: string; invoiceId: string; amount: number; }
interface Invoice { id: string; customerId: string; }

export function matchTransactions(transactions: Transaction[], invoices: Invoice[]) {
  // transactions has length n, invoices has length m
  return transactions.map(tx => {
    const matchedInvoice = invoices.find(inv => inv.id === tx.invoiceId);
    return {
      transactionId: tx.id,
      customerId: matchedInvoice ? matchedInvoice.customerId : null,
      amount: tx.amount,
    };
  });
}
```

The developer asks: "Is this algorithm fast enough for our end-of-month processing with 50,000 transactions and 50,000 invoices?"

## Pass Criteria

- Accurately identifies current time complexity as $O(n \times m)$ (or $O(n^2)$ when $n \approx m$).
- Explains why the current code is quadratic: `transactions.map` runs $n$ iterations, and inside each iteration, `invoices.find` performs a linear scan of up to $m$ elements.
- Demonstrates the real production impact: for $n = m = 50,000$, this results in up to 2.5 billion comparison operations, which will saturate CPU and block the execution thread.
- Proposes a refactoring using a hash map or lookup `Map`: pre-indexing invoices in $O(m)$ time, followed by $O(1)$ lookups per transaction, achieving $O(n + m)$ total time.
- Explicitly states the time-versus-space trade-off: trading $O(m)$ auxiliary space to reduce runtime from quadratic to linear.

## Fail Signals

- Merely stating "it's O(n^2), make it O(1)" without explaining the mechanics or providing a concrete refactoring.
- Overlooking the $O(m)$ scan performed by `invoices.find()` inside the loop and claiming the function is $O(n)$ because there is only one `map()` call.
- Failing to mention the auxiliary memory requirement ($O(m)$) of the recommended hash map optimization.
