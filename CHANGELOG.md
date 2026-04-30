# Changelog

All notable changes to promptlint are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-04-30

### Added
- **PL084 WorkflowContractMissingRule** — flags prompts that ask an agent to drive a multi-step workflow without specifying the workflow contract (entry/exit, artifacts, handoff). Brings total rule count to **35** across 10 categories.
- Codex agent workflow scaffolding under `.agent-workflows/` and `.agents/skills/` (planner / worker / judge / refinery / release-auditor) plus top-level `AGENTS.md`. Used for the workflow-prompt-quality pilot that produced PL084.
- Test fixtures `tests/fixtures/workflow_prompt_clean.txt` and `tests/fixtures/workflow_prompt_weak.txt` covering the new rule.
- `.gitattributes` for LF line-ending normalization (carried from v0.2.1).

### Changed
- Parsing and shared model types now delegated to `prompttools-core`; promptlint imports from the upstream package rather than maintaining its own copies.
- README hero rewritten to lead with the lint-and-rewrite value proposition.

### Fixed
- Replaced placeholder contact email with the GitHub Issues link.
- Added explicit legal disclaimer and Terms of Service pointer.

## [0.2.1] - 2026-04-29

### Changed
- Documentation refresh covering PL090 and the 34-rule / 10-category surface.
- Hero README copy update.

### Fixed
- Removed fake contact email; routed support through GitHub Issues.
- Added legal disclaimer and Terms of Service link.

## [0.2.0] - earlier

Initial public release with the 33-rule baseline.

[0.3.0]: https://github.com/scottconverse/promptlint/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/scottconverse/promptlint/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/scottconverse/promptlint/releases/tag/v0.2.0
