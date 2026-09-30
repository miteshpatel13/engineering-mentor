#!/usr/bin/env bash
set -euo pipefail
mkdir -p .specify/memory .claude/skills specs/004-customer-pricing src/pricing src/checkout
cat > .specify/memory/constitution.md <<'EOF'
# Shop Constitution
## I. Test-first
Every behavior change ships with automated tests.
## II. Simplicity
Prefer the smallest design that satisfies the spec.
EOF
printf '{"feature_directory": "specs/004-customer-pricing"}\n' > .specify/feature.json
for s in constitution specify clarify plan tasks analyze implement converge checklist; do
  mkdir -p .claude/skills/speckit-$s
  printf -- '---\nname: speckit-%s\ndescription: Spec Kit %s\n---\n' "$s" "$s" > .claude/skills/speckit-$s/SKILL.md
done
printf 'def unit_price(sku):\n    return CATALOG[sku].list_price\n' > src/pricing/prices.py
printf 'from pricing.prices import unit_price\n\ndef order_total(items):\n    return sum(unit_price(i.sku) * i.qty for i in items)\n' > src/checkout/totals.py
cat > specs/004-customer-pricing/spec.md <<'EOF'
# Feature: Customer-level pricing
## Requirements
- FR-1: Enterprise customers have negotiated per-SKU prices.
- FR-2: At checkout, a customer's negotiated price replaces the list price for that SKU.
- FR-3: Orders record which price source (list or negotiated) was used.
EOF
cat > specs/004-customer-pricing/plan.md <<'EOF'
# Implementation Plan: Customer-level pricing
## Technical Context
Python 3.12, PostgreSQL 15. The orders table has about 30 million rows and takes live writes.
## Constitution Check
Test-first: PASS. Simplicity: PASS.
## Data Model
- New table customer_prices(customer_id BIGINT, sku TEXT, price NUMERIC).
- Migration: ALTER TABLE orders ADD COLUMN price_source TEXT NOT NULL;
## API
- POST /orders accepts an optional unit_price per line item. When present, the server stores it as the line price so negotiated prices from the sales team's client app are honoured.
## Rollout
Deploy the migration and the code together.
EOF
