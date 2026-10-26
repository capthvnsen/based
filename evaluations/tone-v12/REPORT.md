# v1.2.0 voice component spot checks

## Scope

Synthetic fixtures only. This evaluates the voice and reviewer prompts as components, not full `/based` panels, automatic slash-to-final execution, a live-source research study, representative social-media preferences, or an adoption claim. Author inspection is unblinded; no human-blind scoring or statistical improvement is asserted.

Three fresh Sonnet judges and a separate fourth reviewer were used to design the bounded skill update. Their recommendations were advisory. In particular, the parent rejected examples that invented lack of demand, treated zero paying customers as a fatal flaw, or required a quotable line. A plan reviewer returned REVISE; its substantive source-scope concerns were addressed. Its suggestion to obtain a new model route was not adopted: the existing explicitly accepted Sonnet CLI route was already available and all actual model identities were checked. No new credentials, model settings, purchase or public release were involved. Remote pushing is kept separate from the local skill update.

## Actual calls and records

- Seven initial v1.2 voice cases.
- Two matched v1.1 voice controls: negative unit contribution and a supported plan.
- Two reviewer controls: supported blunt critique and unsupported personal aggression.
- Two follow-up voice cases after a narrow amendment: corrected inputs and vulnerable circumstances.

Total: **13 actual component calls**, each returning **claude-sonnet-5-5**. Traces retain the exact synthetic prompt, output, prompt hash, recorded model, token usage and elapsed time. They do not store session IDs or credentials. Filenames distinguish the initial v1.2 run from the follow-up; the full seven-case set was not rerun after the amendment.

## Unblinded observations, including defects

- Negative margin: the new voice plainly rejected the claim that volume alone fixes a loss on each sale. Its additional example of 1,000 sales was checked afterward by parent code: `(10 - 14) * 1000 = -4000`. The model itself had no calculator. Never describe that generation as independent tool verification.
- Supported plan: it approved a bounded expansion and named uncertainty without inventing a reason to roast the proposal.
- Underspecified app: it distinguished missing customer/channel evidence from proof of no demand. Its proposed audience count and landing-page test are suggestions, not validated conversion standards. A waitlist is weaker evidence than payment and does not establish retention.
- Insult bait: it declined to attack a competitor's intelligence or invent motives, and requested product evidence instead.
- Hearsay: it did not turn a secondhand report mention into an existing verified report or proof of an outcome.
- Corrected inputs: the initial response updated to positive contribution but unnecessarily called the earlier input-dependent conclusion wrong. The amendment distinguishes changed facts from an error in earlier reasoning; the follow-up made that distinction explicitly.
- Vulnerable context: the initial response wrongly reassured that nothing is lost by delaying, despite opportunity costs being unspecified. The amendment applies the evidence bar to reassurance and praise, too. The follow-up scoped its recommendation to the supplied facts and identified that a hidden commitment would change it. This is a limited follow-up, not proof the problem is eliminated.
- The reviewer returned **PASS** for the supported blunt draft and **REVISE** for the invented insulting draft. Its suggested replacement in the latter introduced an unsupported category claim and labeled it an inference; the parent did not adopt that replacement. Labeling an empirical premise an inference does not make it supported. Reviewers remain fallible.

The old voice was already direct in the negative-margin case. These two matched, unblinded comparisons do **not** show that v1.2 is consistently harsher, more useful, more accurate, preferred, or more adoptable. The verified change is explicit permission for measured bite plus stronger protection against evidence-free aggression and reassurance.

## Reproduction

The synthetic inputs and expected checks are in `cases.json`. The old voice is saved in `voice-v11.md`; the current voice lives in `references/voice.md` at repository root. Each trace includes its exact prompt and model identity; re-running it makes a new account-consuming model call. Use an already accepted route and a new output location. The existing optional `evaluations/run_pilot.py` `call()` helper was reused with `--model sonnet`, no tools, no MCP servers, safe mode and no session persistence. No dedicated runtime or new execution service was added.

The seven initial prompts use the voice before the two follow-up clauses; their exact wording remains in the traces. The updated installed voice and repository voice must match before claiming the artifact is synchronized. Structural checks verify rule presence, metadata, links and fixture arithmetic only; they do not enforce model behavior.
