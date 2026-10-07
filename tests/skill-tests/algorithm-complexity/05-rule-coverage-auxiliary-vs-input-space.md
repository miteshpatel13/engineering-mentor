---
id: algorithm-complexity-05-rule-coverage-auxiliary-vs-input-space
category: rule-coverage
skill_under_test: skills/algorithm-complexity/SKILL.md
---

# Scenario: Disentangling Input Space, Auxiliary Space, and Call Stack Growth

## Input Material

A junior engineer asks for feedback on a recursive binary search tree depth calculation:

```typescript
interface TreeNode {
  val: number;
  left: TreeNode | null;
  right: TreeNode | null;
}

export function maxDepth(root: TreeNode | null): number {
  if (root === null) return 0;
  const leftDepth = maxDepth(root.left);
  const rightDepth = maxDepth(root.right);
  return Math.max(leftDepth, rightDepth) + 1;
}
```

The engineer states:
"Since we don't allocate any arrays or objects, the space complexity is $O(1)$."

## Pass Criteria

- Corrects the engineer's assertion that space complexity is $O(1)$.
- Strictly distinguishes **Input Space**, **Auxiliary Space**, and **Total Space**:
  - Input Space: $O(n)$ where $n$ is the number of nodes stored in the tree passed into the function.
  - Auxiliary Space: Determined by the call stack frames allocated during recursion.
- Explains recursive call stack mechanics: each recursive call creates a new stack frame holding parameters (`root`), local variables (`leftDepth`, `rightDepth`), and return addresses.
- Details the best, average, and worst-case auxiliary space:
  - Best / Average Case (balanced tree): Stack depth is $O(\log n)$, so auxiliary space is $O(\log n)$.
  - Worst Case (degenerate/skewed linked-list tree): Stack depth is $O(n)$, so auxiliary space is $O(n)$.
- Mentors on the risk of call stack exhaustion (`Maximum call stack size exceeded`) if the tree is unbalanced and $n > 10,000$, and mentions iterative traversal (e.g. using an explicit queue for BFS or loop with stack) as a production alternative.

## Fail Signals

- Agreeing that auxiliary space is $O(1)$ because no heap structures are instantiated.
- Conflating Input Space with Auxiliary Space.
- Failing to distinguish between balanced tree $O(\log n)$ and skewed tree $O(n)$ call stack depth.
