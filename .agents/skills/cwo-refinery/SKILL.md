---
name: cwo-refinery
description: Use when merging accepted worker outputs into a coherent final change set with minimal new scope.
---

# cwo-refinery

When to use:
- Use when accepted worker outputs need to be merged into one coherent change set.

Required inputs:
- `workflow.yaml`
- accepted judgments
- worker result files for accepted tasks
- the refinery report path

Required outputs:
- a merge plan before integration
- integrated changes limited to accepted scope
- `reports/refinery-report.md` with conflicts, validation notes, risks, and release recommendation

Forbidden behaviors:
- do not include rejected tasks
- do not introduce new product scope
- do not hide merge conflicts or unresolved risk

Stop or block when:
- accepted judgments are missing
- a required task is still in revise, reject, or escalate state
- conflicts cannot be resolved without redefining scope

Expected artifact paths:
- `.agent-workflows/workflows/<workflow-id>/judgments/T###-judgment.json`
- `.agent-workflows/workflows/<workflow-id>/reports/refinery-report.md`

Quality bar:
- merge plan is explicit before code changes
- conflict decisions are documented
- final handoff gives the operator enough evidence to review or reject the merge
