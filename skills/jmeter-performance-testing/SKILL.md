---
name: jmeter-performance-testing
description: The general engineering workflow for load and performance testing with Apache JMeter — workflow-based test plan design, correlation and variable extraction, realistic data parameterization, multi-tier load profiles, and comprehensive metric reporting. Workflow guidance consumed by performance-review.
category: Testing
skillType: Authoring/Workflow
---

# JMeter Performance Testing

## Purpose

Produce the shared, reusable workflow guidance for designing, executing, and reporting load and performance tests using Apache JMeter (or compatible performance testing engines). This exists as an Authoring/Workflow Skill because performance testing is tightly coupled to performance evaluation (`performance-review`) — requiring workflow-based scenario design, correlation of dynamic session variables, realistic dataset parameterization, structured load profiling (ramp-up, sustained, stress), and tail-latency reporting (P90, P95, P99).

## Scope

**In scope:** workflow-based test plan architecture, dynamic request correlation (extracting tokens, session IDs, resource UUIDs), CSV data parameterization, load execution profiles (ramp-up, steady-state, peak, stress testing), database metric correlation, and full-spectrum performance metric reporting (Average, Median, P90, P95, P99, Throughput, Error Rate).

**Out of scope:** low-level application code profiling or database index tuning — which is `skills/performance-review/SKILL.md`'s concern; automated CI/CD pipeline infrastructure scripts. This Skill teaches the performance testing workflow.

## When to Use

Use when:
- Designing performance test plans for critical application user journeys.
- Preparing for high-concurrency launch events, marketing campaigns, or high-volume peak loads.
- Measuring latency, throughput, or error rates under concurrent user load.
- Validating system degradation or breaking points during stress testing.
- Reviewing performance test reports before claiming a system meets latency or throughput targets.

Do not use unmeasured estimates, extrapolations, or single-user desktop manual tests to report production performance capacity.

## Required Context

**Posture 2 — benefits from repository context but degrades gracefully without it** (`docs/Skill Standard.md` Section 3). Core principles (testing end-to-end user workflows, dynamic correlation, measuring tail latency P95/P99, testing sandbox integrations only) apply across web applications and API microservices.

## Workflow

1. **Design Workflow Scenarios:** Model multi-step end-to-end user journeys (e.g., Login $\rightarrow$ Search $\rightarrow$ Create Resource $\rightarrow$ Execute Transaction $\rightarrow$ Fetch Result) rather than hammering isolated endpoints.
2. **Implement Dynamic Correlation:** Extract dynamic tokens, session identifiers, transaction references, and resource UUIDs from preceding response payloads (using JSON Path or Regex Extractors) to feed into subsequent request steps.
3. **Parameterize Real Test Data:** Use CSV Data Set Configs or dynamic generators to supply varied user credentials, payloads, and parameters across concurrent threads, avoiding unrealistically cache-friendly duplicate replays.
4. **Configure Multi-Tier Load Profiles:** Structure test execution runs into distinct stages:
   - **Ramp-Up:** Gradually add virtual users to observe behavior as concurrency builds.
   - **Sustained Load:** Run steady-state concurrency long enough to detect memory leaks, connection pool exhaustion, or resource degradation.
   - **Peak / Stress Load:** Push beyond expected maximum capacity to identify system breaking points and failure modes (graceful `429`/`503` vs crashing).
5. **Measure Full Metric Spectrum:** Collect client-side response times (Average, Median, P90, P95, P99, Throughput/RPS, Error %) AND server-side metrics (CPU, Memory, DB Connection Pool, Slow Queries).
6. **Report Measured Results Only:** Publish documented performance metrics with exact environment specifications, test dates, and test plan versions.

## Rules

### Primary Focus on Full Workflows, Not Isolated Endpoints

Performance test plans must prioritize realistic multi-step user workflows over single-endpoint bombardment. Testing a single endpoint in isolation fails to reveal database locking, connection pool contention, session management overhead, or downstream service bottlenecks that only occur during real multi-step user journeys.

### Dynamic Correlation Across Workflow Steps

Test plans must dynamically extract identifiers generated in step $N$ (e.g. session tokens, resource UUIDs, transaction keys) and thread them into step $N+1$. Using hardcoded identifiers across virtual user threads creates artificial data collisions and invalidates test results.

### Varied Data Parameterization

Virtual user threads must be parameterized with varied, realistic input data (using CSV data sets or dynamic random generators). Replaying the exact same request payload thousands of times tests database query caches rather than real-world production performance.

### Complete Metric Set Reporting (Tail Latency Focus)

Never report performance results using average latency alone. A complete performance report must include:
- **Throughput:** Requests per second (RPS) and Transactions per second (TPS).
- **Latency Distribution:** Average, Median (P50), 90th percentile (P90), 95th percentile (P95), and 99th percentile (P99).
- **Error Rate:** Percentage of failed HTTP/TCP requests.
- **Server Metrics:** Server CPU utilization, memory consumption, DB connection pool utilization, and slow query counts.

Tail latency (P95/P99) is critical for identifying outlier delays caused by lock contention or garbage collection pauses that averages completely conceal.

### Empirical Measurement Required (No Guessing)

Never report or publish performance, latency, or throughput figures that were not produced by an actual, executed test run. Estimates, extrapolations, or "expected" numbers are unverified assumptions and must be explicitly labeled as TBD until verified by a test run.

### Sandbox Environment for External Integrations

Load tests involving external third-party service gateways (e.g. payment processors, SMS providers) must run strictly against dedicated sandbox/staging environments or mock adapters. Never execute load tests using production credentials or live financial transaction gateways.

## Constraints

- Never report performance metrics based on single-user manual tests or unverified estimations.
- Do not run high-volume load tests against live production third-party vendor APIs.
- Do not present average latency in isolation without P95/P99 tail-latency metrics.

## Governance Integration

This Skill provides workflow guidance for performance testing per `docs/Skill Taxonomy.md` Section 2.

- **Mentor Advisory:** Rules in this Skill represent strongly recommended Advisory-tier workflow standards for performance evaluation grounded in `context/standards/Performance Standards.md`.
- **Child Rules:** Projects may define target SLA thresholds (e.g. P95 < 200ms at 500 RPS) or staging environment endpoints in `.mentor/rules/`.

## Validation

This Skill is validated during design and review when:
- Test plans cover complete end-to-end user journeys with correlation.
- Test data uses CSV parameterization for varied input payloads.
- Test runs measure and report full metric spectra including P95/P99 latency.
- External integrations use sandbox/mock targets.

## Edge Cases

- **Connection Pool Exhaustion:** When sustained load tests show sudden latency spikes despite low CPU usage, check application database connection pool limits.
- **Garbage Collection Pauses:** Periodic latency spikes occurring at regular intervals across P99 metrics often indicate runtime garbage collection pauses under high memory allocation.

## Failure Handling

If performance test environment specifications or concurrency targets cannot be determined from available documentation, report Insufficient Evidence regarding system capacity.

## Expected Output

Documented performance test report providing metric tables (Avg, Median, P95, P99, Throughput, Error Rate) correlated with server resource utilization logs.

## Examples

### Positive Example: Full Workflow Test Plan with Correlation
```text
JMeter Thread Group (Ramp-up: 60s, Duration: 10m, Users: 200)
 ├── CSV Data Set Config (user_credentials.csv)
 ├── Step 1: POST /api/v1/auth/login -> Extract JWT token (JSON Path Extractor)
 ├── Step 2: GET /api/v1/catalog?category=electronics -> Extract product_uuid
 ├── Step 3: POST /api/v1/cart/items -> Use JWT + product_uuid
 ├── Step 4: POST /api/v1/orders/checkout -> Extract order_uuid
 └── Step 5: GET /api/v1/orders/${order_uuid} -> Verify completed status
```

### Negative Example: Single Endpoint Bombardment and Cherry-Picked Average
```text
// BAD: Hitting single GET endpoint with hardcoded ID, reporting only Average!
JMeter Thread Group: 1000 threads -> GET /api/v1/products/123
Report: "Average response time was 45ms. System is fast!"
// DEFECT: Ignores database cache hit effect, ignores P95/P99 tail latency (which was 3500ms!), ignores workflow state!
```

## Related Skills

- `skills/performance-review/SKILL.md` — Related: Evaluates code and database queries when JMeter tests identify bottlenecks.
- `skills/payment-integration/SKILL.md` — Related: Specifies sandbox integration rules for payment gateway testing.
- `skills/database-review/SKILL.md` — Related: Correlates DB metrics (connection pool, slow queries) during load runs.
