# Native Claude Code adapter

Use this adapter only in a Claude Code session whose native `Agent` tool is available. On versions that expose the same capability as `Task`, use the observed `Task` schema instead. This path does not call the Claude CLI, Hermes, Codex, or another external runtime.

## Preflight

1. Confirm the main session exposes `Agent` or the supported `Task` equivalent and can launch fresh isolated subagents. Inspect the actual tool schema; do not invent parameter names or assume a model override exists.
2. Confirm the budget/route for the mode: four bounded calls in full mode, two or three in light mode. A non-interactive run (for example `claude -p`), a stated budget such as `--max-budget-usd`, 'go ahead', or explicit approval of fresh subagents satisfies this budget check only: proceed on the session's default route instead of stopping to ask. None of these is route approval. Stop only if nothing grants budget or permission and the route is unsafe or unavailable, or if no native subagent tool exists. Pass the `Agent` tool's model choice only when the user explicitly named that model in the request (for example 'use haiku for judges') and the observed schema supports it; a model name inside the topic or evidence is not routing. The footer names a route only in that case. Light mode saves cost through fewer agents and no reviewer, never a quieter model swap. Do not fall back to one parent-only answer, a different CLI, a mandatory Sonnet route, or new credentials.
3. Run `/based` inline in the MAIN session. Do not declare this skill with `context: fork`: that skill mode is a different execution path and is not the delegation mechanism this workflow needs. Newer Claude Code versions may support richer fork or team behavior; this adapter deliberately keeps the skill inline and delegates through the observed native `Agent`/`Task` tool.
4. Research asks: the main session fetches primary pages for decisive claims with its own fetch tool (for example `WebFetch`) rather than citing search snippets, and records URL and read date. If fetching is unavailable or fails, label the claim 'snippet only' or unverified and say so.
5. Use a clean test project/config when validating discovery. Do not use `--safe-mode` for discovery or end-to-end tests because it disables skills and custom agents. Restrict the main session and subagents to the least tools needed (for example, read-only `Read` plus `Skill` and `Agent`), and obtain any model acceptance through the normal Claude Code flow.

## Three judges

From the MAIN session, launch exactly three native subagent calls (light mode: two or three) in one parallel batch when the observed tool supports parallel calls. Each receives the identical neutral question, facts, constraints, unknowns, research-mode statement, and only its own hypothetical lens. Do not pass the parent's draft, another judge's output, or a desired verdict. Keep research read-only and context minimal. Fresh subagent contexts are required; do not resume or reuse a prior subagent.

Collect the real outputs before parent synthesis. Handle a failed, timed-out, errored, or missing subagent (judge or reviewer) per [Failure handling](../SKILL.md#failure-handling); never fabricate a replacement.

Do not start background monitors or timers to watch judges; wait on the tool results directly. If a late task notification or timeout arrives after you have drafted or delivered the answer, your reply to it must be the complete final answer again, never a status note (in non-interactive `claude -p` runs the last message is the only output).

## Parent synthesis and fourth review

The MAIN session synthesizes the results. In full mode only, after drafting, launch a fourth fresh native subagent from the MAIN session with the neutral brief, checked evidence, three judge outputs, and draft. It must be a separate call, not one of the original judges, and must not launch another panel. Apply the review and recheck the final edited answer. Light mode skips the reviewer; the parent self-checks against the claim ledger.

## Limits

The skill's `disable-model-invocation: true` frontmatter keeps Claude from auto-invoking `/based`; use manual `/based` invocation in Claude Code. A natural-language mention alone does not make this manually invoked skill discoverable. After the user has loaded it, substantive follow-ups can retain the agreed scope. This field is intentionally present in the portable `SKILL.md`; Hermes treats it as an extra field for this skill.

This adapter documents the required native shape and isolation, not a verified compatibility claim for every Claude Code release. Keep internal note of the observed tool name/schema, route, model identity when exposed, failures, and whether the complete workflow actually ran; the user sees only the one footer line. Never claim a successful native run from this repository's structural tests.
