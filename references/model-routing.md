# Model routing for independent deliberation

## Choose the route before launching

1. Inspect the actual delegation tool schema and the active profile's model/provider settings without displaying secrets. Use native Hermes delegation when its configured route satisfies the requested budget; do not infer per-child model controls that the tool does not expose.
2. If using a separately authenticated CLI, inspect its current help and authentication status. Explicitly select the requested model. A prompt saying 'use Sonnet' is not model selection. Do not change global routing or install a provider merely to run the panel without approval.
3. Disclose the actual route and avoid price assertions without a current source. Record returned model identities; an alias can resolve to a different version later. Never silently substitute a premium fallback.
4. Keep the three judge contexts separate and start the reviewer only after synthesis. Bound execution time and requested output size. Treat nonzero exit, timeout, error status, or missing output as a failed agent rather than a completed review.

## Claude Code option

The listed flags were checked against the installed Claude Code 2.1.293 help on October 24, 2026 (UTC). This is a tested recipe, not a minimum-version or all-version compatibility claim. Inspect local help before use; no Claude subscription is required for the native Hermes route.

When the installed CLI supports these flags and is already authenticated, use a separate process and a fresh empty working directory for each judge and reviewer:

```sh
claude -p --model sonnet \
  --tools "" --safe-mode \
  --strict-mcp-config --mcp-config '{"mcpServers":{}}' \
  --no-session-persistence --output-format json
```

Supply the complete neutral brief and that agent's prompt through stdin. Do not use resume/continue or share prior transcripts between judges. Do not use `--bare` when relying on subscription OAuth: that mode skips that authentication path. Do not add permission-bypass flags.

Parse exit status, `is_error`, result text, and returned model usage; retain a minimal local execution record without credentials. Separate empty working directories, no tools, disabled customizations, and an empty MCP configuration reduce unintended context exposure; they are not an OS-level sandbox or a guarantee against provider retention. Only send task-relevant material.

Tool-free judges and reviewers cannot browse, calculate through tools, or independently inspect files. The parent must supply evidence, perform consequential source and arithmetic checks, and distinguish its observations from reviewer-verified facts. If read-only research tools are enabled on a different route, give all judges the same starting brief and apply the evidence contract to any additional sources they introduce.

## Verification scope

Report separately: skill discovery, model connectivity, component execution, full invocation-to-final workflow, and answer-quality comparison. A clean clone exposing `/based` does not prove the entire workflow runs; a successful manual four-process test does not prove every user's model routing or slash invocation. Never collapse these gates into 'fully tested'.