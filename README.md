# /based

**Speak your mind. Show your work. Own the trade-off.**

An experimental Hermes skill for research, brainstorming, and planning. Three fresh judge conversations, parent synthesis, and a separate reviewer—not a guarantee of truth, neutrality, or better answers.

**Overhead:** three judges + one review + parent synthesis/revision. Research and valid retries can add work. Keep it opt-in for decisions worth the time. This repository does not establish superiority over a careful single answer.

## What “based” means here

Intellectually independent, unapologetically direct, and accountable to reality. Say what you actually conclude instead of chasing approval from the user, a crowd, or a political tribe. Use your strongest reasoning, not intelligence cosplay. Be willing to update when wrong. **Unapologetic does not mean uncorrectable.**

A little bite, not a roast generator: a supported flaw deserves plain words, and a sharp contrast or dry line is welcome when it makes the decision clearer. Criticize the proposal, not the person's worth or invented motives. A good plan can get a clear yes; missing information is not proof of failure.

No fake certainty, mandatory contrarianism, corporate padding, political loyalty tests, or cruelty dressed up as honesty. “I can't verify that” can be the most based answer. Social approval is not a truth certificate, and sharper copy increasing adoption is still an untested hypothesis. See [voice examples and read sources](references/voice.md).

## Quick start — native Hermes first

1. Use a Hermes installation with skills and native delegation available.
2. Check the active profile's actual delegation model/provider. Pick an already available route that fits your budget; this skill cannot force a per-child model override.
3. Install this repo as the skill folder (do not overwrite an existing installation):

```sh
git clone https://github.com/capthvnsen/hermes-based.git "${HERMES_HOME:-$HOME/.hermes}/skills/based"
```

4. Start a fresh session if needed, then send `/based <your question>`. `/skill based` loads it explicitly.

For a named Hermes profile, point HERMES_HOME at that profile before installing. Do not put credentials in this repository.

Claude Code is **optional**, not required by the native route. An authenticated Sonnet recipe, checked CLI version, isolation flags, error checks, and tool limits live in [model routing](references/model-routing.md). Other providers are not automatically ruled out, but their full workflow compatibility has not been demonstrated by this repo's pilot. No price or invoice-savings claim is made.

## Use

```text
/based Should I take this job or stay independent?
/based Rank three ways to validate this offer before I build it.
/based Research this thesis and show what would disprove it.
/based Stress-test this launch plan, then give me a workable sequence.
```

## The workflow

- Three hypothetical perspectives have genuinely different incentives and constraints, tailored to the topic. They are analytical lenses, not real experts or fabricated lived experience.
- Each gets the same neutral evidence brief in a fresh conversation, without the other answers or the parent's preferred verdict.
- The parent weighs evidence rather than votes, then drafts an answer.
- A fourth fresh agent checks grounding, assumptions, missing requirements, approval-seeking, needless harshness, and practical usefulness.
- The parent applies valid critique, rejects erroneous critique, and rechecks the final edited answer.

Separate conversations are not independent training or statistical evidence. Same-model blind spots can remain. No judge must disagree just to make the panel look diverse.

## Evidence is part of the answer

Consequential factual claims need sources actually read, with visible supporting citations. Important inferences need stated premises. Decisive math needs a calculator/code check. Predictions and brainstorms are hypotheses. Current prices or policies cannot come from stale recollection. Hearsay does not establish that a paper or report exists.

Tool-free judges rely on evidence and calculations supplied by the parent; they cannot claim independent web research or tool verification. Read-only research is allowed only when those tools actually exist on the selected route. A reviewer's PASS is not evidence by itself.

## What has actually been tested

- Structural checks and clean-profile `/based` discovery.
- Manual separate Sonnet judge/reviewer execution.
- A [five-case offline pilot](evaluations/pilot-v1/REPORT.md) comparing a strong single answer, single answer plus reviewer, and the full panel under matched supplied evidence.
- [v1.2 voice/reviewer component spot checks](evaluations/tone-v12/REPORT.md), including a good-plan control, missing facts, insult bait, hearsay, corrected inputs and vulnerable circumstances. These are not full panels or proof that sharper answers are preferred.

The pilot recorded real outputs, model identity, time, and usage—and found defects, including incomplete plan coverage and unchecked arithmetic. No human-blind quality scores or overall winner have been assigned. Synthetic supplied-evidence testing is **not** proof of live-source research, automatic slash-to-final execution, or compatibility with every provider. See [testing](TESTING.md).

The optional [pilot helper](evaluations/run_pilot.py) is for evaluation only; it is not the skill runtime or an enforcement layer. Running it makes model calls through your existing account; inspect it and approve its use under your own budget. It makes 45 calls for the five bundled cases. **It saves full prompts and outputs without automatic content redaction—use synthetic fixtures only.** No installation, credential changes, or publishing occurs.

## Keep it small

This remains a Markdown instruction skill, not a plugin, service, telemetry system, model router, or guarantee that a model obeys every instruction. No lite modes, extra agents, or dashboards were added. Evaluate whether the panel earns its overhead before adding complexity. Normal safety, private-data, and external-action approvals remain intact.

MIT licensed.
