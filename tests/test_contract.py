"""Structural and evaluation-helper tests; NOT proof of LLM compliance."""
import importlib.util
import json
import math
from pathlib import Path
import re
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load_pilot():
    spec = importlib.util.spec_from_file_location("based_pilot", ROOT / "evaluations/run_pilot.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StructuralChecks(unittest.TestCase):
    def test_frontmatter(self):
        text = (ROOT / "SKILL.md").read_text()
        self.assertTrue(text.startswith("---\n"))
        header = text.split("---", 2)[1]
        self.assertIn("name: based", header)
        description = re.search(r'description: "([^"\n]+)"', header).group(1)
        self.assertLessEqual(len(description), 60)
        self.assertIn("version: 1.3.0", header)
        self.assertIn("disable-model-invocation: true", header)

    def test_local_links(self):
        for path in ROOT.rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if not target.startswith(("https:", "http:", "#", "mailto:")):
                    self.assertTrue((path.parent / target.split("#")[0]).is_file(), (path, target))

    def test_runtime_adapters_exist_and_are_linked(self):
        skill = (ROOT / "SKILL.md").read_text()
        hermes = (ROOT / "adapters/hermes.md").read_text()
        claude = (ROOT / "adapters/claude-code.md").read_text()
        self.assertIn("adapters/hermes.md", skill)
        self.assertIn("adapters/claude-code.md", skill)
        self.assertIn("delegate_task(tasks=[", hermes)
        self.assertIn("Agent", claude)
        self.assertIn("Task", claude)
        self.assertIn("MAIN", claude)
        self.assertIn("Do not use `--safe-mode`", claude)

    def test_adapter_invocation_limits_are_documented(self):
        hermes = (ROOT / "adapters/hermes.md").read_text()
        claude = (ROOT / "adapters/claude-code.md").read_text()
        self.assertIn("oneshot_max_children", hermes)
        self.assertIn("--skills based", hermes)
        self.assertIn("does not expand", hermes)
        self.assertIn("manual `/based`", claude)

    def test_shared_core_has_no_runtime_orchestration_calls(self):
        skill = (ROOT / "SKILL.md").read_text()
        self.assertNotIn("delegate_task(", skill)
        self.assertNotIn("claude -p", skill)
        self.assertIn("exactly THREE", skill)
        self.assertIn("FOURTH, separate reviewer", skill)
        self.assertIn("Synthesize by evidence", skill)

    def test_supporting_documents_exist(self):
        for name in ["panel", "reviewer", "voice", "model-routing", "evaluation"]:
            self.assertTrue((ROOT / "references" / (name + ".md")).is_file())

    def test_case_coverage_and_evidence_shape(self):
        cases = json.loads((ROOT / "evaluations/cases.json").read_text())["cases"]
        self.assertEqual(len(cases), 5)
        self.assertEqual(len({case["id"] for case in cases}), 5)
        self.assertEqual({case["task"] for case in cases}, {"research", "planning", "brainstorming", "judgment"})
        for case in cases:
            self.assertEqual(len(case["lenses"]), 3)
            self.assertEqual(len(set(case["lenses"])), 3)
            self.assertTrue(case["checks"])
            for item in case["evidence"]:
                self.assertEqual(set(item), {"id", "type", "text"})

    def test_financial_fixture_calculations(self):
        case = json.loads((ROOT / "evaluations/cases.json").read_text())["cases"][0]
        actual = json.loads(next(x["text"] for x in case["evidence"] if x["id"] == "CALC1"))
        expected = {"four_client_revenue": 4 * 1995,
                    "four_client_profit": 4 * (1995 - 675) - 2300,
                    "four_client_owner_income": (4 * (1995 - 675) - 2300) * .5,
                    "minimum_clients_for_9000_owner_income": math.ceil((9000 / .5 + 2300) / (1995 - 675)),
                    "owner_income_at_16": (16 * (1995 - 675) - 2300) * .5}
        self.assertEqual(actual, expected)


    def test_tone_permission_and_limits_are_documented(self):
        # Presence checks only: these are NOT model-behavior guarantees.
        voice = (ROOT / "references/voice.md").read_text()
        for phrase in ["bracing, plain-spoken candor", "restrained dry wit",
                       "Unknown does not mean absent", "If the plan holds up, say so",
                       "For grief, crisis, or vulnerability", "not a representative study",
                       "sharper answers increase adoption"]:
            self.assertIn(phrase, voice)

    def test_reviewer_does_not_require_false_aggression(self):
        reviewer = (ROOT / "references/reviewer.md").read_text()
        for phrase in ["Material false aggression requires REVISE",
                       "lack of paying users alone is not a fatal flaw",
                       "may pass without any sting", "different conclusion from a strong normal answer"]:
            self.assertIn(phrase, reviewer)

    def test_tone_fixture_shape_and_checked_arithmetic(self):
        fixture = json.loads((ROOT / "evaluations/tone-v12/cases.json").read_text())
        self.assertTrue(fixture["synthetic_only"])
        cases = {case["id"]: case for case in fixture["cases"]}
        self.assertEqual(len(cases), 7)
        self.assertEqual(cases["negative-margin"]["checked"]["contribution_before_fixed_costs"], 10 - 14)
        self.assertEqual(cases["sound-plan"]["checked"]["contribution_before_fixed_costs"], 10 - 4)
        self.assertEqual(cases["corrected-facts"]["checked"]["corrected_contribution"], 10 - 4)
        for name in ["thin-brief", "personal-insult-bait", "hearsay-and-flattery", "vulnerable-context"]:
            self.assertTrue(cases[name]["checks"])


class EvaluationHelperChecks(unittest.TestCase):
    def setUp(self):
        self.pilot = load_pilot()
        self.tmp = tempfile.TemporaryDirectory(prefix="based-test-", dir=str(ROOT))
        self.addCleanup(self.tmp.cleanup)

    def run_mocked(self, response):
        records = []
        with patch.object(self.pilot.subprocess, "run", return_value=response) as run:
            output = self.pilot.call("synthetic prompt", "test", records, "sonnet", self.tmp.name)
        return output, records, run.call_args

    def test_success_records_actual_model_and_usage_without_session_id(self):
        data = {"subtype": "success", "is_error": False, "result": "answer",
                "modelUsage": {"claude-sonnet-test": {}}, "usage": {"input_tokens": 1},
                "session_id": "not-for-shipping"}
        output, records, args = self.run_mocked(types.SimpleNamespace(returncode=0, stdout=json.dumps(data)))
        self.assertEqual(output, "answer")
        self.assertEqual(records[0]["returned_models"], ["claude-sonnet-test"])
        self.assertNotIn("session_id", records[0])
        command = args.args[0]
        self.assertIn("--safe-mode", command)
        self.assertIn("--strict-mcp-config", command)
        self.assertEqual(command[command.index("--tools") + 1], "")
        self.assertNotIn("--fallback-model", command)

    def test_nonzero_exit_is_not_success(self):
        with self.assertRaises(RuntimeError):
            self.run_mocked(types.SimpleNamespace(returncode=1, stdout="{}"))

    def test_model_error_is_not_success(self):
        with self.assertRaises(RuntimeError):
            self.run_mocked(types.SimpleNamespace(returncode=0, stdout=json.dumps({"subtype": "success", "is_error": True, "result": "wrong"})))

    def test_missing_model_identity_is_not_success(self):
        with self.assertRaises(RuntimeError):
            self.run_mocked(types.SimpleNamespace(returncode=0, stdout=json.dumps({"subtype": "success", "is_error": False, "result": "answer"})))

    def test_unexpected_model_is_not_silently_accepted(self):
        with self.assertRaises(RuntimeError):
            self.run_mocked(types.SimpleNamespace(returncode=0, stdout=json.dumps({"subtype": "success", "is_error": False, "result": "answer", "modelUsage": {"claude-opus-test": {}}})))

    def test_timeout_propagates_without_fallback(self):
        with patch.object(self.pilot.subprocess, "run", side_effect=self.pilot.subprocess.TimeoutExpired("claude", 180)) as run:
            with self.assertRaises(self.pilot.subprocess.TimeoutExpired):
                self.pilot.call("prompt", "test", [], "sonnet", self.tmp.name)
            self.assertEqual(run.call_count, 1)


if __name__ == "__main__":
    unittest.main()
