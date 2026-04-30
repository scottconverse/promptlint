# Pilot Retrospective

- Workflow ID: `workflow-prompt-quality-pilot`
- Target Repo: `promptlint`
- Date: `2026-04-29`

## Answers

- Did the planner produce good task boundaries?
  Yes. Splitting the pilot into rule implementation, tests/fixtures, and docs/CLI coverage kept each worker slice small and made the final merge straightforward.

- Did the workers stay within scope?
  Yes. T001 stayed in `promptlint/rules`, T002 stayed in `tests`, and T003 stayed in `README.md` plus `tests/test_cli.py`.

- Did the judges catch meaningful issues?
  Yes. The judge flow surfaced that T001 still needed supporting tests/docs before merge and recorded the heuristic nature of `PL084` rather than treating the first task as complete on its own.

- Did the refinery step help or add friction?
  It helped. The refinery pass was the right place to integrate the slices, run full-repo validation, and record the baseline `PL082` warning on `tests/fixtures/clean.yaml` so the pilot report stayed honest.

- Were generated prompts clear enough to use without rewriting?
  Mostly. They were usable, but one worker still returned `commands_run` in the wrong shape, which suggests the output contract section could be even more explicit in future pilots.

- Were any CWO artifacts missing or awkward?
  Slightly. The generated operator review file started as a skeletal summary and needed a richer refinery report plus this retrospective to tell the full story.

- Did the fixed task-ID locking behave correctly?
  Yes. The external pilot created and used the workflow artifacts without duplicate task IDs or workflow corruption.

- Did any new CWO bugs appear?
  No hard blocker appeared, but there is a usability issue: malformed worker result artifacts are easy to produce and `cwo status` fails hard on them instead of reporting a friendlier validation error.

- What should change before pilot #2?
  Tighten worker-result contract guidance or validation messaging, enrich the generated operator report a bit more, and keep using narrow 2-4 task pilots so the workflow remains easy to judge.
