# Verification by gate

## Structural lint

`python -m unittest discover -s tests -v` validates metadata, supporting links, evaluation-fixture structure, and checked fixture arithmetic. These tests do not prove an LLM follows instructions. See the individual test names for exact coverage.

## Install and command discovery

A clean clone into an isolated HERMES_HOME skills directory exposed `/based` through the installed Hermes command scanner. This proves discovery on the tested install, not execution on every runtime/provider.

## Model and workflow components

The initial smoke test used three separate Sonnet conversations on a fictional founder question, followed by parent synthesis and a fourth fresh Sonnet reviewer. The reviewer returned REVISE; that was not a fully passing quality benchmark. Returned model usage identified claude-sonnet-5-5.

## Comparative pilot

The [five-case offline pilot](evaluations/pilot-v1/REPORT.md) completed 45 real calls with three conditions. It records real traces, token usage, and elapsed time, and includes regressions rather than only wins. The report separates unblinded author observations from pending human scores. It does not test live-source retrieval, statistical superiority, or full automated slash-to-final execution. Final guard improvements were made after this pilot; no wholesale rerun is claimed.

## Targeted final-reviewer sensitivity checks

After the pilot-driven amendments, two new tool-free Sonnet reviewer calls received deliberately flawed synthetic drafts. Both returned REVISE: one identified stale pricing, hearsay upgraded into a report, and a false tool-verification claim; the other identified unproven demand and missing timeline, owner, budget, and stop conditions. See the [evidence check](evaluations/targeted-v11/reject-false-evidence.json) and [plan check](evaluations/targeted-v11/preserve-plan-constraints.json). These are limited component checks, not a rerun of the comparative pilot or proof that every revised answer will satisfy the reviewer. There is no clean-draft control in these two checks, so false-REVISE behavior remains untested. Reviewer suggestions themselves still require parent scrutiny.

## v1.2 tone spot checks

The [v1.2 voice report](evaluations/tone-v12/REPORT.md) records 13 actual Sonnet component calls: seven initial new-voice fixtures, two old-voice controls, two reviewer controls, and two follow-ups after a narrow amendment. The clean reviewer control returned PASS and the insulting, unsupported draft returned REVISE. Initial defects and fallible reviewer suggestions are preserved, not hidden. The author inspection was unblinded; no representative preference, adoption improvement, automatic full-panel compliance, or rerun of the earlier comparative pilot is claimed. Current structural tests check the new rules' presence and fixture math, not LLM compliance.

## Reproduce

Requires Python standard library and an existing authenticated Claude Code supporting the flags in [model routing](references/model-routing.md). The optional helper is not required to install/use the skill:

```sh
python evaluations/run_pilot.py --output evaluations/my-new-run
```

Inspect prompts and approve account usage first. Five cases make 45 model calls; no model price is assumed. Use a new output path: existing results are not overwritten. On any model failure the run is marked incomplete; no silent premium fallback or fabricated result is allowed. Judge working directories are separate; only synthetic fixture content is supplied. The default model alias can resolve differently later; actual returned identities are recorded.

## Remaining limits

No human-blind scores yet, no general quality guarantee, no live-web research evaluation, no demonstrated non-Claude full workflow, and no programmatic enforcement of the Markdown skill. Context isolation is not an OS sandbox. Do not describe the skill as fully tested or unbiased.
