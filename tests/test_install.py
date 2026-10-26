import os
import tempfile
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class InstallDestinationTests(unittest.TestCase):
    def test_default_destination_uses_runtime_home(self):
        import install

        with tempfile.TemporaryDirectory(prefix="based-home-") as home:
            with patch.dict(os.environ, {"HERMES_HOME": home}, clear=False):
                self.assertEqual(
                    install.default_destination("hermes"),
                    Path(home) / "skills" / "based",
                )

    def test_default_destination_uses_claude_config_dir(self):
        import install

        with tempfile.TemporaryDirectory(prefix="claude-config-") as config:
            with patch.dict(os.environ, {"CLAUDE_CONFIG_DIR": config}, clear=False):
                self.assertEqual(
                    install.default_destination("claude"),
                    Path(config) / "skills" / "based",
                )

    def test_runtime_choices_reject_unknown(self):
        import install

        with redirect_stderr(StringIO()):
            with self.assertRaises(SystemExit):
                install.build_parser().parse_args(["--runtime", "bogus"])

    def test_parser_accepts_explicit_destination(self):
        import install

        args = install.build_parser().parse_args(["--runtime", "claude", "--dest", "a path"])
        self.assertEqual(args.runtime, "claude")
        self.assertEqual(args.dest, Path("a path"))

    def test_installs_preserve_runtime_opt_in_fields(self):
        import install

        with tempfile.TemporaryDirectory(prefix="based-runtime-fields-") as parent:
            for runtime in ("hermes", "claude"):
                destination = Path(parent) / runtime
                install.install(runtime, destination)
                frontmatter = (destination / "SKILL.md").read_text().split("---", 2)[1]
                self.assertIn("disable-model-invocation: true", frontmatter)
                self.assertIn("metadata:\n  hermes:", frontmatter)

    def test_main_installs_using_explicit_destination(self):
        import install

        with tempfile.TemporaryDirectory(prefix="based-main-") as parent:
            destination = Path(parent) / "space path" / "based"
            result = install.main(["--runtime", "claude", "--dest", str(destination)])

            self.assertEqual(result, 0)
            self.assertTrue((destination / "SKILL.md").is_file())

    def test_existing_destination_is_not_overwritten(self):
        import install

        with tempfile.TemporaryDirectory(prefix="based-existing-") as parent:
            destination = Path(parent) / "based"
            destination.mkdir()
            marker = destination / "keep.txt"
            marker.write_text("do not overwrite")

            with self.assertRaises(FileExistsError):
                install.install("hermes", destination)

            self.assertEqual(marker.read_text(), "do not overwrite")

    def test_empty_existing_destination_is_preserved(self):
        import install

        with tempfile.TemporaryDirectory(prefix="based-empty-existing-") as parent:
            destination = Path(parent) / "based"
            destination.mkdir()

            with self.assertRaises(FileExistsError):
                install.install("hermes", destination)

            self.assertTrue(destination.is_dir())
            self.assertEqual(list(destination.iterdir()), [])

    def test_failed_move_removes_only_new_partial_install(self):
        import install

        with tempfile.TemporaryDirectory(prefix="based-rollback-") as parent:
            destination = Path(parent) / "based"
            original_move = install.shutil.move
            calls = []

            def fail_after_first_move(source, target):
                calls.append(source)
                if len(calls) == 2:
                    raise OSError("synthetic interrupted install")
                return original_move(source, target)

            with patch.object(install.shutil, "move", side_effect=fail_after_first_move):
                with self.assertRaisesRegex(OSError, "synthetic interrupted install"):
                    install.install("hermes", destination)
            self.assertFalse(destination.exists())
            self.assertEqual(list(Path(parent).iterdir()), [])

    def test_install_copies_skill_and_references_to_spaced_destination(self):
        import install

        with tempfile.TemporaryDirectory(prefix="based-install-") as parent:
            destination = Path(parent) / "custom home" / "skills" / "based"
            result = install.install("hermes", destination)

            self.assertEqual(result, destination)
            self.assertTrue((destination / "SKILL.md").is_file())
            self.assertTrue((destination / "adapters" / "hermes.md").is_file())
            self.assertTrue((destination / "adapters" / "claude-code.md").is_file())
            for reference in ("evaluation", "model-routing", "panel", "reviewer", "voice"):
                self.assertTrue((destination / "references" / f"{reference}.md").is_file())
            self.assertFalse((destination / "evaluations").exists())


if __name__ == "__main__":
    unittest.main()
