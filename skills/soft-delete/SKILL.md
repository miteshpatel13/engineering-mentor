---
name: soft-delete
description: The general engineering pattern for logical (soft) deletion — marking a record unavailable for normal use while retaining it — versus physical (hard) deletion. Covers structural query-visibility exclusion, natural-key uniqueness after deletion, restoration, cascading behavior, authorization implications, retention, and auditability. Reference material consumed by database-review and security-review when evaluating whether a specific implementation actually gets this right.
category: Domain Patterns
skillType: Domain Pattern
---

# Soft Delete

## Purpose

Produce the shared, reusable reference pattern for logical (soft) deletion — retaining a "deleted" record rather than physically removing it, for history, audit, referential integrity, or possible restoration — as distinct from physical (hard) deletion and from several adjacent lifecycle concepts that are easy to conflate with it. This exists as its own Skill because `database-review` (schema/query correctness) and `security-review` (whether authorization still applies to a soft-deleted record) both touch pieces of this pattern in their own Rules without teaching the pattern itself, following `docs/Skill Taxonomy.md` Section 2's composition model.

## Scope

**In scope:** logical vs. physical deletion semantics, structural query-visibility exclusion of deleted records, natural-key uniqueness after soft deletion, restoration ("undelete") semantics, cascading and relationship considerations, authorization implications of a still-existing-but-hidden record, retention and the hard-delete boundary, and auditability of the deletion event itself.

**Out of scope:** whether a specific existing schema or query actually implements this pattern correctly — that is `skills/database-review/SKILL.md`'s Rules → Constraints and Nullability / Indexes and Query Patterns; whether authorization is correctly enforced on a resource regardless of its deletion state — `skills/security-review/SKILL.md`'s Rules → Authentication vs. Authorization; the broader structural decision of which service owns a soft-deletable table's data, or cross-service cascading — `skills/architecture-review/SKILL.md`'s data-ownership concern, when the relationship crosses a service boundary rather than living inside one data store; whether an API contract correctly represents a deleted resource (e.g. `404` vs. a tombstone response) — `skills/api-review/SKILL.md`'s Rules → Response Contracts and Consistency. This Skill teaches the pattern; it produces no findings of its own.

## When to Use

Use when: designing any delete operation for business data that shouldn't disappear from history, audit, or reporting; deciding whether a table needs soft-delete at all versus hard-delete-only versus a different lifecycle-state model; reviewing whether a query correctly excludes deleted rows by default; or adding a uniqueness constraint to a table that has soft-delete.

Do not use for data with no retention/history requirement at all, where physical deletion is the simpler, correct choice (Rules → Retention and the Hard-Delete Boundary) — applying soft-delete reflexively to every table is itself a form of the over-engineering this Skill's own Rules caution against.

## Required Context

**Posture 2 — benefits from repository context but degrades gracefully without it** (`docs/Skill Standard.md` Section 3). The pattern is generalizable and useful in the abstract; applying it concretely benefits from knowing the declared database engine's actual uniqueness-constraint capabilities (Rules → Natural-Key Uniqueness). This Skill does not itself invoke `skills/context-discovery/SKILL.md` — a consuming Review-type Skill has already done so, per its own posture-3 requirement, before applying this Skill's pattern to real code.

## Workflow

Reference material, not an end-to-end process invoked on its own (`docs/Skill Taxonomy.md` Section 2) — the sequence below is the design-decision order whoever applies this pattern works through:

1. Determine whether this data needs to remain retrievable for history/audit/compliance after "deletion," or whether physical removal is actually correct (Rules → Retention and the Hard-Delete Boundary). Not every table needs soft-delete.
2. If soft-delete applies, decide how deleted-state is represented and ensure query-visibility exclusion is structural (Rules → Query Visibility), not per-call-site.
3. Decide whether the table has natural-key uniqueness constraints that need to account for soft-deleted rows (Rules → Natural-Key Uniqueness).
4. Decide restoration semantics explicitly (Rules → Restoration).
5. Decide cascading behavior per relationship explicitly (Rules → Cascading and Relationship Considerations) — never leave it to incidental ORM/FK defaults.
6. Confirm authorization checks apply to a soft-deleted record exactly as to an active one (Rules → Authorization Implications).
7. Decide the retention window and hard-delete boundary, if any.
8. Ensure the deletion event itself is auditable (Rules → Auditability).

## Rules

### Logical vs. Physical Deletion

Soft delete marks a record unavailable for normal use while physically retaining it; hard delete physically removes the row. This is a per-table (or per-data-category) decision, not a system-wide default to assume — state explicitly which applies to a given table and why (Rules → Retention and the Hard-Delete Boundary covers when hard delete is actually correct).

### Query Visibility — Structural Exclusion, Not Per-Call-Site

Every read path that returns business data must exclude soft-deleted rows by default, with an explicit, separately-named opt-in for the rare case that needs them (an admin trash view, an audit export, a restoration flow). Enforce this structurally — a repository base class, a global query scope/interceptor, or the data-access layer's built-in support — never left to every call site remembering to add the filter by hand; a missing filter should be structurally impossible, not a code-review checklist item. Where a transaction soft-deletes a row and then reads it back within the same transaction, decide explicitly whether it should see its own pending deletion — an inconsistent answer between call sites is itself a defect.

### Distinguishing Deletion From Adjacent Lifecycle Concepts

Several distinct concepts are easy to conflate under one "deleted" flag, and conflating them causes real defects. Distinguish at minimum: **soft deletion** ("this record should not exist for any normal purpose" — this Skill's concern); **deactivation** (a record that stays fully visible in historical/read views and stays referentially valid, but is excluded from new-selection pickers — e.g. a discontinued option in a reference list); **a business status/lifecycle transition** (a normal, expected state change — cancelled, archived, completed — that must stay fully visible in reports and audit exports, never the same as deletion); and **anonymization/erasure** (removing identifying content from an otherwise-intact, still-queryable, still-referenceable record, typically for a privacy/compliance request — not soft deletion; applying the deletion flag during anonymization would incorrectly remove the row from views that still need it). Using one flag for more than one of these is a design defect, not a shortcut.

### Natural-Key Uniqueness After Soft Deletion

A natural-key uniqueness constraint on a soft-deletable table must not permanently block reuse of a value once its owning row is soft-deleted — a plain, unconditional `UNIQUE` constraint does exactly that, since the deleted row still counts. The general solution is a *conditional*/*partial* uniqueness constraint enforced only against non-deleted rows, via whatever mechanism the underlying store actually supports (a native partial/filtered unique index where the engine offers one; an engine-specific workaround, such as a computed column collapsing to a sentinel value for deleted rows with the constraint placed on that column, where it doesn't). State which mechanism applies for the actual declared engine — never assume one the engine doesn't support. System-generated opaque identifiers meant never to be reused after deletion are a legitimate exception and stay as plain, permanent unique constraints (see `skills/uuid-strategy/SKILL.md`).

### Restoration

If restoration ("undelete") is supported, define what it means when the world has moved on since deletion — a uniqueness value the record held may have been legitimately reused by a different row since (Rules → Natural-Key Uniqueness), or a related record may itself have changed — and re-check these conditions rather than blindly clearing the deleted flag. If restoration is not supported, say so explicitly; an unstated "no" reads as an oversight, not a decision.

### Cascading and Relationship Considerations

Never let cascading soft-delete behavior follow ORM/FK cascade defaults incidentally. For each relationship between a soft-deletable parent and its children, decide explicitly whether deleting the parent should also soft-delete the children, or whether children remain visible on their own terms. Both are legitimate depending on whether child records represent independent historical facts (usually should remain visible) or genuinely dependent data with no meaning once the parent is gone. Document the decision per relationship — never apply one blanket rule to an entire schema without checking whether it actually holds for each relationship.

### Authorization Implications

A soft-deleted record still physically exists and can still be reached by anything that doesn't go through the structural query-visibility exclusion (a direct lookup by ID, an admin endpoint, a report against the raw table). Authorization checks must still apply to it exactly as to an active record — "it's deleted" is not itself an authorization boundary, and a caller who couldn't access the record before deletion must not gain access to it, or infer its prior existence, through a path that bypasses the visibility filter.

### Retention and the Hard-Delete Boundary

Decide, per data category, whether physical deletion is ever appropriate on top of soft-delete — a genuine compliance/legal erasure requirement, a retention policy with an actual expiration, or a specific approved purge process — and, where PII erasure is the driver, prefer anonymization over physical row removal wherever the record must remain referentially valid for dependent data. A table with no such requirement may reasonably retain soft-deleted rows indefinitely; state which applies rather than leaving hard-delete timing undefined.

### Auditability

A soft-delete operation is a state change to real data and should be auditable the same way any other significant state change is — who performed it, when, and, where the data model supports it, the record's state immediately before. This Skill states the requirement generally; the actual audit-logging mechanism is a separate concern outside its scope.

## Constraints

Never present a specific storage mechanism (particular column names, a particular engine's partial-index syntax, a particular ORM's soft-delete plugin) as a universal requirement — those are implementation choices; this Skill states the pattern. Never assume cascading soft-delete behavior in either direction without an explicit, stated decision per relationship (Rules → Cascading, restated here as a hard boundary because it's the most common source of silent defects in soft-delete implementations). Never treat "the record is soft-deleted" as itself sufficient authorization reasoning.

## Governance Integration

This Skill does not itself invoke `skills/context-discovery/SKILL.md`, evaluate a specific child repository's compliance, or produce a governance-classified finding — reference material, consumed by Review-type Skills per `docs/Skill Taxonomy.md` Section 2.

**Tier of this Skill's own guidance.** **Mentor Advisory** — a strongly recommended reusable pattern, not a self-assigned Mandatory floor. Grounded in existing Mentor Standards without inventing beyond them: `context/standards/Database Standards.md`'s "Protect data integrity with appropriate constraints" bears directly on Rules → Natural-Key Uniqueness. This Skill does not itself elevate any point to Mentor Mandatory; that classification, where warranted against specific code, is `database-review`'s or `security-review`'s own call at review time.

**Child Rules and Exceptions**, classified through `scripts/evaluate_governance.py` exactly as for any other Advisory-tier Mentor guidance, by a consuming Review-type Skill:

- **Compatible / Additive** — a child rule narrowing this guidance to a specific mechanism (e.g. a specific retention window, a specific column-naming convention) without contradicting the structural-exclusion or conditional-uniqueness principles is Compatible or Additive, and honored.
- **Override** — a Child Advisory or Child Configurable rule legitimately replacing a specific mechanism this Skill would otherwise suggest (e.g. a status-enum-based lifecycle model instead of a boolean-plus-timestamp pair, for a valid project reason) is a legitimate Override at the Advisory tier.
- **Conflict** — a Child Mandatory data-retention or erasure policy that disagrees with this Skill's own Advisory retention reasoning is a genuine Conflict per `docs/Governance Precedence Model.md` Section 10 category 4 — Child Mandatory outranks Mentor Advisory, so the child's policy governs, but the consuming Skill states the conflict rather than silently absorbing it.
- **Prohibited Override** — this Skill's own guidance is Advisory-tier, so a child rule/exception targeting it specifically is never itself a Prohibited Override case. A Prohibited Override can still arise when a consuming Skill's own Mandatory-grounded finding (e.g. `database-review` citing Database Standards' data-integrity bullet against a specific missing constraint) is what a child rule/exception attempts to waive — that is the consuming Skill's own classification to make.
- **Unknown/Indeterminate applicability** — when a discovered child rule's scope doesn't clearly state whether it covers deletion-relevant code, the consuming Skill reports Insufficient Evidence rather than assuming either way.

**Severity independence.** This Skill produces no findings and assigns no severity. A consuming Skill's finding severity and governance classification remain independent axes per `docs/Governance Precedence Model.md` Section 12.

## Validation

This Skill produces no artifact of its own to validate. Its guidance is applied correctly when whoever uses it can state, for a specific soft-deletable table: its query-visibility exclusion mechanism, whether and how natural-key uniqueness is handled, its restoration semantics, its per-relationship cascading decisions, and its retention/hard-delete boundary. A design that says "this table has soft-delete" without being able to state these is under-specified against this Skill's own Rules.

## Edge Cases

- **A soft-deletable table with no natural-key uniqueness constraints at all.** The conditional-uniqueness concern (Rules → Natural-Key Uniqueness) simply doesn't arise; state this rather than applying it reflexively.
- **A record soft-deleted, then a new record legitimately created reusing the same natural-key value.** Must succeed cleanly, not silently fail or resurrect the old record — the direct test of Rules → Natural-Key Uniqueness actually working.
- **A relationship where the child table has no soft-delete of its own.** Cascading soft-delete can't apply to it in the usual sense; its visibility must be governed by its own status/active-parent check instead, stated explicitly (Rules → Cascading).
- **A pure reference/master-data table with an admin-managed active/inactive toggle but no genuine "deletion" concept.** This is Deactivation (Rules → Distinguishing Adjacent Lifecycle Concepts), not soft-delete — it doesn't need this Skill's deletion-specific reasoning (query-visibility exclusion, natural-key handling) applied to it.

## Failure Handling

When the material doesn't establish whether a table needs soft-delete, hard-delete-only, or a different lifecycle model, state that explicitly as Insufficient Evidence per the Mentor Operating Model's No Invention Rule, rather than assuming soft-delete is the default. When the material doesn't establish the declared engine's uniqueness-constraint capabilities, state that the correct mechanism can't be confirmed rather than assuming one.

## Expected Output

Reference material — no review, artifact, or decision of its own (`docs/Skill Taxonomy.md` Section 2). A consuming Review-type Skill's own Expected Output is what actually gets produced when this Skill's guidance is applied to real code.

## Examples

**Positive example.** A table has a deleted-state pair (a boolean flag plus a timestamp) and a repository base class that excludes deleted rows from every "active" query method by default, with a separately-named `includeDeleted` method for the one admin trash view that needs it. Its one natural-key uniqueness constraint uses a conditional/partial mechanism appropriate to the declared engine, so a deleted row's value becomes reusable.

**Negative example (conflates deletion with cancellation).** A `Status` enum's `DELETED` value is used both for an order a customer explicitly cancelled and for an order an admin removed as a data-entry error. A reporting query that excludes `DELETED` orders now silently drops legitimately cancelled orders from revenue/history reports — the exact defect Rules → Distinguishing Adjacent Lifecycle Concepts warns against.

**Restoration example.** An "undelete" action for a soft-deleted account restores it by clearing the deleted flag with no further checks, but a different account has since been created reusing that account's now-freed email address. The restoration silently produces two active accounts with the same email — Rules → Restoration requires re-checking this exact condition before restoring.

**Cascading example, contrasted.** A `Project` is soft-deleted. Its completed `Invoice` records remain visible on their own (independent historical facts, per Rules → Cascading) — a customer's payment history shouldn't vanish. Its in-progress `DraftTask` records, which have no meaning without an active project, are explicitly cascade-deleted alongside it. The two decisions are made and documented separately, not defaulted to the same behavior.

**Boundary example (soft-delete vs. database-review / security-review).** This Skill states the query-visibility-exclusion and conditional-uniqueness patterns above. Whether a *specific* migration actually adds the right kind of constraint is `database-review`'s concern; whether a *specific* endpoint's authorization check still applies to a soft-deleted resource reachable via direct lookup is `security-review`'s concern.

## Related Skills

- `skills/database-review/SKILL.md` — Related: reviews whether a specific schema/query actually implements this Skill's structural-exclusion and conditional-uniqueness patterns; consumes this Skill as reference material, does not depend on it to function.
- `skills/security-review/SKILL.md` — Related: verifies authorization still applies to a soft-deleted record reachable outside the structural exclusion (Rules → Authorization Implications); ownership of the authorization correctness question stays with `security-review`.
- `skills/architecture-review/SKILL.md` — Related: owns the structural data-ownership/cascading decision when a soft-deletable relationship crosses a service boundary; this Skill owns the mechanics within one data store.
- `skills/api-review/SKILL.md` — Related: whether a deleted resource's contract response (`404` vs. a tombstone shape) is consistent is `api-review`'s Rules → Response Contracts and Consistency concern.
- `skills/uuid-strategy/SKILL.md` — Related: system-generated opaque identifiers are the one legitimate exception to this Skill's conditional-uniqueness reasoning (Rules → Natural-Key Uniqueness); see that Skill for identifier-strategy design itself.
