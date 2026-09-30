---
type: regex
# Non-canonical severity labels used as labels: "[Minor]", "MAJOR", or "Blocker:".
pattern: '\[(Blocker|Major|Minor|Informational)\]|\b(BLOCKER|MAJOR|MINOR|INFORMATIONAL)\b|\b(Blocker|Major|Minor)\s*:'
match: not_contains
---
