---
name: payment-integration
description: The general engineering pattern for payment gateway integration — server-side amount calculation, payment provider adapter isolation, webhook/callback idempotency, refund processing, invoice snapshots, and PCI/credentials safety. Reference material consumed by database-review, security-review, and api-contract-design.
category: Domain Patterns
skillType: Domain Pattern
---

# Payment Integration

## Purpose

Produce the shared, reusable reference pattern for integrating third-party payment gateways (e.g., Stripe, PayPal, PayU) into backend application architectures. This exists as its own Skill because payment integration carries critical financial, security, and data-integrity requirements — requiring server-side amount recalculation, strict webhook deduplication (`skills/idempotency/SKILL.md`), provider abstraction, refund validation, and invoice snapshotting.

## Scope

**In scope:** server-side payable amount calculation, payment gateway adapter/provider abstraction, transaction ledger recording, webhook/callback signature verification and idempotency, refund validation and status tracking, immutable legal invoice snapshotting, and PCI-compliance boundaries.

**Out of scope:** configuring specific payment gateway dashboard accounts or API keys; evaluating database locking performance during checkout — which is `skills/database-review/SKILL.md`'s concern. This Skill teaches the payment architecture pattern.

## When to Use

Use when:
- Designing payment checkout, initiation, or webhook ingestion flows.
- Implementing payment gateway provider adapters or switching payment processors.
- Building refund, partial refund, or chargeback handling logic.
- Generating tax invoices or billing receipts based on payment completion.
- Reviewing financial transaction code for security or data integrity vulnerabilities.

Do not use for non-financial internal state transitions where monetary payment verification is not involved.

## Required Context

**Posture 2 — benefits from repository context but degrades gracefully without it** (`docs/Skill Standard.md` Section 3). Core principles (server-side recalculation, provider abstraction, webhook signature verification, atomic idempotency) apply across all payment processors and backend stacks.

## Workflow

1. **Calculate Payable Amount Server-Side:** Recompute item prices, fees, taxes, and discounts from authoritative database models at the exact moment of payment initiation.
2. **Isolate Provider via Adapter:** Encapsulate provider-specific API calls, signature generation, and payload mappings behind a generic `PaymentProvider` interface.
3. **Record Attempt in Transaction Ledger:** Persist a `PaymentTransaction` record prior to sending the initiation request to the gateway, generating a unique transaction reference.
4. **Ingest Webhook with Signature & Idempotency Check:** Verify gateway signatures on inbound webhooks, look up the transaction reference, and enforce atomic idempotency (`skills/idempotency/SKILL.md`) to ignore duplicate success notifications.
5. **Derive Payment Status Authoritatively:** Treat the transaction ledger as the single source of truth for payment status. Never update business entity payment states without an underlying ledger entry.
6. **Process Refunds with Limit Validation:** Validate that proposed refunds do not exceed the original net transaction amount before sending refund requests to the gateway.
7. **Freeze Legal Invoice Snapshots:** On payment completion, snapshot organization legal details (tax ID, business address, rates) into the invoice record to ensure historical immutability.

## Rules

### Server-Side Amount Recalculation

The backend must calculate the final payable amount authoritatively from database configuration and validated line items. Client-submitted prices, totals, or discount percentages must never be accepted as the charge amount. If a client payload includes an expected total, the backend must recalculate the total independently and reject the request if any discrepancy exists.

### Payment Provider Adapter Isolation

Payment gateway integrations must be isolated behind a generic provider interface (e.g. `PaymentProvider`). Application services interact exclusively with the generic interface. Gateway-specific SDKs, API HTTP clients, signature algorithms, and webhook payload structures must be contained within dedicated adapter implementations (e.g., `StripeAdapter`, `PayUAdapter`).

### One Transaction Attempt per Ledger Record

Every payment attempt (initial try, retry after decline, abandoned checkout) must produce a distinct `PaymentTransaction` record in the database, carrying a unique gateway transaction reference. Do not overwrite or mutate historical failed attempts.

### Mandatory Webhook Signature Verification and Idempotency

Inbound payment webhooks and callbacks must undergo two mandatory checks before executing business logic:
1. **Signature Verification:** Verify the cryptographically signed hash/signature header using the provider's secret key. Reject unverified webhooks immediately with `401 Unauthorized` or `400 Bad Request`.
2. **Atomic Idempotency:** Check if the transaction reference has already been processed as `SUCCESS`. Replays of already-successful notifications must return HTTP success (to acknowledge receipt to the gateway) while executing zero duplicate side-effects (no duplicate invoices, emails, or fulfillment triggers). See `skills/idempotency/SKILL.md`.

### Derived Business Entity Payment Status

Domain entity payment statuses (e.g. `Order.payment_status`, `Registration.payment_status`) must be derived cached values updated exclusively by transaction ledger state updates. Manual or offline payments entered by administrators must also record a formal `PaymentTransaction` entry (marked as manual/offline method) rather than directly overriding the entity status flag.

### Refund Sum Validation and Lifecycle

Refunds must be modeled as a distinct one-to-many child entity against the original `PaymentTransaction`. Before initiating a refund:
- Calculate `(Original Transaction Amount) - (Sum of non-failed prior refunds)`.
- Reject any new refund request that exceeds the remaining net balance.
- Track refund lifecycle states explicitly (`INITIATED`, `PROCESSING`, `COMPLETED`, `FAILED`). Never mark a refund `COMPLETED` prior to gateway confirmation.

### Immutable Invoice Legal Snapshots

Tax invoices issued upon payment completion must capture a frozen JSON snapshot of the seller's legal entity details (tax ID, corporate name, address, tax rate) at the exact moment of issue. Subsequent updates to organization settings or tax rates must not alter historical invoice records.

### Sensitive Data Storage Boundaries (PCI Compliance)

Application databases must never store raw credit card numbers, CVVs, PINs, or sensitive authentication data. Store only opaque payment gateway tokens, transaction references, and payment method summaries (e.g., `Visa ending in 4242`). Payment gateway secret keys must be injected via secure environment configuration (`skills/security-review/SKILL.md`).

## Constraints

- Never accept a client-submitted monetary amount as the authoritative charge amount.
- Do not bypass webhook signature verification or idempotency checks on payment callbacks.
- Never update domain entity payment statuses without creating an underlying `PaymentTransaction` record.
- Do not store raw PCI-restricted card data in application databases.

## Governance Integration

This Skill supplies reference material (Domain Pattern) per `docs/Skill Taxonomy.md` Section 2.

- **Mentor Advisory:** Rules in this Skill represent strongly recommended Advisory-tier standards for financial data integrity and security grounded in `context/standards/Security Standards.md` and `context/standards/API & Backend Standards.md`.
- **Child Rules:** Child rules in `.mentor/rules/` may specify supported payment processors, currency formats, or tax calculation rules.

## Validation

This Skill is validated during design and review when:
- Payment amounts are recomputed server-side prior to gateway initiation.
- Gateway adapters encapsulate provider SDKs and signature routines.
- Webhooks verify signatures and execute atomic idempotency checks (`skills/idempotency/SKILL.md`).
- Refund amounts are validated against remaining transaction balances.
- Invoices snapshot legal entity data at issue time.

## Edge Cases

- **Asynchronous Webhook Delays:** Webhooks may arrive out of order or after a long network delay. Idempotency checks must handle late webhooks without regressing transaction states.
- **Partial Refunds:** Multiple partial refunds against a single transaction must be tracked cumulatively to prevent cumulative over-refunding.
- **Currency Precision:** Monetary values must be computed using fixed-precision decimals (e.g. `DECIMAL(12,2)` or integer cents/smallest currency units) to avoid floating-point rounding errors.

## Failure Handling

If payment webhook structures or gateway signature requirements cannot be established from provided code artifacts, report Insufficient Evidence rather than assuming payment completion, per the Mentor Operating Model No Invention Rule.

## Expected Output

Reference material. Consuming Review Skills (`database-review`, `security-review`, `api-contract-design`) format review findings using `context/templates/Review Template.md`.

## Examples

### Positive Example: Server Amount Calculation and Idempotent Webhook
```typescript
// Initiation: Server recomputes total price authoritatively
async initiatePayment(bookingId: string): Promise<PaymentSession> {
  const booking = await this.bookingRepo.findById(bookingId);
  const calculatedAmount = booking.items.reduce((sum, item) => sum + item.unitPrice * item.qty, 0);

  const txn = await this.txnRepo.create({
    bookingId,
    amount: calculatedAmount,
    status: PaymentStatus.INITIATED,
    gatewayRef: this.generateUniqueRef()
  });

  return this.paymentAdapter.createSession({ txnRef: txn.gatewayRef, amount: calculatedAmount });
}

// Webhook: Verified signature and idempotent lookup
async handleWebhook(payload: string, signature: string): Promise<void> {
  if (!this.paymentAdapter.verifySignature(payload, signature)) {
    throw new UnauthorizedException('Invalid webhook signature');
  }

  const event = this.paymentAdapter.parseWebhook(payload);
  const txn = await this.txnRepo.findByGatewayRef(event.txnRef);

  if (txn.status === PaymentStatus.SUCCESS) {
    return; // Silent no-op for duplicate webhook
  }

  await this.txnRepo.updateStatusAtomically(txn.id, PaymentStatus.SUCCESS);
  await this.invoiceService.generateInvoiceSnapshot(txn);
}
```

### Negative Example: Client-Submitted Amount and Unverified Webhook
```typescript
// BAD: Client passes payment amount directly to gateway initiation
async initiatePayment(clientAmount: number): Promise<PaymentSession> {
  return this.stripe.sessions.create({ amount: clientAmount }); // SECURITY DEFECT!
}

// BAD: Webhook accepts payload without signature verification or idempotency check
app.post('/webhook', (req, res) => {
  markOrderPaid(req.body.orderId); // DEFECT: Unverified signature & duplicate side-effects!
  res.send({ status: 'ok' });
});
```

## Related Skills

- `skills/idempotency/SKILL.md` — Related: Provides the atomic deduplication pattern for payment webhooks and retries.
- `skills/security-review/SKILL.md` — Related: Evaluates PCI boundaries, secret management, and webhook signature verification.
- `skills/validation/SKILL.md` — Related: Mandates server-side recalculation of input parameters.
- `skills/database-review/SKILL.md` — Related: Evaluates schema transaction boundaries and unique index constraints for payment ledgers.
