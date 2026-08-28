---
name: idempotency
description: The general engineering pattern for making an operation safe to receive more than once — request identity, constraint-backed enforcement, replay behavior, response consistency, and retention of idempotency state — so a retry, a webhook redelivery, an at-least-once queue delivery, or a resubmitted user action never produces a duplicate side effect. Reference material consumed by database-review and api-review when evaluating whether a specific implementation actually gets this right.
category: Domain Patterns
skillType: Domain Pattern
---

# Idempotency

## Purpose

Produce the shared, reusable reference pattern for making an operation idempotent — safe to execute more than once with the same effect and observable result as executing it once. This exists as its own Skill because idempotency is a cross-cutting design concern that `database-review` (data-integrity/race-condition angle) and `api-review` (contract/retry-safety angle) both currently assume as background knowledge in their own Rules rather than teach — neither owns "how to design idempotency correctly," only "does this specific implementation have it." This Skill is the reference material both point to, following `docs/Skill Taxonomy.md` Section 2's composition model (a Domain Pattern Skill supplies the pattern; a Review Skill checks for it in real code).

## Scope

**In scope:** the general idempotency pattern — establishing request identity (idempotency keys/tokens, natural business keys, provider-supplied references), constraint-backed enforcement that closes the check-and-act race window, replay behavior (silently returning the original result vs. visibly surfacing the duplicate as a distinct signal), response consistency across replays, expiration/retention of stored idempotency state, and the boundary between where idempotency is enforced (a database constraint, an atomic key-store operation) versus where it is merely verified (a Review-type Skill reading existing code).

**Out of scope:** evaluating whether a specific existing schema or query actually implements this pattern correctly — that is `skills/database-review/SKILL.md`'s Rules → Transactions and Concurrency and Constraints and Nullability; evaluating whether a specific API contract exposes an appropriate idempotency mechanism — that is `skills/api-review/SKILL.md`'s Rules → Idempotency; measuring the actual latency/throughput cost of an idempotency mechanism under load — `skills/performance-review/SKILL.md`'s concern; general code correctness unrelated to duplicate-request handling — `skills/code-review/SKILL.md`'s concern. This Skill teaches the pattern. It does not itself review a repository's implementation of it, and produces no findings of its own.

## When to Use

Use when: designing any operation that can plausibly receive the same logical request more than once — a webhook/callback handler, a client retry over an unreliable network, a queue or job system with at-least-once delivery, or a user-initiated action a client might resubmit (double-click, browser back-and-resubmit, offline-then-reconnect sync); when `database-review` or `api-review` need reference material for what correct idempotency looks like while reviewing a specific implementation; or when deciding whether a new operation needs idempotency treatment at all, and what it should look like.

Do not use for an operation that genuinely cannot be received more than once for the same logical intent (e.g. a single interactive confirmation step with no retry path and no external callback) — applying this pattern reflexively to every write operation is itself a form of over-engineering this Skill's own Rules (below) caution against.

## Required Context

**Posture 2 — benefits from repository context but degrades gracefully without it** (`docs/Skill Standard.md` Section 3). This Skill's guidance is generalizable and useful in the abstract; when repository context is available (declared database engine, ORM, whether the surface is synchronous request/response or queue-based), the guidance applies more concretely, but the pattern itself doesn't require that context to be correct. This Skill does not itself invoke `skills/context-discovery/SKILL.md` — it is reference material, not an evaluation of a specific repository. A consuming Review-type Skill (`database-review`, `api-review`) has already invoked Context Discovery, per its own posture 3 requirement, before applying this Skill's pattern to real code.

## Workflow

This Skill is reference material, not an end-to-end process invoked against a repository on its own (`docs/Skill Taxonomy.md` Section 2) — its "workflow" is the sequence of design decisions whoever applies this pattern (an author, or a Review-type Skill checking for it) works through:

1. Determine whether the operation can plausibly be received more than once for the same logical intent (Edge Cases and Scope, above). If not plausible, idempotency treatment is not warranted — say so rather than applying the pattern reflexively.
2. Identify the request identity: the stable value that identifies "this is the same logical request" — a client-supplied idempotency key, a natural business key already unique to the operation, or a provider-supplied transaction/event reference. An operation with no candidate identity cannot be made idempotent until one is introduced (Edge Cases).
3. Choose an enforcement mechanism that closes the race window between checking and acting (Rules → Constraint-Backed Enforcement) — never a plain read-then-write check in application code alone.
4. Decide replay behavior: return the original result silently, or surface the duplicate visibly as a distinct signal (Rules → Replay Behavior) — and state which, and why.
5. Decide retention/expiration for any stored idempotency state (Rules → Expiration and Retention).
6. Document the mechanism where a Review-type Skill can find and verify it (Related Skills).

## Rules

### Request Identity

Every idempotent operation needs a stable value identifying "this is the same logical request as before" — without one, idempotency cannot be enforced, only guessed at. Three sources are legitimate: a client-supplied idempotency key (a token the client generates once per logical intent and resends unchanged on every retry of that same intent — the pattern most synchronous request/response APIs use for client-initiated writes); a natural business key already unique to the operation by definition (e.g. a one-per-parent relationship that shouldn't exist twice); or a provider-supplied reference on an inbound callback/webhook (the event or transaction identifier the external system itself considers authoritative). A generated-on-receipt value (a fresh UUID assigned by the server on every inbound call) is never a valid request identity — it identifies the *attempt*, not the *intent*, and defeats the purpose.

### Constraint-Backed Enforcement, Not Check-Then-Act

The enforcement mechanism must close the race window between "check whether this has already happened" and "act." A plain sequence of "query for an existing record, then insert if none found" has a window in which two concurrent requests carrying the same request identity can both pass the check before either has inserted — this is a genuine race, not a theoretical one, under realistic concurrent-retry conditions (a client that times out and retries while the first attempt is still in flight is the common real-world trigger). The enforcement mechanism must instead be atomic: a database uniqueness constraint the insert itself can violate, an atomic key-store operation (an insert-if-absent primitive, a compare-and-swap), or an equivalent mechanism the underlying store guarantees is atomic under concurrency. Application code sits on top of this as the response-shaping layer (Rules → Replay Behavior), not as the enforcement mechanism itself.

### Atomicity of the Check-and-Act Step

The enforcement mechanism and the operation's actual side effect must be atomic with respect to each other, not merely atomic with respect to other identical requests. Recording "this request identity has been seen" as a separate step from performing the operation's actual side effect, with any gap between the two, reopens a version of the same race: a concurrent retry can observe the identity as "not yet seen" and proceed, or a crash between the two steps can leave the system having recorded the identity without ever having performed the effect (or the reverse). Prefer a mechanism where the enforcement check and the side effect happen inside the same transaction or the same atomic operation, not as two separately-committed steps.

### Replay Behavior — Silent No-Op vs. Visible Duplicate Signal

Both are legitimate idempotent behaviors; which one is correct depends on what the duplicate means to the caller, and the choice must be explicit, not accidental. Silently returning the original result (as if the duplicate never happened) is correct when the duplicate carries no meaningful information for the caller beyond "did this succeed" — most webhook redelivery and most client-retry cases. Visibly surfacing the duplicate as a distinct, named signal (not silently swallowed, not a generic error) is correct when the fact that a duplicate occurred is itself meaningful information the caller needs — e.g. a second attempt at an operation that has a real-world, one-time physical meaning, where a caller genuinely needs to know "this already happened" as distinct from "this succeeded just now." Treating every replay identically regardless of which case applies is a design smell, not a simplification.

### Response Consistency Across Replays

A replayed request must receive a response consistent with the original outcome, not a response that implies the operation ran again. Concretely: the same success/failure status, referencing the same underlying record/result the original request produced — not a generic `409 Conflict` with no path back to the original result when the caller's own retry logic reasonably expects to be able to proceed as if the first response had simply been delayed. An idempotency mechanism that enforces "no duplicate side effect" but then returns an unhelpful error on replay, forcing the caller to separately look up what actually happened, is only half-built.

### Expiration and Retention of Idempotency State

Stored idempotency state (a key-store entry, a uniqueness-constrained row) needs a deliberate retention decision, not an implicit one. Retained forever, the storage grows unbounded and, for a key-store approach, may eventually need its own cleanup mechanism; retained too briefly, a legitimate retry that arrives after the window has closed (a slow client, a long queue backlog, a caller that retries hours later after an outage) is treated as a new request and produces a real duplicate — this is not the pattern working correctly, it is the window closing before it should have. Choose a retention window with the caller's realistic maximum retry timeframe in mind, not an arbitrary default; where the underlying uniqueness is enforced by a permanent database constraint on a natural business key (rather than a client-supplied key in a separate store), retention is effectively unbounded by construction and this decision doesn't arise the same way.

### Concurrency Under Duplicate Requests

Two requests carrying the same request identity, arriving concurrently, must both observe a correct outcome — one performs the side effect and returns its result; the other observes the enforcement mechanism's rejection (constraint violation, failed atomic insert) and, per Rules → Replay Behavior, returns the equivalent result rather than surfacing the low-level enforcement failure (a raw constraint-violation error) to the caller. A design that lets the concurrent loser's raw storage-layer error leak to the caller has correctly prevented the duplicate side effect but has not correctly implemented idempotency's caller-facing contract.

### Database vs. Application-Layer Enforcement Boundary

State explicitly which layer owns enforcement for a given operation, because the two failure modes differ. Database-layer enforcement (a uniqueness constraint) is simpler to reason about, survives a bypass of the normal application code path (a direct insert, a bulk-load script), and requires no separate storage — but only applies where a genuine natural or generated-and-persisted key exists to constrain on. Application-layer enforcement (an atomic key-store operation, a distributed lock) is necessary when the request identity is a client-supplied value the persistence layer's own schema doesn't naturally constrain on, or when the operation spans multiple underlying stores — but introduces a second system whose own availability and consistency guarantees now matter to correctness.

## Constraints

Never present a specific mechanism (a particular idempotency-key header name, a particular retention window, a particular database engine's constraint syntax, a particular queue system's delivery guarantee) as a universal requirement — those are implementation choices a consuming Skill or a specific repository makes; this Skill states the pattern, not a mandated mechanism. Never claim a specific technology (a particular database, ORM, queue system, or payment provider) is required to implement this pattern — the pattern is technology-agnostic; any technology named in Examples (below) is an illustration, not a requirement, per the Mentor Operating Model's No Invention Rule and Reuse Principle.

## Governance Integration

This Skill does not itself invoke `skills/context-discovery/SKILL.md`, does not evaluate a specific child repository's compliance, and does not produce a governance-classified finding — it is reference material (Domain Pattern), consumed by Review-type Skills per `docs/Skill Taxonomy.md` Section 2. The classification behavior below states how this Skill's guidance interacts with a child repository's own declared rules and exceptions, per `docs/Governance Precedence Model.md` and `scripts/evaluate_governance.py` (`docs/Governance Evaluation.md`) — the same mechanism `skills/code-review/SKILL.md`'s Child Governance rules use, not a parallel one.

**Tier of this Skill's own guidance.** The Rules above state a **Mentor Advisory** pattern — a strongly recommended reusable engineering pattern, not a self-assigned Mandatory floor (`docs/Governance Precedence Model.md` Section 2: a Skill does not acquire Mandatory authority by word choice, however confidently phrased). This guidance is grounded in existing Mentor Standards that already touch this ground — `context/standards/Database Standards.md`'s "Protect data integrity with appropriate constraints" and "Consider race conditions and locking," and `context/standards/API & Backend Standards.md`'s "Design for duplicate requests and concurrency" and "Consider idempotency for retryable operations" — without inventing beyond them. This Skill does not itself elevate any point to Mentor Mandatory; that classification, where warranted against specific code producing a specific data-integrity finding, is `database-review`'s or `api-review`'s own call at review time, citing those same Standards.

**Child Rules and Exceptions.** A child repository may declare its own idempotency convention in `.mentor/rules/` (e.g. a specific header name, a specific retention window). When a consuming Review-type Skill encounters such a rule while applying this Skill's pattern to real code, it classifies the relationship through `scripts/evaluate_governance.py`, exactly as for any other Advisory-tier Mentor guidance:

- **Compatible / Additive** — a child rule that narrows this guidance to a specific mechanism without contradicting the underlying constraint-backed-enforcement principle (e.g. "use header `Idempotency-Key`, retain 24h") is Compatible or Additive, and is honored.
- **Override** — a Child Advisory or Child Configurable rule that legitimately replaces a specific mechanism this Skill's guidance would otherwise suggest, for a valid project reason (e.g. a distributed lock instead of a database constraint, given the project's actual architecture), is a legitimate Override at the Advisory tier — this Skill's guidance yields.
- **Conflict** — a Child Mandatory rule that disagrees with this Skill's Advisory guidance (e.g. a child data-retention policy that conflicts with this Skill's retention-window reasoning) is a genuine Conflict per `docs/Governance Precedence Model.md` Section 10 category 4 — Child Mandatory outranks Mentor Advisory, so the child's rule governs, but the consuming Skill states the conflict; it does not silently absorb it.
- **Prohibited Override** — this Skill's own guidance is Advisory-tier, not Mentor Mandatory or security/safety-classified, so a child rule or exception targeting *this Skill's guidance specifically* is never itself a Prohibited Override case. A Prohibited Override can still arise at review time when a consuming Skill's own Mandatory-grounded data-integrity finding (citing the Standards above, against actual code) is what a child rule or exception attempts to override — that is the consuming Skill's (`database-review`'s or `api-review`'s) own Governance Integration to classify, not this Skill's.
- **Unknown/Indeterminate applicability** — when a discovered child rule's scope doesn't clearly state whether it covers idempotency-relevant code, the consuming Skill reports Insufficient Evidence rather than assuming either way, per `scripts/evaluate_governance.py`'s `unknown` classification.

**Severity independence.** This Skill produces no findings and assigns no severity. When a consuming Review-type Skill produces a finding using this Skill's guidance, that finding's severity (`context/standards/Severity Taxonomy.md`) and its governance classification remain independent axes, per `docs/Governance Precedence Model.md` Section 12 — a Prohibited Override classification never implies CRITICAL by itself, and a Compatible classification never implies INFO by itself.

## Validation

This Skill produces no artifact of its own to validate — it is reference material (Domain Pattern), not an evaluation. Its guidance is applied correctly when whoever uses it (an author designing an operation, or a Review-type Skill checking one) can state, for the specific operation in question: its request identity, its enforcement mechanism and why it's atomic, its replay behavior and why that choice fits the operation, and its retention decision. A finding or design that says "this needs idempotency" without being able to state which of these is actually missing or wrong is under-specified against this Skill's own Rules.

## Edge Cases

- **A webhook/callback where duplicate delivery is a stated, expected behavior of the upstream provider, not a bug.** The pattern must treat this as the normal case it is designed for, not as an anomaly to special-case.
- **A distributed system where the enforcement mechanism lives on a different node or service than the one first receiving the request.** The race window between "receive" and "enforce" can be wider than a single-process check-then-act would suggest — state this explicitly rather than assuming a single-node model.
- **A client-supplied idempotency key reused across genuinely different logical requests** (a client bug, or parameters that changed between calls carrying the same key). The pattern must decide, and state, whether this is treated as "same request, return the original result" or rejected as a key-collision error — silently picking the wrong one is a correctness risk, not an implementation detail.
- **A retry that arrives after the idempotency state's retention window has already expired.** This is the window closing, not the pattern degrading gracefully — a duplicate side effect here is a real bug against Rules → Expiration and Retention, not an acceptable edge case to shrug off.
- **An operation with no natural request identity available at all** (no client-supplied key, no unique business key, no provider reference). Idempotency cannot be enforced without one; Workflow step 2 is establishing this identity, and an operation genuinely lacking one should be treated as the actual finding when reviewed, not silently assumed to be fine.

## Failure Handling

When the material under review doesn't establish whether an operation can plausibly be received more than once, or doesn't show what request identity (if any) exists, state that explicitly as Insufficient Evidence rather than assuming idempotency is or isn't needed — per the Mentor Operating Model's No Invention Rule. This Skill, being reference material, has no live "cannot proceed" state of its own; this section describes what a consuming Skill should do when this pattern can't yet be applied to a specific case because the material doesn't establish enough to apply it.

## Expected Output

Reference material — no review, artifact, or decision of its own (`docs/Skill Taxonomy.md` Section 2: a Domain Pattern Skill is never invoked end-to-end against a real repository on its own). A consuming Review-type Skill's own Expected Output (a structured review, per `context/templates/Review Template.md`) is what actually gets produced when this Skill's guidance is applied to real code.

## Examples

**Positive example (correct idempotent operation).** An order-submission endpoint requires a client-supplied `Idempotency-Key` header. The order table has a `UNIQUE` constraint on `(customer_id, idempotency_key)`. On insert, a constraint violation is caught and the handler returns the existing order's data with the same `200`/`201` status the original request would have returned, rather than a generic error. Two concurrent requests with the same key: one inserts and returns the new order; the other hits the constraint violation and returns the same order — no duplicate order, no leaked storage-layer error, consistent response either way.

**Negative example (incorrect — check-then-act, not idempotent).** The same endpoint instead does `SELECT` for an existing order with that key, and if none is found, performs an `INSERT`. Under concurrent duplicate requests, both can pass the `SELECT` before either commits the `INSERT`, producing two orders for one logical submission. This looks idempotent in isolated, sequential testing and fails exactly under the realistic concurrent-retry condition the pattern exists to handle.

**Retry-behavior example.** A payment-provider webhook redelivers the same `event_id` after the receiver's `200` acknowledgment was lost in transit (a common, expected provider behavior, not a bug). The handler looks up `event_id` in a uniqueness-constrained processed-events table; found, it returns success immediately without re-triggering the payment-confirmation side effects (Rules → Replay Behavior: silent no-op is correct here, since the redelivery carries no new information for the caller).

**Concurrency example.** A "redeem this one-time invite code" operation receives two nearly-simultaneous requests for the same code from two different users (a race the client side cannot prevent). A `UNIQUE` constraint on `invite_code_id` in the redemption table ensures exactly one insert succeeds; the losing request's constraint violation is translated into "this code has already been redeemed" — a visible, distinct signal to that caller (Rules → Replay Behavior: this is a case where the duplicate itself is meaningful information, not a silent no-op).

**Boundary example (idempotency vs. database-review / api-review).** This Skill states that the order-submission example above needs a uniqueness constraint and a caught-violation response path. Whether a *specific* migration actually adds that constraint correctly (nullability, index shape) is `database-review`'s Rules → Constraints and Nullability; whether the endpoint's *contract* documents the `Idempotency-Key` requirement and its retry semantics is `api-review`'s Rules → Idempotency. This Skill supplies the pattern both check for.

## Related Skills

- `skills/database-review/SKILL.md` — Related: reviews whether a specific schema/query actually implements this Skill's constraint-backed-enforcement pattern (Rules → Constraints and Nullability, Transactions and Concurrency); consumes this Skill as reference material, does not depend on it to function.
- `skills/api-review/SKILL.md` — Related: reviews whether a specific API contract exposes an appropriate idempotency mechanism (Rules → Idempotency); consumes this Skill as reference material, same non-dependency relationship.
- `skills/security-review/SKILL.md` — Related: a broken idempotency mechanism can itself be an abuse vector (e.g. exploiting a check-then-act race to double-spend or bypass a limit) — `security-review`'s Rules → Abuse and Resource Exhaustion may reference this Skill's pattern when relevant; ownership of the security angle stays with `security-review`.
- `skills/performance-review/SKILL.md` — Related: an idempotency mechanism's measured performance cost (lock contention, key-store lookup latency) is `performance-review`'s concern; this Skill states the correctness pattern only, not its performance characteristics.
