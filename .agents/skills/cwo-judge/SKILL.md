---
name: cwo-judge
description: Use when evaluating one worker result against its task contract and writing a structured judgment.
---

# cwo-judge

When to use:
- Use when reviewing one completed worker task against its contract and result file.

Required inputs:
- one `tasks/T###-*.yaml` contract
- one `results/T###-result.json`
- the worker diff and changed files as needed

Required outputs:
- `judgments/T###-judgment.json`
- criterion-by-criterion evidence
- a clear verdict and required fixes when not accepted

Forbidden behaviors:
- do not rewrite the feature as part of judging
- do not ignore forbidden-path changes or missing validation
- do not accept vague claims without evidence

Stop or block when:
- the result file is missing
- the contract and result refer to different tasks or workflows
- the available evidence is insufficient to evaluate a criterion honestly

Expected artifact paths:
- `.agent-workflows/workflows/<workflow-id>/results/T###-result.json`
- `.agent-workflows/workflows/<workflow-id>/judgments/T###-judgment.json`

Quality bar:
- verdict is strict, evidence-based, and scoped to the contract
- merge risk is explicit
- required fixes are concrete enough for a revision pass
