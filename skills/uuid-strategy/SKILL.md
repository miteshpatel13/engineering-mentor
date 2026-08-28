---
name: uuid-strategy
description: The general engineering pattern for identifier strategy — internal vs. public/external identifiers, when an opaque (e.g. UUID) identifier is warranted vs. a simple sequential one, generation strategy, storage/indexing tradeoffs, resolution boundaries, and exposure/security considerations. Reference material consumed by database-review, api-review, and security-review when evaluating whether a specific implementation actually gets this right.
category: Domain Patterns
skillType: Domain Pattern
---

# UUID Strategy

## Purpose

Produce the shared, reusable reference pattern for identifier strategy — the common split between an internal identifier (optimized for storage, joins, and performance) and a public/external identifier (optimized for opacity and non-enumerability), when each is actually warranted, and how resolution between them should be handled end-to-end. This exists as its own Skill because `database-review`, `api-review`, and `security-review` each touch one piece of this decision (indexing, contract shape, authorization) without teaching the identifier-strategy decision itself, following `docs/Skill Taxonomy.md` Section 2's composition model.

## Scope

**In scope:** identifier purpose and audience (internal vs. public/external), when an opaque, non-sequential identifier (a UUID or equivalent) is warranted versus when a simple sequential identifier is sufficient, generation strategy (store-generated vs. application-generated) and its tradeoffs, collision considerations, storage representation and indexing/ordering implications, the resolution boundary between public and internal identifiers, migration concerns when introducing or changing an identifier strategy, and exposure/security considerations.

**Out of scope:** whether a specific schema correctly implements the chosen storage/indexing approach — `skills/database-review/SKILL.md`'s Rules → Indexes and Query Patterns; whether authorization is correctly enforced on a resource regardless of identifier shape — `skills/security-review/SKILL.md`'s Rules → Authentication vs. Authorization (an opaque identifier is not an authorization mechanism — Rules → Exposure and Security Considerations, below, states this as a hard boundary); whether a specific API contract correctly exposes the public identifier and excludes the internal one — `skills/api-review/SKILL.md`'s Rules → Response Contracts and Consistency; cross-service identifier-flow design in a distributed system — `skills/architecture-review/SKILL.md`'s boundary concern, when the question is structural rather than single-store mechanics. This Skill teaches the pattern; it produces no findings of its own.

## When to Use

Use when: designing identifier strategy for a new resource type; deciding whether an existing sequential identifier should be supplemented or replaced with an opaque public identifier; reviewing whether a numeric/sequential identifier is inappropriately exposed on an external surface; or choosing between generation approaches for a new opaque identifier.

Do not use to justify adding an opaque identifier to a resource with no external audience and no enumeration/sensitivity concern — Rules → When an Opaque Identifier Is Warranted states this is not automatic.

## Required Context

**Posture 2 — benefits from repository context but degrades gracefully without it** (`docs/Skill Standard.md` Section 3). The pattern is generalizable; applying it concretely benefits from knowing the declared database engine's identifier-generation capabilities (Rules → Generation Strategy). This Skill does not itself invoke `skills/context-discovery/SKILL.md` — a consuming Review-type Skill has already done so.

## Workflow

Reference material, not an end-to-end process invoked on its own — the sequence below is the design-decision order whoever applies this pattern works through:

1. Determine the identifier's audience — will it ever appear in a URL, a request/response body, a log line, or any surface outside full administrative trust (Rules → Identifier Purpose and Audience)? If never, a simple internal identifier may be entirely sufficient.
2. If a public-facing identifier is needed, decide whether opacity/non-enumerability is actually required (Rules → When an Opaque Identifier Is Warranted) — not every public identifier needs to be opaque.
3. Choose a generation strategy and understand its tradeoffs (Rules → Generation Strategy).
4. Decide storage representation and its indexing/ordering implications (Rules → Storage, Indexing, and Ordering).
5. Design the resolution boundary (Rules → Resolution Boundary) and confirm nothing internal-identifier-shaped reaches a surface outside it (Rules → Exposure and Security Considerations).

## Rules

### Identifier Purpose and Audience

The first question is who ever sees an identifier: a purely internal identifier (used only in joins, internal service-to-service calls, internal logs not externally reachable) has different requirements from one appearing in a URL, a request/response body, or any externally-reachable surface. Conflating the two — using one identifier for both purposes — is what creates the problems the remaining Rules address; keeping them separate from the start avoids most of them.

### When an Opaque Identifier Is Warranted

An opaque, non-sequential public identifier is warranted when: sequential exposure would let a caller enumerate other resources by incrementing a visible value (a scale/business-information leak, distinct from an authorization defect — see Exposure and Security Considerations); the identifier crosses a trust or organizational boundary where a predictable internal scheme would leak implementation detail; or a resource's existence/count is itself sensitive. It is not automatically warranted for every resource — a small, non-sensitive, internal-only reference table gains little from opacity and pays a real cost (Rules → Storage, Indexing, and Ordering) for no benefit. State the reasoning; don't apply an opaque identifier reflexively to every identifier in a schema.

### Generation Strategy

Two broad approaches, both legitimate, with different tradeoffs. **Store-generated** (the underlying database produces the value on insert) guarantees a value exists even for a write path that bypasses application code (a raw insert, a bulk-load script), at the cost of coupling the schema to a specific engine's capability. **Application-generated** (the application layer produces the value before or during insert) keeps generation visible in application code and tests, and is engine-portable, at the cost of requiring every insert path — including tooling and seed scripts — to remember to set it. Pick one mechanism and apply it consistently across the resources that need it; deciding per-resource, ad hoc, produces the inconsistency this Rule exists to prevent.

### Collision Considerations

A well-formed random identifier with adequate entropy (a standard random UUID or equivalent) has a collision probability low enough to treat as effectively zero for practical purposes — but this depends on actually using a generation method with sufficient randomness; a shortened, non-random, or narrow custom scheme does not inherit this property automatically by being called "a UUID" or similar, and its actual collision probability should be reasoned about explicitly. Regardless of the generation method's theoretical safety, the storage layer's own uniqueness constraint — not application-side reasoning alone — is what must actually prevent a collision from being persisted.

### Storage, Indexing, and Ordering

A random (non-sequential) identifier as the primary storage/index key has a real, measurable cost distinct from its logical correctness: insert order becomes effectively random relative to the index's physical layout, which can fragment the index and hurt insert/range-scan performance at scale, compared to a monotonically-increasing key. Where this matters, a common resolution is to keep a separate sequential internal identifier as the actual physical/clustering key and store the opaque public identifier as a secondary, uniquely-indexed column — not as the primary storage key itself. Whether this distinction actually matters for a given system's scale is a `skills/performance-review/SKILL.md` / `skills/database-review/SKILL.md` question this Skill flags but does not itself resolve.

### Resolution Boundary

Resolve a public identifier to whatever internal identifier the rest of the system actually uses exactly once, as early in the request path as possible — not scattered through business logic, and not re-resolved redundantly by downstream layers that already received the internal identifier. Everything downstream of that boundary uses the internal identifier; the public identifier resurfaces only when constructing an external-facing response.

### Exposure and Security Considerations

Never expose an internal, sequential, or otherwise enumerable identifier on any externally-reachable surface — a URL, a response body, an error message, a client-visible pagination cursor, or a log line a non-administrative caller could plausibly reach. This includes incidental leaks: an error message echoing an internal identifier instead of the public one, or a generic entity-to-JSON serializer that includes every column by default rather than an explicit response shape. **Opacity is not authorization.** A non-guessable public identifier makes a resource harder to enumerate; it does nothing to enforce that the caller holding that identifier is actually allowed to access the resource it names — that check remains entirely `skills/security-review/SKILL.md`'s Rules → Authentication vs. Authorization concern, and this Skill's guidance must never be read as a substitute for it.

### Migration Concerns

Introducing an opaque public identifier onto a resource type that previously exposed its internal one is a backward-compatibility concern for any existing consumer holding the old identifier — decide and state whether the old identifier continues to resolve during a transition period or is cut over immediately, per `skills/api-review/SKILL.md`'s Rules → Versioning and Backward Compatibility, which governs the contract-level decision; this Skill only flags that the decision exists.

## Constraints

Never claim opaque identifiers are unconditionally superior to sequential identifiers — Rules → When an Opaque Identifier Is Warranted and Storage, Indexing, and Ordering both state real, situational tradeoffs; presenting this as a universal best practice would misstate the pattern. Never present a specific generation mechanism, storage type, or database engine's capability as a requirement — Rules → Generation Strategy states two legitimate approaches, not one mandated approach. Never let this Skill's opacity guidance be read as a substitute for actual authorization enforcement (Rules → Exposure and Security Considerations restates this as a hard boundary because it is the most common real-world misunderstanding of this pattern).

## Governance Integration

This Skill does not itself invoke `skills/context-discovery/SKILL.md`, evaluate a specific child repository's compliance, or produce a governance-classified finding — reference material, consumed by Review-type Skills per `docs/Skill Taxonomy.md` Section 2.

**Tier of this Skill's own guidance.** **Mentor Advisory** — a strongly recommended reusable pattern, not a self-assigned Mandatory floor. This Skill does not cite a Mandatory-floor grounding of its own (unlike `skills/idempotency/SKILL.md` and `skills/soft-delete/SKILL.md`, which cite explicit Database/API Standards bullets) — no `context/standards/*.md` document names identifier-opacity strategy specifically. Its Exposure and Security Considerations Rule is informed by, and explicitly does not duplicate or weaken, `skills/security-review/SKILL.md`'s existing Rules → Authentication vs. Authorization (IDOR/BOLA) and Rules → Secrets and Sensitive Data — this Skill's own guidance never substitutes for that Skill's Mandatory-adjacent authorization findings, stated explicitly in Rules → Exposure and Security Considerations above.

**Child Rules and Exceptions**, classified through `scripts/evaluate_governance.py` exactly as for any other Advisory-tier Mentor guidance, by a consuming Review-type Skill:

- **Compatible / Additive** — a child rule narrowing this guidance to a specific mechanism (e.g. a specific identifier format, a specific header/path-parameter convention) without contradicting the opacity or resolution-boundary principles is Compatible or Additive, and honored.
- **Override** — a Child Advisory or Child Configurable rule legitimately replacing a specific mechanism this Skill would otherwise suggest (e.g. a project mandates application-generated identifiers everywhere for a valid tooling reason) is a legitimate Override at the Advisory tier.
- **Conflict** — a Child Mandatory rule that disagrees with this Skill's Advisory guidance (e.g. a child compliance rule mandating a specific identifier format this Skill's collision-safety reasoning would advise against) is a genuine Conflict per `docs/Governance Precedence Model.md` Section 10 category 4 — Child Mandatory outranks Mentor Advisory, so the child's rule governs, but the consuming Skill states the conflict.
- **Prohibited Override** — this Skill's own guidance is Advisory-tier, so a child rule/exception targeting it specifically is never itself a Prohibited Override case. A Prohibited Override can still arise when a consuming Skill's own Mandatory-grounded finding (e.g. `security-review` citing an authorization requirement against a specific missing ownership check) is what a child rule/exception attempts to waive — that is the consuming Skill's own classification, not this Skill's.
- **Unknown/Indeterminate applicability** — when a discovered child rule's scope doesn't clearly state whether it covers identifier-strategy-relevant code, the consuming Skill reports Insufficient Evidence rather than assuming either way.

**Severity independence.** This Skill produces no findings and assigns no severity. A consuming Skill's finding severity and governance classification remain independent axes per `docs/Governance Precedence Model.md` Section 12.

## Validation

This Skill produces no artifact of its own to validate. Its guidance is applied correctly when whoever uses it can state, for a specific identifier: its audience, whether opacity is actually warranted and why, its generation strategy, its resolution boundary, and — separately — that authorization is enforced independently of the identifier's shape. A design that adds an opaque identifier "for security" with no separate authorization check is under-specified against this Skill's own Rules.

## Edge Cases

- **A resource whose existence/count is not sensitive and is never reachable outside a trusted internal boundary.** An opaque public identifier provides no benefit here; state this rather than applying the pattern reflexively (Rules → When an Opaque Identifier Is Warranted).
- **A storage layer that doesn't support store-generated opaque values at all** (an older engine, a constrained managed-service tier). Application-generated becomes the only viable choice, not a stylistic preference (Rules → Generation Strategy).
- **A public identifier that legitimately needs to encode meaningful, caller-visible ordering** (e.g. a pagination cursor needing stable, monotonic ordering). A fully random opaque identifier alone doesn't provide this — state the additional requirement rather than assuming opacity alone suffices for that use case.
- **A resource identified by a naturally-unique external value not generated by this system at all** (a value assigned by an external registry/authority). The generation-strategy reasoning doesn't apply the same way; the identifier's uniqueness is asserted by the external source, and this Skill's Resolution Boundary and Exposure Rules are what still apply.

## Failure Handling

When the material doesn't establish an identifier's actual audience (internal-only vs. externally reachable), state that explicitly as Insufficient Evidence per the Mentor Operating Model's No Invention Rule, rather than assuming either an opaque or a sequential strategy is already correct. When the material doesn't establish the declared engine's generation capabilities, state that the generation-strategy choice can't be confirmed rather than assuming one.

## Expected Output

Reference material — no review, artifact, or decision of its own (`docs/Skill Taxonomy.md` Section 2). A consuming Review-type Skill's own Expected Output is what actually gets produced when this Skill's guidance is applied to real code.

## Examples

**Positive example (appropriate opaque-identifier use).** A public API resource reachable by any authenticated user, where sequential IDs would let a caller enumerate other users' resource counts, uses a random opaque public identifier for every external reference, with a separate sequential internal identifier retained for storage/joins (Rules → Storage, Indexing, and Ordering).

**Negative example (inappropriate use).** A purely internal, admin-only configuration table with no external surface at all is given a random opaque primary key "for consistency with the rest of the schema." No benefit is gained (Rules → When an Opaque Identifier Is Warranted), and the resulting index fragmentation (Rules → Storage, Indexing, and Ordering) is a real, avoidable cost for zero gain.

**Generation-strategy comparison example.** The same resource type could use a store-generated default-expression value (simpler, guarantees a value on any insert path, ties the schema to the engine's capability) or an application-generated value before insert (portable, requires every insert path to remember to set it). Rules → Generation Strategy states the tradeoff explicitly rather than declaring either universally correct.

**Storage/API boundary example.** A response DTO explicitly serializes only the public identifier field; a generic "serialize the whole entity" shortcut that would leak the internal identifier is called out as the specific defect Rules → Exposure and Security Considerations addresses.

**Boundary example (uuid-strategy vs. security-review).** A resource correctly uses an opaque public identifier, but has no ownership check at all. This Skill's guidance is fully satisfied (opacity is correctly implemented) — the resource is still exploitable by anyone possessing a leaked or shared identifier. This is entirely `security-review`'s Authorization finding, not something this Skill's guidance resolves; Rules → Exposure and Security Considerations states this distinction explicitly.

## Related Skills

- `skills/database-review/SKILL.md` — Related: reviews whether a specific schema actually implements the storage/indexing tradeoff (Rules → Storage, Indexing, and Ordering) correctly; consumes this Skill as reference material, does not depend on it to function.
- `skills/security-review/SKILL.md` — Related: authorization enforcement remains entirely its own concern (Rules → Authentication vs. Authorization); this Skill's Exposure Rule explicitly states opacity is not a substitute for it.
- `skills/api-review/SKILL.md` — Related: reviews whether a contract's response DTOs and path parameters correctly use the public identifier, and whether an identifier-strategy migration is backward-compatible (Rules → Response Contracts, Rules → Versioning and Backward Compatibility).
- `skills/architecture-review/SKILL.md` — Related: owns cross-service identifier-flow design when the question is structural rather than single-store mechanics.
- `skills/soft-delete/SKILL.md` — Related: system-generated opaque identifiers are the one legitimate exception to that Skill's conditional-uniqueness reasoning; this Skill is where that identifier's own design is owned.
