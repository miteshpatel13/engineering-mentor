---
description: Before a schema change, codebase-orientation must build an evidence-based footprint by direct inspection when Graft is unavailable, including a non-code SQL view consumer.
tags: [smoke, graft, orientation]
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

We want to split `users.name` into `first_name` and `last_name`. Before we plan anything: what in this codebase would that change touch?
