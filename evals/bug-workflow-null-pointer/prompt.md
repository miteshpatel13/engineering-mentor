---
description: A small bug must get an assess/fix/test flow without being forced through spec-driven development.
tags: [smoke, routing]
max_turns: 15
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
---

Fix this crash, it happens when the cart is empty:

```
TypeError: Cannot read properties of null (reading 'items')
at cartTotal (src/cart.js:3:22)
```

```js
// src/cart.js
export function cartTotal(cart) {
  return cart.items.reduce((sum, i) => sum + i.price * i.qty, 0);
}
```
