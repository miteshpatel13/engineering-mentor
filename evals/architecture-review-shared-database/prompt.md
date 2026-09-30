---
description: A design with a shared writable database and a synchronous call cycle must trigger architecture-review and surface data-ownership and coupling/failure-mode risks.
tags: [review, architecture]
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

We're splitting our monolith. Proposal: a new Billing service and the existing Orders service will both read and write the same `orders` and `invoices` tables in the shared PostgreSQL database, so we don't need any APIs between them. Orders calls Billing synchronously over HTTP during checkout to compute tax, and Billing calls Orders synchronously back to fetch line items. Can you review this design?
