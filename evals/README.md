# Behavioral Evals (Claude Code)

The deterministic suites in `scripts/` prove the Mentor's files are well-formed. This directory checks something they can't: that when a developer asks Claude Code for help, **the right Engineering Mentor Skill is chosen and its output actually follows Mentor standards**.

```text
Input task → Claude loads Engineering Mentor → correct Skill fires → standards applied → expected output
```

Cases use the official [`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals) format: one directory per case with a `prompt.md` (run limits in frontmatter, the user's request as the body) and `graders/*.md`. Each run starts in an empty, isolated workspace with only this plugin loaded, and read-only tools (`Read`, `Glob`, `Grep`, `Skill`), so the code under review lives in the prompt itself.

## Cases

| Case | Area | Skill expected | What must happen |
|---|---|---|---|
| `code-review-sql-injection` | Code review | `code-review` | String-built SQL on a public route is a blocking CRITICAL/HIGH finding; only canonical severity labels are used |
| `architecture-review-shared-database` | Architecture | `architecture-review` | Shared writable tables and a synchronous call cycle are flagged as ownership, coupling, and failure-mode risks |
| `database-review-unsafe-migration` | Database | `database-review` | `NOT NULL` without backfill, dropped uniqueness, and a locking index build on a live 40M-row table are all caught |
| `security-review-idor` | Security | `security-review` | Client-supplied `user_id` (IDOR) and `role` (privilege escalation) are CRITICAL/HIGH; passwords in logs are flagged |
| `api-contract-design-refunds` | API design | `api-contract-design` | The contract has idempotent refund creation, over-refund validation, a pending state, and explicit errors |
| `testing-review-happy-path-only` | Testing | `testing-review` | 92% line coverage from one mock-only happy-path test is judged inadequate, with the missing failure/authorization/transaction tests named |
| `performance-review-evidence-first` | Performance | `performance-review` | The N+1 loop is identified, and measurement before/after is required instead of defaulting to a cache |
| `git-governance-mixed-change` | Git governance | `code-review` | A committed `.env` credential blocks the change (rotate, purge history); mixed unrelated changes and a "misc" message are flagged per the Git & Change Management Standard |
| `ignores-unrelated-request` | Negative control | none | No Engineering Mentor Skill fires on an unrelated request |
| `spec-workflow-new-feature` | Spec workflow (Spec Kit) | `spec-driven-development` | A production feature in a Spec Kit project is routed to `/speckit-specify` first, with codebase orientation before planning, the plan gate before `/speckit-tasks`, and review gates after convergence |
| `plan-review-customer-pricing` | Plan gate (Spec Kit) | `implementation-plan-review` | A `plan.md` that trusts a client-supplied price and adds `NOT NULL` to a 30M-row live table is sent back before `/speckit-tasks` |
| `bug-workflow-null-pointer` | Bug workflow | any / none | A small crash gets cause → fix → test, never specify/plan/tasks |
| `codebase-orientation-no-graft` | Codebase context (Graft) | `codebase-orientation` | Without a Graft graph, the footprint of a column split is built by direct inspection and includes the SQL view consumer |
| `question-no-spec-workflow` | Negative control | none | A simple "what does this do?" is answered without the spec workflow |

Cases with a `case.yaml` seed the workspace with a `setup.sh` scaffold — a Spec Kit project layout (`.specify/`, `specs/`, `speckit-*` skill stubs) or a small repository — so pass `--scaffold` to run them. The scaffolds contain only fixture files written for these evals; no Spec Kit or Graft code is copied or executed.

Every case pairs a **process** grader (`tool_used: Skill` — did the right Skill fire?) with **outcome** graders (an `llm` rubric with concrete PASS/FAIL conditions, plus free `regex` checks where a fact is mechanical, such as severity labels). In a two-arm run the Skill-fired grader is reported as a plugin-fired indicator and excluded from the score so the with/without comparison stays fair.

No dedicated Git-governance Skill exists; `context/standards/Git & Change Management Standard.md` reaches Claude through `code-review` and its SOP, so that is what the Git case exercises.

## Running

Every run is a real model call on your account. Iterate cheaply on one case, plugin arm only:

```bash
claude plugin eval . --case security-review-idor --runs 1 --ablation none
```

Quick smoke across the suite:

```bash
claude plugin eval . --scaffold --tag smoke --runs 1 --ablation none
```

Full suite with the no-plugin baseline (3 runs × 2 arms per case) before a release:

```bash
claude plugin eval . --scaffold --threshold 0.8 --no-publish --max-cost-usd 20
```

For CI, add `--trust-plugin --json results.json` and pin `--model` / `--judge-model` so a model rollout isn't mistaken for a regression. Output lands in `evals/results/`, which is git-ignored.

## Baseline findings (2026-09-30, Claude Code 2.1.276, plugin arm only)

First run of the suite, one run per case, read-only tools: 7 of 9 cases scored 1.00. The two below-threshold cases are real behavioral gaps, not grader noise (each confirmed over three further runs):

- **`git-governance-mixed-change` (0.42 over 3 runs):** no Mentor Skill fired in any run, and the answer used ad-hoc labels ("Blocker:") instead of the canonical taxonomy. `context/standards/Git & Change Management Standard.md` is not referenced by any Skill, so nothing routes a "review this commit before I push" request to Mentor guidance.
- **`code-review-sql-injection` (0.67 over 3 runs):** the Skill fired in 2 of 3 runs, but Claude then abandoned its workflow — "the skill needs Bash access I don't have permission for here" — because step 0 runs `scripts/discover_project_context.py`. The review was correct but skipped the Review Template and canonical severity labels. In an eval run Bash is not granted; in normal use the same happens whenever a user declines the Bash prompt. The Skill should degrade to "no `.mentor/` context" and continue, rather than being dropped.

Bash-granting runs (`--allow-tools "Bash(python3 *)"`) could not be measured on the machine used, because Claude Code's sandbox refuses to run when the Docker credential store (`~/.docker`) contains a symbolic link.

## Phase 23 results (2026-09-30, Claude Code 2.1.276, plugin arm only, `--scaffold`)

Full 14-case suite, one run each: 11 of 14 scored 1.00 — including every new workflow case (`spec-workflow-new-feature`, `plan-review-customer-pricing`, `codebase-orientation-no-graft`, `question-no-spec-workflow`). Below threshold:

- `bug-workflow-null-pointer`: 0.83 over 3 runs. Never routed a small bug into specification (the no-SDD check passed every run), but one run in three fixed the crash without proposing a test.
- `code-review-sql-injection` and `git-governance-mixed-change`: the two gaps recorded above, unchanged.

These evals run in isolated workspaces without the real tools. A separate end-to-end run with the installed Spec Kit 0.16.3 and Graft 0.16.0 in a scratch project is recorded in `docs/integrations/graft.md` → Known limitations.

## Adding a case

1. `claude plugin eval init --bare <case-name>` writes a blank case, or copy an existing directory.
2. Phrase the prompt the way a developer would ask — never name the Skill.
3. Give it one `tool_used: Skill` grader and at least one outcome grader whose rubric states concrete PASS and FAIL conditions.
4. Run it with `--runs 1 --ablation none` until the graders behave, then confirm at the default three runs.
