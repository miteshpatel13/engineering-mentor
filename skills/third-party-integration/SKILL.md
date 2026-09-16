---
name: third-party-integration
description: The comprehensive engineering workflow and reference architecture for analyzing, designing, implementing, reviewing, testing, securing, and operating third-party integrations across APIs, webhooks, events, files, SDKs, and enterprise systems.
category: Integrations
skillType: Authoring/Workflow
---

# Third-Party Integration

## Purpose

Provide an authoritative, end-to-end engineering discipline for integrating external systems, third-party software, and external services into any software architecture. External integrations are inherently cross-boundary operations that introduce external failure modes, latency, security vulnerabilities, schema volatility, and data inconsistency into a codebase. This Skill guides an engineering agent or practitioner through the complete integration lifecycle—from initial capability discovery and pattern selection, to adapter-isolated implementation, strict boundary validation, security hardening, rate limiting, retry/timeout controls, idempotency, testing, and operational runbooks. It ensures external dependencies remain well-isolated behind Anti-Corruption Layers (ACL) rather than leaking third-party assumptions into the core business domain.

## Scope

**In scope:**
- **The 20 canonical integration types:**
  1. REST APIs (JSON/HTTP, OpenAPI/Swagger specifications)
  2. GraphQL APIs (Queries, mutations, subscriptions, schema federation)
  3. SOAP/XML Web Services (WSDL, WS-Security, XML schemas)
  4. Webhooks (Inbound HTTP callback endpoints, signature verification, async ingestion)
  5. OAuth 2.0 / OpenID Connect (Authorization Code + PKCE, Client Credentials, Refresh Token lifecycles)
  6. API Key, Basic Authentication, and Bearer Token integrations
  7. SDK-based integrations (Vendor client libraries, wrapper boundaries)
  8. File-based integrations (CSV, JSON, XML, Excel, EDI formats)
  9. SFTP/FTP file transfers (SSH key auth, atomic file uploads, polling, checksums)
  10. Direct database integrations (Read replicas, foreign data wrappers, staging tables, CDC)
  11. Message queues and event-driven integrations (Apache Kafka, RabbitMQ, AWS SQS/SNS, Google Cloud Pub/Sub)
  12. Payment gateway integrations (Checkout flows, ledger recording, refund limits, PCI boundaries)
  13. Communication integrations (Email, SMS, WhatsApp, Push notifications)
  14. Cloud storage integrations (Object storage, presigned URLs, streaming transfers)
  15. CRM integrations (Salesforce, HubSpot, custom CRMs, bidirectional synchronization)
  16. ERP integrations (SAP, NetSuite, inventory/order synchronization)
  17. Accounting integrations (QuickBooks, Xero, invoice reconciliation)
  18. Analytics and telemetry integrations (Segment, Mixpanel, Google Analytics, event streaming)
  19. SSO and SAML 2.0 integrations (Identity Provider/Service Provider metadata, assertions, JIT provisioning)
  20. iPaaS integrations (Zapier, Make, Workato, Tray.io webhooks and embedded connectors)
- **The complete 18-step integration lifecycle:** From initial requirements to operational runbooks and deprecation.
- **Architectural patterns:** Adapter Pattern, Anti-Corruption Layer (ACL), Gateway/Client abstraction, Outbox Pattern, Dead-Letter Queue (DLQ), Circuit Breaker, Asynchronous Job Dispatch.
- **Security & Data Privacy:** Secret management, zero-hardcoding enforcement, webhook signature verification, credential rotation, PII masking, request/response boundary sanitization.
- **Reliability & Resilience:** Connection/read timeouts, exponential backoff with full jitter, retryable vs. non-retryable error classification, rate limiting, and constraint-backed idempotency.
- **Data Synchronization:** Real-time, webhook-driven, scheduled polling, batch sync, delta sync, conflict resolution, and periodic reconciliation.
- **Testing:** Unit mocking, integration wiremocking, contract testing, sandbox verification, and failure/chaos injection.
- **Documentation & Runbooks:** Authoring standardized 22-section integration specifications and operational runbooks.
- **Code Review:** Systematic review checklist for evaluating existing third-party integration code.

**Out of scope:**
- Internal database index optimization (delegated to `skills/database-indexing/SKILL.md` and `skills/database-review/SKILL.md`).
- General internal API contract design for client-to-backend internal endpoints (owned by `skills/api-contract-design/SKILL.md`).
- Detailed payment ledger accounting and financial refund logic (delegated to `skills/payment-integration/SKILL.md`).
- Specialized multi-channel notification template registries and audience targeting (delegated to `skills/notification-integration/SKILL.md`).
- Cloud object storage adapter implementations (delegated to `skills/file-storage/SKILL.md`).

## When to Use

Use this Skill when:
- Designing a new integration with an external service, SaaS platform, vendor API, or external partner.
- Selecting the appropriate integration pattern (REST vs. Webhook vs. Queue vs. SFTP vs. SDK vs. iPaaS).
- Establishing authentication mechanisms (OAuth 2.0 flows, token refresh loops, mTLS, API keys).
- Implementing inbound webhook endpoints that require signature verification and replay prevention.
- Implementing an outbound integration client or Anti-Corruption Layer (ACL).
- Designing retry policies, backoff schedules, circuit breakers, or rate limiters for external calls.
- Designing data synchronization, conflict handling, and reconciliation between internal and external systems.
- Reviewing existing integration code for reliability, security leaks, missing timeouts, or tight coupling.
- Creating comprehensive integration documentation, technical specifications, or operational runbooks.

Do not use for internal inter-service communication governed entirely by internal microservice RPC or monolithic domain boundaries.

## Required Context

**Posture 2 — benefits from repository context but degrades gracefully without it** (`docs/Skill Standard.md` Section 3).

When available, inspect the repository's Normalized Project Context (`skills/context-discovery/SKILL.md`):
- `stack`: Programming language, HTTP client libraries, background job/queue frameworks (e.g., Celery, BullMQ, Sidekiq, Kafka, SQS), and database engine.
- `architecture`: Monolith, modular monolith, microservices, or event-driven architecture.
- `childRules` & `exceptions`: Repository-specific policies regarding external HTTP libraries, secret storage providers (e.g., AWS Secrets Manager, Vault, environment variables), or external network access.

When repository context is not available, provide technology-agnostic architectural designs and language-idiomatic pattern specifications.

## Workflow

The integration lifecycle consists of 18 sequential steps. An engineering agent must navigate these steps methodically, avoiding the temptation to jump straight to making HTTP requests.

```text
Requirement
    ↓
Integration Discovery
    ↓
Integration Type Selection
    ↓
Third-Party Capability Analysis
    ↓
Architecture & Data Flow
    ↓
Authentication & Authorization
    ↓
API / Event Contract
    ↓
Implementation & Adapter Isolation
    ↓
Error Handling & Classification
    ↓
Retry & Timeout Strategy
    ↓
Idempotency & Replay Protection
    ↓
Rate Limiting & Concurrency
    ↓
Security & Sensitive Data (PII)
    ↓
Logging & Observability
    ↓
Data Synchronization & Reconciliation
    ↓
Multi-Tier Testing
    ↓
Failure Recovery & Degradation
    ↓
Documentation & Operational Maintenance
```

### Step 1: Requirement & Capability Identification
Define the business capability being integrated. Clarify the business objective, the user value, the authoritative system of record for each entity, and the regulatory/compliance constraints.

### Step 2: Integration Discovery
Systematically answer the 17 integration discovery questions:
1. What business capability is being enabled?
2. Which specific third-party system, platform, or vendor is involved?
3. What exact data entities need to move between systems?
4. Is communication inbound (third-party calls us), outbound (we call third-party), or bidirectional?
5. Is the interaction pattern synchronous (real-time user waiting) or asynchronous (background/deferred)?
6. What communication protocols does the third-party expose (REST, GraphQL, Webhooks, SFTP, AMQP, gRPC)?
7. What authentication mechanism is mandated (OAuth 2.0, API Key, Mutual TLS, SAML)?
8. What specific APIs, webhooks, event topics, or file structures are available?
9. What are the vendor's documented rate limits (per second, minute, day, or concurrent connections)?
10. What are the expected latency SLAs and timeout requirements?
11. What are the vendor's retry and idempotency rules?
12. Does the third party support webhooks or push notifications, or is polling required?
13. What data must be persisted locally vs. fetched on demand?
14. What happens if the third-party system is completely unavailable?
15. What happens if our system is unavailable or experiencing downtime when the vendor sends data?
16. What happens if the exact same event or request is received multiple times?
17. What are the security, privacy, and compliance requirements (GDPR, HIPAA, PCI-DSS, SOC 2)?

### Step 3: Integration Type & Pattern Selection
Apply the Integration Decision Framework to select the optimal mechanism rather than defaulting to synchronous REST calls.

#### Integration Decision Framework
```text
Does the third party expose a programmatic API?
        │
       Yes ─────────────────────────────────────────── No
        │                                              │
Is real-time response required for user interaction?   Do they export/import files?
     │                  │                                   │                 │
    Yes                 No                                 Yes                No
     ↓                  ↓                                   ↓                 ↓
 Synchronous       Is event-driven push available?        SFTP / Batch    Direct DB / CDC /
 REST / GraphQL         │               │                 File Exchange   iPaaS / Scrape
                        Yes             No
                        ↓               ↓
                     Webhook /       Scheduled Polling /
                     Message Queue   Batch Sync
```

- **REST / GraphQL**: Use for request/response operations requiring immediate feedback (e.g., real-time address validation, payment authorization, instant balance check).
- **Webhooks + Background Workers**: Use for asynchronous notification of state changes (e.g., payment success, shipment tracking, document signed).
- **Message Queues (Kafka / SQS / RabbitMQ)**: Use when integrating with enterprise event streams or when decoupling high-throughput asynchronous payloads.
- **SFTP / File Exchange (CSV, JSON, EDI)**: Use for legacy enterprise, banking, supply chain, or large bulk batch feeds (e.g., overnight catalog or ledger synchronization).
- **SDK vs. Direct HTTP**: Prefer direct HTTP/JSON with standard typed clients when SDKs are unmaintained, bloated, or obscure error handling; use official maintained SDKs only when they provide complex cryptographic signing, streaming, or active protocol maintenance.
- **iPaaS (Zapier, Workato, Make)**: Use for non-core, rapid-prototyping, low-volume back-office automations; avoid for core transaction paths.

### Step 4: Third-Party Capability Analysis
Inspect the third-party API documentation, OpenAPI/Swagger specifications, SDK code, and rate-limit headers. Identify API versions, deprecation schedules, sandbox availability, pagination styles (offset, cursor, link-header), and error formats.

### Step 5: Architecture & Data Flow
Design the end-to-end architecture enforcing the **Anti-Corruption Layer (ACL)** pattern:

```text
+-------------------------------------------------------------+
|                        Your System                          |
|                                                             |
|   +-----------------------+     +-----------------------+   |
|   | Core Domain Services  |     | Core Domain Models    |   |
|   +-----------------------+     +-----------------------+   |
|               │                             ▲               |
|   Uses Domain │                             │ Domain DTO    |
|   Interfaces  ▼                             │               |
|   +─────────────────────────────────────────────────────+   |
|   |          Integration Layer / Adapter (ACL)          |   |
|   |  - Generic Port/Interface Definition                |   |
|   |  - Third-Party Client Implementation                |   |
|   |  - Bidirectional Data Mapping (External <-> Domain) |   |
|   |  - Error Translation to Domain Exceptions           |   |
|   +─────────────────────────────────────────────────────+   |
+───────────────────│─────────────────────────▲───────────────+
                    │ Network Calls           │ Inbound Webhooks
                    ▼                         │
+-------------------------------------------------------------+
|                     Third-Party System                      |
+-------------------------------------------------------------+
```

Produce sequence diagrams for:
- Standard request/response flow.
- Inbound webhook processing flow.
- Asynchronous job execution and retry flow.
- Reconciliation and periodic sync flow.

### Step 6: Authentication & Authorization Lifecycle
Implement robust credential and token management:
- **OAuth 2.0 Authorization Code + PKCE**: For user-delegated access; handle state validation, authorization code exchange, secure token storage, and automatic refresh before expiration.
- **OAuth 2.0 Client Credentials**: For machine-to-machine integrations; cache access tokens with a safety margin (e.g., refresh 5 minutes before `expires_in`).
- **API Key / Bearer Token**: Inject via secure configuration headers (`Authorization: Bearer <token>`); never pass tokens in query parameters where they leak into logs.
- **Mutual TLS (mTLS)**: For high-security banking/enterprise integrations; manage client certificates, CA validation, and certificate rotation schedules.
- **Token Storage**: Encrypt tokens at rest; never store access or refresh tokens in plaintext.

### Step 7: API / Event Contract Specification
Document the precise contracts at the integration boundary:
- Endpoint URL, HTTP method, and API version.
- Exact request headers, query parameters, and JSON/XML schema.
- Expected response schema across 2xx success statuses.
- Error response schema across 4xx and 5xx statuses.
- Webhook payload structure, event types, and signature header names.

### Step 8: Implementation & Adapter Isolation
Implement the integration using dedicated classes/modules:
- `Port / Interface`: Declares technology-agnostic business operations (e.g., `CustomerCrmPort`).
- `Adapter`: Implements the interface by orchestrating the HTTP client, authentication, and data mappers (e.g., `HubspotCrmAdapter`).
- `Client`: Low-level HTTP/transport client handling serialization, headers, connection pooling, and timeouts.
- `Mappers / Translators`: Pure functions converting third-party DTOs to internal domain models and vice versa.

### Step 9: Boundary Validation & Error Mapping
- **Outbound Request Validation**: Validate outbound payloads against internal constraints before transmitting over the network.
- **Inbound Response Validation**: Parse and validate third-party responses using strict schemas (e.g., Zod, Pydantic, JSON Schema); never assume external responses match documentation.
- **Centralized Error Mapping**: Catch network errors, HTTP 4xx/5xx responses, and timeout exceptions at the adapter boundary. Translate them into typed domain exceptions (e.g., `IntegrationUnavailableException`, `ResourceNotFoundException`, `RateLimitExceededException`).

### Step 10: Retry, Timeout & Circuit Breaker Strategy
- **Explicit Timeouts**: Configure connect timeouts (e.g., 2–5s) and read/socket timeouts (e.g., 5–30s). Never leave timeouts at language defaults (often infinite).
- **Error Classification**:
  - *Retryable Errors*: HTTP 408 (Request Timeout), HTTP 429 (Too Many Requests), HTTP 500 (Internal Error - verify idempotency first), HTTP 502 (Bad Gateway), HTTP 503 (Service Unavailable), HTTP 504 (Gateway Timeout), TCP connection resets, DNS resolution glitches.
  - *Non-Retryable Errors*: HTTP 400 (Bad Request), HTTP 401 (Unauthorized - trigger re-auth or alert), HTTP 403 (Forbidden), HTTP 404 (Not Found), HTTP 422 (Unprocessable Entity).
- **Exponential Backoff & Full Jitter**:
  $$\text{WaitTime} = \text{random}(0, \min(\text{MaxBackoff}, \text{InitialBackoff} \times 2^{\text{attempt}}))$$
- **Circuit Breaker**: When failure rates exceed a threshold (e.g., 50% failures over 20 consecutive requests), open the circuit immediately to fail fast and protect system threads; transition to half-open after a cooldown window.

### Step 11: Idempotency & Replay Protection
- Provide a unique, deterministic idempotency key for outbound mutating requests (e.g., `Idempotency-Key: <uuid-or-hash>`) per `skills/idempotency/SKILL.md`.
- Persist state transitions in an internal transactional outbox or ledger before dispatching external calls.
- For inbound webhooks, store processed event IDs in a dedicated idempotency table with a database unique constraint to prevent duplicate processing.

### Step 12: Rate Limiting & Concurrency Control
- Respect third-party rate limit headers: `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`, `Retry-After`.
- Implement client-side rate limiters (token bucket, leaky bucket) to throttle outbound request rates below the vendor's threshold.
- Back off immediately when receiving an HTTP 429 response; parse the `Retry-After` header (seconds or HTTP date) to pause execution.

### Step 13: Security & Sensitive Data (PII)
- **Secret Management**: Retrieve credentials from environment variables, secret managers, or vault stores. Never hardcode credentials.
- **Sensitive Data & PII**: Identify PII (names, emails, phone numbers, SSNs, financial details) transmitted to third parties. Encrypt at rest and in transit.
- **Webhook Signature Verification**: Verify HMAC SHA-256 signatures over raw request bodies using constant-time comparison algorithms to prevent timing attacks.
- **Replay Protection**: Verify webhook timestamps against current server time with a strict tolerance window (e.g., $\le 300$ seconds).

### Step 14: Logging & Observability
- Generate and propagate a `Correlation-ID` / `Trace-ID` across outbound requests via headers (`X-Correlation-ID`, W3C `traceparent`).
- Log integration request lifecycle events: method, target host, sanitized URL, response status, duration (latency ms), and retry attempt count.
- **Redact Sensitive Data**: Mask Authorization headers, API keys, passwords, credit card numbers, and PII from request and response log payloads.
- Track metrics: Request count by status, error rate, p50/p95/p99 latency, rate limit quota remaining, circuit breaker state.

### Step 15: Data Synchronization & Reconciliation
- **Synchronization Strategies**:
  - *Real-time*: Event-driven webhook ingestion or inline transactional triggers.
  - *Incremental (Delta) Sync*: Periodic polling using high-watermark timestamps (`updated_at > :last_sync_timestamp`) or cursor tokens.
  - *Full Batch Sync*: Scheduled off-peak bulk extraction and alignment.
- **Conflict Handling**: Define precedence rules (e.g., "Internal system wins", "Third party wins", "Latest timestamp wins", or "Manual review queue").
- **Reconciliation Engine**: Implement daily or weekly reconciliation jobs that compare internal record states against third-party exports to detect and heal drift.

### Step 16: Multi-Tier Testing Strategy
- **Unit Tests**: Test mappers, validators, and error translators in isolation with mock data.
- **Integration Tests (WireMock / VCR)**: Test the HTTP client and adapter against recorded or simulated third-party responses, including error statuses, malformed JSON, and timeouts.
- **Contract Tests**: Verify request schemas and expected response structures against published OpenAPI/JSON schemas.
- **Webhook Handlers**: Test signature verification, timestamp verification, payload parsing, idempotency deduplication, and asynchronous queue dispatching.
- **Failure Injection**: Test behavior under network timeouts, HTTP 429 rate limiting, HTTP 503 outages, and socket disconnections.

### Step 17: Failure Recovery & Degradation
- Define graceful degradation behavior: Can cached data be returned? Can non-critical features be hidden? Can write operations be queued for deferred processing?
- Route unrecoverable, permanently failed events to a Dead-Letter Queue (DLQ) with error context.
- Provide administrative re-drive capabilities to reprocess DLQ messages after third-party recovery.

### Step 18: Integration Documentation & Operational Maintenance
- Produce the canonical 22-section Integration Specification Document.
- Document alert thresholds, runbooks for credential rotation, escalation paths for third-party outages, and deprecation plans.

---

## Rules

### Adapter / Anti-Corruption Layer Isolation
Application business logic and domain services must never directly import or invoke third-party SDKs, HTTP clients, or vendor-specific data structures. All interactions must pass through a domain-owned interface (Port) implemented by an Adapter. Third-party entities must be translated into internal domain models at the boundary.

### Secret Management & Zero Hardcoding
*(Mentor Mandatory baseline via `context/standards/Security Standard.md`)*
API keys, client secrets, private keys, webhook signing secrets, and basic authentication passwords must never be committed to source code or configuration files. They must be injected at runtime via environment variables or fetched from an approved secrets manager. Any PR containing hardcoded credentials must be blocked with CRITICAL severity.

### Asynchronous Ingestion of Webhooks
Inbound webhook endpoints must verify signatures, validate payload structure, enforce idempotency checks, enqueue the payload for background processing, and return an immediate HTTP 200 or 202 response. Heavy business processing, complex database transactions, or cascading external API calls must never run synchronously within the webhook HTTP request thread.

```text
Third Party
    ↓ (HTTP POST)
Webhook Endpoint
    ↓
1. Verify Signature & Timestamp (Constant-Time HMAC)
    ↓
2. Validate Schema
    ↓
3. Check Idempotency (Unique constraint / KV store)
    ↓
4. Enqueue Job to Background Queue (BullMQ, Celery, SQS)
    ↓
5. Return HTTP 200/202 Acknowledgment (< 250ms)
    │
    ▼ (Asynchronous Worker)
Background Worker Processes Business Logic
```

### Mandatory Explicit Timeouts
*(Mentor Mandatory baseline)*
Every network request to a third-party service must have explicitly declared connection and read/socket timeouts. Defaulting to client library defaults that allow indefinite blocking is prohibited. Connect timeouts must not exceed 5 seconds; read timeouts must not exceed 30 seconds unless explicitly justified for long-running batch exports.

### Retryable vs. Non-Retryable Error Classification
Retries must only be attempted on transient, retryable errors (network connection drops, timeouts, HTTP 408, HTTP 429, HTTP 500, 502, 503, 504). Client errors (HTTP 400, 401, 403, 404, 422) represent deterministic validation or permission failures and must never be retried automatically without manual intervention or token renewal.

### Full Jitter on Exponential Backoff
When retrying failed requests, exponential backoff must incorporate full random jitter. Deterministic exponential backoff without jitter causes synchronized retry storms ("thundering herd") that overwhelm recovering third-party services.

### Constraint-Backed Idempotency
*(Mentor Mandatory / Data Integrity baseline via `skills/idempotency/SKILL.md`)*
Mutating integration operations (outbound payment charges, entity creation, webhook processing) must be protected by database-enforced unique constraints on an idempotency key. Check-then-act application logic without unique constraints is susceptible to race conditions and duplicate side-effects.

### OAuth Token Lifecycle Management
OAuth 2.0 access tokens must be cached and refreshed automatically before expiration. Implement a token refresh lock or single-flight mechanism to prevent concurrent requests from triggering multiple simultaneous token refresh calls when an access token expires.

### PII Protection and Log Redaction
Personal Identifiable Information (PII) and authentication secrets must be redacted or masked in application logs and telemetry. Full HTTP request or response bodies containing authorization headers, passwords, credit card numbers, or customer identity details must never be written to plaintext logs.

### Circuit Breaker Implementation on Synchronous Paths
Outbound synchronous integration calls executed within user-facing request paths must be protected by a circuit breaker. When the third-party endpoint fails consistently, the circuit breaker must trip to fast-fail subsequent requests and allow fallback degradation, preventing thread exhaustion in the host application.

---

## Constraints

- Never commit or recommend hardcoding third-party API credentials, webhook secrets, or private keys.
- Never execute long-running or blocking business transactions directly inside synchronous inbound webhook HTTP handlers.
- Never retry non-retryable 4xx client errors (400, 403, 404, 422).
- Never allow third-party DTOs or vendor schema formats to leak beyond the integration adapter into core domain entities.
- Never issue network calls with infinite or unconfigured timeouts.
- Never perform check-then-insert idempotency verification without an underlying database unique constraint.

---

## Governance Integration

Authoring/Workflow-type Skill, invoked during system design, implementation, and code review:
- Invokes `skills/context-discovery/SKILL.md` to discover repository stack, queue infrastructure, and declared child governance.
- Strictly adheres to Mentor Mandatory baselines established in `context/standards/Security Standard.md` (zero hardcoded secrets, authentication/authorization checks, PII protection) and `skills/idempotency/SKILL.md` (constraint-backed deduplication).
- When conducting reviews of existing third-party integrations, maps findings strictly to `context/standards/Severity Taxonomy.md` (CRITICAL for exposed credentials or unverified webhooks; HIGH for missing timeouts, unbounded retries, or duplicate transaction vulnerabilities; MEDIUM for missing circuit breakers or incomplete error mapping).
- Evaluates child repository exceptions through `scripts/evaluate_governance.py` when evaluating project compliance.

---

## Validation

An integration design, implementation, or specification is validated and complete when:
1. **Discovery Complete**: All 17 discovery questions have been answered or explicitly recorded as pending vendor clarification.
2. **Adapter Boundary Established**: A distinct interface/port separates application business logic from vendor-specific transport and data formats.
3. **Security Verified**: Secrets are configuration-driven, inbound webhooks verify HMAC signatures with constant-time comparison and timestamp tolerance, and PII is masked.
4. **Resilience Enforced**: Explicit connect/read timeouts are declared, retries use exponential backoff with full jitter, non-retryable errors are excluded from retries, and circuit breakers protect synchronous paths.
5. **Idempotency Backed by Constraints**: Unique constraints prevent duplicate transaction or webhook execution.
6. **Asynchronous Webhook Ingestion**: Webhook handlers acknowledge with HTTP 200/202 within $\le 250$ms and offload processing to a background worker.
7. **Testing Plan Covers Failure Modes**: Unit, mock integration, contract, and chaos/failure injection test scenarios are defined.
8. **Specification Document Complete**: The 22-section integration document is fully populated.

---

## Edge Cases

- **Silent Schema Drift**: The third party adds, deprecates, or mutates fields without incrementing API version numbers. Handled by configuring DTO mappers to tolerate unknown fields while validating required fields strictly.
- **Clock Drift in Webhook Verification**: The third-party timestamp header deviates slightly from server clock. Handled by allowing a configurable tolerance window (typically 300 seconds) before rejecting payloads as expired.
- **Out-of-Order Webhook Delivery**: Webhook event `order.updated` arrives before `order.created` due to network routing. Handled by checking entity versioning or event sequence timestamps; if an entity does not exist, queue the update event with exponential backoff or fetch the latest full state via GET API.
- **Rate Limit Reset Race Condition**: A 429 `Retry-After` header specifies 1 second, but all waiting workers retry at the exact same millisecond. Handled by adding jitter to the `Retry-After` delay.
- **Concurrent OAuth Token Refresh**: Multiple worker processes simultaneously detect an expired token and attempt to refresh it with the same single-use refresh token, causing all but one to fail and revoke the grant. Handled by distributed locking (e.g., Redis lock) or single-flight refresh coordination.
- **Partial Batch Failures**: An API accepting 100 items processes 80 successfully and fails on 20. Handled by inspecting individual item status codes in the response and isolating failed records for dead-lettering without failing the entire batch.

---

## Failure Handling

- **Vendor Documentation Ambiguity**: When vendor API docs omit rate limits, idempotency keys, or error schemas, explicitly flag these as `UNKNOWN / TBD` and design conservative defaults (e.g., assume 5 req/sec limit, implement client-side idempotency, treat unparseable errors as 500s) until verified in sandbox.
- **Prolonged Third-Party Outage**: When a vendor is down for hours, transition the adapter into degraded mode: serve stale cached data where safe, queue outbound commands in durable outbox tables, trip circuit breakers to avoid blocking user threads, and surface user-facing notices.
- **Revoked Credentials / Expired OAuth Grant**: When an authentication attempt yields HTTP 401 even after a refresh attempt, mark the integration connection as `DISCONNECTED / AUTH_REQUIRED`, log a CRITICAL alert, and notify administrators to re-authenticate.
- **Exceeded Webhook Retry Limits**: When internal downstream workers fail repeatedly on a webhook event, move the message to a Dead-Letter Queue (DLQ) and preserve the raw payload, headers, and stack trace for manual re-drive.

---

## Expected Output

Depending on the prompt and integration lifecycle stage, this Skill produces:
1. **Technical Integration Specification**: Comprehensive document following the 22-section standard below.
2. **Architecture & Sequence Diagrams**: Mermaid diagrams depicting system context, adapter boundaries, and asynchronous data flows.
3. **Adapter Code & Contracts**: Typed Port interfaces, Adapter implementations, DTO models, and error mappers.
4. **Code Review Audit Report**: Findings-style audit identifying integration anti-patterns, security risks, and reliability vulnerabilities.
5. **Operational Runbook**: Maintenance, credential rotation, alert thresholds, and troubleshooting procedures.

### Standard 22-Section Integration Specification Template

```markdown
# Integration Specification: [Third-Party System Name]

## 1. Integration Overview
[Summary of capability, business value, and key stakeholders]

## 2. Business Purpose
[Detailed business requirements, user stories, and authoritative systems of record]

## 3. Third-Party System
[Vendor profile, platform version, documentation links, API status page, and support SLAs]

## 4. Integration Type
[Mechanism selected: REST, GraphQL, Webhook, Queue, SFTP, SDK, iPaaS, with selection rationale]

## 5. Architecture
[System context diagram, component boundaries, Anti-Corruption Layer structure]

## 6. Data Flow
[Mermaid sequence diagrams for standard, asynchronous, and exception flows]

## 7. Authentication & Credentials
[OAuth 2.0 flow, API Key, mTLS, token refresh lifecycle, and secret storage location]

## 8. API / Event Contracts
[Endpoints, HTTP methods, request/response JSON schemas, and status codes]

## 9. Data Mapping
[Field-by-field mapping table: Third-Party Field <-> Transformation <-> Internal Domain Field]

## 10. Error Handling & Exception Mapping
[Vendor error codes, mapping to internal domain exceptions, and user-facing messages]

## 11. Retry Strategy
[Classification of retryable vs. non-retryable errors, backoff formula, and max attempts]

## 12. Idempotency & Replay Protection
[Outbound idempotency keys, inbound webhook event deduplication, and database constraints]

## 13. Rate Limiting & Concurrency
[Vendor quotas, rate limit headers, client-side token bucket config, and concurrency limits]

## 14. Security & Compliance
[Secret management, webhook signature verification, TLS enforcement, PII masking, compliance]

## 15. Logging & Observability
[Correlation ID propagation, sanitized log fields, metrics, dashboard specs, and alert rules]

## 16. Synchronization Strategy
[Real-time vs. batch sync, delta high-watermarks, conflict resolution rules, and reconciliation]

## 17. Failure & Recovery
[Circuit breaker parameters, graceful degradation, fallback mechanisms, and dead-letter queues]

## 18. Testing Strategy
[Unit mock coverage, WireMock integration tests, contract tests, and sandbox verification]

## 19. Configuration
[Environment variables, feature flags, connection pool settings, and timeout values]

## 20. Deployment & Infrastructure
[Egress IP whitelisting, network gateways, worker queues, and infrastructure prerequisites]

## 21. Operational Runbook
[Credential rotation procedure, alert response guides, DLQ re-drive instructions, health checks]

## 22. Known Limitations & Deprecations
[Vendor API constraints, roadmap limitations, unhandled edge cases, and deprecation timelines]
```

---

## Examples

### Positive Example: Asynchronous E-Commerce Order Webhook & CRM Sync

**Context**: Ingesting `order.completed` webhooks from an external e-commerce provider (Shopify/Stripe) and synchronizing customer order history to an external CRM (HubSpot).

**Implementation Details**:
1. **Webhook Ingestion**:
   - HTTP endpoint `/api/v1/webhooks/orders` receives raw payload.
   - Verifies HMAC SHA-256 signature in constant time using `crypto.timingSafeEqual`.
   - Checks `X-Shopify-Hmac-Sha256` and timestamp within 300s window.
   - Inserts record into `webhook_events` table with unique constraint on `(provider, event_id)`. If duplicate, returns HTTP 200 immediately without reprocessing.
   - Enqueues job `ProcessOrderWebhookJob` into Redis-backed queue.
   - Returns HTTP 200 in 45ms.
2. **Adapter & Anti-Corruption Layer**:
   - Background worker invokes `HubspotCrmAdapter` which implements `CustomerCrmPort`.
   - Outbound call configured with 3s connect timeout, 10s socket timeout.
   - Throttled by client-side rate limiter to 10 req/sec (respecting HubSpot tier).
   - Wrapped in retry policy: retries HTTP 429/503 up to 3 times with exponential backoff ($1\text{s}, 2\text{s}, 4\text{s}$) plus full jitter; rejects HTTP 400/404 immediately.
   - Logs request duration, response status, and `X-Correlation-ID`; masks customer email and phone number in logs.

### Negative Example: Tightly Coupled Synchronous Integration Anti-Pattern

**Scenario**: A team implements external CRM contact creation directly inside user registration.

```python
# ANTI-PATTERN: DO NOT DO THIS
@app.post("/register")
def register_user(request: UserRegistrationRequest):
    # 1. Internal registration
    user = db.create_user(request.email, request.password)
    
    # 2. Tightly coupled third-party call inside HTTP request thread
    # Flaw: No adapter/interface; raw third-party SDK imported in domain controller
    # Flaw: Hardcoded API key in code
    # Flaw: No timeout specified (will hang if CRM is slow)
    # Flaw: Synchronous blocking call impacts user response time
    # Flaw: If CRM fails, user registration transaction fails
    client = ThirdPartyCrmClient(api_key="sk_live_123456789")
    crm_contact = client.create_contact({
        "email": user.email,
        "first_name": request.first_name,
        "credit_card": request.credit_card_number  # Flaw: PII / PCI leakage!
    })
    
    return {"status": "ok", "user_id": user.id}
```

**Why It Fails**:
- Direct dependency on third-party SDK leaks vendor schemas into domain controllers.
- Hardcoded API key creates a critical security vulnerability.
- Infinite default timeout allows vendor latency or outage to exhaust application server worker threads.
- Unhandled external failures cause internal registration to roll back or crash.
- Sensitive credit card data is transmitted to an unauthorized external system.

---

## Related Skills

- `skills/idempotency/SKILL.md` — Dependency: Provides the foundational pattern for constraint-backed request identity, deduplication, and safe replaying consumed during webhook and mutating API integrations.
- `skills/payment-integration/SKILL.md` — Related: Specializes third-party integration patterns for payment gateways, financial ledgers, refund limits, and PCI compliance boundaries.
- `skills/notification-integration/SKILL.md` — Related: Specializes integration architecture for multi-channel messaging (SMS, Email, Push) and dynamic audience resolution.
- `skills/file-storage/SKILL.md` — Related: Specializes integration patterns for cloud object storage providers, presigned URLs, and MIME validation.
- `skills/api-contract-design/SKILL.md` — Related: Designs API contracts and schemas before implementation; complements the external contract specifications designed in this Skill.
- `skills/api-review/SKILL.md` — Related: Evaluates API contracts for consistency, backward compatibility, and error semantics.
- `skills/architecture-review/SKILL.md` — Related: Evaluates system boundaries, module coupling, and Anti-Corruption Layer isolation.
- `skills/security-review/SKILL.md` — Related: Evaluates integration security, authentication lifecycles, and credential protection.
- `skills/context-discovery/SKILL.md` — Dependency: Discovers child repository stack, libraries, and architecture prior to designing integration adapters.
