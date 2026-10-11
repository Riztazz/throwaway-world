"""One way to build a command line for the tools: argparse, an exact help text, a typo is an error.

The hand-rolled parsers that came before silently ignored a misspelt flag (`record.py decision --afects magic.md` wrote a decision
with no `affects`; `new_item.py story x --frm novel` made a short story). With argparse an unknown flag stops the command with exit 2
and the usage line, abbreviations are not accepted, and `--help` is generated.

    parser = make_parser("record.py", __doc__)
    args = parse(parser, argv)          # a Namespace, or an int exit code (0 after --help, 2 after a usage error)
    if isinstance(args, int):
        return args
    root = resolve_root(args.world)     # --world PATH, else the nearest folder above here with a manifest.json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .paths import find_world_root


class CliError(Exception):
    """A problem to report as `error: ...` with exit code 2."""


class Parser(argparse.ArgumentParser):
    """ArgumentParser that refuses abbreviated flags (`--titl` for `--title`), also in its sub-commands (they use this class too)."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("allow_abbrev", False)
        super().__init__(*args, **kwargs)


def make_parser(prog: str, doc: str, world: bool = True) -> argparse.ArgumentParser:
    text = (doc or "").strip()
    head, _, rest = text.partition("\n\n")
    if head.startswith("Usage:"):  # argparse prints its own usage line; keep any prose that followed ours
        head = "\n".join(head.split("\n")[1:]).strip() or None
        if rest == "" and head is None:
            rest = ""
    parser = Parser(prog=prog, description=head, epilog=rest or None, formatter_class=argparse.RawDescriptionHelpFormatter)
    if world:
        add_world_option(parser)
    return parser


def add_world_option(parser: argparse.ArgumentParser, suppress: bool = False) -> None:
    parser.add_argument("--world", metavar="PATH", default=argparse.SUPPRESS if suppress else None,
                        help="the world folder (default: the nearest folder above the current one that has a manifest.json)")


def add_subcommand(sub, name: str, help: str) -> argparse.ArgumentParser:
    """A sub-command that also accepts --world after its name (`record.py decision --title X --world PATH`)."""
    parser = sub.add_parser(name, help=help)
    add_world_option(parser, suppress=True)  # SUPPRESS: a value given before the command is not overwritten by the sub-command's default
    return parser


def parse(parser: argparse.ArgumentParser, argv: list[str]) -> argparse.Namespace | int:
    """Parse argv. Instead of exiting, return the exit code when argparse wants to stop (after --help or on a usage error)."""
    try:
        return parser.parse_args(argv)
    except SystemExit as stop:
        return int(stop.code or 0)


def resolve_root(explicit: str | None = None, start: Path | None = None) -> Path:
    """The world folder: the one named, else the nearest above `start` (default: the current folder), else the current folder itself
    (so a tool run outside a world reports its own "no manifest.json" message)."""
    if explicit:
        return Path(explicit)
    here = start or Path.cwd()
    return find_world_root(here) or here


def require_world(explicit: str | None = None, start: Path | None = None) -> Path:
    """Like resolve_root, but a folder without manifest.json is an error."""
    root = resolve_root(explicit, start)
    if not (root / "manifest.json").is_file():
        raise CliError("run this from a world folder (no manifest.json found here or above), or pass --world PATH")
    return root


def fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 2
