---
type: llm
---

PASS if the response identifies that `cart` is null for an empty cart (the cause), proposes a guarded fix (for example returning 0 when cart or cart.items is missing), and recommends or provides a test for the empty/null cart case.
FAIL if the response proposes writing a specification or plan before fixing, or gives a fix with no test.
