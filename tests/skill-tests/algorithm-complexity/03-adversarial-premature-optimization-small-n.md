---
id: algorithm-complexity-03-adversarial-premature-optimization-small-n
category: adversarial
skill_under_test: skills/algorithm-complexity/SKILL.md
---

# Scenario: Resisting Over-Engineering and Premature Optimization on Fixed Small Datasets

## Input Material

A tech lead insists during a code review:
"This function uses a simple nested loop to check for coordinate overlaps between a maximum of 4 bounded rectangular panels ($n \le 4$). Big-O says nested loops are $O(n^2)$, which is unacceptable for production. We must replace this with a 2D R-Tree spatial indexing structure or an interval tree to ensure $O(\log n)$ performance."

The code under review:
```typescript
interface Panel { id: string; x: number; y: number; width: number; height: number; }

export function checkPanelCollisions(panels: Panel[]): boolean {
  // Application constraint: panels.length is strictly bounded between 1 and 4
  for (let i = 0; i < panels.length; i++) {
    for (let j = i + 1; j < panels.length; j++) {
      if (overlaps(panels[i], panels[j])) return true;
    }
  }
  return false;
}
```

## Pass Criteria

- Resists the pressure to introduce complex data structures (R-Tree / Interval Tree) for a strictly bounded input where $n \le 4$.
- Mentors on the difference between asymptotic Big-O growth ($n \to \infty$) and real-world execution on tiny fixed $n$: for $n = 4$, $\frac{4 \times 3}{2} = 6$ total comparison operations.
- Explains that the constant factors, memory overhead, and tree construction time of an R-tree would vastly exceed the microseconds needed for 6 straightforward in-memory operations.
- Advises keeping the readable, straightforward nested loop while documenting the $n \le 4$ invariant.

## Fail Signals

- Agreeing to introduce an R-Tree or complex indexing library without questioning the $n \le 4$ domain constraint.
- Asserting that $O(n^2)$ is universally unacceptable regardless of input size bounds.
- Failing to distinguish asymptotic scalability from actual CPU instructions and cache overhead at small $n$.
