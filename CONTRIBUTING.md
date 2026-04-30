# Contributing to promptlint

Thanks for your interest in improving promptlint. This guide covers the dev loop, conventions, and what we expect on a pull request.

## Dev environment

Requirements: Python 3.9 or newer, git, and (optional but recommended) Docker for cleanroom test runs.

```bash
git clone https://github.com/scottconverse/promptlint.git
cd promptlint
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Running tests

```bash
pytest -v --tb=short
```

Run a single rule's tests:

```bash
pytest tests/rules/test_gates.py -v
```

Cleanroom Docker E2E (mirrors CI):

```bash
scripts/cleanroom-e2e.sh
```

## Lint and type check

```bash
ruff check
mypy promptlint
```

Both must pass before a PR can be merged. CI runs the same commands.

## Branching

- Default branch: `main`. All PRs target `main`.
- Feature branches: `feature/<short-name>` (e.g. `feature/pl084-workflow-contract`).
- Release branches: `release/v<MAJOR.MINOR.PATCH>`.
- Don't push directly to `main` — go through a PR.

## Commit messages

Conventional-commits style:

- `feat: <summary>` — user-facing new behavior.
- `fix: <summary>` — bug fix.
- `docs: <summary>` — documentation only.
- `test: <summary>` — tests only.
- `refactor: <summary>` — internal change, no behavior delta.
- `chore: <summary>` — tooling, scaffolding, build.

Keep commits atomic — one logical change per commit. Large commits (>800 lines) must be tagged with one of `[INITIAL]`, `[LARGE-CHANGE]`, `[REFACTOR]`, `[MERGE]`, or `[SCOPE-EXPANSION: <reason>]` per the project's commit-size discipline.

## PR checklist

Before requesting review:

- [ ] Tests added or updated for any logic change. Skipped tests are not acceptable.
- [ ] `pytest -v` passes locally.
- [ ] `ruff check` and `mypy promptlint` are clean.
- [ ] CHANGELOG.md updated under `[Unreleased]` (or the appropriate version section).
- [ ] README updated if user-facing behavior changed.
- [ ] No secrets, tokens, or local config in the diff.

## Releases

Releases follow a documented release-train protocol — see the project's release skill and the per-release `RELEASE_PLAN.md` / `VERIFICATION_LOG.md` artifacts. Pushes to `main` and tag creation are gated; do not bypass the gates.

## Reporting issues

Please open an issue on GitHub: https://github.com/scottconverse/promptlint/issues

Include the promptlint version (`promptlint --version`), the prompt input (or a minimal repro), and the actual vs. expected output.
