# Verification by gate

## Structural and safe-install tests

Run the complete stdlib suite from the repository root:

```sh
python -m unittest discover -s tests -v
python -m unittest discover -s tests -q
```

The tests validate metadata, links, supporting documents, evidence-fixture shape, checked fixture arithmetic, tone/reviewer contracts, runtime-adapter separation, and the optional installer. Installer coverage includes custom paths with spaces, `HERMES_HOME`/`CLAUDE_CONFIG_DIR` defaults, explicit destinations, runtime validation, refusal to overwrite, allowlisted adapters/references, evaluation-artifact exclusion, and the manual-only/metadata frontmatter fields. These tests do not prove that an LLM follows the instructions.

`python install.py --runtime ...` is optional. It uses only the Python standard library, has no credential or model dependency, and refuses an existing destination. Use a temporary/custom destination for testing; never point it at a real profile unless that is the user's explicit action.

## Hermes frontmatter parser check

The v1.3 frontmatter includes Claude Code's `disable-model-invocation: true` field. A local Hermes parser check confirms the field is parsed without rejection; the parent’s native clean-context test still must verify discovery and activation behavior. This is not a native panel run.

## Native runtime gates pending parent exercise

These exact native paths are proposed for the parent to exercise in clean contexts; this repository does not claim they have succeeded:

1. **Hermes:** in a fresh session with the native delegation tool and an accepted configured delegation route, preflight the actual schema, then issue one native batch with exactly three task objects:

   ```text
   delegate_task(tasks=[
     {"goal": "Judge through lens A using the shared panel template", "context": "Neutral brief + lens A"},
     {"goal": "Judge through lens B using the shared panel template", "context": "Neutral brief + lens B"},
     {"goal": "Judge through lens C using the shared panel template", "context": "Neutral brief + lens C"}
   ])
   ```

   Keep the same neutral facts in all three contexts, do not pass a pretend per-child model/provider override, collect all three real results, synthesize in the parent, then issue one separate native reviewer task with the neutral brief, evidence, three outputs, and draft.

2. **Claude Code:** from the MAIN session, explicitly invoke `/based` in a clean `CLAUDE_CONFIG_DIR` with the skill discoverable in the test project's `.claude/skills/based`. Confirm the observed native `Agent` schema (or supported `Task` equivalent), then launch three fresh isolated subagents in one parallel turn with the shared neutral brief plus one lens each; synthesize in MAIN; launch a fourth fresh reviewer from MAIN. Do not use `--safe-mode` for discovery/E2E because it disables skills/custom agents. Restrict tools to the least required read-only set and use only an explicitly accepted route/model.

Record capability preflight, actual model identity when exposed, failures, and whether all four stages completed. A clean install proves discovery only; a component call proves neither full invocation-to-final behavior nor quality improvement. Do not report a successful native workflow until the parent has exercised it.

## Historical evaluation artifacts

The optional `evaluations/run_pilot.py` helper and retained v1.2 reports are evaluation-only. They may make model calls through a separately authenticated account and save prompts/results; synthetic fixtures are required. They are not imported by the installer or runtime adapters, and they are not v1.3 compatibility evidence. No model calls are required for the repository test suite.
