"""Usage: py -3 tools/svg_check.py MAP.svg [--world ROOT --map SVG_FILE_NAME]

Checks one SVG against the STUDIO handoff rules. With --world and --map it also
cross-checks the manifest row's `places` keys. Exit status 1 when any error is found.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worlddesign.cli import fail, make_parser, parse  # noqa: E402
from worlddesign.svgcheck import check_svg  # noqa: E402
from worlddesign.textio import use_utf8  # noqa: E402


def main(argv: list[str]) -> int:
    use_utf8()
    parser = make_parser("svg_check.py", __doc__, world=False)
    parser.add_argument("svg", help="the SVG file to check")
    parser.add_argument("--world", metavar="ROOT", help="also cross-check the manifest row's `places` keys in this world")
    parser.add_argument("--map", help="the map row's svg file name in manifest.json (default: the SVG's own file name)")
    args = parse(parser, argv)
    if isinstance(args, int):
        return args
    if args.map and not args.world:
        return fail("--map needs --world")
    svg = Path(args.svg)
    places = None
    if args.world:
        manifest = json.loads((Path(args.world) / "manifest.json").read_bytes().decode("utf-8-sig"))
        name = args.map or svg.name
        row = next((m for m in manifest.get("maps", []) if m.get("svg") == name), None)
        if row is None:
            return fail(f"no map row for {name} in manifest.json")
        places = row.get("places") or {}
    issues = check_svg(svg, places)
    for issue in issues:
        print(issue)
    count = len([i for i in issues if i.level == "error"])
    print(f"{count} error(s), {len(issues) - count} warning(s)")
    return 1 if count else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
