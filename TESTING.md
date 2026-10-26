# Verification by gate

## Structural, helper and safe-install suite

From the repository root:

```sh
python -m unittest discover -s tests -v
```

The current suite passes **27 tests**. Coverage includes metadata, relative links, supporting documents, supplied-evidence shape, fixture arithmetic, tone/reviewer rules, runtime-adapter separation and installer behavior. Installer cases exercise custom paths with spaces, custom runtime homes, runtime validation, explicit destinations, existing-destination refusal, allowlisted payloads, evaluation exclusion and interrupted-install rollback. The new rollback regression was observed failing before the fix.

These are structural/helper/installer tests, not proof an LLM follows instructions. They require no model calls or credentials.

## Native v1.3 execution

See the [native verification report](evaluations/native-v13/REPORT.md) and [sanitized receipts](evaluations/native-v13/receipts.json).

- Hermes **0.22.0+119.g0e427d7**, configured `gpt-5.6-luna` on the existing accepted `openai-codex` route: clean test profile home, installed skill, preloaded `--skills based`, native three-task delegation followed by a separate reviewer task. Full manifests confirmed four completed workers and correct stage order.
- Claude Code **2.1.293**, accepted Sonnet route with `claude-sonnet-5-5` reported: clean config and project skill, direct `/based` invocation, four native `Agent` calls. The first three were parallel in one assistant message; native completion notifications confirmed all judges returned before review and review finished before final output.

Two actual invocations were inspected per runtime. These are full native workflows, unlike the earlier manually orchestrated CLI component tests. Final synthetic outputs were within their requested word limit. Initial Claude length/provenance defects are retained; the follow-up prompt also changed, so no controlled improvement claim is made.

The exact final runtime payloads match repository hashes. Hermes parsed the additional Claude frontmatter field and discovered `/based` in an isolated skills directory. Claude manual invocation loaded the skill in a fresh project. No global configuration, credentials, or unrelated profile settings were changed; temporary validation profiles used supported authentication fallback without copying auth files. Raw account/session metadata stays outside Git.

## Installation and invocation limits

The optional `install.py` uses only the standard library, copies the eight allowlisted instruction files, and refuses any existing destination. It does not install another runtime, set up credentials, select a model, edit global settings or copy evaluation traces. Test fresh or custom destinations rather than overwriting real skill installations.

On the tested Hermes build, one-shot `-q "/based ..."` does not expand the slash command; use `--skills based` with an explicit request. One-shot child limits must allow a three-judge batch and a later reviewer; the clean test profile explicitly used `oneshot_max_children: 4`. Normal interactive invocation remains `/based ...`.

Claude's manual-only frontmatter requires explicit `/based`; a natural-language mention alone does not make that disabled-auto-invocation skill discoverable. Do not use `--safe-mode` for skill discovery tests because it disables skills. All native paths require capability and accepted-budget preflight, and must report missing tools or limits honestly.

## Historical artifacts and remaining limits

The [older five-case pilot](evaluations/pilot-v1/REPORT.md) and [v1.2 voice checks](evaluations/tone-v12/REPORT.md) remain limited historical evidence. `evaluations/run_pilot.py` is an optional account-consuming evaluation tool, not a skill runtime dependency. It saves full prompts/results and must receive only synthetic data.

No test here establishes compatibility with every version/provider/platform, reliable obedience on every request, live-source research quality, statistical superiority, bias elimination, human preference or adoption gains. Same-model blind spots and fallible reviewers remain. This repository is an experimental instruction skill, not an enforcement engine.
