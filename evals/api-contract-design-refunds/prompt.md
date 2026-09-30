---
description: A from-scratch API contract request must trigger api-contract-design and produce a contract that is retry-safe, validates amounts server-side, and defines error semantics.
tags: [design, api]
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

We need to add refunds to our payments API. Merchants should be able to refund all or part of a captured payment, and refunds can take a few seconds to settle with the card processor. Nothing exists yet — please design the API contract for this before we write any code.
