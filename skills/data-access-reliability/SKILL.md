---
name: data-access-reliability
description: The general engineering pattern for using a shared database safely under concurrency — connection acquisition and release, transaction boundaries, hold-and-wait pool self-deadlock, connection-pool budgeting across instances, lock contention from derived-data recomputation, safe deadlock retry, and once-per-period execution of scheduled jobs and migrations across instances. Use when writing or reviewing code that checks out a connection or opens a transaction, fans out database work, calls an external service from inside data-access code, sizes a connection pool, adds a scheduled job, or when diagnosing platform-wide stalls, "too many connections", connection-reuse errors, or deadlocks. Reference material consumed by database-review, performance-review, and code-review.
category: Database
skillType: Domain Pattern
---

# Data-Access Reliability

> **Resource paths:** Mentor file paths in this Skill (`context/…`, `docs/…`, `scripts/…`, `skills/…`, `tests/…`) are relative to the Engineering Mentor root, not the repository being worked on; `.mentor/…` paths refer to the target repository. In Claude Code the Mentor root is `${CLAUDE_PLUGIN_ROOT}` — read and run Mentor files from there.

## Purpose

Supply the reusable pattern for keeping a shared database available and consistent when many requests, jobs, and application instances use it at once. It exists as its own Skill because these failures are not query-cost problems — they come from how connections and transactions are *held*, and they surface far from their cause: one leaked or double-released connection, or one job holding a connection while waiting for another, can stall every unrelated endpoint on every instance. `database-review` evaluates schema, queries, and migrations; `performance-review` evaluates measured bottlenecks; neither owns "how long, how many, and on whose behalf a connection is held." This Skill is that reference, following `docs/Skill Taxonomy.md` Section 2's composition model.

## Scope

**In scope:** connection acquisition and release (manual checkout, query runners, pooled clients); transaction boundaries and what must happen on every exit path; work performed while a connection or transaction is held (network calls, queue waits, fan-out); hold-and-wait pool self-deadlock; connection-pool sizing against the database's connection budget across all instances and deploy surges; fail-fast behavior when the pool is saturated; lock contention caused by concurrent writers to the same aggregate and by per-row derived-data recomputation (triggers, synchronous summary rebuilds); deadlock retry and its precondition of atomicity; once-per-period execution of scheduled jobs and schema migrations when several instances run the same code; static and runtime enforcement of release discipline; and the diagnostic signatures that point at these causes.

**Out of scope:** query plans, indexes, schema design, and migration safety of the DDL itself — `skills/database-review/SKILL.md`; general latency measurement and optimization method — `skills/performance-review/SKILL.md`; the duplicate-request pattern for a single operation — `skills/idempotency/SKILL.md` (this Skill's retry rule depends on it but does not restate it); timeouts, retries, and circuit breaking for the external service itself — `skills/third-party-integration/SKILL.md` (this Skill only forbids making that call while holding a database resource); infrastructure provisioning (instance class, proxies, replicas) — explicitly nowhere in the Mentor; that is an operational decision for the child repository's owners.

## When to Use

Use when: code checks out a connection, creates a query runner, or opens a transaction manually; code starts many database operations concurrently (loops of un-awaited calls, `Promise.all`/gather over a large or unbounded set); data-access code calls an external HTTP API, publishes to a queue, or waits on user input; a connection pool is being sized or a second pool/data source is being introduced; a scheduled job, cron, or migration runner is added to an application that runs on more than one instance; a table gains triggers or a write path synchronously recomputes an aggregate; a retry-on-deadlock is proposed; or production shows clustered stalls across unrelated endpoints, "too many connections", errors about a connection being closed or already released, lock-wait timeouts, or deadlocks.

Do not use for a single short query through an ORM or client that borrows and returns the connection itself, with no manual checkout, no transaction, and no concurrency concern — there is nothing to hold, so applying this pattern adds ceremony without benefit.

## Required Context

**Posture 2 — benefits from repository context but degrades gracefully without it** (`docs/Skill Standard.md` Section 3). The pattern is correct in the abstract. With repository context — the database engine and its connection limit, the driver/ORM and how it acquires and releases connections, how many instances run (including during deploys), whether scheduled jobs run in-process — the guidance becomes concrete (exact pool numbers, exact release API). This Skill does not invoke `skills/context-discovery/SKILL.md` itself; a consuming Review-type Skill has already done so. When a number the rule depends on is unknown (instance count, the database's connection limit), say it is unknown and state the rule as a formula rather than inventing the number.

## Workflow

Reference material, not a standalone process (`docs/Skill Taxonomy.md` Section 2). Whoever applies it — an author, or a Review-type Skill checking for it — works through these decisions:

1. **Locate every acquisition.** Find each place a connection is checked out or a transaction opened manually, and each place the framework does it implicitly for a unit of work.
2. **Trace every exit path** from each acquisition — success, each early return, each thrown error — and confirm the connection is released exactly once and any open transaction is ended (Rules → Connection Lifecycle, Transaction Boundaries).
3. **List what happens while it is held.** Any network call, queue wait, user wait, or need for a *second* connection is a finding (Rules → Hold-and-Wait).
4. **Count concurrency.** For fan-out code, determine the maximum number of simultaneous connections it can demand and compare with the pool (Rules → Bounded Concurrency).
5. **Check the budget.** Pools per process × processes per instance × peak instances (including deploy surge) against the database's usable connection limit (Rules → Pool Budget).
6. **Check contention.** Identify writers that converge on the same rows or aggregate, and per-row derived-data recomputation inside write transactions (Rules → Lock Contention and Derived Data).
7. **Check multi-instance execution** of scheduled jobs and migrations (Rules → Once-Per-Period Execution).
8. **Confirm enforcement and visibility** — a static check for release placement, pool metrics, and failures that reach alerting (Rules → Enforcement, Observability).

## Rules

All Rules below are **Mentor Advisory** unless marked otherwise. The two marked Mandatory instantiate existing floors in `context/standards/Database Standards.md` ("Use transactions when atomicity is required", "Consider race conditions and locking") and its connection-lifecycle bullets.

### Connection Lifecycle (Mentor Mandatory — Database Standards)

Borrow a connection as late as possible and release it on **every** path, **exactly once** — in the language's guaranteed-cleanup construct (`finally`, `defer`, a context manager, a `using` block), never only on the success path. Two failure modes are equally serious:
- **Never released** (a leak): each call permanently consumes one pool slot until the database's idle timeout kills it — often hours. A handful of such calls under load exhausts the pool.
- **Released twice** (release after commit *and* again in cleanup): many drivers do not guard against a duplicate release, so one physical connection is handed to two callers at once. One request's statements can then run inside another request's transaction and be committed or rolled back with it — silent data corruption — and it often surfaces only later, when an idle-reaping pool setting turns the silent sharing into visible "connection closed" errors.

Prefer the framework's managed unit of work (a `transaction(callback)` helper, an ORM repository call) over manual checkout: it makes both mistakes structurally impossible. Do not acquire a connection that is never used — it occupies a slot for the whole request.

### Transaction Boundaries (Mentor Mandatory — Database Standards)

Inside an open transaction:
- Every early exit (validation failure, "not found", business-rule rejection) **rolls back** before returning. Releasing a connection with a transaction still open either returns the open transaction to the pool for the next caller or leaves locks held.
- Every write belonging to the unit goes through the **transaction's own handle**. A write issued through a different repository/connection in the middle of the unit runs outside the transaction and is not atomic with it — a common ORM mistake because both handles look identical in code.
- Validate everything you can **before the first write**, so a rejection never leaves partial rows behind.
- Session-scoped state set on a pooled connection (session variables, settings, temporary tables, advisory locks) is reset **on the same connection** in cleanup — otherwise it silently leaks into whichever request receives that connection next. Such state also pins a connection when a connection proxy sits in front of the database; prefer designs that don't need it.

### Hold-and-Wait: Never Hold While Waiting

Never hold a connection or an open transaction while waiting on something slower or unbounded: an external HTTP call, a message-broker publish that can block, a lock in another system, user input, or a **second connection from the same pool**. The last case is a classic pool self-deadlock: when N concurrent tasks each hold one connection and need another, and N ≥ pool size, every connection is held by a task waiting for a connection that will never free. Every other request on that instance then queues behind them until a timeout breaks the cycle — observed as minutes-long stalls across unrelated endpoints, simultaneously on every instance that runs the same job. Restructure as: read what you need → release → do the slow work → reacquire to write; or perform the external call before opening the transaction and record its result after.

### Bounded Concurrency

Never start an unbounded number of database-touching tasks at once (an un-awaited loop over users × tenants, a gather over every row of a result set). Bound it explicitly (a semaphore, a concurrency-limited pool, fixed-size batches) to a number comfortably below the pool size, and remember each parallel query inside a single request also takes its own connection. A fire-and-forget call whose result nobody awaits also loses its errors — attach error handling or await it.

### Pool Budget and Fail-Fast

The database's usable connection limit (its maximum minus a reserve for administration and migrations) must cover **pools per process × processes per instance × peak instance count, including the temporary surge during a rolling deploy and autoscaling**. Keep the steady-state total at or below roughly 80% of usable. Two independent pools in one process (e.g. a framework-managed data source plus a legacy one) silently double the demand — use one pool per process and assert it at startup. Make the pool size configuration-driven and validated, not a constant. Give the pool's wait queue a bound and a short wait, so a saturated pool fails fast with a retryable "busy" response instead of letting requests hang for minutes; expose pool total/free/waiting as metrics so the budget can be checked against reality. When the instance count cannot fit the budget, the fix is operational (a connection proxy, a larger database) — say so rather than shrinking pools until requests starve.

### Lock Contention and Derived Data

Concurrent writers converging on the same rows or the same aggregate row deadlock under the default isolation of most relational databases — especially when each write also recomputes a company- or tenant-wide summary inside the same transaction (per-row triggers calling a recompute procedure, or application code rebuilding totals synchronously). A bulk write of N rows then recomputes the whole aggregate N times while holding locks. Prefer: (1) serialize writers per aggregate (one tenant's documents posted sequentially; parallelism across tenants); (2) move recomputation out of the write path — mark the aggregate dirty on write and recompute once, asynchronously and debounced, under a single-execution guard; shadow-compare old and new results before removing the synchronous path. Keep the deliberate row locks that protect read-modify-write sequences (stock decrements, sequence/number generation) — contention is not a reason to remove correctness locks.

### Deadlock Retry Requires Atomicity

Retry a unit of work on the database's deadlock and lock-wait-timeout errors only when the **whole unit is one transaction** — otherwise each retry repeats the writes that already committed and creates duplicates (`skills/idempotency/SKILL.md` governs making the unit safe to repeat). Retry the entire transaction, not the failed statement; bound the attempts (e.g. 3) with jittered backoff; and treat a retry loop as a mitigation, not a fix for contention the previous Rule could remove. Catching the error, logging it, and returning "failed" with no retry and no alert is the worst combination: the failure is invisible and the partial state stays.

### Once-Per-Period Execution Across Instances

In-process schedulers run on **every** instance, so each scheduled job runs once per instance per period — duplicating side effects (paid messages, emails, invoices) and multiplying load. Guard each run with a distributed single-execution lock keyed by job and period (an atomic set-if-absent with a TTL longer than the period's jitter, released only by its owner), or move scheduling to a single external trigger. Schema migrations follow the same rule: run them as a one-off deploy step, or under a database advisory lock **held on one dedicated connection** (a lock acquired through a pool may be taken and released on different connections). A trigger that can be invoked without authentication is a separate, more urgent defect — report it to `skills/security-review/SKILL.md`'s domain.

### Enforcement

Make the lifecycle rules mechanically checked, not remembered: a static check (AST or lint rule) that every manual acquisition has a release inside guaranteed cleanup in the same function, run in the test gate so a new violation fails the build — including test and integration-test files, which leak connections in CI the same way. A runtime guard that turns a second release into a no-op and rolls back a transaction left open at release is a valuable safety net, but it does not replace fixing call sites.

### Observability

Data-access failures must be visible: pool saturation and wait-time metrics; background jobs instrumented as transactions so their errors and durations appear in APM; deadlock and pool-queue-limit log lines wired to an alarm. Errors swallowed in a catch block that only prints are not handled — they are hidden.

## Constraints

- Never recommend removing a correctness lock (row lock on read-modify-write, sequence-generation lock) to reduce contention.
- Never recommend retrying a non-atomic unit of work.
- Never invent the child repository's instance count, database connection limit, or pool size — state the budget as a formula when the numbers are unknown.
- Never recommend infrastructure changes as if they were code changes; name them as operational decisions for the repository's owners.

## Governance Integration

The two Rules marked Mentor Mandatory instantiate `context/standards/Database Standards.md` (transactions when atomicity is required; race conditions and locking; the connection-lifecycle bullets). Everything else is Mentor Advisory — a recommended pattern a child repository may override with a documented reason (`docs/Governance Precedence Model.md`). This Skill produces no findings of its own; a consuming Review-type Skill (`database-review`, `performance-review`, `code-review`) that finds a violation classifies it through its own Child Governance mechanism and assigns severity from `context/standards/Severity Taxonomy.md`. A child rule that waives the Mandatory connection-lifecycle or transaction-boundary floor for production code is a Prohibited Override for data-integrity reasons.

## Validation

Applying this Skill was correct when: every manual acquisition named has its exit paths traced (not just the happy path); every "held while waiting" claim names the specific wait; any pool-budget statement shows its formula and which inputs are known vs. unknown; any retry recommendation names the atomic unit it wraps; any contention finding names the converging writers or the aggregate; and no number was invented. A static release-placement check reporting zero violations is supporting evidence for Connection Lifecycle, not proof of Transaction Boundaries (early-exit rollback and wrong-handle writes need reading the code).

## Edge Cases

- **A framework-managed unit of work** (callback-style transaction helper) already guarantees release and rollback-on-throw — but an early `return` of a "failure" value from inside the callback commits whatever was written before it. Check what the helper does on a normal return.
- **Long-running batch or reporting jobs** that legitimately need a connection for minutes: give them a dedicated, separately-sized pool or a replica, rather than letting them consume the request pool.
- **Read-only methods that open a transaction or manual runner** for no reason: the fix is to remove the runner, not to add release code around it.
- **Single-instance applications today** still need once-per-period guards before they scale out; flag the latent duplication as Advisory rather than ignoring it.
- **Advisory locks and session variables behind a connection proxy** pin the client connection; list them so the operators can judge the proxy's benefit.

## Failure Handling

If the code that acquires or releases connections isn't visible (it's in a shared helper not included in the material), say the lifecycle cannot be confirmed and name the helper to inspect — do not assume it's correct. If production evidence (stall timing, error text) is offered without code, frame causes as hypotheses mapped to the diagnostic signatures below, ranked, and name what evidence would confirm each.

**Diagnostic signatures** (hypotheses to confirm, not conclusions):

| Signature | Most likely causes |
|---|---|
| Clustered stalls of seconds to minutes across many unrelated endpoints, on all instances at once, often at a fixed time of day | Pool self-deadlock or exhaustion from a scheduled job (Hold-and-Wait, Bounded Concurrency); leaked connections |
| Median latency normal but average and max huge on trivial queries (tiny config tables) | Waiting for a connection, not query cost |
| "Connection closed" / "can't add command" / connection-already-released errors | Double release; open transaction returned to the pool |
| "Too many connections" during deploys or scale-out | Pool budget exceeded; two pools per process |
| Deadlock / lock-wait errors in background posting jobs | Same-aggregate concurrent writers; per-row derived-data recomputation |
| Duplicate side effects once per instance | Missing once-per-period guard |

## Expected Output

Reference guidance applied to a design or to code: for each acquisition point, the lifecycle verdict and any fix; for each concurrency or budget concern, the formula and the recommended bound; for contention, the restructuring; and, when diagnosing, the ranked hypotheses with the evidence that would confirm each. No severity-classified findings of its own — a consuming Review-type Skill emits those.

## Examples

**Positive example.** A scheduled job iterates every (user × tenant) pair and, for each, starts an un-awaited task that opens a manual query runner, reads a row, then calls a condition check that opens a *second* runner, then calls a messaging API with no timeout, releasing the first runner in `finally`. Applying this Skill: Hold-and-Wait (needs a second connection while holding the first, and holds across an external call) plus Bounded Concurrency (unbounded un-awaited fan-out) → with more pairs than the pool size the pool self-deadlocks and every endpoint on the instance stalls until a timeout. Recommendation: await with a small concurrency bound; drop the manual runners and use per-query borrowing; make the external call with a timeout and without holding a connection; load shared config once per run; guard the job with a once-per-period lock because it runs on every instance.

**Negative example (correctly declines).** A request handler calls one repository method that runs a single primary-key lookup through the ORM, which borrows and returns the connection itself; no transaction, no fan-out. Nothing is held, so this Skill has no guidance to add — it says so rather than recommending manual transaction management.

## Related Skills

- `skills/database-review/SKILL.md` — consumes this Skill's Rules when reviewing transactions and concurrency in specific code; owns schema, query plans, and migration DDL safety.
- `skills/performance-review/SKILL.md` — consumes the Diagnostic signatures when a measured stall points at the data-access layer; owns measurement and targets.
- `skills/code-review/SKILL.md` — consumes Connection Lifecycle and Transaction Boundaries as correctness checks on a diff.
- `skills/idempotency/SKILL.md` — is depended on by Deadlock Retry Requires Atomicity for making the retried unit safe.
- `skills/third-party-integration/SKILL.md` — shares a boundary: it owns the external call's own timeout/retry; this Skill only forbids holding database resources across it.
