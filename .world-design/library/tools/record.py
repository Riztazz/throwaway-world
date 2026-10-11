"""Write decisions and change records the right way (any provider).

    py -3 .world-design/library/tools/record.py decision --type creative --status proposed --title "Magic costs memory" --affects magic.md [--blocking] [--authority "the user's exact words"] [--why "..."]
    py -3 .world-design/library/tools/record.py accept D-0004 --authority "the user's exact words"
    py -3 .world-design/library/tools/record.py supersede D-0004 --by D-0009
    py -3 .world-design/library/tools/record.py change --mode edit --tier T2 --pages gate.md --dependents keep.md --summary "..." [--authority "..."] [--role fiction-writer]

Gives the next free id, the frontmatter the lint expects, the inbox line for an open question and a refreshed decisions/INDEX.md.
`accepted` decisions and T3 records need the user's exact words in --authority: only the user accepts, and the tool cannot
check that the words are theirs. Run it from the world folder.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worlddesign.cli import add_subcommand, CliError, fail, make_parser, parse, require_world  # noqa: E402
from worlddesign.records import RecordError, accept, new_change, new_decision, supersede  # noqa: E402
from worlddesign.textio import use_utf8  # noqa: E402


def _split(text: str) -> list[str]:
    return [p.strip() for p in text.split(",") if p.strip()]


def build_parser():
    parser = make_parser("record.py", __doc__)
    sub = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")
    p = add_subcommand(sub, "decision", help="write a decision (an open question also goes in decisions/INBOX.md)")
    p.add_argument("--type", default="creative", help="creative, project or question (default creative)")
    p.add_argument("--status", default="proposed", help="open, proposed, accepted or rejected (default proposed)")
    p.add_argument("--title", default="", help="one line")
    p.add_argument("--affects", default="", help="comma-separated page files")
    p.add_argument("--blocking", action="store_true", help="the question blocks work until answered")
    p.add_argument("--authority", default="", help="the user's exact words (required for accepted)")
    p.add_argument("--why", default="", help="one or two sentences")
    p = add_subcommand(sub, "accept", help="accept a decision with the user's exact words")
    p.add_argument("id", help="for example D-0004")
    p.add_argument("--authority", default="", help="the user's exact words (required)")
    p = add_subcommand(sub, "supersede", help="mark a decision superseded by another")
    p.add_argument("id")
    p.add_argument("--by", required=True, help="the decision that replaces it")
    p = add_subcommand(sub, "change", help="write a change record")
    p.add_argument("--mode", default="", help="explore, extend, edit or lock")
    p.add_argument("--tier", default="", help="T1b, T2 or T3")
    p.add_argument("--pages", default="", help="comma-separated page files changed")
    p.add_argument("--dependents", default="", help="comma-separated page files that depend on them")
    p.add_argument("--summary", default="", help="at most five lines")
    p.add_argument("--authority", default="", help="the user's exact words (required for T3 and accepted)")
    p.add_argument("--status", default="proposed", help="proposed, integrated, accepted or rejected")
    p.add_argument("--role", default="", help="the role that made the change")
    return parser


def main(argv: list[str]) -> int:
    use_utf8()
    args = parse(build_parser(), argv)
    if isinstance(args, int):
        return args
    try:
        root = require_world(args.world)
        if args.command == "decision":
            path = new_decision(root, args.type, args.status, args.title, _split(args.affects), args.blocking, args.authority, args.why)
            print(f"wrote {path.relative_to(root).as_posix()}")
        elif args.command == "accept":
            print(f"accepted {args.id}: {accept(root, args.id, args.authority).relative_to(root).as_posix()}")
        elif args.command == "supersede":
            print("updated " + ", ".join(p.relative_to(root).as_posix() for p in supersede(root, args.id, args.by)))
        else:
            path = new_change(root, args.mode, args.tier, _split(args.pages), args.summary, _split(args.dependents), args.authority, args.status, args.role)
            print(f"wrote {path.relative_to(root).as_posix()}")
    except (RecordError, CliError, OSError, ValueError) as error:
        return fail(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
