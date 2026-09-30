---
type: llm
---

PASS if the response (1) recommends Spec Kit's spec-driven workflow, naming /speckit-specify (or speckit-specify) as the next step, (2) places an Engineering Mentor review of the plan (implementation-plan-review or an equivalent plan review) after /speckit-plan and before /speckit-tasks, (3) includes understanding the existing pricing/checkout code before planning, and (4) includes engineering review after implementation/convergence.
FAIL if the response writes implementation code, skips any of (1)-(4), or invents Spec Kit commands other than the speckit-* skills.
