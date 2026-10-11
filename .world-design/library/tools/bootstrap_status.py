"""Where the bootstrap stands, and whether the pitch round may start (read-only, any provider).

    py -3 .world-design/library/tools/bootstrap_status.py [WORLD_ROOT] [--strict]

Lists what the bootstrap wrote and what still waits for your approval (the reference map, voice.md, the exemplars), derived
from the files. `--strict` exits 1 when the world is not ready for the pitch round.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worlddesign.bootstrap_state import build_state  # noqa: E402
from worlddesign.cli import make_parser, parse, resolve_root  # noqa: E402
from worlddesign.textio import use_utf8  # noqa: E402


def main(argv: list[str]) -> int:
    use_utf8()
    parser = make_parser("bootstrap_status.py", __doc__, world=False)
    parser.add_argument("root", nargs="?", help="the world folder (default: the nearest folder above here with a manifest.json)")
    parser.add_argument("--world", help="the same as the positional folder")
    parser.add_argument("--strict", action="store_true", help="exit 1 while anything still waits for the user's approval")
    args = parse(parser, argv)
    if isinstance(args, int):
        return args
    root = resolve_root(args.root or args.world)
    if not (root / "manifest.json").is_file():
        print(f"{root} is not a world folder (no manifest.json)", file=sys.stderr)
        return 2
    text, blockers = build_state(root)
    print(text)
    return 1 if blockers and args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
