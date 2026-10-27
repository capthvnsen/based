# /based

**Based? Based on what? `/based` answers both:** a straight verdict, then the receipts.

A portable instruction skill for research, brainstorming, and planning: three fresh judge conversations, parent synthesis, and a separate fourth reviewer. A light mode drops the reviewer for brainstorms and low-stakes asks.

## Quickstart

Requires Python 3.9+ for the optional installer. For Claude Code, the recommended user install path is `~/.claude/skills/based` (or `$CLAUDE_CONFIG_DIR/skills/based` when configured):

```sh
git clone https://github.com/capthvnsen/based.git
cd based
python3 install.py --runtime claude
```

In Claude Code, invoke the skill manually:

```text
/based Rank three ways to validate this offer before I build it.
```

For Hermes, run `python3 install.py --runtime hermes`; its default destination is `${HERMES_HOME:-$HOME/.hermes}/skills/based`. Interactive use is also `/based <question>`. On the tested Hermes build, one-shot CLI use requires `hermes chat --skills based -q "Use the loaded based skill for ..."`; `-q "/based ..."` does not expand the command.

## What it sounds like

Illustrative output on a synthetic premise, not a recorded run:

```text
/based Should I spend the seed money on ads? Each sale is $10 and costs me $14.

Based verdict: Don't scale yet. Right now every sale is a $4 donation to
your customers, and ads just donate faster.

More customers scale the loss, not the business. Fix the margin first:
raise price, cut unit cost, or both.
Dissent: a capped ad test to measure demand, not profit, is defensible
if you book it as research spend.

Based on what?
- Price $10, variable cost $14: supplied by you.
- 10 - 14 = -4 per sale: code-checked.
- Cringe assumption: that volume fixes margin. Nothing supplied shows unit
  cost falls with scale. If it does, the call changes.

Next move: find a price or unit cost that clears $14 with room for overhead,
test it on a small batch, then revisit ads.

Full panel: 3 judges + reviewer (Based ✅), session default route; 1 fix applied.
```

That last line is the only process talk you get; judge and reviewer details stay internal. A brainstorm runs light by default and ends with something like `Light mode, unreviewed: 3 judges.` Force either with `/based full ...` or `/based light ...`.

## Status and limits

**v0.21.0 — experimental beta.** Earlier native-test records use the previous v1.3 label; the beta renumbering did not change the tested workflow. See [version history](CHANGELOG.md).

**Overhead:** full mode is three judges + one review + parent synthesis/revision; light mode drops the review. Research and valid retries can add work. Keep it opt-in for decisions worth the time. Separate conversations can share same-model blind spots, and a reviewer's PASS is not evidence by itself. This repository does not establish better accuracy, human preference, or adoption than a careful single answer, or compatibility with every runtime version, provider, and platform.

This remains a Markdown instruction skill with a stdlib-only installer. Model obedience is not enforced. Normal safety, private-data, and external-action approvals remain intact.

## Install options

The helper creates missing parent directories and installs six allowlisted files: `SKILL.md`, the selected runtime's adapter, and four runtime references (`model-routing`, `panel`, `reviewer`, `voice`). It excludes the other adapter, maintainer-only `references/evaluation.md`, and all evaluation artifacts. In installed copies, links to omitted documents point to their repository pages; source files stay unchanged.

```sh
# Preview every file that would be written; writes nothing:
python3 install.py --runtime claude --dry-run

# Isolated project/custom destination, including paths with spaces:
python3 install.py --runtime claude --dest "$PWD/.claude/skills/based"
python3 install.py --runtime hermes --dest "$PWD/.test-home/skills/based"
```

An existing destination is refused unless you request an upgrade. Symlink destinations are refused. The helper does not edit settings, credentials, or model routing. For manual installation, copy the same six files and adjust links to omitted documents; keep `evaluations/` out of runtime skill directories.

Claude Code enforces manual `/based` invocation through `disable-model-invocation: true`. Hermes accepts the extra field; its opt-in behavior relies on the instructions and an explicit request, not a demonstrated harness toggle.

## Upgrade

Update your checkout, then rerun the installer with the same runtime and destination:

```sh
git pull --ff-only
python3 install.py --runtime claude --upgrade --dry-run
python3 install.py --runtime claude --upgrade
```

Use `--dest` again if you installed to a custom location. `--upgrade` (alias `--force`) moves the entire existing directory to `<target>.bak-<timestamp>` before replacing it, and prints the backup path. Local edits stay in the backup; they are not merged into the new install. A failed replacement restores the previous install. With no existing destination, `--upgrade` performs a fresh install. Keep any backups you need; the helper does not prune them.

## Uninstall

```sh
python3 install.py --runtime claude --uninstall --dry-run
python3 install.py --runtime claude --uninstall
```

For Hermes, select `--runtime hermes`; for custom installs, pass the original `--dest`. Uninstall removes the whole selected skill directory, including local additions, and leaves sibling backups intact. It requires a regular `SKILL.md` marker and refuses missing, unmarked, or symlink destinations. To restore a backup, move it back to the original path after removing the current install.

## What “based” means here

Intellectually independent, unapologetically direct, and accountable to reality. Say what you actually conclude instead of chasing approval from the user, a crowd, or a political tribe. Use your strongest reasoning, and update when wrong. **Unapologetic does not mean uncorrectable.** The flavor follows Lil B's original sense of the word: be yourself, unbothered, positive. It dials down for formal docs and off for serious or sensitive topics, and it never trims the evidence.

A little bite, not a roast generator: a supported flaw deserves plain words, and a sharp contrast or dry line is welcome when it makes the decision clearer. Criticize the proposal, not the person's worth or invented motives. A good plan can get a clear yes; missing information is not proof of failure.

No fake certainty, mandatory contrarianism, corporate padding, political loyalty tests, or cruelty dressed up as honesty. “I can't verify that” can be the most based answer. See [voice examples and read sources](references/voice.md).

## Native runtime paths

The shared core is runtime-neutral. Choose exactly one adapter before launching the panel:

- [Native Hermes](adapters/hermes.md): uses the actual `delegate_task(tasks=[...])` batch shape. Children inherit the active delegation model/provider; the skill does not select a per-child model.
- [Native Claude Code](adapters/claude-code.md): uses the main session's observed native `Agent` tool, or the supported `Task` equivalent. `/based` stays inline in the main session; this path does not call the Claude CLI or Hermes.

Both adapters require capability and budget preflight. A non-interactive run or a stated budget/permission ('go ahead', `--max-budget-usd`) satisfies it: the run proceeds on the session's default route and names it in the process line. Without that, or when the native tool, fresh-context isolation, or a usable route is missing, it stops honestly. There is no one-agent fallback, mandatory Sonnet route, new-key setup, or silent premium substitution. Check Hermes child limits before running: the tested one-shot profile allowed four children. Claude discovery/E2E validation should use a clean `CLAUDE_CONFIG_DIR` without `--safe-mode`, because `--safe-mode` disables skills and custom agents; restrict tools explicitly instead.

## Use and workflow

```text
/based Should I take this job or stay independent?
/based Research this thesis and show what would disprove it.
/based Stress-test this launch plan, then give me a workable sequence.
/based light Brainstorm ten cheap ways to find my first five customers.
```

Loading the skill or asking what it does does not launch agents. Follow-up clarification stays within the current panel unless the user requests a materially new judgment or a fresh panel.

- Three hypothetical perspectives have different incentives and constraints, tailored to the topic. They are analytical lenses, not real experts or fabricated lived experience.
- Each gets the same neutral evidence brief in a fresh conversation, without the other answers or the parent's preferred verdict. No judge must disagree just to make the panel look diverse.
- The parent weighs evidence rather than votes, then drafts an answer.
- In full mode, a fourth fresh agent checks grounding, assumptions, missing requirements, approval-seeking, needless harshness, and practical usefulness.
- The parent applies valid critique, rejects erroneous critique, and rechecks the final edited answer.

Consequential factual claims need sources actually read, with visible supporting citations; for research, the parent opens the primary page and cites URL and read date, labelling anything else 'snippet only'. Judges name real tools, vendors, and benchmarks, labelled '(unverified)' unless checked. Important inferences need stated premises. Decisive math needs a calculator/code check. Predictions and brainstorms are hypotheses. Current prices or policies cannot come from stale recollection. Hearsay does not establish that a paper or report exists.

Tool-free judges rely on evidence and calculations supplied by the parent; they cannot claim independent web research or tool verification. Read-only research is allowed only when those tools exist on the selected native route.

## What has actually been tested

The free local suite covers structural contracts, installed links, evidence shapes, fixture arithmetic, evaluation helpers with mocked calls, and installer lifecycle behavior. Run it with `python3 -m unittest discover -s tests`. CI runs the same suite on Ubuntu with Python 3.9/3.12 and macOS with Python 3.11/3.12. See [testing details](TESTING.md).

Historical native invocation-to-final workflows were exercised twice per runtime on **Hermes 0.22.0+119.g0e427d7** and **Claude Code 2.1.293** on Linux. Native completion records confirmed three judges and a later fourth reviewer. Final synthetic outputs fit the requested length; the initial Claude length/provenance failure is preserved. See the [native verification report](evaluations/native-v13/REPORT.md) and [sanitized receipts](evaluations/native-v13/receipts.json). Raw account/session traces remain private. Older component tests are historical evidence, and the optional evaluation helper is not a runtime dependency.

In one synthetic example, each sale earned $10 and cost $14 in variable expenses. Both native workflows rejected making that profitable through volume alone. The final Claude answer put it plainly: **“Funding buys runway, not profitability.”** The report preserves the full example and initial defects.

MIT licensed.
