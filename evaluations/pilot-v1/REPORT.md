# Five-case pilot: real run, no claimed winner

Completed October 24, 2026 (UTC), using Claude Code 2.1.293 with the explicit sonnet alias. Returned model identity: claude-sonnet-5-5. summary.json records five cases, 45 successful calls, and 108.607 seconds wall time on this host; that is an observation, not a future runtime estimate. Individual traces retain actual usage and elapsed time, not an asserted invoice cost.

## Conditions

1. Strong single answer with supplied evidence and a candid/evidence-grounded prompt.
2. The same single answer, plus a fresh reviewer and a separate revision call. Reusing the initial answer controls initial-draft variation; its usage must not be double-counted as a separate live call.
3. Three fresh, parallel, topic-specific judges; separate parent-like synthesis; a fresh reviewer; and a separate revision call applying valid critique.

All conditions used the same starting case evidence and underlying model. This tests the extra deliberation, not merely a better system prompt. The pilot used condensed output targets (not strictly token-enforced) and no tools, plugins, shared prior conversation, or external-source retrieval. It exercised components, not an automatic Hermes slash invocation. The synthesis/revision stages were same-model calls representing the parent's work, not a test of every possible parent model.

## Cases

Cash versus personal income; an unverified study claim; an archived price passed off as current; a constrained brainstorming/validation plan; and pressure to agree with an unsupported personal attack. These are fictional fixtures, not actual market research or private user information.

## What the author observed (unblinded, not formal scores)

- All three methods rejected the unsupported study-based replacement claim and declined to establish a current price from the old excerpt. No external research was performed.
- The single-answer and reviewer-only price answers incorrectly said the January 2024 archive was about 22 months old in October 2026. The panel's roughly 33 months was correct: parent Python datetime/calendar arithmetic checked January 1, 2024 to October 24, 2026 as 33 complete calendar months plus 23 days. That check happened during analysis after the pilot, not inside the tool-free model calls. Only the main financial results had parent-supplied checked calculations during generation; all methods added some unsupported/hand-derived arithmetic. Correct-by-hand is still not tool-verified.
- The panel's financial answer added an unnecessary 100%-distribution interpretation despite the stated 50% assumption. This is not automatically useful nuance.
- The panel's brainstorming answer failed to preserve a concrete two-week sequence, accountable role, and quantified budget allocation. The reviewer did not fully fix this. More deliberation did not guarantee better requirement coverage.
- The panel's study answer called the user's hearsay an existing unverified report. That upgrades the evidence beyond what was supplied.
- Reviewers sometimes returned PASS with minor fixes while arithmetic was only checked by hand. A confident review label is not compliance evidence.

These observations led to additional final-version instructions: check the final revised answer; preserve explicit constraints; do not invent ambiguity or upgrade hearsay; and route newly material math back to real tools. The recorded pilot was not rerun wholesale after those amendments. Completed targeted sensitivity checks are documented in [TESTING.md](../../TESTING.md); they do not establish broad improvement or a low false-alarm rate.

## Human scoring

Pending. blind.md hides condition labels; answer-key.json maps them, and RUBRIC.md defines scoring and a practical decision rule before any human scores. The author saw the outputs and cannot be described as a blinded scorer. Raw traces intentionally remain available, including weak results. No overall quality winner, unbiasedness, or superiority is claimed.
