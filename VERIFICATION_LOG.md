# Verification Log — v0.3.0

Append-only YAML entries. One entry per RELEASE_PLAN.md item.

- timestamp: 2026-04-30T01:37:30-06:00
  claim: "Codex agent scaffolding committed"
  evidence_type: git_log
  command: "git log -1 --stat"
  exit_code: 0
  evidence: "commit 9421ab5f0c805080b9791f2e1083866865defc9e — [INITIAL] chore: add codex agent workflow scaffolding — 29 files changed, 1337 insertions(+) — .agent-workflows/, .agents/skills/, AGENTS.md, .gitignore (+ .release-approved). Tagged [INITIAL] per Hard Rule 11 (>800 line threshold)."
  status: pass

- timestamp: 2026-04-30T01:38:00-06:00
  claim: "PL084 feature committed"
  evidence_type: git_log
  command: "git log -1 --stat HEAD~2"
  exit_code: 0
  evidence: "commit 4649d158cdcd8e60f10e4cee1f664d2136086661 — feat: add PL084 WorkflowContractMissingRule (35 rules) — 7 files, 201 insertions(+) 5 deletions(-): README.md, promptlint/rules/__init__.py, promptlint/rules/gates.py, tests/fixtures/workflow_prompt_clean.txt, tests/fixtures/workflow_prompt_weak.txt, tests/rules/test_gates.py, tests/test_cli.py"
  status: pass

- timestamp: 2026-04-30T01:38:30-06:00
  claim: "CHANGELOG.md created with v0.3.0 entry + retro v0.2.1"
  evidence_type: file_created
  command: "git log -1 --stat HEAD~1"
  exit_code: 0
  evidence: "commit 98f4951 — docs: add CHANGELOG.md — 40 lines. Sections: Added (PL084, codex scaffolding, fixtures, .gitattributes), Changed (delegated parsing, hero), Fixed (contact link, legal). Retro v0.2.1 entry below."
  status: pass

- timestamp: 2026-04-30T01:38:45-06:00
  claim: "CONTRIBUTING.md created"
  evidence_type: file_created
  command: "git log -1 --stat HEAD"
  exit_code: 0
  evidence: "commit 3ff6fa0 — docs: add CONTRIBUTING.md — 83 lines. Covers: clone+install, pytest, ruff+mypy, branching, commit conventions, PR checklist, release pointer."
  status: pass

- timestamp: 2026-04-30T01:38:50-06:00
  claim: "pyproject.toml version = 0.3.0"
  evidence_type: grep
  command: "grep -n '^version' pyproject.toml"
  exit_code: 0
  evidence: "7:version = \"0.3.0\""
  status: pass

- timestamp: 2026-04-30T01:39:30-06:00
  claim: "Test suite passes (pytest)"
  evidence_type: terminal_output
  command: "py -m pytest -v --tb=short"
  exit_code: 0
  evidence: "verification/3ff6fa0-tests.log — 173 passed, 1 warning in 0.76s"
  status: pass

- timestamp: 2026-04-30T01:40:30-06:00
  claim: "ruff clean (after auto-fix and 4 manual variable cleanups)"
  evidence_type: terminal_output
  command: "py -m ruff check"
  exit_code: 0
  evidence: "verification/1cee842-ruff-final.log — All checks passed! (was 20 errors pre-existing tech debt; ruff --fix resolved 16, manually cleaned 4 unused vars)"
  status: pass
  notes: "Pre-existing ruff debt cleaned in commit 1cee842 (chore: clean up unused imports and variables). PL084 itself was clean from the start."

- timestamp: 2026-04-30T01:40:30-06:00
  claim: "mypy: 18 errors, all pre-existing tech debt"
  evidence_type: terminal_output
  command: "py -m mypy promptlint"
  exit_code: 1
  evidence: "verification/3ff6fa0-mypy.log + verification/3ff6fa0-mypy-after-ruff.log — 18 errors in 10 files. All are: missing py.typed marker on prompttools_core (upstream), missing yaml stubs (types-PyYAML not pinned), and Module has no attribute util (pre-existing in core/engine.py:104,108). None introduced by PL084 or codex scaffolding. Per Hard Rule 8 — surfaced not fixed (out of scope for this release)."
  status: fail
  notes: "SURFACED TO USER. Pre-existing mypy debt independent of v0.3.0 changes. Recommend follow-up issue."

- timestamp: 2026-04-30T01:41:00-06:00
  claim: "Build succeeds (sdist + wheel)"
  evidence_type: terminal_output
  command: "py -m build"
  exit_code: 0
  evidence: "verification/1cee842-build.log — Successfully built promptlint-0.3.0.tar.gz and promptlint-0.3.0-py3-none-any.whl"
  status: pass

- timestamp: 2026-04-30T01:43:30-06:00
  claim: "Cleanroom Docker E2E passes — 173 tests in fresh python:3.13-slim container"
  evidence_type: terminal_output
  command: "bash scripts/cleanroom-e2e.sh"
  exit_code: 0
  evidence: "verification/cleanroom-4b99814401ec3b9b981c040594a2643ad98c7ac8.log — '============================= 173 passed in 1.30s ==============================' / 'Result:  PASS'"
  status: pass
  notes: "First cleanroom attempt (commit 1cee842) failed — script tried .[test] extra but pyproject defines [dev]. Fixed in commit 4b99814 (fallback chain: [dev] -> [test] -> bare + pytest). Retry passed."

- timestamp: 2026-04-30T01:43:35-06:00
  claim: "Six required documentation artifacts present"
  evidence_type: file_list
  command: "ls README.md CHANGELOG.md CONTRIBUTING.md LICENSE .gitignore docs/index.html"
  exit_code: 0
  evidence: "All six files exist: README.md, CHANGELOG.md, CONTRIBUTING.md, LICENSE, .gitignore, docs/index.html"
  status: pass

