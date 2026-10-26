# Runtime-neutral routing and capability contract

Choose the runtime before launching. The shared skill requires exactly three independent judges, parent synthesis, and a separate fourth review; the runtime adapter supplies the native calls.

1. Inspect the selected runtime's actual orchestration schema and the active model/provider route without displaying secrets.
2. Confirm the route is explicitly accepted or already verified as acceptable for the task's budget. Do not infer a model override from prompt text, and do not assert current pricing without a current source.
3. Confirm the runtime can provide four bounded fresh-agent calls. If the native tool, model route, budget, or isolation capability is missing or unverified, fail honestly. Never substitute one parent answer, another CLI, new credentials, or a silent premium fallback.
4. State whether agents are tool-free or have bounded read-only tools. Tool-free agents reason only from the evidence and checked calculations supplied by the parent; they must not claim to browse, inspect sources, or verify arithmetic independently.
5. Treat nonzero exits, timeouts, error statuses, missing outputs, and unsupported schemas as failed stages. Preserve incomplete status rather than manufacturing a result.

Use [the Hermes adapter](../adapters/hermes.md) for native `delegate_task` and [the Claude Code adapter](../adapters/claude-code.md) for native `Agent`/supported `Task`. These are separate routes; neither depends on the other CLI.

## Verification scope

Report these gates separately: skill discovery, capability/schema preflight, model connectivity and accepted route, individual component execution, full three-judge → parent-synthesis → fourth-review behavior, and answer-quality comparison. A clean install proves discovery only. Structural tests prove document invariants only. A successful component run does not prove full invocation-to-final behavior or general quality improvement.
