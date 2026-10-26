# Native Claude Code adapter

Use this adapter only in a Claude Code session whose native `Agent` tool is available. On versions that expose the same capability as `Task`, use the observed `Task` schema instead. This path does not call the Claude CLI, Hermes, Codex, or another external runtime.

## Preflight

1. Confirm the main session exposes `Agent` or the supported `Task` equivalent and can launch fresh isolated subagents. Inspect the actual tool schema; do not invent parameter names or assume a model override exists.
2. Confirm the user's accepted model/route and budget for four bounded calls. A model name in a prompt is not routing. If the native subagent tool or an acceptable route is unavailable, stop and report the blocker. Do not fall back to one parent-only answer, a different CLI, a mandatory Sonnet route, or new credentials.
3. Run `/based` inline in the MAIN session. Do not declare this skill with `context: fork`: that skill mode is a different execution path and is not the delegation mechanism this workflow needs. Newer Claude Code versions may support richer fork or team behavior; this adapter deliberately keeps the skill inline and delegates through the observed native `Agent`/`Task` tool.
4. Use a clean test project/config when validating discovery. Do not use `--safe-mode` for discovery or end-to-end tests because it disables skills and custom agents. Restrict the main session and subagents to the least tools needed (for example, read-only `Read` plus `Skill` and `Agent`), and obtain any model acceptance through the normal Claude Code flow.

## Three judges

From the MAIN session, launch exactly three native subagent calls in one parallel batch when the observed tool supports parallel calls. Each receives the identical neutral question, facts, constraints, unknowns, research-mode statement, and only its own hypothetical lens. Do not pass the parent's draft, another judge's output, or a desired verdict. Keep research read-only and context minimal. Fresh subagent contexts are required; do not resume or reuse a prior subagent.

Collect all three real outputs before parent synthesis. Treat a failed, timed-out, errored, or missing subagent as incomplete; retry at most once when safe and never fabricate a replacement.

## Parent synthesis and fourth review

The MAIN session synthesizes the three results. Only after drafting, launch a fourth fresh native subagent from the MAIN session with the neutral brief, checked evidence, three judge outputs, and draft. It must be a separate call, not one of the original judges, and must not launch another panel. Apply the review and recheck the final edited answer.

## Limits

The skill's `disable-model-invocation: true` frontmatter keeps Claude from auto-invoking `/based`; the user must invoke it. Claude Code still accepts a direct `/based ...` invocation. This field is intentionally present in the portable `SKILL.md`; Hermes treats it as an extra field for this skill.

This adapter documents the required native shape and isolation, not a verified compatibility claim for every Claude Code release. Record the observed tool name/schema, route, model identity when exposed, failures, and whether the complete four-agent workflow actually ran. Never claim a successful native run from this repository's structural tests.
