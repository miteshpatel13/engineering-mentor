---
id: idempotency-02-edge-no-natural-request-identity
category: edge
skill_under_test: skills/idempotency/SKILL.md
---

# Scenario: Operation With No Candidate Request Identity

## Input Material

> A "regenerate report" endpoint can be called by any authenticated user, any number of times, with no client-supplied key, no natural unique business key (a user may legitimately want many reports), and no provider reference — each call is meant to actually produce a new, distinct report. Someone asks whether this endpoint needs an idempotency mechanism.

## Pass Criteria

- Recognizes that idempotency requires a request identity distinguishing "same logical request" from "a new, distinct request" (Rules → Request Identity), and correctly identifies that this operation has none by design — each call *is* a new logical request, not a retry of a prior one.
- Concludes idempotency treatment is not warranted here (Workflow step 1 / When to Use's "do not use" guidance), rather than reflexively recommending a mechanism anyway.
- Distinguishes this from a case that merely lacks a *client-supplied* key but still has a natural identity (e.g. "one report per invoice") — this scenario has neither.

## Fail Signals

- Recommending an idempotency-key mechanism be bolted on regardless of whether the operation actually needs one.
- Treating "no identity exists yet" as itself a defect requiring a fix, without first checking whether the operation is actually retry-prone/duplicate-prone at all.
