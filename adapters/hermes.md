# Native Hermes adapter

Use this adapter only in a Hermes session with the native `delegate_task` tool available. It is the preferred Hermes path; it does not call Claude Code, Codex, or another CLI.

## Preflight

1. Confirm the active session exposes `delegate_task` with the documented single-task and `tasks=[...]` batch forms.
2. Inspect the active profile's configured delegation model/provider and any concurrency/budget limits without displaying secrets. Native children inherit that configured route; this adapter does not invent or pass a per-child `model`, `provider`, `api_key`, or `toolsets` override.
3. Confirm the selected route is acceptable to the user and can support four bounded calls (three judges plus one later reviewer). If the tool, route, or budget is unavailable or unverified, stop and report the exact blocker. Do not downgrade to one parent-only answer or pretend that a prompt selecting a model changed routing.
4. Decide whether the children are tool-free or have bounded read-only tools. In tool-free mode, put the checked evidence and arithmetic in every task's `context`; children must not claim independent source or calculator verification.

Hermes accepts the Claude-oriented `disable-model-invocation: true` frontmatter field as an extra skill field; it does not make this adapter auto-run. Keep `/based` explicitly invoked by the user.

### CLI invocation and child limits

On the tested build, `hermes chat -q "/based ..."` does not expand the slash command. Interactive `/based ...` is supported; for one-shot CLI use `hermes chat --skills based -q "Use the loaded based skill for ..."`. The parent needs read access to the adapter and supporting references as well as delegation.

Inspect one-shot child limits before starting. On the tested build `delegation.oneshot_max_children` defaults to two; the full workflow requires allowance for at least four children, including the later reviewer. A clean test profile can explicitly set `oneshot_max_children: 4`; do not silently change a user's profile or global limits. Report a missing allowance as a preflight blocker and ask for the appropriate supported configuration. A single depth limit should still prevent recursive judge panels.

## Three judges

Send exactly one parallel batch with exactly three task objects. The native call shape is:

```text
delegate_task(tasks=[
  {"goal": "Judge through lens A; return the panel template", "context": "Neutral brief + lens A"},
  {"goal": "Judge through lens B; return the panel template", "context": "Neutral brief + lens B"},
  {"goal": "Judge through lens C; return the panel template", "context": "Neutral brief + lens C"}
])
```

Each child receives the same neutral question, facts, constraints, unknowns, and research-mode statement, plus only its own lens. Do not include the parent's draft or another judge's output. `delegate_task` provides a fresh conversation and returns only child summaries to the parent; shared project context files may also be visible, so do not place unrelated private material in the workspace.

Collect all three real results before synthesis. A failed, timed-out, errored, or missing result is incomplete; retry at most once when safe and never fabricate a substitute.

## Parent synthesis and fourth review

The parent synthesizes the three results in the main session. After drafting, issue one separate single `delegate_task` call for the fourth reviewer with the neutral brief, checked evidence, all three judge outputs, and the draft. Do not put the reviewer in the original batch, and do not ask it to spawn another panel. Apply and recheck valid review findings before answering.

Hermes batch delegation may deliver completions asynchronously. End the turn when the batch is waiting instead of polling handles in a loop; continue only when the native results are delivered.

## Limits

This adapter documents orchestration, not a guarantee that the configured child route is cheap, available, or accurate. Report the actual route and failures. Never add keys, edit global routing, silently use a premium fallback, or claim a full panel when preflight or execution failed.
