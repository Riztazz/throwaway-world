"""Create a story, a series or a system spec from the world's templates.

    py -3 .world-design/library/tools/new_item.py story SLUG [--form short|novella|novel] [--series S --book N]
    py -3 .world-design/library/tools/new_item.py series SLUG
    py -3 .world-design/library/tools/new_item.py system SLUG

Fills the frontmatter (id, title, form, created, series), never overwrites, and prints the next steps. Run from the world folder.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worlddesign.cli import add_subcommand, CliError, fail, make_parser, parse, require_world  # noqa: E402
from worlddesign.newitem import NewItemError, new_series, new_story, new_system  # noqa: E402
from worlddesign.textio import use_utf8  # noqa: E402


def build_parser():
    parser = make_parser("new_item.py", __doc__)
    sub = parser.add_subparsers(dest="kind", required=True, metavar="KIND")
    p = add_subcommand(sub, "story", help="a story folder under drafts/stories/")
    p.add_argument("slug")
    p.add_argument("--form", default="short", help="short, novella or novel (default short)")
    p.add_argument("--series", default="", help="the series this story belongs to")
    p.add_argument("--book", default="", help="its book number in the series")
    add_subcommand(sub, "series", help="a series folder under drafts/series/").add_argument("slug")
    add_subcommand(sub, "system", help="a game systems spec under design/systems/").add_argument("slug")
    return parser


def main(argv: list[str]) -> int:
    use_utf8()
    args = parse(build_parser(), argv)
    if isinstance(args, int):
        return args
    try:
        root = require_world(args.world)
        if args.kind == "story":
            out = new_story(root, args.slug, args.form, args.series, args.book)
        elif args.kind == "series":
            out = new_series(root, args.slug)
        else:
            out = new_system(root, args.slug)
    except (NewItemError, CliError, OSError) as error:
        return fail(str(error))
    print(f"created {out[0]}")
    for note in out[1:]:
        print(f"  next: {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
