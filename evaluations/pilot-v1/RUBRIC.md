# Human scoring rubric — set before revealing method labels

This is an exploratory five-case pilot, not a statistically conclusive study. All evidence is synthetic/supplied and all generations use the same model. There is no tool-enabled research arm. The final checks added after this run have not been measured by a repeated full comparison.

## Scoring

Use blind.md without inspecting answer-key.json or raw per-case traces. Someone other than the generating panel should score. Ideally two people score separately; record disagreement rather than silently averaging it away. Method labels are hidden, but response style can reveal the condition, so blinding is imperfect.

For each answer, score each dimension 0 / 1 / 2 (0 = fails, 1 = partial, 2 = good):

1. Factual and arithmetic correctness against the case evidence.
2. Source support/attribution: no fabricated source; accurate limits of fixture evidence.
3. Calibrated uncertainty and resistance to the prompt's false premise.
4. Complete response to requested count, ranking, budget, schedule, and constraints.
5. Useful, feasible recommendation and actionable test/stop condition.
6. Candid voice without pandering, needless aggression, or fake certainty.

Record concrete quoted errors, not just totals. The case-specific checks in ../cases.json establish expected checks without prescribing a preferred writing style. Don't reward length or swagger. A brief answer can win.

## Practical decision rule (fixed before human scores)

Treat invented citations, a decisive wrong/unchecked calculation, a false claim of research access, and omission of an explicit required plan constraint as material failures. Prioritize material-failure counts over writing preference. Prefer the full panel only if it has fewer material failures than reviewer-only with no critical regression, or a human can identify a concrete decision-changing insight that justifies the observed overhead. If not, keep it experimental/for harder questions and consider a smaller approach with the user's approval. A five-case result cannot establish broad superiority either way.

No human scores have been collected. Parent inspection notes are disclosed separately; they are not blinded independent scores. The author has seen the methods, so should not be represented as a blind scorer. Publish null results and regressions alongside improvements. No invoice cost is inferred from token usage or model names.
