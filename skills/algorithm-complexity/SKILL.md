---
name: algorithm-complexity
description: Practical algorithm and performance mentoring to analyze, review, and optimize time and space complexity in production code. Guides Big-O derivation, loops, recursion, call stacks, auxiliary memory, and complexity trade-offs.
category: Core Engineering
skillType: Domain Pattern
---

# Algorithm Complexity

> **Resource paths:** Mentor file paths in this Skill (`context/…`, `docs/…`, `scripts/…`, `skills/…`, `tests/…`) are relative to the Engineering Mentor root, not the repository being worked on; `.mentor/…` paths refer to the target repository. In Claude Code the Mentor root is `${CLAUDE_PLUGIN_ROOT}` — read and run Mentor files from there.

## Purpose

Produce the shared, reusable engineering and mentoring pattern for analyzing, reviewing, and improving the algorithmic time and space complexity of real production code. This exists as its own Skill because reasoning about algorithmic scalability is a foundational software engineering discipline that `skills/code-review/SKILL.md` and `skills/performance-review/SKILL.md` consume when evaluating computational bottlenecks, nested iterations, data structure selections, and memory growth. Rather than superficially labeling code as "O(n)" or reflexively asserting "use O(1)", this Skill teaches developers how to methodically derive complexity from code structure, distinguish bounds and execution cases, evaluate auxiliary space, and make principled performance trade-offs.

## Scope

**In scope:**
- Time complexity classification and asymptotic growth analysis: O(1) constant, O(log n) logarithmic, O(n) linear, O(n log n) linearithmic, O(n²) quadratic, O(n³) cubic, O(2ⁿ) exponential, and O(n!) factorial.
- Complexity bounds and behavioral cases: best case, average case, worst case, amortized complexity, upper bounds (Big-O / $O$), tight bounds ($\Theta$), and lower bounds ($\Omega$) when relevant.
- Space complexity decomposition: distinguishing input space, auxiliary space (extra memory used by the algorithm during execution), and total space.
- Memory structures and overhead: call stack growth from recursion, iteration vs. recursion stack frames, temporary data structures (hash maps, arrays, buffers, sets), heap allocation, and time/space trade-offs.
- Big-O derivation rules: dropping constants, dropping lower-order terms, additive rules for sequential blocks, multiplicative rules for nested iterations, branch complexity, and accounting for hidden costs of language built-ins (e.g., slicing, array copying, string concatenation, indexOf).
- Mentoring and review discipline: explaining the mechanical "why" behind algorithmic scaling and guiding developers through step-by-step refactoring of high-complexity hotspots.
Secondary category: `Performance`.

**Out of scope:**
- Measuring live production wall-clock latency, I/O bottlenecks, or network execution times — that is `skills/performance-review/SKILL.md`'s concern.
- Relational database query execution plans, indexes, and SQL query tuning — that is `skills/database-review/SKILL.md`'s and `skills/database-indexing/SKILL.md`'s concern.
- Authoring Apache JMeter load and concurrency testing plans — that is `skills/jmeter-performance-testing/SKILL.md`'s concern.
This Skill provides algorithmic analysis and mentoring patterns; it produces no standalone review findings unless consumed by a Review-type Skill.

## When to Use

Use when:
- Reviewing code with loops, nested iterations, recursion, or heavy data-structure transformations to identify scalability bottlenecks.
- Analyzing the asymptotic time and space complexity of an existing algorithm, function, or pull request.
- Mentoring developers on why an implementation slows down non-linearly as dataset sizes grow.
- Evaluating memory overhead, recursion stack depth, or potential stack overflow / out-of-memory risks.
- Choosing the right algorithm or data structure (e.g., array vs. hash table vs. balanced tree vs. queue) for a specific production workload.
- Refactoring quadratic O(n²) or cubic O(n³) operations into linear O(n) or linearithmic O(n log n) alternatives.
- Calculating amortized cost for dynamic array resizing, hash table rehashing, or batching workflows.

Do not use when:
- The bottleneck is external I/O, database round-trips, or network latency rather than CPU/memory algorithmic complexity.
- Estimating execution times for tiny, fixed-size datasets ($n \le 10$) where constant factors and memory layout dominate asymptotic Big-O behavior.

## Required Context

**Posture 2 — benefits from repository context but degrades gracefully without it** (`docs/Skill Standard.md` Section 3). The mathematical principles of Big-O complexity analysis and algorithm design apply universally across programming languages and runtimes. When specific runtime context (such as language version, compiler/engine optimizations, recursion stack limits, or garbage collection mechanics) is available via `skills/context-discovery/SKILL.md`, recommendations adapt to language-specific standard library complexities, but core asymptotic analysis remains valid in the abstract.

## Workflow

1. **Identify the Input Variables:** Define what $n$, $m$, $k$, etc. represent in the algorithm (e.g., array length, string length, graph vertices/edges, tree depth). Never assume a single $n$ when multiple independent inputs are processed.
2. **Deconstruct Code Structure:** Trace control flow — sequential execution blocks, single loops, nested loops, conditional branches, and recursive invocations.
3. **Account for Hidden Built-In Costs:** Inspect standard library and language built-in operations inside loops (e.g., `Array.prototype.indexOf`, `includes`, `slice`, `splice`, string concatenations, set lookups) to ensure internal operations are not mistakenly assumed to be O(1).
4. **Derive Asymptotic Time Complexity:**
   - **Sequential blocks (Additive Rule):** Sum the costs of successive steps ($T(n) = T_1(n) + T_2(n)$).
   - **Nested loops (Multiplicative Rule):** Multiply outer loop iterations by inner loop work ($T(n) = \text{outer iterations} \times \text{inner work}$).
   - **Recursive calls:** Solve recurrence relations via recursion tree expansion, step counting, or the Master Theorem.
   - **Simplify:** Drop constant multipliers ($O(3n) \to O(n)$) and drop lower-order terms ($O(n^2 + 5n + 10) \to O(n^2)$).
5. **Analyze Best, Average, Worst, and Amortized Cases:** Evaluate input variations (e.g., already sorted vs. reverse sorted inputs, hash collision frequency, dynamic array capacity doubling).
6. **Decompose Space Complexity:**
   - Measure **Input Space** (size of parameters passed into the function).
   - Measure **Auxiliary Space** (additional memory allocated during execution: local variables, temporary collections, call stack frames).
   - Calculate **Total Space** ($\text{Input Space} + \text{Auxiliary Space}$).
   - Inspect maximum call stack depth for recursive functions to assess stack-overflow risk.
7. **Formulate Mentoring and Trade-Off Guidance:** Explain the mechanical cause of the bottleneck, demonstrate the production impact as $n$ scales, and guide the developer through refactoring options with explicit time-vs-space trade-offs.

## Rules

### Big-O Derivation Rules

To derive Big-O complexity from code, apply these fundamental rules systematically:

1. **Drop Constants:** Big-O measures growth rate as $n \to \infty$. Constant factors do not alter the growth category.
   - $O(2n) \to O(n)$
   - $O(100) \to O(1)$
   - $O(0.5 n^2) \to O(n^2)$

2. **Drop Lower-Order Terms:** Only the term with the fastest growth rate matters as $n$ approaches infinity.
   - $O(n^2 + 3n + 100) \to O(n^2)$
   - $O(n \log n + n) \to O(n \log n)$
   - $O(2^n + n^3) \to O(2^n)$

3. **Additive Rule (Sequential Operations):** When operations execute sequentially, sum their complexities:
   ```typescript
   // Step 1: O(n)
   for (const item of items) {
     doConstantWork(item);
   }

   // Step 2: O(m)
   for (const record of records) {
     doConstantWork(record);
   }
   // Total Time: O(n + m). If n === m, O(2n) -> O(n).
   ```

4. **Multiplicative Rule (Nested Operations):** When operations nest, multiply the outer loop iterations by the inner work:
   ```typescript
   // Outer loop runs n times: O(n)
   for (const item of items) {
     // Inner loop runs m times: O(m)
     for (const other of others) {
       doConstantWork(item, other); // O(1)
     }
   }
   // Total Time: O(n * m). If items and others both have size n, O(n^2).
   ```

5. **Loop with Halving / Doubling Iterations (Logarithmic Rule):** When the loop variable multiplies or divides by a constant factor on each step, the loop executes in $O(\log n)$ iterations:
   ```typescript
   let i = 1;
   while (i < n) {
     i = i * 2; // O(log n)
   }
   ```

6. **Branching / Conditional Rule:** A conditional branch executes one path. Analyze the worst-case branch unless reasoning about average or amortized execution:
   ```typescript
   if (condition) {
     // O(n) branch
   } else {
     // O(1) branch
   }
   // Worst-Case Time: O(n)
   ```

### Time Complexity Classes and Behavior

Always distinguish the standard complexity classes and understand their practical scaling behavior:

- **O(1) — Constant Time:** Runtime does not depend on the input size $n$.
  - *Examples:* Hash map key lookup (without collisions), array index lookup (`arr[i]`), pushing to a stack, basic arithmetic operations.
- **O(log n) — Logarithmic Time:** Each step reduces the remaining problem size by a fractional factor (typically half).
  - *Examples:* Binary search in a sorted array, balanced binary search tree operations (AVL, Red-Black), finding an element in a binary heap.
- **O(n) — Linear Time:** Runtime grows in direct linear proportion to input size $n$.
  - *Examples:* Iterating through an array, linear search, finding minimum/maximum in an unsorted array, copying an array.
- **O(n log n) — Linearithmic Time:** Occurs when dividing a problem into logarithmic subproblems and performing linear work to combine them.
  - *Examples:* Efficient comparison sorts (Merge Sort, Heap Sort, Quick Sort average case).
- **O(n²) — Quadratic Time:** Work grows with the square of input size. Routinely caused by nested loops over the same collection.
  - *Examples:* Bubble sort, selection sort, insertion sort worst case, brute-force pair comparisons, nested loops.
- **O(n³) — Cubic Time:** Work grows with the cube of input size. Often caused by three nested loops.
  - *Examples:* Naive matrix multiplication, checking all triplets in an array.
- **O(2ⁿ) — Exponential Time:** Runtime doubles with each additional element in the input. Impractical for production workloads beyond very small $n$ ($n > 25$).
  - *Examples:* Recursive calculation of Fibonacci numbers without memoization, generating all subsets (power set) of a set.
- **O(n!) — Factorial Time:** Runtime multiplies by $n$ at each step. Completely intractable for $n > 12$.
  - *Examples:* Generating all permutations of a string or array, brute-force Traveling Salesperson Problem.

### Complexity Bounds and Cases

When describing algorithmic performance, do not use "O" loosely to mean "takes this long". Use precise terminology:

1. **Upper Bound (Big-O / $O$):** Mathematical ceiling on growth rate. Represents the worst possible growth rate as $n \to \infty$.
2. **Tight Bound (Big-Theta / $\Theta$):** Both an upper and lower bound. Describes the exact asymptotic growth rate when upper and lower bounds coincide.
3. **Lower Bound (Big-Omega / $\Omega$):** Mathematical floor on growth rate. Represents the minimum work an algorithm must perform.

Distinguish the four execution cases:
- **Best Case:** Input configuration requiring the least work (e.g., target element is at index 0 in linear search: $\Omega(1)$).
- **Average Case:** Expected runtime over all possible valid inputs of size $n$, assuming a probability distribution (e.g., QuickSort average case: $\Theta(n \log n)$).
- **Worst Case:** Input configuration maximizing work (e.g., QuickSort on already sorted array with naive pivot: $O(n^2)$).
- **Amortized Complexity:** Average cost per operation across a sequence of operations, guaranteeing that occasional expensive steps are paid for by frequent cheap steps.
  - *Dynamic Array Appends:* Appending is $O(1)$ most of the time. When capacity is exceeded, an array of size $2n$ is allocated and elements copied ($O(n)$ step). Over $n$ appends, total copy work is $O(n)$, giving an amortized cost of $O(1)$ per append.
  - *Hash Table Insertions:* Average amortized $O(1)$, but can spike to $O(n)$ during rehashing/resizing or pathological key hash collisions.

### Space Complexity: Input vs. Auxiliary vs. Total Space

Always separate the components of memory consumption:

1. **Input Space:** Memory required to store the input data given to the function. For an array of size $n$, input space is $O(n)$.
2. **Auxiliary Space:** Extra or temporary memory allocated by the algorithm *excluding* the input data.
   - In-place algorithms (e.g., standard quicksort partitioning, in-place array reversal) use $O(1)$ auxiliary space.
   - Algorithms that allocate a new array or hash map of size $n$ use $O(n)$ auxiliary space.
3. **Total Space:** Sum of Input Space and Auxiliary Space ($\text{Total} = \text{Input} + \text{Auxiliary}$).

When evaluating an algorithm's memory footprint:
- **O(1) Auxiliary Space:** Modifies data in-place or uses only a few primitive tracking variables.
- **O(log n) Auxiliary Space:** Typically the call stack depth of balanced divide-and-conquer recursion (e.g., Merge Sort call stack without counting array copies, or balanced BST recursion).
- **O(n) Auxiliary Space:** Allocating temporary arrays, HashMaps, Sets, or unbalanced recursion call stacks.

### Call Stack and Recursion Memory

Every function call in a recursive algorithm allocates a new stack frame on the call stack containing parameters, return addresses, and local variables.
- Recursive depth $d$ consumes $O(d)$ auxiliary stack space.
- A recursive Fibonacci implementation without memoization has depth $O(n)$, consuming $O(n)$ stack space despite $O(2^n)$ time complexity.
- A balanced divide-and-conquer algorithm (e.g., binary search) has depth $O(\log n)$, consuming $O(\log n)$ stack space.
- Recursive linear iteration over an array of size $n$ risks a `RangeError: Maximum call stack size exceeded` in runtimes (e.g., Node.js / V8) whose default call stack limit is around 10,000 frames. Refactor to iterative loops when stack depth can exceed safe limits.

### Hidden Complexity in Language Built-Ins

A frequent source of accidental quadratic complexity in production code is calling linear-time built-in library functions inside a loop:

- **Array Search Methods:** `arr.includes()`, `arr.indexOf()`, `arr.find()`, `arr.findIndex()` are $O(n)$ linear searches. Calling them inside a `for` loop or `arr.filter()` turns an $O(n)$ loop into an $O(n^2)$ quadratic bottleneck.
- **Array Mutation Methods:** `arr.shift()`, `arr.unshift()`, and `arr.splice()` re-index elements and take $O(n)$ time. Calling `arr.shift()` inside a loop of size $n$ results in $O(n^2)$ time.
- **Array Slicing and Spreading:** `arr.slice()` and `[...arr]` allocate a new array and copy $k$ elements, taking $O(k)$ time and $O(k)$ auxiliary space.
- **String Concatenation in Loops:** In languages with immutable strings (e.g., Java, JavaScript, Python), `str += char` inside an $n$-iteration loop creates a new string copy on each iteration, causing $O(n^2)$ time and $O(n^2)$ total memory allocations. Use string builders or array joins instead.

### Memory vs. Time Trade-offs

Engineering mentoring must guide practical trade-offs rather than dogmatic optimizations:

- **Trading Space for Time (Caching / Indexing):** Using an $O(n)$ auxiliary hash map (lookup index) to reduce lookup time from an $O(n^2)$ nested loop down to $O(n)$ linear time. This is almost always the right trade-off in web request handlers when memory is modest ($n < 100,000$).
- **Trading Time for Space (Streaming / Multi-pass):** Using an $O(1)$ auxiliary space streaming pipeline when processing massive datasets (e.g., 100M rows) to avoid Out-Of-Memory (OOM) errors, accepting slightly higher processing time or multiple passes.

### Mentoring Discipline: Teach Why, Don't Just State Big-O

When providing complexity feedback during reviews or pairing:
1. **Never make unsupported assertions:** Do not write "Change this to O(1)" without explaining *how* and *why*.
2. **Translate to production impact:** Show the developer what the complexity curve means with real numbers:
   - For $n = 1,000$: $O(n)$ is $1,000$ operations; $O(n^2)$ is $1,000,000$ operations.
   - For $n = 50,000$: $O(n)$ completes in milliseconds; $O(n^2)$ takes 2.5 billion operations, pegging the CPU and causing request timeouts.
3. **Provide actionable refactoring steps:** Provide the before-and-after code, highlight the data structure change, and compare time and space complexities explicitly.

## Constraints

- Never guess the complexity of standard library functions without verifying runtime mechanics for the target language.
- Never conflate Input Space with Auxiliary Space when reporting space complexity.
- Never demand complex data structure optimizations for small, bounded collections ($n \le 10$) where constant factors, cache locality, and allocation overhead make simple arrays faster in practice.
- Never propose an algorithmic optimization that sacrifices correctness, type safety, or data integrity for negligible gains.

## Governance Integration

This Skill supplies reference material (Domain Pattern) consumed by Review-type Skills (`skills/code-review/SKILL.md`, `skills/performance-review/SKILL.md`) per `docs/Skill Taxonomy.md` Section 2.

- **Mentor Advisory:** Guidance in this Skill represents fundamental algorithmic engineering standards grounded in `context/standards/Performance Standards.md` and `context/standards/Engineering Standards.md`.
- **Child Rules:** Child repositories may declare algorithmic limits (e.g., prohibiting unbounded in-memory array filtering on request threads or setting maximum recursion limits) in `.mentor/rules/`. Compatible child rules enforce stricter repository boundaries without altering asymptotic complexity definitions.

## Validation

This Skill produces no standalone review artifact directly. Its patterns are verified when:
- Complexities derived from code accurately reflect mathematical loop bounds, recursive branching, and built-in library costs.
- Distinctions between best, worst, average, and amortized cases are clearly articulated with supporting rationale.
- Auxiliary space is cleanly separated from input space.
- Concrete refactoring suggestions demonstrate reduced asymptotic complexity or an explicit, justified trade-off.

## Edge Cases

- **Variable-Bound Inner Loops:** An inner loop whose limit depends on the outer loop index $i$ (e.g., `for (let j = i + 1; j < n; j++)`): $\sum_{i=1}^{n-1} (n - i) = \frac{n(n-1)}{2} = \frac{n^2 - n}{2} \to O(n^2)$, not $O(n)$.
- **Distinct Input Dimensions ($n$ and $m$):** Processing an array of size $n$ against another of size $m$ is $O(n \cdot m)$ or $O(n + m)$, not $O(n^2)$ or $O(n)$, unless $n \approx m$ is proven.
- **Amortized Constant vs. Worst-Case Latency Spikes:** In low-latency or real-time systems, an $O(1)$ amortized operation (like hash table insertion or dynamic array resizing) can produce an occasional $O(n)$ latency spike that violates strict tail-latency SLAs.
- **Tail Call Optimization (TCO) Limitations:** While some language specifications define tail call optimization to convert tail recursion into $O(1)$ stack space, most modern production runtimes (including JavaScript V8 and Python) do not support TCO. Always assume recursion consumes $O(d)$ stack space unless verified otherwise.
- **Cache Locality and Constant Factors:** Contiguous memory traversal (e.g., flat arrays) benefits from CPU cache lines and branch prediction, frequently outperforming pointer-heavy $O(1)$ or $O(\log n)$ structures (like linked lists or node-based trees) for moderate $n$.

## Failure Handling

When code structure is too dynamic, relies on external state, or depends on inputs that cannot be mathematically bounded (e.g., while-loops terminating on non-deterministic network I/O, external interrupts, or user interaction), state that algorithmic complexity is **indeterminate from code alone**, per the Mentor Operating Model No Invention Rule. Explicitly name the missing loop termination invariants or missing runtime constraints required to complete analysis.

## Expected Output

Reference material and mentoring structure. Consuming Review Skills (`skills/code-review/SKILL.md`, `skills/performance-review/SKILL.md`) format review findings using `context/templates/Review Template.md`. Mentoring outputs provide:

1. **Current Complexity Breakdown:** Time complexity (Best, Average, Worst, Amortized) and Space complexity (Input, Auxiliary, Total).
2. **Derivation Walkthrough:** Step-by-step breakdown explaining outer loops, inner operations, and hidden built-in costs.
3. **Production Scaling Impact:** Explanation of how execution time and memory scale as $n$ grows.
4. **Refactoring Recommendation:** Step-by-step code transformation with a comparative Before-vs-After complexity table.

## Examples

### Positive Example: Refactoring Quadratic Nested Lookup to Linear Time

#### Initial Code:
```typescript
interface User { id: string; name: string; }
interface Order { id: string; userId: string; amount: number; }

export function attachUserNames(orders: Order[], users: User[]): (Order & { userName: string })[] {
  // orders has length n, users has length m
  return orders.map(order => {
    // Array.prototype.find performs a linear search over users: O(m)
    const user = users.find(u => u.id === order.userId);
    return {
      ...order,
      userName: user ? user.name : 'Unknown',
    };
  });
}
```

#### Mentoring & Complexity Breakdown:
- **Input Dimensions:** $n = \text{orders.length}$, $m = \text{users.length}$.
- **Initial Time Complexity:** $O(n \times m)$. The outer `.map()` runs $n$ times. Inside each iteration, `.find()` scans up to $m$ users. If $n = 10,000$ and $m = 10,000$, this performs up to $100,000,000$ comparisons.
- **Initial Auxiliary Space:** $O(1)$ auxiliary space (excluding the returned array of size $n$).
- **Bottleneck:** Repeated linear scan for each order.
- **Optimization Strategy:** Trade $O(m)$ auxiliary space to build a lookup `Map` in one pass, turning each lookup from $O(m)$ into $O(1)$.

#### Refactored Code:
```typescript
export function attachUserNames(orders: Order[], users: User[]): (Order & { userName: string })[] {
  // Precompute user lookup map: O(m) time, O(m) auxiliary space
  const userMap = new Map<string, string>();
  for (const user of users) {
    userMap.set(user.id, user.name);
  }

  // Map orders in single linear pass: O(n) time
  return orders.map(order => ({
    ...order,
    userName: userMap.get(order.userId) ?? 'Unknown', // O(1) map lookup
  }));
}
```

#### Comparative Complexity Table:
| Metric | Before | After | Trade-off / Rationale |
|---|---|---|---|
| **Time Complexity** | $O(n \times m)$ | $O(n + m)$ | Replaced nested scan with sequential preprocessing + $O(1)$ lookups. |
| **Auxiliary Space** | $O(1)$ | $O(m)$ | Allocated a `Map` storing $m$ user IDs and names. |
| **Production Impact** | ~100M operations for $n=m=10k$ | ~20k operations for $n=m=10k$ | Prevents CPU saturation and event-loop blocking. |

### Negative Example: Superficial Complexity Analysis with Hidden Built-in Costs

#### Flawed Reviewer Statement:
> "This function only has one `for` loop, so its time complexity is $O(n)$ and it is already optimal."

```typescript
function deduplicateItems(items: string[]): string[] {
  const result: string[] = [];
  for (const item of items) {
    if (!result.includes(item)) { // HIDDEN O(k) LINEAR SCAN
      result.push(item);
    }
  }
  return result;
}
```

#### Correct Mentoring Analysis:
The analysis is incorrect because it ignores the hidden complexity of `result.includes(item)`. On iteration $i$, `result` has up to $i$ elements. `includes()` performs an $O(i)$ linear scan. The total time is $\sum_{i=0}^{n-1} i = \frac{n(n-1)}{2} = O(n^2)$.
The correct refactoring uses a `Set`:
```typescript
function deduplicateItems(items: string[]): string[] {
  return Array.from(new Set(items)); // O(n) time, O(n) auxiliary space
}
```

## Related Skills

- `skills/code-review/SKILL.md` — Related: Consumes this Skill to detect and remediate quadratic or exponential bottlenecks in pull requests and code changes.
- `skills/performance-review/SKILL.md` — Related: Consumes this Skill when diagnosing algorithmic CPU/memory bottlenecks identified in profiling evidence.
- `skills/database-indexing/SKILL.md` — Related: Covers B-Tree $O(\log n)$ and Hash $O(1)$ search complexity patterns at the database storage and index layer.
