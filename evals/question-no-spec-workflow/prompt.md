---
description: A simple question about code must be answered directly, without invoking the spec-driven workflow.
tags: [routing, negative]
max_turns: 5
timeout_seconds: 120
allowed_tools: [Read, Glob, Grep, Skill]
---

What does this function do?

```python
def chunk(xs, n):
return [xs[i:i + n] for i in range(0, len(xs), n)]
```
