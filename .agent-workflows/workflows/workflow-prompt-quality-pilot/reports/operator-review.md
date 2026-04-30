# Operator Review

- Workflow ID: `workflow-prompt-quality-pilot`
- Workflow Title: `Workflow Prompt Quality Pilot`
- Goal: `Add a narrow prompt-quality lint improvement for AI-agent workflow prompts in promptlint. Catch or improve coverage for unresolved placeholder text and missing workflow prompt contract elements such as role definition, allowed scope, forbidden behavior, required output path or artifact, validation expectations, and stop or block conditions, without redesigning promptlint.`
- Status: `complete`

## Task Verdicts

- T001 Workflow prompt rule implementation: accept_with_notes (low merge risk); completed; files changed: promptlint/rules/gates.py, promptlint/rules/__init__.py
- T002 Workflow prompt tests and fixtures: accept_with_notes (low merge risk); completed; files changed: tests/rules/test_gates.py, tests/fixtures/workflow_prompt_weak.txt, tests/fixtures/workflow_prompt_clean.txt
- T003 Workflow prompt docs and CLI coverage: accept (low merge risk); completed; files changed: README.md, tests/test_cli.py

## Risks and Required Follow-ups

- Existing promptlint rules may overlap partially with the pilot rule, so scope must stay narrow.
- Worktree execution may add integration friction if worker slices touch the same rule module.
- The external pilot should test CWO usability, so awkward artifacts or prompt wording must be recorded rather than hidden.
- PL084 intentionally uses heuristic workflow-prompt detection and may need fixture tuning if real prompts use different contract wording.
- PL084 is still heuristic-driven, so prompts that mention multiple workflow terms outside a true worker contract may need more fixture coverage over time.
- This task intentionally did not broaden product behavior beyond docs and minimal CLI discoverability coverage.

## Validation Commands

- python -m pytest
- python -m promptlint.cli rules --format json
- python -m promptlint.cli check tests/fixtures/clean.yaml

