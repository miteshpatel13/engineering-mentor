# Skill Migration & Expansion Plan

## Status

Planning document only. Nothing described here has been implemented. No skill was created, rewritten, merged, split, replaced, deferred, or rejected as a file-system action by this document — every action word below (KEEP / REWRITE / MERGE / SPLIT / REPLACE / REJECT / DEFER / NEW) describes a *proposed future change*, to be executed only in a later, explicitly-authorized phase. This document does not modify `skills/`, `.claude-plugin/plugin.json`, any marketplace configuration, or any child-project runtime/discovery code.

**This is a corrected, finalized revision (Step 10A.1).** The prior version forced every audit-recommended `DEFER` candidate into `REJECT`, which the audit's own vocabulary does not support — `DEFER` and `REJECT` are not semantically interchangeable, and treating them as equivalent risked losing track of real, audit-identified value. This revision adds `DEFER` as an eighth migration action, re-classifies every affected skill against the audit's own recommendation (not invented), adds a dedicated Deferred Candidates section so that provenance is preserved rather than lost, recalculates every count in the document from the corrected classifications rather than carrying forward the prior version's arithmetic, and tightens the dependency graph to distinguish an actual technical dependency from a merely topical relationship. Sections 1–6 are otherwise substantively unchanged from the prior version; Sections 7 onward are rebuilt.

**Sources of truth, in the priority order given for this phase:** the completed `mentor-skills-source` audit (`AUDIT_REPORT.md`, `SKILL_INVENTORY.md`, `SKILL_OVERLAP.md`, `SKILL_QUALITY_REPORT.md`, `SKILL_GAPS.md`, all dated 2026-08-27, in that source repository) as primary; `docs/Skill Standard.md`, `docs/Skill Testing Standard.md`, `docs/Skill Quality Standard.md`, `docs/Skill Taxonomy.md`, `docs/Skill Ecosystem Inventory.md` next; then `docs/Child Repository Integration.md`, `docs/Governance Precedence Model.md`, `docs/Governance Evaluation.md`, `docs/Context Discovery.md`; then the 12 existing Mentor Skills read directly; then existing repository tests and fixtures. Where a claim below rests on a source lower in this list contradicting one higher up, it is flagged explicitly rather than silently resolved in favor of the higher source.

## 1. Executive Summary

**Why this migration exists.** Step 9 established *how* a Mentor Skill must be built, tested, scored, categorized, and lifecycle-managed. It did not decide *what* Engineering Mentor's Skill catalog should actually contain. Separately, the `mentor-skills-source` audit established that a 30-skill, single-project collection exists with substantial reusable engineering depth, and that Engineering Mentor's own 12 Skills are, apart from three mature exceptions, thin stubs. This document connects those two facts into an ordered, governed, dependency-aware plan — including, in this revision, an explicit place for the audit's own genuinely provisional recommendations (`DEFER`) rather than forcing every candidate into a binary keep-or-reject decision it does not deserve.

**What problem it solves.** Without this plan, the natural failure mode is an unreviewed, piecemeal import that copies the source collection's confident, absolute language directly into global Mentor content without a tier decision, without de-hardcoding project-specific facts, and without the test coverage `docs/Skill Testing Standard.md` now requires. A second, narrower failure mode — the one this revision corrects — is collapsing "not ready yet, but worth revisiting" into "worthless," which would silently discard real audit findings (`audit-logging`'s audit-trail schema, `naming-conventions`' acronym-casing discipline) that the audit itself never judged worthless.

**What the desired end state is.** A Mentor Skill catalog of 20 skills (Section 7): the three existing mature Skills unchanged, eight rewritten/replaced Skills carrying real depth where a stub exists today, and eight new Skills filling capability gaps the audit identified — every one meeting `docs/Skill Standard.md`'s structure, `docs/Skill Testing Standard.md`'s minimum fixture bar, and `docs/Skill Quality Standard.md`'s certification threshold before Production. Separately, seven source skills are explicitly preserved as `DEFER` — recorded, not lost, with a stated condition for revisiting each.

**What is explicitly out of scope for this phase.** No Skill file is created, rewritten, merged, split, replaced, or deleted. No existing Skill's behavior changes. `skills/`, `.claude-plugin/plugin.json`, and any marketplace configuration are untouched. No child-project runtime or discovery implementation is created. Architectural questions this plan surfaces but does not resolve — the `category: Review` vs. `skillType: Review` naming overlap carried over from Step 9, and a genuine three-way conflict across the audit's own documents on `data-model-overview`'s disposition — are named explicitly where they arise, not silently decided.

## 2. Current Engineering Mentor Skill Inventory

Unchanged from the prior version of this plan — restates `docs/Skill Ecosystem Inventory.md`'s Section 1 table, cross-checked against each Skill's actual file content, with **current lifecycle state** (per `docs/Skill Taxonomy.md` Section 7) and **migration action** (this plan's classification, Section 8) added.

| Skill | Path | Category | Skill Type | Maturity | Current lifecycle state | Apparent purpose (verified against file) | Test coverage | Governance classification | Quality status | Known limitations | Migration action |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `code-review` | `skills/code-review/SKILL.md` | Review | Review | Mature (~41 KB) | Pre-lifecycle — predates `docs/Skill Taxonomy.md` Section 7; functions as de facto Production content without having formally passed Draft→Implemented→Tested→Reviewed→Certified | General code review with full Child Governance integration | Narrative/regression — 26 fixtures, `tests/skill-tests/code-review/`, including the full 11–26 governance-relationship set | Full — the reference implementation `docs/Skill Standard.md` Section 4 cites | Not scored — no formal `docs/Skill Quality Standard.md` review performed on any of the 12 existing Skills | Frontmatter not yet retrofit to `category`/`skillType` fields (cosmetic, not blocking) | **KEEP** |
| `context-discovery` | `skills/context-discovery/SKILL.md` | Mentor Core | Mentor Core | Mature (~17 KB) | Pre-lifecycle, same basis | Discovers and normalizes `.mentor/` project context, read-only | Deterministic — 45/45 checks | N/A by design | Not scored | Frontmatter retrofit only | **KEEP** |
| `mentor-development` | `skills/mentor-development/SKILL.md` | Mentor Core | Mentor Core | Mature (~11 KB, prose/meta) | Pre-lifecycle, same basis | Governs how Mentor's own repository is developed and reviewed | None (meta-guidance, not a behavioral-fixture candidate) | Not applicable | Not scored | Frontmatter retrofit only | **KEEP** |
| `skill-creator` | `skills/skill-creator/SKILL.md` | Mentor Core | Mentor Core | Stub (~0.7 KB) | Pre-lifecycle | Walks the steps for creating a new Skill | None | N/A | Not scored | Predates `docs/Skill Standard.md`/`docs/Skill Taxonomy.md`; no depth on governance-tier assignment or overlap-checking | **REWRITE** |
| `skill-reviewer` | `skills/skill-reviewer/SKILL.md` | Mentor Core | Mentor Core | Stub (~0.4 KB) | Pre-lifecycle | Reviews an existing Skill for scope/clarity/contradictions/edge cases | None | N/A | Not scored | Predates `docs/Skill Quality Standard.md`'s ten dimensions | **REWRITE** |
| `skill-tester` | `skills/skill-tester/SKILL.md` | Mentor Core | Mentor Core | Stub (~0.5 KB) | Pre-lifecycle | Tests a Skill against realistic/adversarial/failure scenarios | None | N/A | Not scored | Predates `docs/Skill Testing Standard.md`'s two-tier model and minimum fixture bar | **REWRITE** |
| `api-design` | `skills/api-design/SKILL.md` | API | Review (Note A, `docs/Skill Ecosystem Inventory.md`) | Stub (~0.5 KB) | Pre-lifecycle | Evaluates an API contract | None | Not stated | Not scored | Name conflates review and authoring | **REPLACE** |
| `architecture-review` | `skills/architecture-review/SKILL.md` | Architecture | Review | Stub (~0.6 KB) | Pre-lifecycle | Evaluates boundaries/coupling/cohesion/data ownership/failure modes | None | Not stated | Not scored | One sentence of criteria, no worked example | **REWRITE** |
| `database-review` | `skills/database-review/SKILL.md` | Database | Review | Stub (~0.4 KB) | Pre-lifecycle | Evaluates schema/queries/migrations/data-integrity | None | Not stated | Not scored | One sentence of criteria, no engine-specific depth | **REWRITE** |
| `performance-review` | `skills/performance-review/SKILL.md` | Performance | Review | Stub (~0.5 KB) | Pre-lifecycle | Evidence-based performance investigation | None | Not stated | Not scored | One sentence of criteria, no measurement methodology | **REWRITE** |
| `security-review` | `skills/security-review/SKILL.md` | Security | Review | Stub (~0.5 KB) | Pre-lifecycle | Application security review across trust boundaries | None | Not stated | Not scored | One sentence of criteria, no formal finding lifecycle | **REWRITE** |
| `testing-review` | `skills/testing-review/SKILL.md` | Testing | Review | Stub (~0.5 KB) | Pre-lifecycle | Evaluates whether a test suite meaningfully protects behavior | None | Not stated | Not scored | One sentence of criteria, no testing-pyramid worked example | **REWRITE** |

## 3. Source Skill Inventory

Restates `SKILL_INVENTORY.md`, `SKILL_QUALITY_REPORT.md`, and `AUDIT_REPORT.md`'s Import Recommendations from the `mentor-skills-source` audit — the primary source of truth for this phase. No file in `mentor-skills-source` was read again or modified to produce this table. **This revision corrects seven rows from a forced `REJECT` to `DEFER`, matching the audit's own recommendation exactly** — see the Action column and the new Deferred Candidates section for full detail on each.

| # | Source skill | Apparent purpose | Source category | Quality observations | Overlap candidates | Potential Mentor mapping | Proposed action |
|---|---|---|---|---|---|---|---|
| 1 | `api-design` | URL/verb/status-code/pagination conventions | API | 4/4/5/5/4/1/4/N-A/4/0 — 403-vs-404 default stated as absolute | Strong overlap vs. Mentor `api-design` | `api-review` (renamed) + `api-contract-design` (new) | MERGE (dual destination; literal absolute choices excluded per audit's DO-NOT-IMPORT-VERBATIM guidance) |
| 2 | `api-response-standards` | Response envelope, error shape, camelCase rules (self-labeled RECOMMENDATION) | API | 4/4/5/5/5/1/4/N-A/4/0 | Strong overlap vs. Mentor `api-design` | `api-review` + `api-contract-design` | MERGE (dual destination) |
| 3 | `api-testing` | Per-endpoint test checklist | Testing | 4/4/5/5/4/1/4/N-A/4/0 | Overlap vs. Mentor `testing-review` | `testing-review` | MERGE |
| 4 | `audit-logging` | Audit-trail schema, append-only write discipline | Security (Observability secondary) | 4/4/5/5/4/1/5/N-A/3/0 | No direct Mentor counterpart named; no `SKILL_OVERLAP.md` entry of any kind | *(none — see Deferred Candidates)* | **DEFER** — corrected from the prior version's forced REJECT; audit's own Import Recommendations table places this under DEFER with no partial-merge component named anywhere |
| 5 | `authentication-authorization` | Two-identity-system auth model, JWT lifecycle, guard vs. service-layer split | Security | 4/4/5/5/5/1/5/N-A/4/0 — self-reports an `AdminRefreshToken` gap rather than silently deciding it | Overlap vs. Mentor `security-review` | `security-review` (two named principles only) | **DEFER** primary (corrected from forced REJECT) + partial MERGE (401-vs-403 discipline and "resource ownership is a service-layer check" rule → `security-review`, per `SKILL_OVERLAP.md`'s explicit carve-out) |
| 6 | `data-model-overview` | Domain map of the 51-table/11-domain schema | Database | 5/4/5/5/5/1/N-A/N-A/3/0 | Strong overlap vs. Mentor `database-review` cluster | *(contested — see below)* | **DEFER (contested)** — see the three-way conflict note below; corrected from forced REJECT, but flagged as the one item in this table where DEFER itself is disputed by another audit document |
| 7 | `database-design` | Modeling judgment: table vs. column vs. JSON | Database | 5/4/5/5/5/1/4/N-A/4/0 | Strong overlap vs. Mentor `database-review` | `database-review` | MERGE |
| 8 | `database-indexing` | Index design rules | Database/Performance | 5/4/5/5/4/1/N-A/N-A/5/0 | Strong overlap vs. Mentor `database-review` | `database-review` | MERGE |
| 9 | `database-performance` | Engine-layer performance: pooling, transactions, locking | Database/Performance | 5/4/5/5/4/1/4/N-A/4/0 | Strong overlap vs. `database-review` and `performance-review` | `database-review` (primary) + `performance-review` | MERGE |
| 10 | `db-architecture` | Foundational DB-first rules | Database/Architecture | 4/5/5/4/5/1/5/N-A/5/0 — most thorough single file | Strong overlap vs. Mentor `database-review` | `database-review` | MERGE |
| 11 | `dynamic-form-engine` | Form→Version→FieldRegistry→Renderer→Validation→ConditionalLogic→Submission architecture | Domain Patterns/Backend | 4/4/5/5/5/1/4/N-A/4/0 — "best single candidate for a genuinely reusable architecture pattern" | Strong overlap vs. `architecture-review` | `dynamic-configuration-engine` (new) | NEW |
| 12 | `e2e-testing` | Complete journey test scenarios | Testing | 4/4/5/5/4/1/4/N-A/3/0 | Overlap vs. Mentor `testing-review` | `testing-review` | MERGE |
| 13 | `enum-management` | Centralized enum registry mechanics | Database/Core Engineering | 5/4/5/5/5/1/4/N-A/5/0 | Part of `database-review` overlap cluster | `database-review` | MERGE |
| 14 | `file-storage` | File registry + storage-provider abstraction | Backend/Integrations | 4/4/5/5/4/1/5/N-A/4/0 | Partial overlap — no direct counterpart | `integration-adapter-pattern` (new, principle only) | **DEFER** primary (corrected from forced REJECT) + partial MERGE (storage-provider-abstraction principle → `integration-adapter-pattern`) |
| 15 | `idempotency` | Constraint-backed idempotency across 6 named operations | Core Engineering/Distributed Systems | 5/5/5/5/5/1/5/N-A/4/0 — "best-argued skill in the collection" | Partial overlap — no direct counterpart | `idempotency` (new, same name) | NEW |
| 16 | `integration-testing` | Cross-module workflow test coverage | Testing | 4/4/5/5/5/1/4/N-A/4/0 | Overlap vs. Mentor `testing-review` | `testing-review` | MERGE |
| 17 | `jmeter-performance-testing` | JMeter test-plan design | Performance/Testing | 4/4/5/5/4/1/4/N-A/4/0 | Overlap vs. Mentor `performance-review` | `performance-review` | MERGE |
| 18 | `naming-conventions` | Full PascalCase naming system | Core Engineering (DB-heavy) | 4/5/5/5/5/1/N-A/N-A/5/0 | No direct Mentor counterpart | *(none — see Deferred Candidates)* | **DEFER** (corrected from forced REJECT) — audit: "as a *specific* convention," with an explicit stated future trigger |
| 19 | `nestjs-architecture` | Project-specific NestJS layering | Backend/Architecture | 4/4/5/5/4/1/4/N-A/3/0 — "framework-name is in the skill's own title; least portable" | Strong overlap vs. `architecture-review` | `architecture-review` (illustrative example only) | **DEFER** primary (corrected from forced REJECT) + partial MERGE (one labeled illustrative example → `architecture-review`) |
| 20 | `notification-integration` | Provider-agnostic adapter architecture | Integrations | 4/4/5/5/4/1/4/N-A/3/0 | Partial overlap — no direct counterpart | `integration-adapter-pattern` (new, principle only) | MERGE primary (adapter-isolation principle) + **DEFER** (vendor/DLT/WABA-specific remainder — **newly flagged in this revision**; the audit's own DEFER bucket names this skill too, which the prior version's Section 3 table omitted) |
| 21 | `payment-integration` | PayU integration: server-side amount calc, webhook idempotency, refunds | Integrations/Domain Patterns | 5/5/5/5/5/1/5/N-A/4/0 — "single highest-value pattern... for a payments-handling child project" | Partial overlap — no direct counterpart | `idempotency` (new) + `integration-adapter-pattern` (new) | MERGE (dual destination, both NEW targets) |
| 22 | `performance-optimization` | Application/API-layer performance | Performance | 4/4/5/5/5/1/4/N-A/4/0 | Overlap vs. Mentor `performance-review` | `performance-review` | MERGE |
| 23 | `security` | Baseline secure-coding checklist | Security | 5/4/5/5/5/1/5/N-A/4/0 — "directly maps to Security Standards.md item-for-item, at far greater depth" | Strong overlap vs. `security-review` | `security-review` | MERGE |
| 24 | `soft-delete` | `IsDeleted`/`DeletedAt`, generated-column uniqueness pattern | Database/Domain Patterns | 5/5/5/5/5/1/5/N-A/5/0 — "single most reusable piece of domain-pattern writing in the collection" | Part of `database-review` overlap cluster | `soft-delete-and-lifecycle` (new, primary) + `database-review` | NEW primary, trimmed MERGE into `database-review` |
| 25 | `srs-scope-rules` | CONFIRMED/RECOMMENDATION/ASSUMPTION decision log | Requirements | 4/4/5/5/4/1/N-A/N-A/3/0 | No direct counterpart | `requirements-discipline` (new) | NEW |
| 26 | `swagger-openapi` | Endpoint OpenAPI-doc completeness discipline | API/Documentation | 4/4/5/5/5/1/4/N-A/4/0 | Partial overlap — Mentor `api-design` names "documentation" once | `api-contract-design` (new) | MERGE |
| 27 | `technical-documentation` | Implemented/Planned/Recommended/TBD labeling discipline | Documentation | 4/4/5/5/5/1/N-A/N-A/3/0 — "single strongest do-not-lose candidate in the whole audit" | No direct counterpart | `documentation` (new) | NEW |
| 28 | `uuid-strategy` | PK/public-UUID split, resolve-once-at-boundary | Backend/Domain Patterns | 5/4/5/5/5/1/5/N-A/4/0 | Part of `database-review` overlap cluster | `identifier-strategy` (new, primary) + `database-review`/`api-review` | NEW primary, trimmed MERGE contribution |
| 29 | `validation` | Two-layer DTO/service validation | Backend/API | 5/5/5/5/5/1/5/N-A/4/0 | Partial overlap — no direct counterpart | `api-contract-design` (new, primary) | MERGE |
| 30 | `vapt-security-testing` | Formal VAPT process, Finding→Severity→Impact→Remediation→Retest | Security/Testing | 5/5/5/5/5/1/5/N-A/4/0 — "portable almost verbatim into a Mentor security-review skill" | Strong overlap vs. `security-review` | `security-review` | MERGE |

**Three-way conflict on `data-model-overview` (#6), preserved explicitly rather than resolved:** `AUDIT_REPORT.md`'s Import Recommendations table literally lists `data-model-overview` inside the `database-design`+`db-architecture`+`data-model-overview` → `database-review` MERGE row. `AUDIT_REPORT.md` Section 16 (Final Report) item 12 separately places it under "Skills recommended for defer/reject: **Defer**." `SKILL_OVERLAP.md`'s own database-cluster row explicitly *excludes* it from that same merge: *"Leave `data-model-overview`... out entirely — it has no reuse value outside this engagement."* Three locations inside the same audit disagree with each other (MERGE vs. DEFER vs. effectively-REJECT). This plan does not silently pick a winner. It classifies `data-model-overview` as `DEFER` — the option that best preserves information pending resolution — and records it in the Deferred Candidates section with this exact conflict stated, flagging that `SKILL_OVERLAP.md`'s stronger language may mean `REJECT` is ultimately more accurate. Whoever authorizes the next phase should resolve this by reading the source file directly, not by this plan picking a side.

## 4. Capability Taxonomy

Unchanged from the prior version — grouped by `docs/Skill Taxonomy.md` Section 3's existing 20-category list. The only change in this revision is terminology: rows referencing `audit-logging`, `authentication-authorization`, `naming-conventions`, `nestjs-architecture`, `file-storage`, and `notification-integration` now read `DEFER` rather than the prior `REJECT`; no category, count, or target-state claim in this section changes as a result, since none of those six skills fed a category-level target-state claim in the first place (their generalizable contributions, where any exist, were always attributed to the *receiving* skill's category, not their own).

| Category | Mentor today | Source contributes | Target state after this plan |
|---|---|---|---|
| Mentor Core | 5 skills, 2 mature | Nothing | Unchanged in count; `skill-creator`/`skill-reviewer`/`skill-tester` gain real depth (REWRITE) |
| Core Engineering | No skill | `idempotency`, `naming-conventions`, `enum-management` touch this label in source categorization | `idempotency` lands under `Domain Patterns` (Section 7), not `Core Engineering`; `naming-conventions` DEFERRED; no `Core Engineering`-category skill proposed |
| Architecture | 1 stub | `nestjs-architecture`, `dynamic-form-engine` | `architecture-review` REWRITE; `dynamic-configuration-engine` NEW (Domain Patterns category) |
| Backend | No dedicated skill | `nestjs-architecture`, `validation`, `uuid-strategy`, `file-storage` | No dedicated Backend-category skill proposed — content distributes into `api-contract-design`, `database-review`, `identifier-strategy` |
| Frontend | No skill | No skill (source SRS explicitly scopes it out) | **Unchanged — total gap.** See Section 6 and Future Capability Expansion. |
| API | 1 stub | `api-design`, `api-response-standards`, `swagger-openapi` | `api-review` REPLACE; `api-contract-design` NEW |
| Database | 1 stub | 8-skill cluster | `database-review` REWRITE; `soft-delete-and-lifecycle` and `identifier-strategy` NEW (Domain Patterns category) |
| Security | 1 stub | `security`, `vapt-security-testing`, `authentication-authorization` | `security-review` REWRITE |
| Testing | 1 stub | `api-testing`, `e2e-testing`, `integration-testing` | `testing-review` REWRITE |
| Performance | 1 stub | `performance-optimization`, `jmeter-performance-testing`, `database-performance` | `performance-review` REWRITE |
| DevOps/Cloud | No skill | Two checklist mentions only | **Unchanged — total gap.** |
| Observability | No skill | `audit-logging` (compliance-trail only) | **Unchanged — total gap.** `audit-logging` now DEFER, not REJECT — see Deferred Candidates. |
| Distributed Systems | No skill | `idempotency`, `database-performance` touch the edge | **Unchanged — total gap** at the category level; `idempotency` lands under Domain Patterns per `docs/Skill Taxonomy.md`'s own list. |
| Data | No skill | None | **Unchanged — total gap.** |
| Integrations | No skill | `notification-integration`, `payment-integration`, `file-storage` | `integration-adapter-pattern` NEW |
| AI/LLM | No skill | None | **Unchanged — total gap.** |
| Domain Patterns | No skill | `idempotency`, `soft-delete`, `uuid-strategy`, `dynamic-form-engine` | 4 new skills |
| Documentation | No skill | `technical-documentation`, `swagger-openapi` | `documentation` NEW |
| Requirements | No skill | `srs-scope-rules` | `requirements-discipline` NEW |
| Review | `code-review` only | Nothing (0 of 30 source skills are Review-type) | Unchanged |

## 5. Overlap & Deduplication Matrix

Unchanged in substance from the prior version — restates `SKILL_OVERLAP.md`'s A–E classification. Terminology updated: where the prior version said a Strong-overlap row's non-merging remainder was "REJECT," it now says `DEFER`, matching Section 3's correction.

**A. Exact duplicates: none found**, per `SKILL_OVERLAP.md`'s explicit check.

**B. Strong overlap → MERGE, with why:** (unchanged from the prior version — see the six merge clusters: `api-design`+`api-response-standards`→`api-review`/`api-contract-design`; the 8-skill database cluster→`database-review`; `security`+`vapt-security-testing`→`security-review`; the performance cluster→`performance-review`; the testing trio→`testing-review`; `nestjs-architecture`+`dynamic-form-engine`→`architecture-review` (illustrative) / `dynamic-configuration-engine` (new)). Full reasoning retained from the prior version's Section 5; not restated here to avoid duplicating unchanged text — see Section 3 above for the corrected action labels feeding these same clusters.

**C. Partial overlap → proceed separately, boundary stated explicitly:** unchanged list (`swagger-openapi`, `technical-documentation`, `srs-scope-rules`, the three Integrations skills, `idempotency`, `naming-conventions`).

**D. Complementary, no import conflict:** unchanged (`context-discovery`; the four Mentor Core meta-skills; the 30 source skills relative to each other).

**E. No meaningful overlap:** unchanged (`srs-scope-rules`, `technical-documentation` — gap, not overlap; the three `skill-*` meta-skills — no source counterpart exists).

## 6. Capability Gap Matrix

Unchanged from the prior version — restates `SKILL_GAPS.md` Section 11. None of the six DEFER corrections in Section 3 changes a capability-area severity classification here, since `audit-logging` (Observability), `naming-conventions`/`nestjs-architecture` (already excluded from any category-level "adequately covered" claim), `authentication-authorization`/`file-storage`/`notification-integration` (their MERGE-contributed principles were already the basis for the relevant target-state claims, unaffected by the primary-action relabeling) do not change what this table says about Frontend, DevOps/Cloud, Observability, Distributed Systems, Data, AI/LLM, Requirements, Documentation, Integrations, or any other row. See the prior version's full table (retained verbatim in substance): all six total-gap categories remain total gaps with no skill proposed; Requirements, Documentation, Integrations, and the specific weak-coverage rows (security finding lifecycle, testing pyramid, load-testing methodology, idempotency, soft-delete, identifier strategy, dynamic configuration) retain their prior severity and proposed-solution assignments.

## 7. Target Skill Catalog

The complete, final-state Mentor Skill catalog — every skill that will exist once this plan is executed, including the three unchanged mature Skills (correcting the prior version's omission of them from this table, which undercounted the target catalog). 20 skills total. Testing/quality baselines are shared and stated once: **Testing requirement (shared baseline)** = narrative/regression fixtures covering every category in `docs/Skill Testing Standard.md` Section 2, plus the full governance-relationship set for every Review-type skill and any Authoring/Workflow skill that can surface a governance-classified finding. **Quality requirement (shared baseline)** = clears `docs/Skill Quality Standard.md` Section 3's certification threshold. Per-row cells name only what's additional or different. **Dependency** and **Related** are distinguished per Section 10's corrected methodology — a topical relationship is never listed as a Dependency.

| # | Skill | Category | Skill Type | Action | Priority | Source | Dependency (true, per Section 10) |
|---|---|---|---|---|---|---|---|
| 1 | `code-review` | Review | Review | KEEP | P0 | *(unchanged, existing Mentor content)* | `context-discovery` (already implemented, unchanged by this plan) |
| 2 | `context-discovery` | Mentor Core | Mentor Core | KEEP | P0 | *(unchanged, existing Mentor content)* | None |
| 3 | `mentor-development` | Mentor Core | Mentor Core | KEEP | P0 | *(unchanged, existing Mentor content)* | None |
| 4 | `skill-creator` | Mentor Core | Mentor Core | REWRITE | P0 | *(rewritten in place)* | None |
| 5 | `skill-tester` | Mentor Core | Mentor Core | REWRITE | P0 | *(rewritten in place)* | None |
| 6 | `skill-reviewer` | Mentor Core | Mentor Core | REWRITE | P0 | *(rewritten in place)* | `skill-tester` (Reviewed stage scores the Test Coverage dimension against fixtures Tested stage produced — `docs/Skill Taxonomy.md` Section 7's Tested-before-Reviewed ordering) |
| 7 | `requirements-discipline` | Requirements | Authoring/Workflow | NEW | P0 | `srs-scope-rules` | None |
| 8 | `documentation` | Documentation | Authoring/Workflow | NEW | P0 | `technical-documentation`, (secondary) `swagger-openapi` | None |
| 9 | `idempotency` | Domain Patterns | Domain Pattern | NEW | P0 | `idempotency`, (secondary) `payment-integration` | None |
| 10 | `identifier-strategy` | Domain Patterns | Domain Pattern | NEW | P1 | `uuid-strategy` | None |
| 11 | `soft-delete-and-lifecycle` | Domain Patterns | Domain Pattern | NEW | P1 | `soft-delete` | None |
| 12 | `security-review` | Security | Review | REWRITE | P0 | *(rewritten in place)*, generalized `security`+`vapt-security-testing`, two principles from `authentication-authorization` | `context-discovery`; `idempotency` (constraint-backed pattern cited as an evaluation criterion for idempotency-sensitive findings) |
| 13 | `api-review` | API | Review | REPLACE | P1 | *(renamed from Mentor's existing `api-design`)*, generalized `api-design`/`api-response-standards` | `context-discovery`; `identifier-strategy` (never-expose-internal-key finding criterion) |
| 14 | `api-contract-design` | API | Authoring/Workflow | NEW | P1 | `api-design`, `api-response-standards`, `swagger-openapi`, (secondary) `validation` | None (`validation`'s server-authoritative-recompute principle is incorporated as content, not a dependency on a separate target skill — `validation` is not itself a target skill) |
| 15 | `database-review` | Database | Review | REWRITE | P1 | *(rewritten in place)*, generalized 6-source cluster | `context-discovery`; `identifier-strategy` (never-expose-key finding); `soft-delete-and-lifecycle` (uniqueness-pattern-as-option finding) |
| 16 | `architecture-review` | Architecture | Review | REWRITE | P1 | *(rewritten in place)*, one illustrative `nestjs-architecture` example | `context-discovery` |
| 17 | `testing-review` | Testing | Review | REWRITE | P1 | *(rewritten in place)*, generalized testing trio | `context-discovery` |
| 18 | `performance-review` | Performance | Review | REWRITE | P1 | *(rewritten in place)*, generalized performance cluster | `context-discovery` |
| 19 | `integration-adapter-pattern` | Integrations | Authoring/Workflow | NEW | P2 | `notification-integration`, `payment-integration`, `file-storage` (principle only from each) | `idempotency` (webhook-delivery guidance incorporates the at-least-once-delivery idempotency rule) |
| 20 | `dynamic-configuration-engine` | Domain Patterns | Domain Pattern | NEW | P3 | `dynamic-form-engine` | None |

**Every skill above appears exactly once.** No duplicate names, no duplicate canonical destinations (each source skill's MERGE/NEW target is unique to the row it feeds — cross-checked against Section 3's 30-row table and Section 8's decision matrix below).

## 8. Migration Decision Matrix

**Action definitions, as used by this plan (eight actions):**

- **KEEP** — retained with no content or structural change proposed. (Frontmatter retrofit is not counted as a change, per `docs/Skill Standard.md`'s own Status section.)
- **REWRITE** — an existing Mentor skill's content is substantively rebuilt in place, same identity and name.
- **MERGE** — a skill's content is absorbed into another skill (existing or newly created); it does not survive as an independent artifact under its own name.
- **SPLIT** — one skill's scope is divided into two or more distinct skills because it conflates unrelated concerns. **No candidate is classified SPLIT in this plan** — `SKILL_OVERLAP.md` found scope isolation already strong throughout the source collection, and this plan's own review found no existing Mentor skill whose scope needs dividing.
- **REPLACE** — the current skill, under its current name and scope, is discontinued; its function is taken over by one or more differently-named or differently-scoped skills.
- **REJECT** — not migrated in any form, and not preserved for future reconsideration; no revisit condition is stated because none is judged to exist.
- **DEFER** *(new in this revision)* — **a valuable or potentially reusable capability that is intentionally not included in the current target catalog.** Its source and provenance are preserved (Deferred Candidates section, below), and this document states what future evidence or condition would justify revisiting it. DEFER is never treated as equivalent to REJECT: a DEFER item's content is not judged worthless, only not-yet-justified for inclusion now.
- **NEW** — a new, standalone Mentor skill is created, generalized from one or more source skills, carrying its own identity that does not currently exist in Mentor's catalog.

### 8.1 Full classification — 12 current Mentor skills

| Skill | Action |
|---|---|
| `code-review` | KEEP |
| `context-discovery` | KEEP |
| `mentor-development` | KEEP |
| `skill-creator` | REWRITE |
| `skill-reviewer` | REWRITE |
| `skill-tester` | REWRITE |
| `api-design` | REPLACE |
| `architecture-review` | REWRITE |
| `database-review` | REWRITE |
| `performance-review` | REWRITE |
| `security-review` | REWRITE |
| `testing-review` | REWRITE |

**Recalculated counts (current Mentor skills, 12 total):** KEEP = 3 (`code-review`, `context-discovery`, `mentor-development`). REWRITE = 8 (`skill-creator`, `skill-reviewer`, `skill-tester`, `architecture-review`, `database-review`, `performance-review`, `security-review`, `testing-review`). REPLACE = 1 (`api-design`). MERGE = 0. SPLIT = 0. REJECT = 0. DEFER = 0. NEW = 0. **Total: 3 + 8 + 1 = 12.** *(The prior version of this plan stated "4 KEEP, 6 REWRITE, 1 REPLACE" in its closing summary — that was a manual arithmetic error, not a re-classification; the table above was always the source of truth and is unchanged, only recounted correctly here.)*

### 8.2 Full classification — 30 source skills

| Skill | Action |
|---|---|
| `api-design` | MERGE |
| `api-response-standards` | MERGE |
| `api-testing` | MERGE |
| `audit-logging` | **DEFER** |
| `authentication-authorization` | **DEFER** primary + partial MERGE |
| `data-model-overview` | **DEFER** *(contested — see Section 3)* |
| `database-design` | MERGE |
| `database-indexing` | MERGE |
| `database-performance` | MERGE |
| `db-architecture` | MERGE |
| `dynamic-form-engine` | NEW |
| `e2e-testing` | MERGE |
| `enum-management` | MERGE |
| `file-storage` | **DEFER** primary + partial MERGE |
| `idempotency` | NEW |
| `integration-testing` | MERGE |
| `jmeter-performance-testing` | MERGE |
| `naming-conventions` | **DEFER** |
| `nestjs-architecture` | **DEFER** primary + partial MERGE |
| `notification-integration` | MERGE primary + partial **DEFER** |
| `payment-integration` | MERGE |
| `performance-optimization` | MERGE |
| `security` | MERGE |
| `soft-delete` | NEW primary + partial MERGE |
| `srs-scope-rules` | NEW |
| `swagger-openapi` | MERGE |
| `technical-documentation` | NEW |
| `uuid-strategy` | NEW primary + partial MERGE |
| `validation` | MERGE |
| `vapt-security-testing` | MERGE |

**Recalculated counts (source skills, 30 total), by primary action:** MERGE = 18 (`api-design`, `api-response-standards`, `api-testing`, `database-design`, `database-indexing`, `database-performance`, `db-architecture`, `e2e-testing`, `enum-management`, `integration-testing`, `jmeter-performance-testing`, `notification-integration`, `payment-integration`, `performance-optimization`, `security`, `swagger-openapi`, `validation`, `vapt-security-testing`). NEW = 6 (`dynamic-form-engine`, `idempotency`, `soft-delete`, `srs-scope-rules`, `technical-documentation`, `uuid-strategy`). DEFER = 6 (`audit-logging`, `authentication-authorization`, `data-model-overview`, `file-storage`, `naming-conventions`, `nestjs-architecture`). REJECT = 0. KEEP = 0. SPLIT = 0. REPLACE = 0. **Total: 18 + 6 + 6 = 30.**

**Why REJECT = 0 among the 30 source skills, stated explicitly rather than silently avoided:** after moving every genuine DEFER candidate out of the forced-REJECT bucket, no whole source skill remains that this plan judges to have zero future value under any condition. The audit's own "Reject" language (`AUDIT_REPORT.md` Section 16 item 12) targets *specific literal claims* within `api-design`/`api-response-standards` (the PATCH-only, envelope-shape, and 403-vs-404-default choices) if copied verbatim as Mandatory rules — not either skill as a whole; both skills are MERGE, with those specific claims excluded from the merge, which this plan already represents as an exclusion note rather than a separate REJECT classification. This is a reported finding, not an artifact of avoiding the REJECT bucket — if a future phase's direct reading of a DEFER item's source content finds it has no plausible revisit condition, REJECT remains available and should be used then.

**Note on `notification-integration`:** counted under MERGE (primary) because a substantial, already-identified principle (adapter isolation) actively feeds `integration-adapter-pattern`; its vendor/DLT/WABA-specific remainder is separately preserved under DEFER in Section 3 and the Deferred Candidates section, not double-counted in this primary-action tally.

## Deferred Candidates

Every skill classified `DEFER` in Sections 3 and 8, in full, so that no audit-identified value is lost from this document.

### `audit-logging`

- **Reason deferred:** `AUDIT_REPORT.md`'s Import Recommendations table places this under DEFER with no partial-merge destination named anywhere in `SKILL_OVERLAP.md` — real, high-quality content (Safety scored 5/5) with no identified seam into any current target-catalog skill.
- **Potentially reusable concepts:** audit-trail schema shape (actor/action/entity/before-after), the append-only write-discipline constraint, and its cross-reference to `soft-delete`'s deletion semantics.
- **Why not in the current target catalog:** Observability remains a total gap in both repositories (Section 6); `audit-logging` covers compliance-trail logging specifically, not the metrics/tracing/alerting depth an `observability-review` skill would need, so it is not a sufficient seed for that (unbuilt) category on its own.
- **Future evidence that would justify revisiting:** a second, differently-shaped child engagement's own audit-logging or compliance-trail requirements surfacing the same generalizable schema independently (the same "does a second, independent source confirm reusability" test this plan applies elsewhere), or a future decision to build a dedicated Observability-category skill that this content could seed.
- **Likely future destination if approved:** either its own Domain Pattern skill (`audit-trail-schema` or similar), or a section within a future `observability-review` Review-type skill, depending on which is built first.

### `authentication-authorization`

- **Reason deferred:** its core value — a two-identity-system (AdminUser RBAC vs. Doctor OTP) auth model — is this project's specific domain shape, not a generic pattern (`SKILL_OVERLAP.md`'s own assessment); its self-reported `AdminRefreshToken` gap is evidence of the source collection's honesty, not a defect, but doesn't change the model's project-specificity.
- **Potentially reusable concepts:** the 401-vs-403 discipline and the "resource ownership is a service-layer check, not a guard's job" rule — both already extracted and merged into `security-review` (Section 7) as partial contributions, separate from the deferred remainder.
- **Why not in the current target catalog (beyond the two extracted principles):** the two-identity-system model, JWT lifecycle specifics, and guard-implementation details are irreducibly tied to this one project's auth architecture; generalizing them further would either lose their concreteness or require inventing a generic auth model the audit provides no evidence for.
- **Future evidence that would justify revisiting:** a second child engagement with a structurally similar (but not identical) multi-identity auth requirement, surfacing which parts of this model generalize and which don't.
- **Likely future destination if approved:** a Domain Pattern skill on multi-identity-system authorization design, distinct from `security-review`'s evaluation posture.

### `data-model-overview` *(contested — see Section 3's full three-way conflict note)*

- **Reason deferred:** disputed. `AUDIT_REPORT.md` Section 16 places it under Defer; the same document's Import Recommendations table lists it as part of a MERGE into `database-review`; `SKILL_OVERLAP.md` argues it has "no reuse value outside this engagement" and should be left out entirely — closer to REJECT. This plan defers rather than rejects, to avoid discarding something one of the three source locations still values, but flags this as the least confident DEFER classification in this table.
- **Potentially reusable concepts:** none identified with confidence — it is a literal 51-table/11-domain schema map; if it has reusable value, the audit itself does not clearly state what generalizes from a literal schema map beyond the (already separately captured) modeling judgment in `database-design`/`db-architecture`.
- **Why not in the current target catalog:** `database-review` (Section 7) already receives the generalizable modeling judgment from `database-design`, `db-architecture`, `database-indexing`, `database-performance`, `soft-delete`, and `enum-management`; adding a literal schema map on top would be exactly the kind of project-specific content `context/core/Mentor Governance Rules.md` prohibits in global Mentor content.
- **Future evidence that would justify revisiting:** a direct read of the source file itself (not performed by this plan, which relies on the audit's own summaries per its source-priority order) to determine whether `SKILL_OVERLAP.md`'s stronger "no reuse value" claim or the Import Recommendations table's MERGE inclusion is more accurate — this is the specific unresolved step, not a hypothetical future condition.
- **Likely future destination if approved:** none proposed; if the conflict resolves toward `SKILL_OVERLAP.md`'s reading, this item should be reclassified REJECT, not migrated to DEFER-with-a-destination.

### `naming-conventions`

- **Reason deferred:** DEFERRED explicitly "as a *specific* convention" — PascalCase-everywhere is this client's confirmed decision, not a universal one, per `SKILL_OVERLAP.md`.
- **Potentially reusable concepts:** the *shape* of a naming-convention document — an acronym-casing table, an FK-disambiguation rule, generated-column naming guidance — independent of the specific PascalCase choice; the underscore-segment-matching rule for acronym casing is specifically called out by the audit as "a genuinely sharp, non-obvious rule."
- **Why not in the current target catalog:** no target-catalog skill currently has a slot for a naming-convention *template* (as opposed to one project's specific convention); building one now would mean generalizing from a single data point, which the audit's own quality methodology treats cautiously.
- **Future evidence that would justify revisiting:** `SKILL_OVERLAP.md`'s own stated trigger — "if that's ever judged broadly valuable" — i.e., a second source of naming-convention material (another child engagement, or a second generalizable example) confirming the *shape* (not the specific casing choice) is reusable.
- **Likely future destination if approved:** a new Authoring/Workflow skill, tentatively `naming-convention-template`, producing a project-specific naming document rather than asserting one globally.

### `nestjs-architecture`

- **Reason deferred:** "framework-name is in the skill's own title; least portable" per its own quality notes; low reuse outside NestJS projects.
- **Potentially reusable concepts:** the controller→service→repository layering discipline and module-boundary-mapped-to-schema-domain pattern, in the abstract — already partially captured as one labeled illustrative example inside `architecture-review` (Section 7), separate from the deferred remainder (the NestJS-specific mechanics themselves).
- **Why not in the current target catalog (beyond the one illustrative example):** the audit judges this "better suited as a child-repository example than global Mentor content" — its value is real but tied to naming a specific framework, which a global Mentor skill should not do as its primary content.
- **Future evidence that would justify revisiting:** a second, differently-framework-shaped child engagement's own layering skill surfacing the same layering discipline independently of any one framework's name — the same cross-engagement-confirmation test used for `audit-logging` and `authentication-authorization`.
- **Likely future destination if approved:** either a framework-agnostic `layered-backend-architecture` Domain Pattern skill, or simply additional illustrative examples inside `architecture-review` (already its current, partial destination).

### `file-storage`

- **Reason deferred:** DEFERRED "beyond the storage-provider-abstraction principle already covered... via a trimmed version" — i.e., the reusable core is already extracted (Section 7's `integration-adapter-pattern`); the remainder (specific `FilePurpose` enum shape, content-sniffing implementation specifics) is this project's own.
- **Potentially reusable concepts:** the `File` registry + `FilePurpose` enum pattern as a possible future addition to `integration-adapter-pattern` or a dedicated file-handling Domain Pattern, and the content-sniffed (magic-byte) MIME validation technique, which the audit calls "a correct, non-negotiable practice" independent of this project.
- **Why not in the current target catalog (beyond the one extracted principle):** the specific registry schema and enum shape are this project's implementation choice, not yet confirmed as the only reasonable shape for a generic file-handling pattern.
- **Future evidence that would justify revisiting:** a second source confirming the `File`-registry shape (not just the adapter-isolation principle, already confirmed) generalizes.
- **Likely future destination if approved:** an addition to `integration-adapter-pattern`, or its own Domain Pattern skill if the registry pattern proves to need more depth than that skill's scope allows.

### `notification-integration` *(newly flagged in this revision — omitted from the prior version's Section 3 table)*

- **Reason deferred:** DEFERRED "vendor/DLT/WABA specifics" per `AUDIT_REPORT.md`'s Import Recommendations table — the adapter-isolation principle is not deferred (it already feeds `integration-adapter-pattern`, Section 7); the India-specific regulatory/vendor mechanics (DLT registration, WABA-specific delivery tracking) are.
- **Potentially reusable concepts:** the `Broadcast`/`NotificationTemplate` schema shape and delivery-tracking/scheduling architecture, independent of the specific Email/SMS/WhatsApp/Push vendors and India-specific compliance.
- **Why not in the current target catalog (beyond the one extracted principle):** regional-compliance-specific mechanics (DLT, WABA) are definitionally not generalizable across jurisdictions without inventing content the audit provides no cross-jurisdiction evidence for.
- **Future evidence that would justify revisiting:** a second child engagement in a different regulatory jurisdiction, confirming which parts of the schema/tracking architecture generalize versus which are India-specific.
- **Likely future destination if approved:** an addition to `integration-adapter-pattern`'s worked examples, or a dedicated notification-architecture Domain Pattern skill if warranted by scale.

## 9. Priority Model

### P0 — Foundational / blocking

`code-review`, `context-discovery`, `mentor-development` are P0 as already-Production, foundational dependencies for everything else — listed for completeness of the target catalog, not as pending implementation work. `skill-creator`/`skill-tester`/`skill-reviewer` are P0 because every REWRITE and NEW skill in this catalog is meant to be built and reviewed *using* them. `requirements-discipline` and `documentation` are P0 for a process-sequencing reason, not a technical-dependency one (Section 10 correctly shows no target skill technically depends on them) — the audit's own recommended import order places them first specifically to avoid re-deriving the same labeling discipline independently inside multiple later skills. `idempotency` is P0 because it is both the single most cleanly portable, highest-value pattern in the audit and a true technical dependency of `security-review` and `integration-adapter-pattern`. `security-review` is P0 because it restates an existing Mentor Mandatory floor that is currently only a 3-line stub.

### P1 — High-value engineering capabilities

`architecture-review`, `database-review`, `performance-review`, `testing-review`, `api-review`, `api-contract-design`, `identifier-strategy`, `soft-delete-and-lifecycle`. `identifier-strategy` and `soft-delete-and-lifecycle` are true dependencies of `database-review`/`api-review` (Section 10), which places them ahead of those Review skills but not ahead of the P0 items above, since nothing at P0 depends on them.

### P2 — Useful expansion capabilities

`integration-adapter-pattern` — genuinely reusable and broadly applicable (most systems integrate with external providers), but depends on `idempotency` already being in place and nothing in the P0/P1 set depends on it.

### P3 — Optional / specialized capabilities

`dynamic-configuration-engine` — evidence-based, not an artificial placement: it is a specialized architectural pattern (registry + versioning + conditional-logic engines are not needed by every system, unlike API/database/security/testing/performance concerns, which every system has), Section 10 shows no target skill has a true dependency on it (only a topical Related link to `architecture-review`), and the audit itself frames `dynamic-form-engine` as valuable specifically *because* it's a strong worked example of a pattern — not because the pattern is broadly urgent. This is the one target-catalog skill this plan places at P3; per this phase's own instruction, P3 is used because the evidence supports it, not avoided because the catalog is small, and not manufactured where the evidence doesn't support it (no other skill in the catalog was found to fit P3 as cleanly).

**Recalculated priority counts, all 20 target skills, exactly one priority each:** P0 = 10 (`code-review`, `context-discovery`, `mentor-development`, `skill-creator`, `skill-tester`, `skill-reviewer`, `requirements-discipline`, `documentation`, `idempotency`, `security-review`). P1 = 8 (`architecture-review`, `database-review`, `performance-review`, `testing-review`, `api-review`, `api-contract-design`, `identifier-strategy`, `soft-delete-and-lifecycle`). P2 = 1 (`integration-adapter-pattern`). P3 = 1 (`dynamic-configuration-engine`). **Total: 10 + 8 + 1 + 1 = 20.**

## Implementation Batch Recommendations

Membership follows dependencies (Section 10) and priority (Section 9) — not name-matching to a batch's descriptive label. Every one of the 20 target skills appears in exactly one batch.

**Batch 0 — Skill ecosystem foundations** (8 skills): `code-review`, `context-discovery`, `mentor-development` (already Production — listed for completeness, no work required), `skill-creator`, `skill-tester`, `skill-reviewer` (REWRITE — the tooling every later batch uses), `requirements-discipline`, `documentation` (NEW — the labeling disciplines the audit's own sequencing places first to avoid rework).

**Batch 1 — Security / data-integrity foundations** (4 skills): `idempotency`, `identifier-strategy`, `soft-delete-and-lifecycle` (NEW Domain Patterns carrying data-integrity content, and true dependencies of Batch 2's Review skills — sequenced before their dependents, never after), `security-review` (REWRITE, restates an existing Mandatory floor).

**Batch 2 — API / database / architecture** (4 skills): `api-review` (REPLACE), `api-contract-design` (NEW), `database-review` (REWRITE), `architecture-review` (REWRITE) — each depends only on Batch 0/1 skills, per Section 10.

**Batch 3 — Testing / performance** (2 skills): `testing-review`, `performance-review` (both REWRITE, depend only on `context-discovery` from Batch 0).

**Batch 4 — Integration / configuration patterns** (1 skill): `integration-adapter-pattern` (NEW, depends on `idempotency` from Batch 1).

**Batch 5 — Deferred candidates that become justified** (0 skills currently): intentionally empty. None of the seven Deferred Candidates above currently has its stated revisit condition satisfied. This batch exists as a placeholder — a DEFER item moves here only if and when a future phase confirms its specific "future evidence" trigger (Deferred Candidates section, above), not by default schedule.

**Batch 6 — Future capability expansion** (1 skill): `dynamic-configuration-engine` (NEW, P3, no true dependents). **Note:** this batch is placed last for `dynamic-configuration-engine` despite its name topically resembling Batch 4's "configuration patterns," because batch membership here follows priority and dependency (Section 9/10), not keyword-matching to a batch's descriptive label — no target skill depends on it, so nothing is blocked by sequencing it last. The six total-gap capability areas (Frontend, DevOps/Cloud, Observability, Distributed Systems, Data, AI/LLM) are not skills and have nothing to sequence into a batch — see Future Capability Expansion, below, which is a roadmap, not an implementation batch.

**Batch membership check:** 8 + 4 + 4 + 2 + 1 + 0 + 1 = 20. Every target skill accounted for exactly once.

## 10. Skill Dependency Graph

**A topical relationship is not a dependency.** This plan distinguishes them explicitly: a **Dependency** exists only where the downstream skill's own Rules, Workflow, or governance-classified findings actually require the upstream skill's established output, contract, or rule to function correctly — not merely where both skills touch a similar subject, originate from the same audit cluster, or are conventionally used in sequence. Everything else is labeled **Related**.

### 10.1 Dependencies (true — 13 edges)

| Upstream | Downstream | Why this is a real dependency, not a topical link |
|---|---|---|
| `context-discovery` | `api-review`, `database-review`, `security-review`, `performance-review`, `testing-review`, `architecture-review` | `docs/Skill Standard.md` Section 3 posture 3 — every Review-type skill MUST invoke `context-discovery` before applying repository-sensitive guidance; this is a stated requirement, not a convention |
| `context-discovery` | `code-review` | Already true today, unchanged by this plan — `code-review`'s existing Workflow step 0 |
| `skill-tester` | `skill-reviewer` | `docs/Skill Taxonomy.md` Section 7's Tested-before-Reviewed ordering: the Reviewed stage scores the Test Coverage dimension (`docs/Skill Quality Standard.md`) against fixtures the Tested stage produced — Reviewed cannot meaningfully happen without Tested's output |
| `identifier-strategy` | `database-review` | `database-review`'s never-expose-internal-key finding criterion is defined by, and cites, `identifier-strategy`'s established rule |
| `identifier-strategy` | `api-review` | Same never-expose-internal-key finding criterion, applied to API responses specifically |
| `soft-delete-and-lifecycle` | `database-review` | `database-review`'s uniqueness-under-soft-delete finding criterion is defined by, and cites, this skill's documented pattern-as-one-option |
| `idempotency` | `security-review` | `security-review`'s idempotency-sensitive findings (e.g. webhook replay, duplicate-submission handling) are defined against this skill's established constraint-backed rule |
| `idempotency` | `integration-adapter-pattern` | A webhook-driven adapter's delivery-handling guidance directly incorporates this skill's at-least-once-delivery idempotency rule, not merely references it topically |

**13 edges total** (context-discovery→6 Review skills counted individually + code-review = 7 edges from context-discovery; skill-tester→skill-reviewer = 1; identifier-strategy→2 = 2; soft-delete-and-lifecycle→1 = 1; idempotency→2 = 2; total 7+1+2+1+2=13).

### 10.2 Related (topical, sequencing, or Complementary-pairing — not a dependency)

| Skill | Related to | Why this is Related, not a Dependency |
|---|---|---|
| `skill-creator` | `skill-tester`, `skill-reviewer` | Produces the artifact they operate on; neither requires `skill-creator`'s specific output format to function |
| `context-discovery` | `requirements-discipline`, `documentation`, `api-contract-design`, `integration-adapter-pattern` | Posture 2 (`docs/Skill Standard.md` Section 3) — "benefits from repository context but degrades gracefully without it," not a hard requirement |
| `idempotency` | `identifier-strategy`, `soft-delete-and-lifecycle` | Same audit cluster ("the DB-identity-and-lifecycle cluster, tightly coupled... best generalized together" per `AUDIT_REPORT.md`), sequenced together for authoring convenience — no skill's Rules actually cite another's contract here |
| `identifier-strategy` | `dynamic-configuration-engine` | A registry pattern needs *some* identifier scheme generically — true of nearly any data model, not a dependency on this specific skill's contract |
| `dynamic-configuration-engine` | `architecture-review` | Folded in as one *illustrative example*, not a finding criterion `architecture-review`'s Rules actually require |
| `database-review` | `performance-review` | Useful context (query/index findings often inform a performance investigation) but `performance-review` functions independently — it does not require `database-review`'s output |
| `api-review` | `api-contract-design` | Complementary pairing per `docs/Skill Taxonomy.md` Section 5 class D — "occupies clearly different ground... cross-reference in Related Skills, no boundary statement needed beyond the type distinction itself." The Taxonomy's own vocabulary for this exact Review/Authoring pairing is "Related," not "Dependency." |

### 10.3 Simplified dependency-only graph

```text
context-discovery
       │  (true dependency — posture 3, MUST invoke)
       ├── api-review
       ├── database-review
       ├── security-review
       ├── performance-review
       ├── testing-review
       ├── architecture-review
       └── code-review          (already true today, unchanged)

skill-tester ──▶ skill-reviewer  (Tested-before-Reviewed, Test Coverage scoring)

identifier-strategy ──▶ database-review
identifier-strategy ──▶ api-review
soft-delete-and-lifecycle ──▶ database-review

idempotency ──▶ security-review
idempotency ──▶ integration-adapter-pattern
```

`mentor-development` is deliberately absent from this graph — it governs how every Skill below it is built and reviewed (an authority relationship), which this plan does not model as a Dependency edge, consistent with the definition above: `mentor-development`'s content is not consumed as a contract by any other skill's Rules, it is the standard those Rules are reviewed against.

## Future Capability Expansion

**This is not implementation.** No skill described in this section is created, and none is added to the Target Skill Catalog (Section 7) or any Implementation Batch, above. This section separates a broader set of engineering capability areas — beyond the 20 categories `docs/Skill Taxonomy.md` already defines — into where each currently stands, per this phase's own no-invention discipline (Section 11 below): "we know this capability is needed" is kept explicitly distinct from "we currently have enough authoritative material to implement this skill."

- **A. Covered by current plan** — a target skill (Section 7) already substantively addresses this.
- **B. Covered weakly** — some real material exists (a checklist, a stub, an adjacent Domain Pattern's edge-case relevance), but no dedicated skill provides real depth.
- **C. Completely missing, but plausibly buildable from established general practice** — no skill exists or is proposed, but the domain is well-established, non-proprietary software-engineering practice (not a specific vendor/framework), such that a future skill could responsibly be drafted without needing genuinely new domain research.
- **D. Requires research** — no skill exists or is proposed, and responsibly building one would require real external/domain/vendor-specific source material neither repository currently has, per the no-invention principle.

| Area | Classification | Basis |
|---|---|---|
| Frontend (general) | D | Total gap per audit; source SRS explicitly scoped it out; would need genuine frontend-engineering source material |
| React | D | No source material in either repository |
| Angular | D | No source material in either repository |
| Next.js | D | No source material in either repository |
| TypeScript | D | No source material; `naming-conventions`' own note about "future TypeScript identifier naming" is the only trace, and that skill is itself DEFERRED |
| Node.js | D | No source material beyond the DEFERRED, framework-named `nestjs-architecture` |
| Backend engineering (general, framework-agnostic) | **A** | Collectively addressed by `architecture-review`, `database-review`, `api-review`/`api-contract-design`, `identifier-strategy`, `idempotency` (Section 7) |
| GraphQL | B | Named explicitly in `api-review`'s own scope/description ("REST/GraphQL design decisions"); no real GraphQL-specific depth exists anywhere — all actual source material is REST-specific |
| DevOps (general) | D | Total gap per audit, beyond two non-skill checklist/SOP documents |
| Docker | D | No source material in either repository |
| Kubernetes | D | No source material in either repository |
| AWS / Cloud | D | No source material in either repository |
| CI/CD | B | `context/checklists/Release Checklist.md`, `context/sop/Production Release SOP.md` exist (bullet lists only, no skill depth) |
| Infrastructure as Code | D | No source material in either repository |
| Observability | D | Total gap per audit; `audit-logging` (DEFERRED) covers compliance-trail logging only, not metrics/tracing/alerting — see Section 6, unchanged at the category level |
| Distributed Systems | B | `idempotency` touches adjacent ground (constraint-backed correctness under concurrency, at-least-once delivery reasoning); multi-service consensus, sagas, and outbox patterns remain uncovered. *Note: this differs from Section 6's category-level gap matrix only in granularity — no `Distributed Systems`-category skill exists or is proposed; Section 6 remains accurate at that level.* |
| Event-driven architecture | D | No source material in either repository |
| Messaging / queues | B | Same `idempotency`/`integration-adapter-pattern` adjacency as Distributed Systems, above; no dedicated messaging-semantics skill |
| Caching | **A** | `performance-review` REWRITE (Section 7) explicitly incorporates the never-cache-list principle from `performance-optimization` |
| Reliability / resilience | B | `idempotency` and Mentor's governance model touch reliability-adjacent concerns; no dedicated circuit-breaker/retry/backoff skill |
| Data engineering | D | Total gap per audit |
| AI/LLM engineering | D | Total gap per audit, despite Mentor itself being AI-agent-consumed — `context/core/Engineering Principles.md` item 15 is the only trace, one bullet |
| Accessibility | D | Frontend's total gap extends here; no source material |
| Developer Experience | C | Not a `docs/Skill Taxonomy.md` category today; no skill addresses DX as its own capability, but this is closer to extendable-from-existing-principles territory than a domain requiring new external research |
| Git / source-control engineering | C | Mentor's own operational conventions already model reasonable practice; a skill could plausibly be drafted from well-established, non-proprietary practice, but none exists or is proposed here |
| Monorepo engineering | C | Same basis as Git/source-control — well-established general practice exists to draw from, but nothing has been built or proposed |

**Tally: A = 2, B = 5, C = 3, D = 16.** (26 areas total, matching the list evaluated, per the instruction's minimum-evaluation set.)

## 11. The No-Invention Principle, Restated for This Plan

Two distinct claims must never be conflated, throughout this document and any future phase built on it: **"we know this capability is needed"** (an observation about engineering practice generally, or about a gap `SKILL_GAPS.md` or this plan's own Section 6/Future Capability Expansion identifies) is not the same claim as **"we currently have enough authoritative material to implement this skill responsibly"** (a claim about whether real, grounded source content exists to build from, per `context/core/Mentor Operating Model.md`'s No Invention Rule, extended by `docs/Skill Taxonomy.md` Section 7 to Skill content specifically, not just repository facts). Every `D` classification in Future Capability Expansion is a case where the first claim is true and the second is explicitly not — that gap is the reason nothing is proposed there. Every target-catalog skill in Section 7, by contrast, is a case where both claims hold: a real capability need, backed by real, audited source material to generalize from.

## Current vs. Target — Final Numbers

**Current Mentor skills: 12.**
**Source skills audited: 30.**
**Target Mentor skills: 20.**
**Net increase: +8** (20 − 12 = 8; verified against Section 7's 20-row table and Section 8.1's 12-row current-skill table).

**By Skill Type, target catalog (20 total, verified against Section 7):**
- Mentor Core: 5 (`context-discovery`, `mentor-development`, `skill-creator`, `skill-tester`, `skill-reviewer`)
- Review: 7 (`code-review`, `api-review`, `database-review`, `security-review`, `performance-review`, `testing-review`, `architecture-review`)
- Authoring/Workflow: 4 (`requirements-discipline`, `documentation`, `api-contract-design`, `integration-adapter-pattern`)
- Domain Pattern: 4 (`idempotency`, `identifier-strategy`, `soft-delete-and-lifecycle`, `dynamic-configuration-engine`)
- **Sum check: 5 + 7 + 4 + 4 = 20.** ✓

**By category, target catalog (20 total):**
- Mentor Core: 5 · Review: 1 (`code-review`) · API: 2 (`api-review`, `api-contract-design`) · Architecture: 1 · Database: 1 · Security: 1 · Testing: 1 · Performance: 1 · Requirements: 1 · Documentation: 1 · Domain Patterns: 4 · Integrations: 1
- **Sum check: 5+1+2+1+1+1+1+1+1+1+4+1 = 20.** ✓
- Categories with zero target skills: Core Engineering, Backend, Frontend, DevOps/Cloud, Observability, Distributed Systems, Data, AI/LLM — **8 categories**, matching `docs/Skill Taxonomy.md` Section 3's 20-category total (12 covered + 8 uncovered = 20 categories). ✓

## Final Consistency Audit

Checked immediately before finishing, per this phase's explicit requirement:

- ✅ **No duplicate target skill names** — Section 7's 20 rows checked against each other; all distinct.
- ✅ **No duplicate canonical destinations** — every MERGE/NEW destination in Section 3's 30-row table cross-checked against Section 7's 20-row catalog; no two source skills claim to be the sole originator of the same target skill without both being listed (e.g., `api-review` correctly shows two contributing source skills, not a conflict).
- ✅ **Every source skill has exactly one primary action** — Section 8.2's 30-row table; dual/secondary contributions are explicitly marked as secondary, never counted as a second primary action.
- ✅ **Every DEFER candidate is explicitly preserved** — all 7 (`audit-logging`, `authentication-authorization`, `data-model-overview`, `file-storage`, `naming-conventions`, `nestjs-architecture`, `notification-integration`) have full Deferred Candidates entries.
- ✅ **Every target skill has category** — Section 7, column 3, no blanks.
- ✅ **Every target skill has skillType** — Section 7, column 4, no blanks.
- ✅ **Every target skill has priority** — Section 9's recalculated table, all 20, exactly one each.
- ✅ **Every target skill has dependency status** — Section 7's Dependency column plus Section 10.1/10.2's exhaustive Dependency/Related tables; every skill in Section 7 either has a stated Dependency, a stated Related link, or explicitly None.
- ✅ **Every target skill has testing expectations** — Section 7's shared baseline paragraph plus per-row exceptions where applicable.
- ✅ **Governance terminology matches existing governance documents** — Mandatory/Configurable/Advisory/Informational and Mentor Mandatory/Child Mandatory usage throughout is unchanged from `docs/Governance Precedence Model.md`/`docs/Child Repository Integration.md` Section 7's own vocabulary; no new term introduced.
- ✅ **No unsupported source claims** — every quality score, quote, and recommendation traces to a specific audit document; no capability was proposed without a named source (Future Capability Expansion's `D` rows are the explicit record of where source material does not exist).
- ✅ **No silent resolution of conflicts** — the `data-model-overview` three-way conflict (Section 3), the DEFER-vs-REJECT vocabulary question this revision itself resolves *by adding DEFER* (not by picking a side within the old vocabulary), and the `category: Review`/`skillType: Review` overlap (unchanged from Step 9) are all stated, not decided.
- ✅ **No skill implementation** — no file under `skills/` was created, edited, renamed, or deleted by this phase.
- ✅ **No production skill modification** — confirmed via `git status` below.

## Notes on This Plan's Scope and Open Items

1. **The `category: Review` vs. `skillType: Review` naming overlap**, carried forward from Step 9 and resurfacing at `api-review`'s catalog entry (Section 7), remains unresolved by this plan.
2. **`data-model-overview`'s three-way conflict** (Section 3, Deferred Candidates) is the one DEFER classification in this plan that is itself contested by the audit's own documents — flagged there in full, not resolved here.
3. **No skill in this plan has been implemented.** Every dependency, priority, batch assignment, and governance-tier expectation is this plan's own forward-looking judgment, subject to correction once a skill actually reaches the Reviewed stage and is checked against real content.
4. **Whether this phase's action vocabulary needed a `DEFER` word was itself an open question in the prior version of this plan; this revision resolves that specific question by adding it**, per the explicit instruction for this pass. No other vocabulary gap is currently known.
