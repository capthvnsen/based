# Verification by gate

## Structural, helper and safe-install suite

From the repository root:

```sh
python -m unittest discover -s tests -v
```

Coverage includes required frontmatter fields, allowlisted source existence, relative links resolving within each installed payload, supplied-evidence shape, fixture arithmetic, tone/reviewer concepts, runtime-adapter separation and installer behavior. Contract checks avoid pinning release versions or exact editorial phrases. Installer cases exercise paths with spaces, runtime homes, runtime validation, dry-run without writes, selected-adapter payloads, existing-destination refusal, upgrade backups (including `--force`), uninstall safety, one-line expected errors and rollback for both fresh and upgraded installs.

[CI](.github/workflows/test.yml) runs `python -m unittest discover -s tests` on push and pull requests, on Ubuntu with Python 3.9/3.12 and macOS with Python 3.11/3.12. The macOS minimum differs because the [Actions Python build manifest](https://github.com/actions/python-versions/blob/main/versions-manifest.json) has no current Python 3.9 ARM macOS build. No dependency installation is required.

These are structural/helper/installer tests, not proof an LLM follows instructions. They require no model calls or credentials.

## Native runtime execution

The release is now **v0.21.0 beta**. Retained native-test records use the previous v1.3 label; only version metadata was renumbered, not the tested workflow. The historical receipt hashes retain their original tested payloads.

See the [native verification report](evaluations/native-v13/REPORT.md) and [sanitized receipts](evaluations/native-v13/receipts.json).

- Hermes **0.22.0+119.g0e427d7**, configured `gpt-5.6-luna` on the existing accepted `openai-codex` route: clean test profile home, installed skill, preloaded `--skills based`, native three-task delegation followed by a separate reviewer task. Full manifests confirmed four completed workers and correct stage order.
- Claude Code **2.1.293**, accepted Sonnet route with `claude-sonnet-5-5` reported: clean config and project skill, direct `/based` invocation, four native `Agent` calls. The first three were parallel in one assistant message; native completion notifications confirmed all judges returned before review and review finished before final output.

Two actual invocations were inspected per runtime. These are full native workflows, unlike the earlier manually orchestrated CLI component tests. Final synthetic outputs were within their requested word limit. Initial Claude length/provenance defects are retained; the follow-up prompt also changed, so no controlled improvement claim is made.

The historical tested runtime payloads matched repository hashes at the time; the current installer selects a smaller payload and rewrites links to omitted documents. Native execution has not been rerun for this installer change. Hermes parsed the additional Claude frontmatter field and discovered `/based` in an isolated skills directory. Claude manual invocation loaded the skill in a fresh project. No global configuration, credentials, or unrelated profile settings were changed; temporary validation profiles used supported authentication fallback without copying auth files. Raw account/session metadata stays outside Git.

## Installation and invocation limits

The optional `install.py` uses only the standard library and requires Python 3.9+. Each runtime receives six files: `SKILL.md`, its selected adapter and four references. The other adapter, `references/evaluation.md` and evaluation traces stay out of the runtime; installed links to omitted documents point to repository pages. Existing destinations require `--upgrade` (alias `--force`), which preserves the previous directory in a timestamped backup before replacement. `--dry-run` previews without creating directories or changing files; `--uninstall` requires a regular `SKILL.md` marker and keeps backups. The installer refuses symlink destinations and replacement/removal of its own source repository. It does not set up credentials, select a model or edit global settings. Tests use temporary directories and simulated filesystem failures rather than modifying real profiles.

On the tested Hermes build, one-shot `-q "/based ..."` does not expand the slash command; use `--skills based` with an explicit request. One-shot child limits must allow a three-judge batch and a later reviewer; the clean test profile explicitly used `oneshot_max_children: 4`. Normal interactive invocation remains `/based ...`.

Claude's manual-only frontmatter requires explicit `/based`; a natural-language mention alone does not make that disabled-auto-invocation skill discoverable. Do not use `--safe-mode` for skill discovery tests because it disables skills. All native paths require capability and accepted-budget preflight, and must report missing tools or limits honestly.

## Historical artifacts and remaining limits

The [older five-case pilot](evaluations/pilot-v1/REPORT.md) and [v1.2 voice checks](evaluations/tone-v12/REPORT.md) remain limited historical evidence. `evaluations/run_pilot.py` is an optional account-consuming evaluation tool, not a skill runtime dependency. It saves full prompts/results and must receive only synthetic data.

No test here establishes compatibility with every version/provider/platform, reliable obedience on every request, live-source research quality, statistical superiority, bias elimination, human preference or adoption gains. Same-model blind spots and fallible reviewers remain. This repository is an experimental instruction skill, not an enforcement engine.
