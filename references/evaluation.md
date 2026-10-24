# Evaluate and share a deliberation skill

## Review before changing

Read the actual skill, supporting prompts, install instructions, tests, and execution evidence. Separate an observed defect from a proposed improvement or a reviewer's inference. Reviewing whether to share is not permission to edit the repository, change visibility, or publish. Make internal skill-library maintenance distinct from a released repository update.

## Establish what was verified

Check the following gates separately and report only the ones exercised:

1. Document structure and valid supporting links.
2. Clean clone into an isolated profile's skills directory and native slash-command discovery.
3. Model connectivity and requested/returned model identity.
4. Three genuinely separate judge conversations, parent synthesis, and a separate reviewer.
5. Actual invocation-to-final behavior, including failed-agent handling and applying a REVISE result.
6. Comparative answer quality.

String-presence tests are structural lint, not evidence of agent compliance. A reviewer returning REVISE proves critique was produced, not that defects were corrected. Keep sanitized artifacts sufficient to inspect the test; do not ship private prompts, credentials, or unrelated user context.

## Small comparison pilot

Before claiming better answers, propose a bounded pilot rather than a benchmark platform:

- Use the same diverse questions and comparable starting evidence for a strong single answer, answer-plus-reviewer, and full three-judge panel plus reviewer.
- Include checkable factual questions, genuine trade-offs, uncertain plans, false premises, missing or unavailable sources, stale claims, and cases where the correct response is insufficient evidence.
- Ask a person or a clearly disclosed non-panel scorer to rate anonymized outputs without method labels. Use a fixed rubric: factual errors, citation support, calibrated uncertainty, useful insight, feasible action, and unnecessary harshness. Disclose scorer/model limitations and any unequal access to evidence or tools.
- Record elapsed time, actual returned model usage, and real cost only when available. Never manufacture prices or infer savings from model names.
- Record whether the judges introduced materially different arguments and whether these changed the final answer. Include null results and regressions, not just wins.
- Define a practical decision rule before scoring. If the full panel shows no useful advantage over reviewer-only, consider simplifying or reserving it for harder questions. A handful of examples is exploratory, not statistically conclusive proof.

## Sharing recommendation

Share as an experimental instruction workflow when its setup and limitations are clear; do not call it unbiased, a truth engine, or a guaranteed quality upgrade without appropriate evidence. Lead documentation with native Hermes routing and the expected three judge calls, separate review, and parent synthesis. Keep provider-specific recipes optional. Branding is a user choice, not a correctness metric.

Do not add lite modes, model routers, dashboards, services, or more agents solely because reviewers suggested them. Explain the trade-off and test whether additional complexity is justified. Preserve the user's requested portable Markdown-skill format unless they approve a broader implementation.