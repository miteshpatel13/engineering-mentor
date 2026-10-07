---
type: llm
---

PASS if the response (1) correctly analyzes the time complexity as O(n * m) (or O(n^2) when n ≈ m), identifying that `customers.find()` performs a linear scan inside the `orders.map()` loop, (2) explains the production impact for 50,000 items (~2.5 billion comparisons), (3) separates auxiliary space (O(m) for the lookup index) from input space, and (4) provides an optimized implementation using a Map or Set that achieves linear time O(n + m).
FAIL if the quadratic bottleneck is missed, if `customers.find()` is assumed to be O(1), or if auxiliary space is conflated with input space.
