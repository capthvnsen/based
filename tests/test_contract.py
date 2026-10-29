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
from urllib.parse import unquote, urlsplit

import install

ROOT = Path(__file__).resolve().parents[1]


def load_pilot():
    spec = importlib.util.spec_from_file_location("based_pilot", ROOT / "evaluations/run_pilot.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StructuralChecks(unittest.TestCase):
    def test_frontmatter(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        _, header, body = text.split("---", 2)
        self.assertTrue(body.strip())
        # Parse the top-level scalar fields; nested runtime metadata may vary.
        fields = dict(re.findall(r"^([\w-]+):[ \t]*(.*)$", header, re.MULTILINE))
        for key in ("name", "description"):
            with self.subTest(field=key):
                self.assertIn(key, fields)
                value = fields[key].strip()
                if value.startswith('"'):
                    value = json.loads(value)
                elif value.startswith("'"):
                    self.assertTrue(value.endswith("'"))
                    value = value[1:-1].replace("''", "'")
                elif value in ("|", ">", "|-", ">-"):
                    value = re.search(rf"^{key}:.*\n((?:[ \t]+[^\n]*\n?)+)",
                                      header, re.MULTILINE).group(1).strip()
                self.assertTrue(value)
                self.assertNotIn(value.lower(), ("null", "~"))
        self.assertEqual(fields.get("disable-model-invocation", "").lower(), "true")

    def test_install_sources_exist(self):
        for relative in install.INSTALL_FILES:
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file())

    def test_installed_markdown_links_resolve_inside_payload(self):
        with tempfile.TemporaryDirectory() as parent:
            for runtime in install.ADAPTERS:
                destination = install.install(runtime, Path(parent) / runtime)
                installed = {path.resolve() for path in destination.rglob("*") if path.is_file()}
                for path in destination.rglob("*.md"):
                    text = path.read_text(encoding="utf-8")
                    links = re.findall(r"\]\(<?([^\s)>]+)>?(?:\s+[^)]*)?\)", text)
                    links += re.findall(r"^\s*\[[^\]]+\]:\s*<?([^\s>]+)>?", text, re.MULTILINE)
                    for target in links:
                        url = urlsplit(target)
                        if not url.scheme and not url.netloc and url.path:
                            with self.subTest(runtime=runtime, path=path, target=target):
                                self.assertIn((path.parent / unquote(url.path)).resolve(), installed)

    def test_runtime_adapters_document_native_tools_and_limits(self):
        for runtime, relative in install.ADAPTERS.items():
            text = (ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(runtime=runtime):
                self.assertRegex(text, r"(?i)preflight")
                self.assertRegex(text, r"(?i)fresh.*(?:context|subagent|conversation)")
                if runtime == "hermes":
                    self.assertIn("delegate_task", text)
                    self.assertIn("tasks=[", text)
                    self.assertIn("oneshot_max_children", text)
                    self.assertIn("--skills based", text)
                else:
                    self.assertRegex(text, r"Agent|Task")
                    self.assertRegex(text, r"(?i)manual.*?/based")

    def test_shared_core_preserves_panel_and_review_contract(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("delegate_task(", skill)
        self.assertNotIn("claude -p", skill)
        self.assertRegex(skill, r"(?i)(?:three|3)\s+judges")
        self.assertRegex(skill, r"(?i)(?:fourth|4th)[^\n.]*reviewer")
        self.assertRegex(skill, r"(?i)synthesi[^\n.]*evidence")
        reviewer = (ROOT / "references/reviewer.md").read_text(encoding="utf-8")
        for verdict in ("PASS", "REVISE"):
            self.assertRegex(reviewer, rf"\b{verdict}\b")

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
        # Presence checks only: these are not model-behavior guarantees.
        voice = (ROOT / "references/voice.md").read_text(encoding="utf-8")
        for concept in (r"candor|candid", r"dry wit|humou?r", r"uncertain|unknown",
                        r"grief|crisis|vulnerab", r"hypothes[ie]s"):
            self.assertRegex(voice, "(?i)" + concept)

    def test_reviewer_checks_evidence_and_false_aggression(self):
        reviewer = (ROOT / "references/reviewer.md").read_text(encoding="utf-8")
        self.assertRegex(reviewer, r"(?i)unsupported[^\n.]*REVISE")
        self.assertRegex(reviewer, r"(?i)false aggression[^\n.]*REVISE")
        self.assertRegex(reviewer, r"(?i)(?:sound|good)[- ]plan[^\n.]*pass")

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
