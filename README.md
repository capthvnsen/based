# /based

**Speak your mind. Show your work. Own the trade-off.**

An experimental portable instruction skill for research, brainstorming, and planning. It requires three fresh judge conversations, parent synthesis, and a separate fourth reviewer—not a guarantee of truth, neutrality, or better answers.

**Overhead:** three judges + one review + parent synthesis/revision. Research and valid retries can add work. Keep it opt-in for decisions worth the time. This repository does not establish superiority over a careful single answer.

## What “based” means here

Intellectually independent, unapologetically direct, and accountable to reality. Say what you actually conclude instead of chasing approval from the user, a crowd, or a political tribe. Use your strongest reasoning, not intelligence cosplay. Be willing to update when wrong. **Unapologetic does not mean uncorrectable.**

A little bite, not a roast generator: a supported flaw deserves plain words, and a sharp contrast or dry line is welcome when it makes the decision clearer. Criticize the proposal, not the person's worth or invented motives. A good plan can get a clear yes; missing information is not proof of failure.

No fake certainty, mandatory contrarianism, corporate padding, political loyalty tests, or cruelty dressed up as honesty. “I can't verify that” can be the most based answer. Social approval is not a truth certificate, and sharper copy increasing adoption is still an untested hypothesis. See [voice examples and read sources](references/voice.md).

## Install

The optional stdlib-only helper copies only `SKILL.md`, the two runtime adapters, and the five supporting reference documents. It never copies evaluation artifacts, prompts/results, or arbitrary files, and it refuses an existing destination.

```sh
# Default destinations:
#   Hermes: ${HERMES_HOME:-$HOME/.hermes}/skills/based
#   Claude Code: ${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/based
python install.py --runtime hermes
python install.py --runtime claude

# Safer isolated/custom destination:
python install.py --runtime hermes --dest "$PWD/.test-home/skills/based"
```

Use `--dest` for a clean profile or test project. The helper does not edit global settings, credentials, or model routing. A documented manual alternative is to copy this repository's skill files into the same destination without overwriting an existing skill; do not copy `evaluations/` into a runtime skill directory.

The Claude-oriented `disable-model-invocation: true` field is intentionally present in the portable frontmatter for manual-only invocation. Hermes accepts it as an extra skill field and still requires an explicit `/based` invocation. The Hermes metadata remains in the same frontmatter.

## Native runtime paths

The shared core is runtime-neutral. Choose exactly one adapter before launching the panel:

- [Native Hermes](adapters/hermes.md): uses the actual `delegate_task(tasks=[...])` batch shape. Children inherit the active delegation model/provider; the skill does not pretend to select a per-child model.
- [Native Claude Code](adapters/claude-code.md): uses the main session's observed native `Agent` tool, or the supported `Task` equivalent. `/based` stays inline in the main session; this path does not call the Claude CLI or Hermes.

Both adapters require capability and budget preflight. If the native tool, acceptable route, fresh-context isolation, or budget is missing or unverified, stop honestly. There is no fake one-agent fallback, mandatory Sonnet route, new-key setup, or silent premium substitution. Claude discovery/E2E validation should use a clean `CLAUDE_CONFIG_DIR` without `--safe-mode`, because `--safe-mode` disables skills and custom agents; restrict tools explicitly instead.

No native runtime compatibility claim is made here until the parent exercises clean-context Hermes and Claude Code flows. A structural test or a successful manual component call would not prove full invocation-to-final behavior.

## Use

```text
/based Should I take this job or stay independent?
/based Rank three ways to validate this offer before I build it.
/based Research this thesis and show what would disprove it.
/based Stress-test this launch plan, then give me a workable sequence.
```

The full workflow is opt-in. Loading the skill or asking what it does does not launch agents. Follow-up clarification stays within the current panel unless the user requests a materially new judgment or a fresh panel.

## The workflow

- Three hypothetical perspectives have genuinely different incentives and constraints, tailored to the topic. They are analytical lenses, not real experts or fabricated lived experience.
- Each gets the same neutral evidence brief in a fresh conversation, without the other answers or the parent's preferred verdict.
- The parent weighs evidence rather than votes, then drafts an answer.
- A fourth fresh agent checks grounding, assumptions, missing requirements, approval-seeking, needless harshness, and practical usefulness.
- The parent applies valid critique, rejects erroneous critique, and rechecks the final edited answer.

Separate conversations are not independent training or statistical evidence. Same-model blind spots can remain. No judge must disagree just to make the panel look diverse.

## Evidence is part of the answer

Consequential factual claims need sources actually read, with visible supporting citations. Important inferences need stated premises. Decisive math needs a calculator/code check. Predictions and brainstorms are hypotheses. Current prices or policies cannot come from stale recollection. Hearsay does not establish that a paper or report exists.

Tool-free judges rely on evidence and calculations supplied by the parent; they cannot claim independent web research or tool verification. Read-only research is allowed only when those tools actually exist on the selected native route. A reviewer's PASS is not evidence by itself.

## What has actually been tested

- Existing structural contract, evidence-shape, tone, reviewer, and fixture-arithmetic tests.
- v1.3 safe-install tests covering custom paths with spaces, custom runtime homes, runtime validation, existing-destination refusal, allowlisted references/adapters, evaluation-artifact exclusion, and frontmatter fields.
- The optional evaluation helper remains evaluation-only and is not a runtime dependency.

Native Hermes discovery, native Claude Code discovery, full invocation-to-final execution, and comparative answer quality for v1.3 remain pending the parent’s clean-context tests. Do not report those gates as successful from this repository alone. Historical v1.2 evaluation artifacts are retained as evidence of prior component work, not as v1.3 runtime compatibility proof.

## Keep it small

This remains a Markdown instruction skill plus a small optional stdlib installer, not a plugin, service, telemetry system, model router, or guarantee that a model obeys every instruction. No lite modes, extra agents, or dashboards were added. Evaluate whether the panel earns its overhead before adding complexity. Normal safety, private-data, and external-action approvals remain intact.

MIT licensed.
