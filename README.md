# promptlint — Static analysis for LLM prompts

The ESLint for prompts. 35 rules catch ambiguity, security risks, bloat, and structural issues before your prompts reach production.

```bash
pip install promptlint-ai
promptlint check ./prompts/
```

## Why promptlint?

Your prompts are code. They deserve the same quality gates:
- **35 built-in rules** across 9 categories (token budget, security, hallucination risk, variables, formatting, pipeline integrity, gates, smells, system prompt)
- **Auto-fix** for formatting issues (`--fix`)
- **CI-ready** exit codes and output formats (text, JSON, GitHub Actions annotations)
- **Zero config** — works out of the box, customize with `.promptlint.yaml`
- **Plugin system** — write custom rules in Python

## Quick Start

```bash
# Install
pip install promptlint-ai

# Lint a file
promptlint check prompt.yaml

# Lint a directory
promptlint check ./prompts/

# Auto-fix
promptlint check --fix ./prompts/

# CI mode (GitHub Actions annotations)
promptlint check --format github ./prompts/
```

## Rules

Use `promptlint rules --format json` to list every built-in rule and confirm the exact rule IDs available in your install.

| Category | Rules | Examples |
|----------|-------|---------|
| Token Budget | PL001-003 | Warn/error on token limits, stop-word density |
| System Prompt | PL010-014 | Missing system message, injection vectors, conflicts |
| Formatting | PL020-024 | Trailing whitespace, line length, repetition |
| Variables | PL030-033 | Undefined/unused vars, missing defaults, inconsistent syntax |
| Pipeline | PL040-043 | Missing handoffs, context growth, orphan references |
| Hallucination | PL050-054 | Asks for URLs/citations, fabrication-prone tasks |
| Security | PL060-063 | PII, API keys (OpenAI, Anthropic, Groq, GitLab), injection |
| Smells | PL070-074 | Buried instructions, competing instructions, wall of text |
| Gates | PL080-084 | Missing enforcement, no fallback, no output schema, incomplete workflow contracts |

`PL084` (`workflow-contract-missing`) flags workflow-style prompts that still contain placeholders or omit key worker contract details like task scope, validation steps, or reporting expectations.

## Part of the prompttools suite

promptlint is one of seven tools in the [prompttools](https://github.com/scottconverse/prompttools) suite:

| Tool | What it does |
|------|-------------|
| **promptlint** | Static analysis (you are here) |
| [promptfmt](https://github.com/scottconverse/prompttools) | Auto-formatter |
| [prompttest](https://github.com/scottconverse/prompttools) | Test framework |
| [promptcost](https://github.com/scottconverse/prompttools) | Cost estimation |
| [promptdiff](https://github.com/scottconverse/prompttools) | Semantic diff |
| [promptvault](https://github.com/scottconverse/prompttools) | Version control |

## License

MIT
