# /based

Three perspectives. One synthesis. One separate reality check.

A portable Hermes skill for research, brainstorming, and planning that challenges your assumptions without becoming a political echo chamber or a performative jerk.

## How it works

1. Hermes chooses three topic-specific hypothetical perspectives with different constraints, incentives, and exposure to downside.
2. Three fresh subagent conversations judge the same neutral brief in parallel, without seeing each other or a preferred answer.
3. Hermes weighs their evidence, objections, and trade-offs and writes its own synthesis.
4. A fourth fresh agent reviews the draft for factual gaps, pandering, ideological framing in either direction, false balance, and needless harshness.
5. Hermes applies the critique before returning the answer.

Perspectives are simulated analytical lenses, not actual lived experience. Separate contexts reduce cross-contamination; the same underlying model can still share blind spots. Consensus is not proof.

## Install

Requires Hermes with skills and a working delegation route. This repo itself is the skill folder. Clone into the active profile's skills directory, provided no `based` directory already exists:

```sh
git clone https://github.com/capthvnsen/hermes-based.git "${HERMES_HOME:-$HOME/.hermes}/skills/based"
```

For a private repo, authenticate GitHub first. Do not overwrite an existing skill. Start a fresh Hermes session if the command does not appear; use `/skill based` to load it explicitly.

## Use

```text
/based Should I take this job or stay independent?
/based Brainstorm an offer for this market and stress-test it.
/based Research this acquisition thesis and identify what would disprove it.
/based Tear apart this launch plan, then make it workable.
```

## Models and cost

Prefer an already configured budget route, such as Sonnet-class when available. No price claim is made. A skill cannot magically override a runtime's model selection. The agent must inspect routing before launch and must not silently use a premium fallback or change global configuration. Four calls are expected: three judges and one reviewer, plus parent synthesis; one additional review is allowed only after a material revision.

A documented alternative uses separate authenticated Claude Code print-mode processes with explicit `--model sonnet`, no tools, customization disabled, no MCP servers, and no session persistence. This avoids changing Hermes-wide delegation settings. The parent supplies researched evidence; tool-free judges do not browse. See SKILL.md for exact isolation flags. Native Hermes delegation is also supported if the configured model meets the user's budget preference.

## What based means

Evidence over flattery. Reality over ideology. No injected political lectures, no reflexive anti-progressive pandering, no stereotyping, and no cruelty masquerading as honesty. A conclusion can be uncomfortable without being absolute. The goal is a useful answer that survives scrutiny, not a particular political verdict.

## Verification

See TESTING.md for the actual smoke test and limitations. The skill is an instruction workflow, not a programmatic enforcement engine. It cannot guarantee every model obeys it or that role diversity eliminates correlated errors. No background service, plugin, global model change, or account integration is installed.

## Files

- `SKILL.md`: workflow and `/based` trigger
- `references/panel.md`: independent judge prompt
- `references/reviewer.md`: separate review prompt
- `tests/test_contract.py`: local structural checks (not behavioral proof)
- `TESTING.md`: real smoke-test outcomes

MIT licensed.
