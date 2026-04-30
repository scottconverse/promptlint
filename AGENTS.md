# Codex Workflow Guidance

- Use `.agent-workflows/` as durable workflow state.
- Use Worktree mode for worker tasks when parallel isolation matters.
- Treat task contracts as the authority for worker scope.
- Do not expand worker scope or refactor unrelated files.
- Write worker result and judge judgment files as part of the workflow.
- Keep final merge, commit, and release decisions under human operator control.
