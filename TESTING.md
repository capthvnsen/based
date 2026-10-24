# Verification

A live bounded smoke test used a hypothetical founder deciding whether to leave employment for an unvalidated product. It did not use private business information.

- Three concurrent Claude Code subprocesses, fresh empty working directories, no tool access, safe mode, empty MCP configuration, no saved sessions.
- Different lenses: household stability, bootstrapped product execution, and cash-flow underwriting.
- All three completed successfully; returned model usage identified `claude-sonnet-5-5`.
- Parent wrote a synthesis that rejected unsupported psychological assumptions and distinguished gross from take-home salary.
- A fourth fresh Sonnet process reviewed the draft and returned REVISE, including a warning about correlated judgments from the same model, ambiguous validation failures, and insufficiently explicit stop conditions.
- The skill was updated to explicitly distinguish fresh-context independence from empirical or statistical independence.

No claim is made that one scenario validates every domain, guarantees unbiased output, proves current model prices, or tests future installations. Structural tests are separate from the live model test. Raw run records remain local and are not shipped with this repo.
