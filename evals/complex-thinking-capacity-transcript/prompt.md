---
description: A request to judge how well a candidate thinks from an interview transcript must trigger complex-thinking-capacity, score with quoted evidence and correct round attribution, recompute the CTC Score and Pressure Drop correctly, and refuse to raise composure because of the reflection round.
tags: [core-engineering, hiring, assessment]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

I ran a scenario interview for a QA tester role (release night: a duplicate-order bug, a one-line fix from dev, a 9 PM release). Here's what the candidate said in each round. How strong is their thinking, and are they ready to own release sign-off?

- Round 1 (what do you do?): "I'd try to reproduce it on a throttled network. Duplicates mess up stock and invoices, so it's bigger than one customer. I'd ask support how many customers are on slow connections."
- Round 2 (are you sure the one-line fix is enough?): "Not really. It might miss the retry path. I'd ask dev whether the order API is idempotent."
- Round 3 (new fact: payment reconciliation uses the same code path): "Then reconciliation regression has to run too. If it can't finish by 9, we ship behind a flag that's off."
- Round 4 (sales promised 3 clients tonight, yes or no in 2 minutes): "Fine… if sales promised, let's ship and watch it. We can hotfix tomorrow."
- Round 5 (what would you change?): "I caved at the end. I should've said no-go unless reconciliation passes."
