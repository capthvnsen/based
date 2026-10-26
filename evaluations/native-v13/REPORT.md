# v1.3 native runtime verification

Observed on October 26, 2026, on Linux. This is a small instruction-skill beta, not a programmatically enforced deliberation engine or proof of answer superiority.

## Verified execution

The [sanitized receipts](receipts.json) record four actual native invocations, two per runtime. Each launched three real judge workers followed by a separate fourth reviewer: 16 worker launches in total. The parent inspected native trace events and completion records rather than relying on an answer claiming a council ran.

- **Claude Code 2.1.293:** fresh `CLAUDE_CONFIG_DIR`, fresh test project, installer-created `.claude/skills/based`; direct `/based` invocation. Existing accepted OAuth authentication was inherited without copying credentials. Native `Agent` appeared four times; the first three were in the same assistant message. Three native completion notifications arrived before the reviewer call, and the review completed before the final answer. The runs requested Sonnet and reported `claude-sonnet-5-5`.
- **Hermes 0.22.0+119.g0e427d7:** fresh temporary profile home, installer-created skill, memory disabled, no private prompts/plugins/config copied. The supported profile authentication fallback used the existing accepted account. `--skills based` activated the skill for a one-shot query. Native delegation made a three-task batch and a later single reviewer task; native manifests confirmed all four completed, with the judges finishing before review. The configured and manifest-recorded model was `gpt-5.6-luna` through the existing `openai-codex` route.

The fixture was synthetic negative unit economics: $10 earned and $14 variable cost per sale, with no other revenue or expected unit-cost reduction. Parent code checked `10 - 14 = -4`. Both final runs rejected volume alone as a fix and distinguished funding a loss from profitability. Final outputs were 168 words (Claude) and 126 words (Hermes), within the requested 180-word limit. The exact final installed payload hashes matched the current repository skill, adapters and references.

## Defects retained, not hidden

The initial Claude invocation completed its native workflow but returned 193 words against a 180-word limit, weakened the supplied arithmetic provenance in the review brief, introduced additional unchecked numerical examples, and summarized rather than forwarding the actual judge outputs. Those are compliance defects, not proof the native tool dispatch failed. Instructions were clarified to preserve actual returned outputs and provenance. The follow-up question also explicitly excluded new numerical examples and distinguished funding from profitability. Therefore the later result is not a controlled comparison proving the instruction edit alone fixed the behavior.

The initial Hermes workflow completed with a 151-word final answer. A validation script for the later run initially failed because it assumed every reviewer call uses a `tasks` array and tried to parse a truncated tool-output preview as complete JSON. The runtime had actually completed. Validation was corrected to recognize the observed single-task form and verify the full native manifests. The later Hermes final answer was 126 words.

A separate read-only code review found a partial-install rollback defect. A regression test was observed failing before the installer was changed to remove only the new destination created by that invocation if a move fails. Existing destinations remain untouched. The complete structural/helper/installer suite now passes 27 tests. Those tests do not prove LLM compliance.

## Reproduction conditions

Install the skill into a clean test destination with `python install.py --runtime claude --dest <test-project>/.claude/skills/based` or the Hermes equivalent.

Claude was launched from the test project with a fresh `CLAUDE_CONFIG_DIR`, accepted `--model sonnet`, native `Read,Skill,Agent` tools, manual permissions and an allowlist for those tools, no MCP servers and no session persistence. The input began with `/based`. Do not use `--safe-mode`: on this build it disables skills. Native background workers were allowed to finish, and their completion notifications were inspected.

Hermes used a fresh profile home with only the skill and a small test configuration. `delegation.oneshot_max_children: 4`, concurrency of four, maximum spawn depth one, and disabled orchestrator recursion were explicit test-profile settings, not changes to the user's normal profile. The parent used `delegation,file` tools so it could read adapters and templates; no write tools were invoked. The entry point was `hermes chat --skills based --format stream-json --query-file <brief>`. On this build, a one-shot `-q "/based ..."` does not expand the slash command. Interactive command discovery was checked separately.

Raw traces can contain account/session metadata, so they are retained privately outside Git. Public receipts contain synthetic final answers, counts, completion observations, model labels and trace/payload hashes, not raw credentials or account/session IDs. The optional pilot helper remains evaluation-only; neither native runtime depends on the other CLI.

## What remains unproven

This verifies a working native route on the tested Linux builds and models, not all Hermes or Claude Code installations, historical versions, operating systems, providers or permissions. Models still make mistakes and reviewers are fallible. Neither clean discovery, successful tool dispatch, nor this synthetic example establishes live-source research quality, bias elimination, consistent reviewer obedience, superior answers, user preference or increased adoption. Capability and budget preflight remain required.
