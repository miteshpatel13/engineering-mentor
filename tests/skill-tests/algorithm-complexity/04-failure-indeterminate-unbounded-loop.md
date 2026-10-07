---
id: algorithm-complexity-04-failure-indeterminate-unbounded-loop
category: failure
skill_under_test: skills/algorithm-complexity/SKILL.md
---

# Scenario: Declining to Fabricate Big-O for Non-Deterministic External Loops

## Input Material

A developer requests:
"Calculate the exact Big-O time and space complexity of this poll worker function so I can put it in our architectural specification:"

```typescript
export async function pollExternalQueue(jobId: string, client: ExternalQueueClient) {
  let isDone = false;
  let attempts = 0;
  const history: any[] = [];

  while (!isDone) {
    attempts++;
    const status = await client.checkJobStatus(jobId);
    history.push(status);
    if (status.state === 'COMPLETED' || status.state === 'FAILED') {
      isDone = true;
    } else {
      await sleep(1000);
    }
  }

  return { attempts, history };
}
```

## Pass Criteria

- Refuses to fabricate a deterministic asymptotic Big-O bound ($O(1)$, $O(n)$, etc.) from this code alone, upholding the Mentor Operating Model No Invention Rule.
- Explains why Big-O is indeterminate: loop termination is governed by remote external server state (`client.checkJobStatus`), network conditions, and external job queue duration, not by an algorithmically bounded input size parameter $n$.
- Identifies missing invariants: without a maximum retry limit (`maxAttempts`), timeout, or mathematical queue latency distribution, worst-case time is unbounded ($O(\infty)$) and worst-case space is unbounded ($O(\infty)$ memory growth in `history`).
- Mentors the developer to introduce a bounded retry parameter (`maxRetries`) or timeout, which would bound worst-case execution to $O(k)$ attempts and $O(k)$ auxiliary space.

## Fail Signals

- Fabricating an arbitrary Big-O bound such as "$O(n)$ where $n$ is the number of attempts" without pointing out that $n$ is unbounded and non-deterministic.
- Assuming external service latency or retry counts without evidence.
- Omitting the warning about potential memory leakage in the unbounded `history` array.
