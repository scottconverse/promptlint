---
name: cwo-release-auditor
description: Use when producing a final operator release checklist covering tests, docs, risks, and unresolved issues.
---

# cwo-release-auditor

When to use:
- Use for the final operator-facing audit before branch, PR, or release review.

Required inputs:
- workflow report artifacts
- judgments and refinery report
- docs, prompts, schemas, and examples touched by the workflow

Required outputs:
- an operator-focused release checklist
- explicit callouts for missing evidence, doc drift, test gaps, or unresolved risk

Forbidden behaviors:
- do not invent test passes that did not happen
- do not treat missing workflow artifacts as acceptable
- do not approve release if validation evidence is incomplete

Stop or block when:
- required workflow artifacts are missing
- prompts, schemas, docs, and examples are out of sync
- unresolved risks lack operator acknowledgment

Expected artifact paths:
- `.agent-workflows/workflows/<workflow-id>/reports/operator-review.md`
- `.agent-workflows/workflows/<workflow-id>/reports/refinery-report.md`

Quality bar:
- release checklist is specific and evidence-based
- remaining risks are clearly separated from accepted work
- operator can decide ship, revise, or reject from the audit alone
