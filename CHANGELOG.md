# Changelog

Version labels describe the skill's instruction revisions. Evaluation directory names identify preserved test artifacts, not separate installable releases or a promise of compatibility. This history comes from the repository's commits and retained reports; earlier labels remain unchanged so the evidence stays traceable.

## Unreleased

- Install only the selected runtime adapter and four runtime references; keep evaluation guidance in the repository. Installed links to omitted documents point back to the repository.
- Add dry-run previews, explicit upgrades with timestamped backups (`--force` aliases `--upgrade`), uninstall, and concise expected-error messages.
- Check installed structure and meaningful contracts without pinning prose or a release version. Add a unit-test matrix covering Ubuntu (Python 3.9/3.12) and macOS (Python 3.11/3.12).
- Put installation and usage first in the README and document upgrade/uninstall behavior.
- Voice v2 after an A/B test found /based rigorous but long, narrated, and flat: one process line max (dissent as a single `Dissent:` line), triggered defect-specific verdict stings in voice.md, concrete named tools/vendors labelled '(unverified)', fetched primary pages for research, a light mode (no reviewer) alongside full, and headless/stated-budget runs proceed on the default route.
- Voice v3 after a round-2 A/B: exactly one fixed-template process line (none with flavor off) and no other process narration; a 1–2 sentence verdict whose sting is required when a supported defect exists and targets the plan, never the panel; the everyone-agrees check moves to the body; brainstorm ideas must be distinct opportunity channels with named sources; plans need a week-by-week operating cadence with owners. The reviewer REVISEs each violation.

## v0.21.0 beta — 2026-10-26

Commit `c1ad020` renumbered the experimental beta from `1.3.0` to `0.21.0`. This was a metadata/documentation change; it did not rerun or change the previously tested workflow. `71ff404` then standardized the public repository URL.

## Historical v1.3.0 — 2026-10-26

Commits `b3d0035` and `f5566d4` introduced portable Hermes/Claude Code adapters and the safe installer, then hardened installation and recorded native runtime verification. [native-v13](evaluations/native-v13/REPORT.md) means the v1.3 native verification set: two observed invocations per runtime, with three judges followed by a separate reviewer. Receipts retain the original tested payload hashes and version labels.

## Historical v1.2.0 — 2026-10-26

Commit `af0cce7` added measured bite to the voice guidance and evidence-bound safeguards against false aggression. [tone-v12](evaluations/tone-v12/REPORT.md) means the v1.2 voice component checks, including v1.1 controls and selected follow-ups. These were component calls, not complete native panels; the full set was not rerun after every amendment.

## Historical v1.1.0 — 2026-10-24 to 2026-10-26

Commit `a2700d8` sharpened the voice and added the evidence-first pilot; `6f1fe9b` synchronized invocation scope and reviewer safeguards. [pilot-v1](evaluations/pilot-v1/REPORT.md) names the first pilot dataset, not a separate v1 release. `evaluations/targeted-v11/` holds focused v1.1 checks for rejecting false evidence and preserving planning constraints. The `v11` suffix means v1.1, not version eleven. These checks do not establish broad improvement or current runtime compatibility.

## Historical v1.0.0 — 2026-10-24

Commit `07b4e87` introduced the independent-judgment skill. `ee972a2` added traceable evidence and checked reasoning while retaining the `1.0.0` version string. The initial 1.x labels preceded the explicit experimental-beta numbering; they should not be read as a stable-release guarantee.
