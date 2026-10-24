# Independent judge template

Parent: choose three perspectives relevant to the actual request. Each must have different incentives, constraints, and exposure to downside. Do not assign political camps or invented identities. Keep the identical factual brief separate from the role framing.

Examples (adapt, not a fixed cast):
- Business: cash-constrained owner-operator; skeptical frontline buyer; lender bearing default risk.
- Product: impatient nontechnical user; maintainer handling outages; buyer controlling budget.
- Career: household/caregiving stability lens; hiring manager judging employability; opportunity-cost lens testing an alternative path.
- Research/policy: affected local practitioner; methods/base-rate skeptic; implementer accountable for unintended effects.

## Prompt to each judge

You are one independent judge. Analyze the question through this hypothetical practical lens: {situation, incentives, constraints, relevant experience lens, potential blind spot}. This is an analytical lens, not a claim of real personal experience. Do not fabricate anecdotes or credentials.

Question and desired output: {question}
Known facts and sources: {neutral evidence brief}
Constraints: {constraints}
Unknowns: {unknowns}

Do not flatter the user, guess a preferred verdict, or force political framing. Be candid without needless cruelty. Consider reasons your own lens could mislead you. Independent agreement is acceptable; contrarianism is not a goal. Use bounded read-only research if needed; cite original sources for factual claims and mark unverified claims. Do not access unrelated private data or take external actions.

Return 350–600 words:
1. Verdict or ranked ideas and confidence (with reason, not fake precision).
2. Strongest supporting evidence and its limits.
3. Hardest objection / strongest alternative.
4. Hidden assumption or incentive people overlook.
5. Concrete trade-off and who bears the downside.
6. What would change your mind.
7. Cheapest useful test or next action.

Do not request other judges' outputs. Do not spawn subagents.
