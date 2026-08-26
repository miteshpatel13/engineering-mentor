# Performance Standards

Performance must be measurable.

Workflow:
1. Define the target.
2. Measure current behavior.
3. Identify the bottleneck.
4. Optimize the bottleneck.
5. Measure again.
6. Verify correctness and regressions.

Consider:
- Database queries
- Indexes
- Network calls
- Serialization
- CPU
- Memory
- Connection pools
- Caching
- Payload size
- Concurrency
- Asynchronous processing

Never promise impossible targets such as zero-time responses.
