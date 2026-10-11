"""Usage: py -3 tools/canon_lint.py [WORLD_ROOT] [--warnings-as-errors]

Checks a world folder (manifest.json + world/) against docs/WORLD-HANDOFF.md and the
mechanical rules in rules/INVENTION.md. Exit status 1 when any error is found.
WORLD_ROOT defaults to the current directory.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worlddesign.cli import make_parser, parse, resolve_root  # noqa: E402
from worlddesign.lint import lint_world  # noqa: E402
from worlddesign.textio import use_utf8  # noqa: E402


def main(argv: list[str]) -> int:
    use_utf8()
    parser = make_parser("canon_lint.py", __doc__, world=False)
    parser.add_argument("root", nargs="?", help="the world folder (default: the nearest folder above here with a manifest.json)")
    parser.add_argument("--world", help="the same as the positional folder")
    parser.add_argument("--warnings-as-errors", action="store_true", help="exit 1 on a warning too")
    args = parse(parser, argv)
    if isinstance(args, int):
        return args
    root = resolve_root(args.root or args.world)
    try:
        issues = lint_world(root)
    except (OSError, ValueError) as error:
        print(f"cannot lint {root}: {error}", file=sys.stderr)
        return 2
    for issue in issues:
        print(issue)
    errors = [i for i in issues if i.level == "error" or args.warnings_as_errors]
    print(f"{len([i for i in issues if i.level == 'error'])} error(s), {len([i for i in issues if i.level == 'warning'])} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
