"""Safe, optional installer for the portable /based skill."""

import argparse
from datetime import datetime
import os
from pathlib import Path
import shutil
import sys
import tempfile
from typing import Union


ADAPTERS = {"hermes": "adapters/hermes.md", "claude": "adapters/claude-code.md"}
INSTALL_FILES = (
    "SKILL.md",
    *ADAPTERS.values(),
    "references/model-routing.md",
    "references/panel.md",
    "references/reviewer.md",
    "references/voice.md",
)
REPOSITORY_FILES = "https://github.com/capthvnsen/based/blob/main/"


def default_destination(runtime: str) -> Path:
    if runtime == "hermes":
        base = os.environ.get("HERMES_HOME") or (Path.home() / ".hermes")
    elif runtime == "claude":
        base = os.environ.get("CLAUDE_CONFIG_DIR") or (Path.home() / ".claude")
    else:
        raise ValueError(f"unsupported runtime: {runtime}")
    return Path(base).expanduser() / "skills" / "based"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install the /based skill safely.")
    parser.add_argument("--runtime", metavar="{hermes,claude}", required=True)
    parser.add_argument("--dest", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="show planned changes without writing")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--upgrade", "--force", action="store_true", help="back up an existing install before replacing it")
    action.add_argument("--uninstall", action="store_true", help="remove the selected install (backups remain)")
    return parser


def install(runtime: str, destination: Union[Path, str], *, upgrade=False,
            dry_run=False, uninstall=False) -> Path:
    if runtime not in ADAPTERS:
        raise ValueError(f"unsupported runtime: {runtime}")
    if upgrade and uninstall:
        raise ValueError("choose either upgrade or uninstall")

    source_root = Path(__file__).resolve().parent
    destination = Path(os.path.abspath(Path(destination).expanduser()))
    if destination.is_symlink():
        raise ValueError(f"refusing symlink destination: {destination}")
    if source_root.is_relative_to(destination.resolve()):
        raise ValueError(f"refusing to replace the source repository or its parent: {destination}")
    exists = os.path.lexists(destination)
    if uninstall:
        marker = destination / "SKILL.md"
        if not marker.is_file() or marker.is_symlink():
            raise ValueError(f"refusing uninstall: no regular SKILL.md at {destination}")
        if dry_run:
            print(f"would remove {destination}")
        else:
            shutil.rmtree(destination)
        return destination
    if exists and not upgrade:
        raise FileExistsError(f"destination exists: {destination}; use --upgrade (or --force) to back up and replace it")
    if exists and not destination.is_dir():
        raise ValueError(f"destination is not a directory: {destination}")

    files = tuple(path for path in INSTALL_FILES
                  if not path.startswith("adapters/") or path == ADAPTERS[runtime])
    for relative in files:
        source = source_root / relative
        if not source.is_file() or source.is_symlink():
            raise FileNotFoundError(f"missing safe-install source file: {relative}")
    backup = None
    if exists:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        backup = destination.with_name(f"{destination.name}.bak-{timestamp}")
    if dry_run:
        if backup:
            print(f"would back up {destination} to {backup}")
        for relative in files:
            print(f"would write {destination / relative}")
        return destination

    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{destination.name}.", dir=destination.parent))
    destination_created = False
    backed_up = False
    try:
        omitted = set(INSTALL_FILES) - set(files) | {"references/evaluation.md"}
        for relative in files:
            source = source_root / relative
            target = staging / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            text = target.read_text(encoding="utf-8")
            # Keep omitted maintainer/other-runtime links usable without shipping those files.
            for missing in omitted:
                link = Path(os.path.relpath(source_root / missing, source.parent)).as_posix()
                text = text.replace(f"]({link})", f"]({REPOSITORY_FILES}{missing})")
            target.write_text(text, encoding="utf-8")

        if backup:
            destination.rename(backup)
            backed_up = True
        destination.mkdir()
        destination_created = True
        for child in staging.iterdir():
            shutil.move(str(child), destination / child.name)
        staging.rmdir()
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        if destination_created:
            # Only remove the partial install created by this invocation.
            shutil.rmtree(destination)
        if backed_up:
            backup.rename(destination)
        raise
    if backup:
        print(f"backed up existing install to {backup}")
    return destination


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        destination = args.dest or default_destination(args.runtime)
        installed = install(args.runtime, destination, upgrade=args.upgrade,
                            dry_run=args.dry_run, uninstall=args.uninstall)
    except (OSError, ValueError) as exc:
        print(f"error: {' '.join(str(exc).splitlines())}", file=sys.stderr)
        return 1
    if not args.dry_run:
        action = "uninstalled" if args.uninstall else "installed"
        print(f"{action} /based for {args.runtime} at {installed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
