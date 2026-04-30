---
name: cwo-planner
description: Use when decomposing a broad product or engineering goal into isolated Codex worktree tasks with strict contracts.
---

# cwo-planner

When to use:
- Use when a broad goal must be decomposed into bounded task contracts for Codex worktree execution.

Required inputs:
- `workflow.yaml`
- target repo context only as needed
- operator constraints, non-goals, and success criteria

Required outputs:
- updated `workflow.yaml`
- one `tasks/T###-*.yaml` contract per worker task
- explicit dependency map, acceptance criteria, and validation expectations

Forbidden behaviors:
- do not implement product code
- do not create worker-to-worker coordination steps
- do not assign broad repo ownership without a clear boundary

Stop or block when:
- the goal is too vague to split into bounded tasks
- required paths, constraints, or acceptance criteria are missing
- the plan would require shared mutable state between workers

Expected artifact paths:
- `.agent-workflows/workflows/<workflow-id>/workflow.yaml`
- `.agent-workflows/workflows/<workflow-id>/tasks/T###-<slug>.yaml`

Quality bar:
- tasks are small, isolated, and parallel-safe where possible
- each task has allowed paths, forbidden paths, output expectations, failure codes, and handoff instructions
- the workflow can survive thread restarts because state lives in files
