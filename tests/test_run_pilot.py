"""Offline runner regressions: no model CLI or network calls."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load_pilot():
    spec = importlib.util.spec_from_file_location("pilot_under_test", ROOT / "evaluations/run_pilot.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.pilot = load_pilot()
        self.cases = json.loads((ROOT / "evaluations/cases.json").read_text())["cases"]
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name)

    def test_placeholders_filled_from_case_without_parent_instructions(self):
        case = dict(self.cases[0], constraints="Keep the supplied ownership split.",
                    unknowns="Future delivery capacity.")
        payload = self.pilot.run_case(case, "sonnet", self.out, self.out, dry_run=True)
        records = {r["stage"]: r["prompt"] for r in payload["records"]}
        for number, lens in enumerate(case["lenses"], 1):
            prompt = records[f"judge-{number}"]
            for value in [case["question"], lens, case["constraints"], case["unknowns"], "CALC1"]:
                self.assertIn(value, prompt)
            for parent_text in ["Parent: choose", "Examples (adapt", "## Prompt to each judge"]:
                self.assertNotIn(parent_text, prompt)
            self.assertNotIn("{question}", prompt)
            self.assertNotIn("{neutral evidence brief}", prompt)
            self.assertNotIn("checks", prompt)
        self.assertIn(case["question"], records["panel-review"])
        self.assertIn("JUDGES:", records["panel-review"])
        self.assertIn("DRAFT:", records["panel-review"])
        self.assertIn("reviewer-only control", records["single-review"])
        self.assertNotIn("Inputs: {", records["panel-review"])

    def test_placeholder_guard_rejects_unfilled_fields_but_allows_json(self):
        for text in ["{question}", "Inputs: {...}", "{neutral evidence brief}",
                     "{situation, incentives, constraints}", "{unknown_field}", "{question:format}"]:
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, "placeholder"):
                self.pilot.build_prompt(text)
        for literal in ['{"value": 42}', json.dumps({"text": '{"value": 42}'})]:
            self.assertEqual(self.pilot.build_prompt(literal), literal)
        self.assertEqual(self.pilot.build_prompt("{question}", {"question": "Actual question"}),
                         "Actual question")

    def test_unfilled_prompt_is_rejected_before_calling_cli(self):
        with patch.object(self.pilot.subprocess, "run") as cli, \
                self.assertRaisesRegex(ValueError, "placeholder"):
            self.pilot.call("Answer {question}", "judge-1", [], "sonnet", self.out)
        cli.assert_not_called()

    def test_cli_failure_preserves_diagnostic_error(self):
        response = types.SimpleNamespace(returncode=1, stdout="", stderr="synthetic authentication error")
        with patch.object(self.pilot.subprocess, "run", return_value=response), \
                self.assertRaisesRegex(RuntimeError, "judge-1:.*synthetic authentication error"):
            self.pilot.call("prompt", "judge-1", [], "sonnet", self.out)

    def test_synthesis_gets_only_synthesis_instructions(self):
        payload = self.pilot.run_case(self.cases[0], "sonnet", self.out, self.out, dry_run=True)
        prompt = next(r["prompt"] for r in payload["records"] if r["stage"] == "panel-draft")
        self.assertIn("Synthesize by evidence, not majority vote", prompt)
        for text in ["name: based", "## Runtime adapters", "## When to Use",
                     "launch exactly THREE judges", "launch a FOURTH"]:
            self.assertNotIn(text, prompt)

    def test_dry_run_builds_every_stage_of_every_case_without_claude(self):
        output = self.out / "dry"
        with patch.object(self.pilot.subprocess, "run") as cli, \
                patch.object(self.pilot, "call") as model, \
                patch.object(self.pilot.shutil, "which", return_value=None), \
                patch("sys.argv", ["run_pilot.py", "--dry-run", "--output", str(output)]), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.pilot.main(), 0)
        cli.assert_not_called()
        model.assert_not_called()
        summary = json.loads((output / "summary.json").read_text())
        self.assertTrue(summary["complete"])
        self.assertEqual(summary["calls"], 0)
        self.assertEqual(summary["prompts"], 45)
        for case in self.cases:
            payload = json.loads((output / (case["id"] + ".json")).read_text())
            self.assertTrue(payload["dry_run"])
            self.assertEqual(len(payload["records"]), 9)
            self.assertNotIn("conditions", payload)
            for record in payload["records"]:
                self.pilot.build_prompt(record["prompt"])
        self.assertFalse((output / "blind.md").exists())
        self.assertFalse((output / "private/answer-key.json").exists())

    def test_failed_stages_are_recorded_and_other_cases_finish(self):
        for failed_stage in ["baseline", "single-review", "single-revision", "judge-1", "judge-2", "judge-3",
                             "panel-draft", "panel-review", "panel-revision"]:
            with self.subTest(stage=failed_stage):
                output = self.out / failed_stage

                def model(prompt, stage, records, requested, scratch):
                    if self.cases[0]["question"] in prompt and stage == failed_stage:
                        raise RuntimeError("synthetic model failure")
                    records.append({"stage": stage, "returned_models": ["claude-sonnet-test"],
                                    "prompt": prompt, "result": "answer"})
                    return "answer"

                stdout = io.StringIO()
                with patch.object(self.pilot, "call", side_effect=model), \
                        patch.object(self.pilot.shutil, "which", return_value="claude"), \
                        patch("sys.argv", ["run_pilot.py", "--output", str(output)]), \
                        contextlib.redirect_stdout(stdout):
                    self.assertEqual(self.pilot.main(), 1)
                summary = json.loads((output / "summary.json").read_text())
                self.assertFalse(summary["complete"])
                self.assertEqual(summary["cases"], 4)
                self.assertEqual(summary["failures"], [{"case": self.cases[0]["id"],
                                 "stage": failed_stage, "error": "synthetic model failure"}])
                self.assertIn(failed_stage, stdout.getvalue())
                for case in self.cases:
                    payload = json.loads((output / (case["id"] + ".json")).read_text())
                    self.assertEqual(bool(payload.get("failures")), case == self.cases[0])
                blind = (output / "blind.md").read_text()
                self.assertNotIn(self.cases[0]["id"], blind)
                self.assertIn(self.cases[-1]["id"], blind)
                self.assertTrue((output / "private/answer-key.json").is_file())
                self.assertFalse((output / "answer-key.json").exists())

    def test_model_identity_checks_aliases_explicit_ids_and_all_reported_models(self):
        for requested, returned, accepted in [
            ("sonnet", ["claude-sonnet-5-5"], True),
            ("opus", ["claude-opus-4-6"], True),
            ("haiku", ["claude-haiku-4-5-20251001"], True),
            ("opus", ["claude-sonnet-5-5"], False),
            ("haiku", ["claude-opus-4-6"], False),
            ("sonnet", ["claude-sonnet-5-5", "claude-opus-4-6"], False),
            ("sonnet", ["claude-notsonnet-5-5"], False),
            ("claude-opus-4-6", ["claude-opus-4-6-20261001"], True),
            ("claude-opus-4-6", ["claude-opus-4-5"], False),
            ("gpt-4.1", ["gpt-4.1-2025-04-14"], True),
            ("gpt-4.1", ["gpt-4.1-mini"], False),
            ("custom-model", ["custom-model"], True),
            ("custom-model", ["different-model"], False),
            ("opus[1m]", ["claude-opus-4-6"], True),
            ("haiku", [], False),
        ]:
            with self.subTest(requested=requested, returned=returned):
                response = types.SimpleNamespace(returncode=0, stdout=json.dumps({
                    "subtype": "success", "is_error": False, "result": "answer",
                    "modelUsage": {name: {} for name in returned},
                }))
                with patch.object(self.pilot.subprocess, "run", return_value=response):
                    if accepted:
                        self.assertEqual(self.pilot.call("prompt", "test", [], requested, self.out), "answer")
                    else:
                        with self.assertRaisesRegex(RuntimeError, "model"):
                            self.pilot.call("prompt", "test", [], requested, self.out)

    def test_help_documents_safe_mode_and_default_output(self):
        output = io.StringIO()
        with patch("sys.argv", ["run_pilot.py", "--help"]), \
                contextlib.redirect_stdout(output), self.assertRaises(SystemExit) as exc:
            self.pilot.main()
        self.assertEqual(exc.exception.code, 0)
        self.assertIn("--safe-mode", output.getvalue())
        self.assertIn("disables skills", output.getvalue())
        self.assertIn("evaluations/results", output.getvalue())
        self.assertIn("--dry-run", output.getvalue())


if __name__ == "__main__":
    unittest.main()
