"""Installer lifecycle checks using temporary directories, never runtime profiles."""

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import install


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="based-install-")
        self.addCleanup(self.tmp.cleanup)
        self.parent = Path(self.tmp.name)
        self.destination = self.parent / "custom home" / "skills" / "based"

    def cli(self, *args):
        stdout, stderr = StringIO(), StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = install.main(["--runtime", "claude", "--dest", str(self.destination), *args])
        return result, stdout.getvalue(), stderr.getvalue()

    def existing_install(self):
        install.install("hermes", self.destination)
        marker = self.destination / "user-notes.txt"
        marker.write_text("preserve local changes", encoding="utf-8")
        return marker

    def test_default_destinations_use_runtime_homes(self):
        for runtime, variable in (("hermes", "HERMES_HOME"), ("claude", "CLAUDE_CONFIG_DIR")):
            with self.subTest(runtime=runtime), patch.dict(os.environ, {variable: str(self.parent)}):
                self.assertEqual(install.default_destination(runtime), self.parent / "skills" / "based")

    def test_default_destinations_fall_back_to_user_home(self):
        with patch.dict(os.environ, {"HERMES_HOME": "", "CLAUDE_CONFIG_DIR": ""}), patch.object(Path, "home", return_value=self.parent):
            self.assertEqual(install.default_destination("hermes"), self.parent / ".hermes/skills/based")
            self.assertEqual(install.default_destination("claude"), self.parent / ".claude/skills/based")

    def test_tilde_destination_is_expanded(self):
        with patch.dict(os.environ, {"HOME": str(self.parent)}):
            result = install.install("hermes", "~/skills/based")
        self.assertEqual(result, self.parent / "skills/based")
        self.assertTrue((result / "SKILL.md").is_file())

    def test_unknown_runtime_has_one_line_error_without_writes(self):
        result, stdout, stderr = self.cli("--runtime", "bogus")
        self.assertEqual(result, 1)
        self.assertEqual(stdout, "")
        self.assertEqual(len(stderr.splitlines()), 1)
        self.assertIn("unsupported runtime: bogus", stderr)
        self.assertEqual(list(self.parent.iterdir()), [])
        with self.assertRaises(ValueError):
            install.install("bogus", self.destination)
        with self.assertRaises(ValueError):
            install.default_destination("bogus")

    def test_main_uses_runtime_default_without_dest(self):
        with patch.dict(os.environ, {"CLAUDE_CONFIG_DIR": str(self.parent)}), redirect_stdout(StringIO()):
            self.assertEqual(install.main(["--runtime", "claude"]), 0)
        self.assertTrue((self.parent / "skills/based/SKILL.md").is_file())

    def test_parser_accepts_explicit_destination(self):
        args = install.build_parser().parse_args(["--runtime", "claude", "--dest", "a path"])
        self.assertEqual(args.dest, Path("a path"))

    def test_installs_only_shared_files_and_selected_adapter(self):
        for runtime in install.ADAPTERS:
            with self.subTest(runtime=runtime):
                destination = self.parent / runtime / "path with spaces" / "based"
                self.assertEqual(install.install(runtime, destination), destination)
                files = {path.relative_to(destination).as_posix() for path in destination.rglob("*") if path.is_file()}
                expected = {path for path in install.INSTALL_FILES if not path.startswith("adapters/")}
                self.assertEqual(files, expected | {install.ADAPTERS[runtime]})
                self.assertFalse((destination / "references/evaluation.md").exists())
                self.assertFalse((destination / "evaluations").exists())
                frontmatter = (destination / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[1]
                self.assertIn("disable-model-invocation: true", frontmatter)
                self.assertIn("metadata:\n  hermes:", frontmatter)

    def test_omitted_document_links_point_to_repository(self):
        source = self.parent / "source"
        linked_files = ("references/evaluation.md", *install.ADAPTERS.values())
        for relative in install.INSTALL_FILES:
            path = source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("\n".join(
                f"[Document]({Path(os.path.relpath(source / target, path.parent)).as_posix()})"
                for target in linked_files
            ), encoding="utf-8")

        with patch.object(install, "__file__", str(source / "install.py")):
            for runtime, adapter in install.ADAPTERS.items():
                destination = install.install(runtime, self.parent / runtime)
                for path in destination.rglob("*.md"):
                    text = path.read_text(encoding="utf-8")
                    for target in linked_files:
                        link = Path(os.path.relpath(destination / target, path.parent)).as_posix()
                        with self.subTest(runtime=runtime, path=path, target=target):
                            if target == adapter:
                                self.assertIn(f"]({link})", text)
                            else:
                                self.assertIn(f"]({install.REPOSITORY_FILES}{target})", text)
                                self.assertNotIn(f"]({link})", text)
                                self.assertFalse((destination / target).exists())

    def test_main_installs_using_explicit_destination(self):
        result, stdout, stderr = self.cli()
        self.assertEqual(result, 0)
        self.assertIn("installed /based", stdout)
        self.assertEqual(stderr, "")
        self.assertTrue((self.destination / "SKILL.md").is_file())

    def test_existing_directory_or_file_is_preserved_without_upgrade(self):
        self.destination.parent.mkdir(parents=True)
        for kind in ("empty directory", "directory", "file"):
            with self.subTest(kind=kind):
                if kind == "file":
                    self.destination.write_text("keep", encoding="utf-8")
                else:
                    self.destination.mkdir()
                    if kind == "directory":
                        (self.destination / "keep.txt").write_text("keep", encoding="utf-8")
                with self.assertRaisesRegex(FileExistsError, "--upgrade"):
                    install.install("hermes", self.destination)
                self.assertTrue(self.destination.exists())
                if kind == "file":
                    self.assertEqual(self.destination.read_text(encoding="utf-8"), "keep")
                    self.destination.unlink()
                else:
                    if kind == "directory":
                        self.assertEqual((self.destination / "keep.txt").read_text(encoding="utf-8"), "keep")
                        (self.destination / "keep.txt").unlink()
                    self.destination.rmdir()

    def test_dry_run_lists_payload_and_does_not_create_parents(self):
        result, stdout, stderr = self.cli("--dry-run")
        self.assertEqual(result, 0)
        self.assertEqual(stderr, "")
        written = [line for line in stdout.splitlines() if line.startswith("would write ")]
        self.assertEqual(len(written), 6)
        self.assertIn(str(self.destination / "adapters/claude-code.md"), stdout)
        self.assertNotIn("adapters/hermes.md", stdout)
        self.assertNotIn("references/evaluation.md", stdout)
        self.assertEqual(list(self.parent.iterdir()), [])

    def test_dry_run_keeps_existing_install_and_requires_upgrade(self):
        marker = self.existing_install()
        self.assertEqual(self.cli("--dry-run")[0], 1)
        result, stdout, stderr = self.cli("--upgrade", "--dry-run")
        self.assertEqual(result, 0)
        self.assertEqual(stderr, "")
        self.assertIn("would back up", stdout)
        self.assertEqual(marker.read_text(encoding="utf-8"), "preserve local changes")
        self.assertEqual(list(self.destination.parent.glob("based.bak-*")), [])

    def test_upgrade_and_force_back_up_old_install_before_replacing(self):
        for flag in ("--upgrade", "--force"):
            with self.subTest(flag=flag):
                marker = self.existing_install() if not self.destination.exists() else self.destination / "user-notes.txt"
                marker.write_text("preserve local changes", encoding="utf-8")
                (self.destination / "references/evaluation.md").write_text("old maintainer material", encoding="utf-8")
                before = set(self.destination.parent.glob("based.bak-*"))
                result, stdout, stderr = self.cli(flag)
                self.assertEqual((result, stderr), (0, ""))
                backups = set(self.destination.parent.glob("based.bak-*")) - before
                self.assertEqual(len(backups), 1)
                backup = backups.pop()
                self.assertRegex(backup.name, r"^based\.bak-\d{8}-\d{6}-\d{6}$")
                self.assertEqual((backup / marker.name).read_text(encoding="utf-8"), "preserve local changes")
                self.assertTrue((backup / "references/evaluation.md").is_file())
                self.assertFalse(marker.exists())
                self.assertFalse((self.destination / "references/evaluation.md").exists())
                self.assertFalse((self.destination / "adapters/hermes.md").exists())
                self.assertTrue((self.destination / "adapters/claude-code.md").is_file())
                self.assertIn(str(backup), stdout)

    def test_upgrade_missing_destination_installs_without_backup(self):
        self.assertEqual(self.cli("--upgrade")[0], 0)
        self.assertTrue(self.destination.is_dir())
        self.assertEqual(list(self.destination.parent.glob("based.bak-*")), [])

    def test_upgrade_refuses_existing_file(self):
        self.destination.parent.mkdir(parents=True)
        self.destination.write_text("keep", encoding="utf-8")
        result, _, stderr = self.cli("--upgrade")
        self.assertEqual(result, 1)
        self.assertIn("not a directory", stderr)
        self.assertEqual(self.destination.read_text(encoding="utf-8"), "keep")

    def test_backup_failure_preserves_old_install_and_removes_staging(self):
        marker = self.existing_install()
        with patch.object(Path, "rename", side_effect=PermissionError("cannot back up")):
            result, _, stderr = self.cli("--upgrade")
        self.assertEqual(result, 1)
        self.assertIn("cannot back up", stderr)
        self.assertTrue(marker.is_file())
        self.assertEqual(list(self.destination.parent.iterdir()), [self.destination])

    def test_copy_failure_preserves_old_install_without_backup_or_staging(self):
        marker = self.existing_install()
        with patch.object(install.shutil, "copy2", side_effect=OSError("interrupted copy")):
            self.assertEqual(self.cli("--upgrade")[0], 1)
        self.assertEqual(marker.read_text(encoding="utf-8"), "preserve local changes")
        self.assertEqual(list(self.destination.parent.iterdir()), [self.destination])

    def test_failed_move_rolls_back_fresh_install_and_upgrade(self):
        original_move = install.shutil.move
        for upgrade in (False, True):
            with self.subTest(upgrade=upgrade):
                marker = self.existing_install() if upgrade else None
                calls = []

                def fail_after_first_move(source, target):
                    calls.append(source)
                    if len(calls) == 2:
                        raise OSError("synthetic interrupted install")
                    return original_move(source, target)

                with patch.object(install.shutil, "move", side_effect=fail_after_first_move), redirect_stdout(StringIO()):
                    with self.assertRaisesRegex(OSError, "synthetic interrupted install"):
                        install.install("claude", self.destination, upgrade=upgrade)
                if upgrade:
                    self.assertEqual(marker.read_text(encoding="utf-8"), "preserve local changes")
                    self.assertTrue((self.destination / "adapters/hermes.md").is_file())
                else:
                    self.assertFalse(self.destination.exists())
                self.assertEqual(list(self.destination.parent.iterdir()), [self.destination] if upgrade else [])

    def test_uninstall_removes_install_but_keeps_backups(self):
        self.existing_install()
        self.assertEqual(self.cli("--upgrade")[0], 0)
        backup = next(self.destination.parent.glob("based.bak-*"))
        result, stdout, stderr = self.cli("--uninstall")
        self.assertEqual((result, stderr), (0, ""))
        self.assertIn("uninstalled /based", stdout)
        self.assertFalse(self.destination.exists())
        self.assertTrue((backup / "user-notes.txt").is_file())

    def test_uninstall_dry_run_keeps_install(self):
        marker = self.existing_install()
        result, stdout, stderr = self.cli("--uninstall", "--dry-run")
        self.assertEqual((result, stderr), (0, ""))
        self.assertIn("would remove", stdout)
        self.assertTrue(marker.is_file())

    def test_uninstall_refuses_missing_or_unmarked_directory(self):
        for exists in (False, True):
            with self.subTest(exists=exists):
                if exists:
                    self.destination.mkdir(parents=True)
                result, _, stderr = self.cli("--uninstall")
                self.assertEqual(result, 1)
                self.assertIn("no regular SKILL.md", stderr)
                self.assertEqual(self.destination.exists(), exists)

    def test_refuses_symlink_destination_and_symlink_skill_marker(self):
        real = self.parent / "real"
        real.mkdir()
        (real / "SKILL.md").write_text("keep", encoding="utf-8")
        self.destination.parent.mkdir(parents=True)
        for target in (real, self.parent / "missing"):
            self.destination.symlink_to(target, target_is_directory=True)
            for flag in ("--upgrade", "--uninstall"):
                self.assertEqual(self.cli(flag)[0], 1)
            self.assertTrue(self.destination.is_symlink())
            self.destination.unlink()
        self.destination.mkdir()
        (self.destination / "SKILL.md").symlink_to(real / "SKILL.md")
        self.assertEqual(self.cli("--uninstall")[0], 1)
        self.assertEqual((real / "SKILL.md").read_text(encoding="utf-8"), "keep")

    def test_source_repository_cannot_be_upgraded_or_uninstalled(self):
        source = Path(install.__file__).resolve().parent
        for destination in (source, source / "tests/..", source.parent):
            for kwargs in ({"upgrade": True}, {"uninstall": True}):
                with self.subTest(destination=destination, kwargs=kwargs):
                    with self.assertRaisesRegex(ValueError, "source repository"):
                        install.install("claude", destination, **kwargs)

    def test_expected_filesystem_errors_are_one_line_without_tracebacks(self):
        for error in (FileNotFoundError("missing target parent"), PermissionError("permission denied\nextra detail")):
            with self.subTest(error=error), patch.object(Path, "mkdir", side_effect=error):
                result, stdout, stderr = self.cli()
                self.assertEqual(result, 1)
                self.assertEqual(stdout, "")
                self.assertEqual(len(stderr.splitlines()), 1)
                self.assertNotIn("Traceback", stderr)
                self.assertIn(str(error).splitlines()[0], stderr)
        self.assertEqual(list(self.parent.iterdir()), [])

    def test_parent_that_is_a_file_has_clean_error(self):
        self.destination.parent.parent.mkdir(parents=True)
        self.destination.parent.write_text("keep parent", encoding="utf-8")
        result, _, stderr = self.cli()
        self.assertEqual(result, 1)
        self.assertEqual(len(stderr.splitlines()), 1)
        self.assertNotIn("Traceback", stderr)
        self.assertEqual(self.destination.parent.read_text(encoding="utf-8"), "keep parent")

    def test_missing_source_is_reported_before_any_write(self):
        with patch.object(Path, "is_file", return_value=False):
            result, _, stderr = self.cli()
        self.assertEqual(result, 1)
        self.assertIn("missing safe-install source file", stderr)
        self.assertEqual(list(self.parent.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
