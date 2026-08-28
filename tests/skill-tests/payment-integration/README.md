# payment-integration Skill — Regression Fixtures

5 narrative fixture specifications for `skills/payment-integration/SKILL.md` (`docs/Skill Taxonomy.md` Section 1). Generalized from external source material with all project-specific schema details removed and replaced with technology-agnostic payment integration patterns.

## Fixtures

| # | File | Category |
|---|---|---|
| 01 | `01-normal-server-amount-recalculation.md` | Normal — recomputing final payable amounts server-side during checkout initiation |
| 02 | `02-edge-webhook-signature-and-idempotency.md` | Edge case — handling duplicate payment webhooks with signature verification and no-op replays |
| 03 | `03-adversarial-cumulative-over-refunding.md` | Adversarial — attempt to issue partial refunds exceeding original transaction total |
| 04 | `04-failure-optimistic-refund-completion.md` | Failure handling — prematurely marking refunds completed before gateway confirmation |
| 05 | `05-rule-coverage-provider-adapter-isolation.md` | Rule coverage — isolating payment gateway SDKs and payloads behind generic adapter interfaces |
