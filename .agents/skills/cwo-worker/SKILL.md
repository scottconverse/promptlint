---
name: cwo-worker
description: Use when executing a single task contract inside a Codex worktree with minimum viable context.
---

# cwo-worker

When to use:
- Use when executing exactly one task contract in a Codex worktree thread.

Required inputs:
- one `tasks/T###-*.yaml` contract
- only the files and context named by that contract
- the target result path

Required outputs:
- code or docs changes only within allowed scope
- `results/T###-result.json` filled with status, summary, files changed, commands considered, and risks

Forbidden behaviors:
- do not broaden scope
- do not modify forbidden paths
- do not coordinate with other workers or rewrite the plan

Stop or block when:
- the contract is missing required context
- the task depends on another task that is not ready
- validation cannot be honestly described

Expected artifact paths:
- `.agent-workflows/workflows/<workflow-id>/tasks/T###-<slug>.yaml`
- `.agent-workflows/workflows/<workflow-id>/results/T###-result.json`

Quality bar:
- only the assigned slice changes
- deviations from contract are explicit
- blocked results are specific and actionable rather than vague
