#!/usr/bin/env bash
set -euo pipefail
mkdir -p .specify/memory .claude/skills src/pricing src/checkout
cat > .specify/memory/constitution.md <<'EOF'
# Shop Constitution
## I. Test-first
Every behavior change ships with automated tests.
## II. Simplicity
Prefer the smallest design that satisfies the spec.
EOF
for s in constitution specify clarify plan tasks analyze implement converge checklist; do
  mkdir -p .claude/skills/speckit-$s
  printf -- '---\nname: speckit-%s\ndescription: Spec Kit %s\n---\n' "$s" "$s" > .claude/skills/speckit-$s/SKILL.md
done
printf 'def unit_price(sku):\n    return CATALOG[sku].list_price\n' > src/pricing/prices.py
printf 'from pricing.prices import unit_price\n\ndef order_total(items):\n    return sum(unit_price(i.sku) * i.qty for i in items)\n' > src/checkout/totals.py
