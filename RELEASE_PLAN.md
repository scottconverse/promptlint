# Release v0.3.0

**Type:** feature
**Summary:** Add PL084 WorkflowContractMissingRule (35 total rules); add codex agent workflow scaffolding
**Generated:** 2026-04-30
**Previous version:** v0.2.1

## Implementation
- [x] Stage and commit codex agent scaffolding: `.agent-workflows/`, `.agents/`, `AGENTS.md` as `chore: add codex agent workflow scaffolding`
- [x] Stage and commit PL084 feature: `promptlint/rules/gates.py`, `promptlint/rules/__init__.py`, `tests/rules/test_gates.py`, `tests/fixtures/workflow_prompt_clean.txt`, `tests/fixtures/workflow_prompt_weak.txt`, `tests/test_cli.py`, `README.md` as `feat: add PL084 WorkflowContractMissingRule (35 rules)`
- [x] Create CHANGELOG.md (Keep a Changelog format) with v0.3.0 entry + retro v0.2.1 entry from git log
- [x] Create CONTRIBUTING.md (clone/install, test/lint commands, branch convention, PR checklist)
- [x] Verify version is `0.3.0` in `pyproject.toml` (already pre-bumped — confirm only)

## Verification
- [x] Test suite passes: `pytest -v --tb=short` (173 passed)
- [x] Lint clean: `ruff check` (clean after auto-fix + 4 manual cleanups)
- [ ] Type check clean: `mypy promptlint` (18 pre-existing errors — surfaced, not fixed; out of scope)
- [x] Build succeeds: `python -m build` (sdist + wheel)
- [x] Cleanroom Docker E2E passes: `scripts/cleanroom-e2e.sh` (173 passed in container)

## Documentation
- [x] README.md current (rule count 35) — already in working tree
- [x] CHANGELOG.md present with v0.3.0 entry
- [x] CONTRIBUTING.md present
- [x] LICENSE present (already)
- [x] .gitignore present (already)
- [x] docs/index.html present (already)

## Release
- [ ] Push branch `release/v0.3.0` to origin
- [ ] CI green on `release/v0.3.0` (poll every 110s, max 30 min)
- [ ] Merge `release/v0.3.0` to `main`
- [ ] Tag `v0.3.0`
- [ ] `gh release create v0.3.0` with summary as release notes

---

## Recent commits since v0.2.1
- 8279ff7 Refactor: delegate parsing and models to prompttools-core
- e54fa24 chore: add .gitattributes for LF normalization
- ab61a70 Update hero README for promptlint
- 01dffb4 Replace fake contact email with GitHub Issues link
- 1c80278 Add legal disclaimer and Terms of Service
- eae3c12 Update docs for PL090: 34 rules, 10 categories
- 9421ab5 [INITIAL] chore: add codex agent workflow scaffolding
- 4649d15 feat: add PL084 WorkflowContractMissingRule (35 rules)
- 98f4951 docs: add CHANGELOG.md
- 3ff6fa0 docs: add CONTRIBUTING.md
- 1cee842 chore: clean up unused imports and variables (ruff --fix)
- b5b6b2e fix: cleanroom script uses [dev] extra (was [test])  [committed wrong file content]
- 4b99814 fix: cleanroom uses [dev] extra so pytest is installed
