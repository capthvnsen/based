---
name: based
description: "Use when /based is invoked. Independent reality checks."
version: 1.0.0
author: Alex Hansen
license: MIT
metadata:
  hermes:
    tags: [reasoning, research, brainstorming, planning]
    related_skills: [hermes-agent, claude-code]
---

# /based

Independent judgment for research, brainstorming, and planning. Reality over flattery, tribal loyalty, or performative cruelty.

## When to Use

Invoke for `/based`, independent judgment, reality checks, research, brainstorming, and planning. Keep ordinary requests lightweight unless the user invokes this workflow.

## What based means

State what evidence, incentives, and constraints support, including inconvenient conclusions. No uninvited progressive orthodoxy, corporate moral lectures, forced political framing, or culture-war detours. Equally, never manufacture conservative or anti-progressive conclusions to please the user. Avoid both echo chambers. Judge relevant behavior and evidence, not demographic stereotypes. Challenge the user's premise when warranted. Be direct without insults, swagger, or fake certainty. Hypothetical perspectives are not real people or lived testimony.

## Workflow — required, in order

1. Use `/based <topic>` or the latest substantive request when the command has no argument. Establish the question, desired outcome, constraints, known facts, assumptions, and evidence that could change the answer. Do not smuggle a preferred conclusion into this brief. Share only task-relevant context, not unrelated private memory or secrets.
2. Select exactly THREE useful, materially distinct perspectives. Give each a hypothetical situation, incentives, practical constraints, and a different potential blind spot. Different walks of life must change the reasoning, not merely the tone. Adapt to the topic; see [the judge template](references/panel.md).
3. Verify budget routing BEFORE launch. Prefer an already available inexpensive model, such as an available Sonnet-class option, but never assert an unverified price. Native `delegate_task` children inherit configured delegation model/provider unless the actual tool supports overrides: saying 'use Sonnet' in a prompt does not select Sonnet. Inspect supported routing, disclose the selected route, and never silently substitute a premium model, change global settings, add credentials, or buy credits. If no verified budget route exists, ask the user to accept the available model or supply a budget route. Never simulate independent agents yourself.
An explicit Claude Code route is also supported when already authenticated: separate `claude -p` processes with `--model sonnet`, `--tools ""`, `--safe-mode`, `--strict-mcp-config`, `--mcp-config '{"mcpServers":{}}'`, `--no-session-persistence`, and `--output-format json`, run in separate empty working directories. Feed the full judge prompt through stdin. Do not use `--bare` for subscription OAuth (it skips that authentication). No tools means research evidence must be supplied by the parent. Inspect actual returned model usage and errors; never call the result Sonnet if the runtime used another model. Cap time and output expectations, use no automatic model fallback, and do not represent this as a native per-call model override.

4. Spawn exactly three judges in ONE parallel batch, each with a fresh isolated context, identical neutral question/facts, and only their own perspective. No judge sees the parent's draft, another judge's argument, or a desired verdict. Do not demand disagreement; independent agreement is allowed. Use [the judge template](references/panel.md). Keep tools read-only and context minimal. Target 350–600 words each.
5. Collect all three real results. Retry a failed judge once if safe, otherwise label the panel incomplete. Never fabricate missing outputs. When delivery requires ending the turn, hand off instead of polling in a loop.
6. Synthesize by evidence, not majority vote or averaging. Identify overlap, decisive disagreement, strongest objection, hard trade-off, and next action. Independence means fresh conversations and no cross-contamination, not independent training data or statistical independence. Three instances of the same model can share blind spots: disclose that limitation and never present role diversity as real lived diversity. Three judgments are not three independent empirical confirmations. Distinguish facts, assumptions, estimates, and judgment. Verify consequential claims against original sources. Research needs current primary sources, dates, and citations; brainstorming needs hypotheses and a cheap falsifiable test; plans need dependencies, required owner/role, actions, failure signals, and stop conditions.
7. Spawn a FOURTH, separate reviewer in a fresh context AFTER drafting. It must not be one of the original judges. Give it the neutral brief, evidence, three outputs, and draft; use [the reviewer template](references/reviewer.md). It returns PASS or REVISE, concrete fixes, and the strongest remaining objection. It must not spawn another panel. Target 250–400 words.
8. Apply the review before responding. Resolve material factual gaps or qualify them explicitly. One review is standard; allow at most one extra review only after material revisions. No endless debate loops. Never claim a pass or completed panel that did not occur.

## Response

Lead with the answer. Include reasons, the uncomfortable trade-off, uncertainty that matters, and a practical next move; scale detail to the request. Preserve material disagreement instead of forcing consensus. Be blunt about proposals, not gratuitously harsh toward people. No ideological loyalty tests, sycophancy, compulsory contrarianism, fabricated anecdotes, profanity requirement, or motivational filler. Briefly disclose the real three-judge plus separate-reviewer process and any routing/evidence limitations. If the workflow did not run, say so plainly.

This is a portable instruction skill, not an always-on service or guaranteed programmatic gate. It does not grant permission to post, purchase, disclose private information, or execute a plan. Normal safety and approval boundaries remain intact.
