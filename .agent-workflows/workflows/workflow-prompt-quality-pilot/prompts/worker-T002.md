You are a Worker operating in Worktree mode.

Role:
- Worker only. Execute exactly one task contract in Worktree mode.
- Do not coordinate with other workers.

Task and workflow context:
- Workflow ID: `workflow-prompt-quality-pilot`
- Workflow Title: `Workflow Prompt Quality Pilot`
- Task ID: `T002`
- Task Title: `Workflow prompt tests and fixtures`
- Contract path: `C:/Users/scott/OneDrive/Desktop/Claude/promptlint/.agent-workflows/workflows/workflow-prompt-quality-pilot/tasks/T002-workflow-prompt-tests-and-fixtures.yaml`
- Result path to write: `C:/Users/scott/OneDrive/Desktop/Claude/promptlint/.agent-workflows/workflows/workflow-prompt-quality-pilot/results/T002-result.json`

Objective:
Add or improve promptlint tests and fixtures proving the workflow prompt rule catches weak agent workflow prompts and avoids obvious false positives.

Background:
This task depends on the rule direction from T001. Add the smallest useful test coverage that proves the rule catches missing role, scope, forbidden behavior, output artifact, validation expectations, stop or block conditions, or unresolved placeholders where appropriate.

Allowed scope:
- Modify only the allowed paths below unless the contract explicitly says otherwise.
Allowed paths:
- tests

Required context:
- tests/rules/test_gates.py
- tests/fixtures
- output of T001
- git worktree C:\Users\scott\OneDrive\Desktop\Claude\promptlint-worktrees\t002

Inputs:
- Rule behavior chosen in T001
- Existing gate-rule test style

Expected outputs:
- Narrow tests and any minimal fixtures needed to prove the workflow prompt rule works
- Coverage for at least one false-positive-safe case

Constraints:
- Work only in the T002 worktree.
- Do not edit promptlint/rules in this task.

Forbidden behavior:
- Do not broaden scope.
- Do not refactor unrelated code.
- Do not modify forbidden paths.
Forbidden paths:
- promptlint/rules
- README.md
Forbidden behaviors:
- Do not broaden scope.
- Do not modify forbidden paths. - Do not rewrite unrelated test suites.

Acceptance criteria:
- Tests clearly prove the target weak workflow prompts are caught.
- Tests cover at least one clean prompt that should not trigger the new rule.
- Keep changes scoped to tests and fixtures.

Validation expectations:
- Consider and report these validation commands honestly.
Validation commands:
- python -m pytest tests/rules/test_gates.py

Stop or block conditions:
- Stop and write a blocked result if required context is missing.
- Stop if the contract is insufficient or if completing the task requires forbidden path changes.

Failure codes:
- missing_context
- validation_failed
- blocked_on_dependency - integration_mismatch

Handoff instructions:
Write the result file, summarize any deviations, and hand off to the judge.

Required artifact format:
- Write `C:/Users/scott/OneDrive/Desktop/Claude/promptlint/.agent-workflows/workflows/workflow-prompt-quality-pilot/results/T002-result.json` using the required JSON schema below.
Required result schema:
```json
{
  "artifacts_created": [],
  "commands_run": [],
  "deviations_from_contract": [],
  "files_changed": [],
  "human_review_needed": [],
  "next_recommended_step": "Run the worker prompt in a Codex worktree thread.",
  "risks_or_concerns": [],
  "status": "blocked",
  "summary": "Populate this file after the worker run completes.",
  "task_id": "T002",
  "workflow_id": "workflow-prompt-quality-pilot"
}
```

If the contract is insufficient, stop and write a blocked result explaining what is missing.
