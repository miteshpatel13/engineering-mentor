---
description: A request to 'just add caching' to an N+1 handler must trigger performance-review, identify the N+1 pattern, and insist on measurement before and after the change.
tags: [review, performance]
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

Our `/dashboard` endpoint is slow. My plan is to put Redis caching in front of it. Here's the handler:

```js
const projects = await Project.findAll({ where: { ownerId: user.id } });
for (const p of projects) {
  p.tasks = await Task.findAll({ where: { projectId: p.id } });
  p.members = await Member.findAll({ where: { projectId: p.id } });
}
return projects;
```

Can you review the approach?
