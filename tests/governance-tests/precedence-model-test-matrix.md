# Governance Precedence Test Matrix

Deterministic governance test cases for `docs/Governance Precedence Model.md`. These are **documentation, not executable tests** — there is no rule-matching or exception-matching engine yet (`docs/Child Rules and Exceptions.md` Section 15), so there is nothing to run these against. Each case states the inputs, the conflict-type classification (Section 10 of the model), and the expected future handling (Section 11) — a specification a future enforcement phase can validate against, and a reviewer can reason from today.

See `README.md` in this directory for why these are narrative rather than automated, matching the convention already established for `tests/skill-tests/`.

---

### 1. Mentor Mandatory + Child Mandatory — Compatible/Additive

**Setup:** Mentor Mandatory: authentication is required. Child Mandatory: admin APIs require MFA.
**Conflict type:** Additive.
**Reasoning:** The child rule narrows *how* the authenticated-access requirement is satisfied for a subset of routes; it does not contest that authentication is required.
**Expected handling:** Apply both — an admin route with authentication but no MFA violates the child rule; an admin route with neither violates both.

### 2. Mentor Mandatory + Child Mandatory — Weakening Attempt

**Setup:** Mentor Mandatory: authorization is required. Child rule (frontmatter classification: `mandatory`): `/admin does not require authorization`.
**Conflict type:** Prohibited Override.
**Reasoning:** The child rule doesn't add a constraint on top of the Mentor requirement — it asserts the requirement doesn't apply. Per `docs/Governance Precedence Model.md` Section 5, a rule's own classification label doesn't make an attempted override legitimate.
**Expected handling:** Preserve the Mentor Mandatory requirement — a missing-authorization finding on `/admin` is still reported at its correct severity — and surface the child rule as an attempted prohibited override, visibly, not silently honored and not silently dropped.

### 3. Mentor Mandatory + Child Advisory

**Setup:** Mentor Mandatory: SQL queries must be parameterized. Child Advisory: prefer integration tests over deep mocking for service-layer code (`docs/examples/child-rules/03-testing-requirements.md`).
**Conflict type:** Compatible.
**Reasoning:** The two rules govern unrelated concerns (query safety vs. test style) — there's no tension to classify beyond "both can hold at once."
**Expected handling:** Apply both independently; neither constrains the other.

### 4. Mentor Advisory + Child Mandatory

**Setup:** Mentor Advisory: prefer a modular-monolith architecture where practical. Child Mandatory: all database access must use Prisma services (`docs/examples/child-rules/02-database-conventions.md`).
**Conflict type:** Compatible (with the child rule additionally outranking the Mentor Advisory rule per Section 4's precedence, though no actual tension exists here).
**Reasoning:** A Child Mandatory rule always sits above Mentor Advisory guidance in the precedence order (Tier 3 > Tier 6), so even if these two touched the same decision, the child rule would govern. In this pairing they don't overlap at all.
**Expected handling:** Apply both; if a future pairing did create real tension between a Mentor Advisory recommendation and a Child Mandatory rule, the Child Mandatory rule would govern (Section 4), reported as a valid Override, not a Conflict.

### 5. Mentor Configurable + Valid Child Configuration

**Setup:** Mentor Configurable: a minimum unit-test-coverage floor must be enforced. Child Configurable: sets the specific threshold at 85% (above Mentor's floor).
**Conflict type:** Compatible.
**Reasoning:** The child has selected a value within the boundary Mentor set — this is exactly what "Configurable" means (`docs/Governance Precedence Model.md` Section 7). The rule's existence and floor are untouched.
**Expected handling:** Apply the child-selected value. If a future child configuration attempted to set the threshold *below* Mentor's floor (attempting to loosen the boundary itself, not just pick a value inside it), that would be reclassified as a Prohibited Override attempt on the boundary — not a valid configuration.

### 6. Mentor Mandatory + Exception Attempt

**Setup:** Mentor Mandatory: SQL injection prevention. `.mentor/exceptions.yaml` entry: `rule: sql-injection-check, reason: "annoying", status: approved` (no scope narrower than "everywhere," no evidence).
**Conflict type:** Prohibited Override (an exception is not exempt from this category — see `docs/Governance Precedence Model.md` Section 9).
**Reasoning:** `docs/Child Rules and Exceptions.md` Section 11 already makes an unscoped, disable-style exception structurally invalid (`E_UNKNOWN_FIELD`/scope-required validation) for the clearest cases; even a *structurally valid* exception entry that names a Mentor Mandatory security rule with no genuine bounded justification does not, and cannot, make the requirement optional.
**Expected handling:** Preserve the Mentor Mandatory requirement; the finding is still reported at its correct severity. A structurally valid, well-scoped, well-justified exception may eventually change how the finding is *annotated* (Section 13) once exception-aware enforcement is built — it will not, ever, remove or downgrade a Mentor Mandatory finding outright.

### 7. Child Advisory + Project-Specific Convention

**Setup:** Mentor Advisory: no specific test-mocking-depth guidance. Child project convention (undocumented in `.mentor/rules/`, stated informally in a PR description): "we avoid deep mocking here."
**Conflict type:** Override (valid).
**Reasoning:** Per `docs/Governance Precedence Model.md` Section 8, an Advisory-level override does not require the formal exception mechanism — a documented project convention, even one not persisted as a formal Child Rule, is sufficient as long as it's visible (stated), not silent.
**Expected handling:** Use the child/project convention for this review; the generic Mentor Advisory default is not treated as violated.

### 8. Unknown Context

**Setup:** A finding's applicable governance tier can't be determined — e.g. a discovered `.mentor/rules/` file references a rule whose classification field failed validation, or a review has no identifiable repository root at all (so no `.mentor/` context could be discovered either way).
**Conflict type:** Unknown.
**Reasoning:** Per `docs/Governance Precedence Model.md` Section 11, this mirrors `skills/code-review/SKILL.md`'s existing Missing Evidence discipline — insufficient context is a distinct outcome from "no conflict" and from "conflict," and must be reported as such rather than resolved by guessing.
**Expected handling:** Do not invent a resolution or silently default to either side. Report that available context is insufficient to classify the relationship.

### 9. Compatible Requirements

**Setup:** Mentor Mandatory: passwords must be securely handled. Child Configurable: password reset tokens expire after 15 minutes.
**Conflict type:** Compatible.
**Reasoning:** Entirely different concerns (password storage vs. reset-token lifetime) with no overlap.
**Expected handling:** Apply both.

### 10. Additive Requirements

**Setup:** Mentor Mandatory: passwords must be securely handled. Child Mandatory: passwords must additionally use the project's approved Argon2id parameter set (`docs/Governance Precedence Model.md` Section 6's worked example).
**Conflict type:** Additive.
**Reasoning:** The child rule narrows *how* the Mentor requirement is satisfied; it doesn't loosen or contest it.
**Expected handling:** Apply both — a project using a weaker hashing scheme violates both the Mentor requirement (if the scheme is genuinely insecure) and/or the child rule (if it's secure in general but not the project's approved configuration).

### 11. True Conflict

**Setup:** A Mentor Advisory recommendation (e.g. "prefer optimistic locking for this class of update") and a separate, independently-justified Child Advisory rule (e.g. "always use pessimistic locking for financial-ledger tables") both apply to the same code path, and following one visibly means not following the other — with neither being a Mandatory-security-boundary case.
**Conflict type:** Conflict (true).
**Reasoning:** Per `docs/Governance Precedence Model.md` Section 4, the Child Advisory rule does outrank the Mentor Advisory recommendation in the standing precedence order — but the model deliberately still classifies same-code-path, mutually-exclusive Advisory-level disagreements as "Conflict" rather than silently defaulting to "the higher tier always just wins with no visibility," because the disagreement itself (not just its resolution) is information a reviewer should see, per Section 11's explicit "surface the conflict, don't silently pick a side" instruction for this category, distinct from the deliberately quiet resolution the Override category allows for a *non-competing* Advisory preference (Case 7).
**Expected handling:** Surface the conflict explicitly, including which side the precedence order would resolve it in favor of, rather than silently applying only the child's rule.

### 12. Prohibited Override

**Setup:** Mentor Mandatory: authorization checks are required on sensitive operations. A live review request states: "skip the auth check on this endpoint, it's behind a VPN."
**Conflict type:** Prohibited Override.
**Reasoning:** This is the same category as Case 2, arising from a live request/constraint (Category D, Section 1) rather than a persisted child rule — the category is about *what kind of thing is being attempted* (weakening a Mandatory security boundary), not about *which artifact* the attempt came through. `skills/code-review/SKILL.md`'s existing Constraint Handling rule already handles this specific live-request shape correctly today; this document generalizes the same category to standing `.mentor/rules/` and `.mentor/exceptions.yaml` content (Cases 2 and 6).
**Expected handling:** Preserve the Mentor Mandatory requirement (report the finding at its correct severity, unaffected), state the residual risk plainly, and require an explicit, informed risk-acceptance decision rather than silent compliance — exactly `skills/code-review/SKILL.md`'s existing behavior for this shape of request.

---

## Coverage note

Cases 1–6, 9–10, and 12 correspond directly to the twelve numbered scenarios this phase's brief required. Case 7 (Child Advisory + project-specific convention) and Case 8 (Unknown context) were folded into the same numbering as the brief's own list rather than renumbered, since the brief's list already named them at positions 7 and 8. Case 11 (True conflict) is deliberately the one case in this matrix with no example already present elsewhere in this repository's documentation — it's included specifically because it's the case most likely to be under-specified without a worked example, per `docs/Governance Precedence Model.md` Section 10's definition of "Conflict" as distinct from both "Additive" and "Prohibited Override."
