---
name: security-review
description: Perform a practical application security review covering trust boundaries, authentication, authorization, input validation, injection, secrets, and abuse scenarios. Use when reviewing security-sensitive code, a new endpoint handling untrusted input, or assessing a change for vulnerability risk.
category: Security
skillType: Review
---

# Security Review

## Purpose

Produce a structured, evidence-based security review of a change, endpoint, or component — trust boundaries, authentication, authorization, input validation, injection classes, secrets handling, and abuse scenarios — grounded in what the material actually shows rather than a generic vulnerability checklist applied without evidence. This Skill exists separately from `skills/code-review/SKILL.md` because security defects have a distinct failure mode (silent until exploited, often invisible without adversarial thinking about how a boundary could be crossed) that warrants a dedicated, systematically-applied review rather than being one concern among many in a general review pass.

## Scope

**In scope:** trust boundaries and where untrusted input enters the system; authentication mechanisms and their weaknesses; authorization and access-control correctness (including IDOR/BOLA — broken object-level authorization); input validation and injection classes (SQL/NoSQL, command, path traversal, XSS, SSRF, insecure deserialization); secrets and credential handling; sensitive-data exposure in logs, errors, or responses; secure logging (log-injection resistance and security-event logging, distinct from what must never be logged); file-upload safety; dependency risk for a vulnerable, reachable dependency; and abuse/misuse scenarios (rate limiting, resource exhaustion) for the specific surface under review.

**Out of scope:** database schema/migration/data-integrity correctness that isn't itself a security boundary (`skills/database-review/SKILL.md`); measured performance characteristics, including of a rate-limiting mechanism's actual throughput (`skills/performance-review/SKILL.md`); and general code-level defects with no security implication (`skills/code-review/SKILL.md`).

## When to Use

Use when: reviewing security-sensitive code — authentication, authorization, session/token handling, cryptography, file upload, or any code processing untrusted input; reviewing a new endpoint or integration boundary; or assessing a proposed change for vulnerability risk before it ships.

Do not use as a substitute for a full penetration test or a formal VAPT process where one is required — this Skill performs a practical, evidence-based review of the material provided, not dynamic exploitation testing.

## Required Context

- The code, endpoint definition, or design under review, with enough surrounding context to identify where trust boundaries actually sit — a snippet with no visibility into what calls it or what authenticates the caller cannot be fully assessed for authorization correctness.
- The target repository's Normalized Project Context (`skills/context-discovery/SKILL.md`), including its declared stack and any declared child rules/exceptions relevant to security posture.

## Workflow

1. Invoke `skills/context-discovery/SKILL.md` to obtain the Normalized Project Context before reasoning about any stack-specific security mechanism (e.g. a framework's built-in CSRF protection).
2. Identify the trust boundaries actually present in the material — where does untrusted input enter, what authenticates the caller, what authorizes the specific action on the specific resource. If this can't be determined from what's provided, proceed to Failure Handling for that specific boundary rather than assuming it's handled elsewhere.
3. Evaluate each Rules category below against the material, applying OWASP Top 10 / OWASP API Security Top 10 categories as a checklist of *things to actively look for*, not a checklist to mechanically confirm present — absence of evidence that a category applies is not evidence the code is vulnerable to it. `context/standards/Security Standards.md` is the grounding checklist the Rules below instantiate; `context/checklists/Security Checklist.md` covers the same categories as a verification aid, not a replacement for judgment.
4. Consider whether the security control can be bypassed through an alternate path — a different endpoint, HTTP method, parameter, or a direct API call that skips a frontend-only check — since frontend validation is never treated as the security control (Rules → Backend Enforcement).
5. When step 1 obtained declared child rules and/or exceptions, apply the Child Governance discipline (Rules, below) — with particular attention to any exception targeting a security-classified Mentor Mandatory requirement (`docs/Governance Precedence Model.md` Section 9's prohibited-override treatment for security exceptions).
6. Produce the review per Expected Output.

## Rules

### Trust Boundaries and Input Validation

Identify every point where untrusted input crosses into the system and confirm it is validated/sanitized before use, not merely before display. Flag validation that exists only client-side with no server-side enforcement of the same rule.

### Authentication vs. Authorization

Distinguish these explicitly: authentication failures (who the caller is) are a different class of defect from authorization failures (what the caller is allowed to do) and must not be conflated in a finding. Flag missing or bypassable authentication, and separately flag missing or incorrect authorization — including IDOR/BOLA, where an authenticated caller can access or modify a resource they don't own by manipulating an identifier.

### Injection Classes

Evaluate for SQL/NoSQL injection, command injection, path traversal, XSS, SSRF, and insecure deserialization wherever the material shows untrusted input reaching a sink for the corresponding operation (a query, a shell command, a file path, an HTML render, an outbound request, a deserializer). Do not report an injection finding against a sink the material doesn't actually show untrusted input reaching.

### Backend Enforcement

Never treat a frontend-only validation or authorization check as sufficient — every security-sensitive rule must be enforced on the backend regardless of what the frontend also does. Consider explicitly whether a control can be bypassed via an alternate endpoint, HTTP method, or direct API request that skips the frontend entirely.

### Secrets and Sensitive Data

Flag a hard-coded secret, API key, or credential, and flag sensitive data (secrets, tokens, PII) exposed through logs, error responses, or stack traces. A production error response must not expose implementation detail, stack traces, or database errors to the client.

### Abuse and Resource Exhaustion

Flag an endpoint accepting untrusted input with no rate limiting or resource bound where abuse is plausible (unbounded file upload size, unbounded query result size, no request-rate control on an expensive operation).

### File-Upload Safety

Flag a file-upload endpoint that trusts the client-supplied filename or declared `Content-Type` without server-side verification of the actual file content — a renamed executable with a spoofed extension or content-type is not caught by trusting client-supplied metadata alone. Flag a filename used directly in a file-system path with no sanitization against path traversal (`../`) or embedded directory separators. Flag uploaded files stored inside the web-served root, or in a location/configuration where an uploaded file could be executed (e.g. a `.php`/`.js` upload served directly by the web server) — uploads should be stored outside the webroot, or under a configuration that guarantees they are never executed, with a generated filename rather than the client-supplied one. Flag the absence of an enforced maximum file size on an upload endpoint that accepts untrusted input.

### Dependency Risk

Flag a dependency with a known vulnerability (a CVE or equivalent advisory) when the material shows the vulnerable code path is reachable from untrusted input or a security-sensitive operation. Per Edge Cases, a dependency merely *having* a known CVE is not itself a Severity-tagged finding — only evidence that the vulnerable path is actually reachable in this codebase's usage makes it one; state the distinction explicitly rather than treating "has a CVE" as sufficient on its own.

### Secure Logging

Flag untrusted input written into a log entry with no sanitization against log injection/forging — a user-controlled string containing newline or control characters can fabricate what appears to be a separate, legitimate log line. This is distinct from Secrets and Sensitive Data (above), which governs what must never be logged; this Rule governs how logged input is written. Separately, flag the absence of logging for security-relevant events (authentication failures, authorization denials, privilege changes) on a security-sensitive surface, where an incident investigation would otherwise have no record to work from.

### Child Governance, Including Security Exceptions

When context discovery obtained parsed child rules and/or exceptions, apply the same discipline `skills/code-review/SKILL.md`'s Child Governance section defines. A child rule or exception that attempts to weaken a security- or safety-classified Mentor Mandatory requirement is always a Prohibited Override (`docs/Governance Precedence Model.md` Section 9) — the underlying finding is preserved and reported at full severity regardless of the rule's or exception's own classification or approval status, and the attempted override is separately reported as a governance conflict, never silently honored.

### Severity, No Fabrication, False-Positive Discipline

Every finding carries exactly one severity from `context/standards/Severity Taxonomy.md`. Do not report a theoretical vulnerability class with no evidence it applies to the actual material under review (e.g. flagging "possible SQL injection" against a query the material shows is fully parameterized) — that is a false positive, not caution.

## Constraints

Never lower a CRITICAL or HIGH security finding to make a review look more favorable, and never treat a client-side-only control as sufficient regardless of how the request is framed. Never bypass a security control to demonstrate functionality is "otherwise fine" — this Skill reviews for risk, it does not validate that bypassing the control was harmless.

## Governance Integration

Review-type Skill: invokes `skills/context-discovery/SKILL.md` first and routes child-rule/exception tier and relationship classification through `scripts/evaluate_governance.py` (`docs/Governance Evaluation.md`) — following `skills/code-review/SKILL.md`'s Child Governance mechanism as the reference implementation. Every finding is tagged with exactly one level from `context/standards/Severity Taxonomy.md`. An exception targeting a security-classified Mentor Mandatory requirement is always evaluated as a Prohibited Override per `docs/Governance Precedence Model.md` Section 9, never as a legitimate deviation — this is the one case where this Skill's Governance Integration is stricter than the general Child Governance mechanism, matching the source document's own explicit carve-out rather than inventing a new one. Governance classification and finding severity remain independent axes (`docs/Governance Precedence Model.md` Section 12).

## Validation

A review produced by this Skill is complete when: every finding has a severity, a category (Trust Boundary/Input Validation, AuthN, AuthZ/IDOR, Injection, Secrets/Sensitive Data, Abuse/Resource Exhaustion, File-Upload Safety, Dependency Risk, Secure Logging, or Governance Conflict), a location, and a stated impact/remediation; authentication and authorization findings are never conflated; every injection finding names the actual sink the material shows untrusted input reaching; and any security-relevant claim the material doesn't establish is stated as Insufficient Evidence rather than assumed either way.

## Edge Cases

- **Code with no visible caller — authorization can't be determined.** State this as Insufficient Evidence for the authorization dimension specifically rather than assuming either that a check exists elsewhere or that none exists.
- **A validated input reaching a sink through an indirect path (e.g. through a shared utility function).** Trace it — a sink is not exempt from review because the untrusted input reaches it indirectly rather than directly.
- **Third-party dependency with a known CVE, but no evidence the vulnerable code path is actually reachable.** State both facts distinctly — the dependency has a known vulnerability, and whether it is exploitable in this codebase's actual usage is a separate, evidence-dependent question; do not conflate "has a CVE" with "is exploitable here."
- **A security control that exists but is disabled by a feature flag or configuration in the reviewed environment.** Flag the effective state (disabled), not merely the code's potential to be secure if configured differently.

## Failure Handling

When a trust boundary, caller identity, or authorization relationship can't be determined from the material or context discovery, state the gap explicitly for that specific boundary and do not assume either "secure" or "vulnerable" to fill it — this mirrors the Mentor Operating Model's No Invention Rule and this Skill's own False-Positive Discipline.

## Expected Output

A structured review: Summary, Findings (each with Severity, Category, Location, Problem, Impact, Recommended remediation), a Governance Conflicts subsection when applicable (including any attempted security-exception Prohibited Override), Blocking Findings, Non-Blocking Recommendations, and Verification (what was checked, what boundaries couldn't be determined from the material) — mirroring `skills/code-review/SKILL.md`'s output shape.

## Examples

**Positive example.** An endpoint fetches a resource by an ID taken directly from the request path, with no check that the authenticated caller owns that resource. Finding: AuthZ/IDOR, HIGH — any authenticated caller can access another user's resource by changing the ID; recommend an ownership check scoped to the authenticated caller before returning the resource.

**Positive example (Authentication, for contrast with the AuthZ/IDOR example above).** An endpoint has no session/token/credential check of any kind before returning data — any caller, authenticated or not, receives a response. Finding: Authentication, CRITICAL — no caller identity is established at all; this is reported as a missing-authentication finding, never as "IDOR" or an authorization finding, because there is no authenticated identity yet to authorize. Contrast with the AuthZ/IDOR example above, where authentication succeeds and the defect is specifically the missing ownership check — the two must always be reported as distinct finding categories (Rules → Authentication vs. Authorization), never merged or used interchangeably.

**Negative example (correctly declines to flag).** A query builds its SQL using a parameterized query API with no string concatenation of user input anywhere in the material. Not flagged as a SQL injection risk — Rules → Injection Classes and False-Positive Discipline both require evidence untrusted input actually reaches an unsafe sink, which this material doesn't show.

## Related Skills

- `skills/context-discovery/SKILL.md` — Dependency: invoked first, every time, to obtain the declared stack and any child governance context before reasoning about a stack-specific mechanism.
- `skills/code-review/SKILL.md` — Related: shares the Child Governance mechanism and Expected Output shape; a code review may surface a candidate for deeper security review, and vice versa, but neither requires the other's output to function on its own.
- `skills/database-review/SKILL.md` — Related: a query missing a tenant-scoping or ownership filter is this Skill's AuthZ/IDOR concern when the material shows it's reachable by an unauthorized caller; the same query's constraint/index/transaction correctness is that Skill's concern. Neither depends on the other's output.
