---
id: algorithm-complexity-02-edge-hidden-builtin-complexity
category: edge
skill_under_test: skills/algorithm-complexity/SKILL.md
---

# Scenario: Unmasking Hidden Linear Costs in Standard Library Built-Ins

## Input Material

A pull request introduces a deduplication function for tags:

```typescript
export function uniqueTags(rawTags: string[]): string[] {
  const seen: string[] = [];
  for (const tag of rawTags) {
    if (!seen.includes(tag)) {
      seen.push(tag);
    }
  }
  return seen;
}
```

The author's PR description states: "Simple single loop over `rawTags`, $O(n)$ time complexity, minimal memory overhead."

## Pass Criteria

- Challenges the PR author's claim that time complexity is $O(n)$.
- Explains the hidden built-in cost: `seen.includes(tag)` is an $O(k)$ linear search over the `seen` array on each iteration, where $k$ grows up to $n$.
- Derives the true worst-case time complexity: $\sum_{k=1}^n k = \frac{n(n+1)}{2} = O(n^2)$.
- Explains why `Set.prototype.has` or `new Set(rawTags)` provides $O(1)$ average lookup time instead of $O(n)$, reducing the overall time complexity to $O(n)$.
- Notes that space complexity is $O(n)$ auxiliary space in both implementations, but the `Set` implementation provides the intended linear execution time.

## Fail Signals

- Accepting the PR author's assertion that the single loop implies $O(n)$ time complexity.
- Failing to explain that `includes()` on an array is a linear-time search operation.
- Recommending sorting without analyzing the resulting $O(n \log n)$ time cost compared to an $O(n)$ Set-based solution.
