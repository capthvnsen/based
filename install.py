"""Safe, optional installer for the portable /based skill."""

import argparse
import os
from pathlib import Path
import shutil
import tempfile
from typing import Union


INSTALL_FILES = (
    "SKILL.md",
    "adapters/hermes.md",
    "adapters/claude-code.md",
    "references/evaluation.md",
    "references/model-routing.md",
    "references/panel.md",
    "references/reviewer.md",
    "references/voice.md",
)


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
    parser.add_argument("--runtime", choices=("hermes", "claude"), required=True)
    parser.add_argument("--dest", type=Path)
    return parser


def install(runtime: str, destination: Union[Path, str]) -> Path:
    if runtime not in {"hermes", "claude"}:
        raise ValueError(f"unsupported runtime: {runtime}")

    source_root = Path(__file__).resolve().parent
    destination = Path(destination).expanduser()
    if os.path.lexists(destination):
        raise FileExistsError(f"refusing to overwrite existing destination: {destination}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{destination.name}.", dir=destination.parent))
    destination_created = False
    try:
        for relative in INSTALL_FILES:
            source = source_root / relative
            if not source.is_file() or source.is_symlink():
                raise FileNotFoundError(f"missing safe-install source file: {relative}")
            target = staging / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

        destination.mkdir()
        destination_created = True
        for child in staging.iterdir():
            shutil.move(str(child), destination / child.name)
        staging.rmdir()
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        if destination_created and destination.is_dir() and not any(destination.iterdir()):
            destination.rmdir()
        raise
    return destination


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    destination = args.dest or default_destination(args.runtime)
    try:
        installed = install(args.runtime, destination)
    except (FileExistsError, FileNotFoundError, OSError) as exc:
        parser.error(str(exc))
    print(f"installed /based for {args.runtime} at {installed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
