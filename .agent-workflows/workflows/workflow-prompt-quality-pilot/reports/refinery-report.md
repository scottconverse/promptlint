# Refinery Report

- Workflow ID: `workflow-prompt-quality-pilot`
- Workflow Title: `Workflow Prompt Quality Pilot`
- Source Branch: `main`
- Base Branch: `main`
- Accepted Tasks: `T001 (accept_with_notes), T002 (accept_with_notes), T003 (accept)`
- Rejected or Excluded Tasks: `None`
- Release Recommendation: `Approve for pilot use`

## Merge Plan

1. Integrate the narrow PL084 gate rule and built-in rule registration from `T001`.
2. Integrate the focused PL084 fixtures and gate-rule coverage from `T002`.
3. Integrate the README and CLI discoverability updates from `T003`.
4. Validate the full repo, then verify the weak and clean workflow fixtures behave as expected from the CLI.

## Files Merged

- `promptlint/rules/gates.py`
- `promptlint/rules/__init__.py`
- `tests/rules/test_gates.py`
- `tests/fixtures/workflow_prompt_weak.txt`
- `tests/fixtures/workflow_prompt_clean.txt`
- `README.md`
- `tests/test_cli.py`

## Conflicts Encountered

- Worker slices depended on the T001 rule shape, so the T001 rule files were copied into the T002 and T003 worktrees before downstream work continued.
- No textual merge conflicts occurred in the final integration pass.

## Conflict Resolutions

- Treated T001 as the source-of-truth rule implementation.
- Limited T002 to tests and fixtures only.
- Limited T003 to README and CLI-facing test coverage only.

## Validation Commands Requested

- `python -m pytest`
- `python -m promptlint.cli rules --format json`
- `python -m promptlint.cli check tests/fixtures/clean.yaml`

## Validation Commands Run

- `python -m pytest`
- `python -m promptlint.cli rules --format json`
- `python -m promptlint.cli check tests/fixtures/workflow_prompt_weak.txt`
- `python -m promptlint.cli check tests/fixtures/workflow_prompt_clean.txt`
- `python -m promptlint.cli check tests/fixtures/clean.yaml`

## Validation Results

- `python -m pytest`: passed (`173 passed, 1 warning`)
- `python -m promptlint.cli rules --format json`: passed and lists `PL084 workflow-contract-missing` in the `gate` category
- `python -m promptlint.cli check tests/fixtures/workflow_prompt_weak.txt`: expected warning result; PL084 fired alongside PL022
- `python -m promptlint.cli check tests/fixtures/workflow_prompt_clean.txt`: passed with no violations
- `python -m promptlint.cli check tests/fixtures/clean.yaml`: warning-only failure caused by pre-existing `PL082 output-schema-missing`; this is a baseline fixture behavior, not a regression from the pilot

## Unresolved Risks

- `PL084` remains heuristic and section-pattern based; broader real-world fixture coverage may still be useful before claiming wide workflow-prompt coverage.
- The weak workflow fixture currently triggers both `PL022` and `PL084`, which is acceptable for this pilot but may need UX review later if rule messaging becomes noisy.
- One worker initially wrote a result artifact with an invalid `commands_run` shape, and that had to be normalized by hand before `cwo status` could read it cleanly.

## Rollback Notes

- Revert `PL084` by removing `WorkflowContractMissingRule` from `promptlint/rules/gates.py` and its registration from `promptlint/rules/__init__.py`.
- Revert the pilot coverage by removing the two workflow prompt fixtures plus the new PL084 tests and CLI assertions.
- Re-run `python -m pytest` and `python -m promptlint.cli rules --format json` after any rollback.

## Operator Review Checklist

- [x] All three worker result files exist.
- [x] All three judgment files exist.
- [x] Final integrated repo validation was run in the main checkout.
- [x] The workflow left behind prompts, results, judgments, and reports.
- [x] The pilot stayed narrow and avoided unrelated promptlint redesign.
- [x] CWO worktree locking held; no duplicate task IDs or workflow corruption occurred.

## Final Summary

The refinery pass integrated a small real promptlint improvement: `PL084 workflow-contract-missing`, a narrow gate rule for weak AI-agent workflow prompts. The pilot also added focused fixtures, gate-rule tests, and CLI/README discoverability coverage. The target repo validates successfully for the integrated change set, with one documented baseline warning on `tests/fixtures/clean.yaml` that predates this pilot.
