---
description: A request to analyze time and space complexity must trigger algorithm-complexity, derive quadratic complexity from nested iteration and hidden built-in costs, distinguish auxiliary space from input space, and propose an optimized linear approach with a Map/Set.
tags: [core-engineering, complexity, performance]
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

Can you review the algorithmic complexity of this function? It will process batches of up to 50,000 orders and customers.

```typescript
interface Order { id: string; customerId: string; amount: number; }
interface Customer { id: string; name: string; tier: string; }

export function enrichOrdersWithCustomerTier(orders: Order[], customers: Customer[]) {
  return orders.map(order => {
    const customer = customers.find(c => c.id === order.customerId);
    return {
      ...order,
      customerTier: customer ? customer.tier : 'STANDARD',
    };
  });
}
```

What is the time and space complexity, and how should we optimize it if needed?
