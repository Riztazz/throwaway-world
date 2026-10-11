"""Query and maintain a world's index, ledger and baseline.

Run from the world folder, or pass --world PATH before the command. `search` is for "does this already exist?" before inventing anything;
`snapshot` is only for a checkpoint the user approved.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worlddesign.cli import add_subcommand, make_parser, parse, resolve_root  # noqa: E402
from worlddesign.entryfacts import refresh_entry  # noqa: E402
from worlddesign.ledger import BASELINE_REL, consume_authorizations, build_decisions_index, load_baseline, load_decisions, write_stale  # noqa: E402
from worlddesign.search import search  # noqa: E402
from worlddesign.review_packet import PACKET_REL, build_review_packet  # noqa: E402
from worlddesign.summary import SUMMARY_REL, build_session_summary  # noqa: E402
from worlddesign.textio import write_text  # noqa: E402
from worlddesign.world import World, build_index, load_world, page_hash_snapshot  # noqa: E402
from worlddesign.textio import use_utf8  # noqa: E402


def _page(world: World, name: str):
    file = name if name.endswith(".md") else f"{name}.md"
    if file not in world.pages:
        raise ValueError(f"{name}: not a page in manifest.json")
    return world.pages[file]


def build_parser():
    parser = make_parser("canon_index.py", __doc__)
    sub = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")
    add_subcommand(sub, "index", help="write INDEX.md (pages, types, status, summaries, links in/out) and ledger/last-session.md")
    p = add_subcommand(sub, "summary", help="write ledger/last-session.md: what changed, open proposals and decisions, stories in progress")
    p.add_argument("--print", action="store_true", help="print it instead of writing the file")
    p = add_subcommand(sub, "review-packet", help="write work/review-packet.md for a read-only reviewer: changed pages, neighbours, facts, decisions, a checklist")
    p.add_argument("--pages", help="comma-separated page files (default: the pages changed since the checkpoint)")
    p.add_argument("--print", action="store_true", help="print it instead of writing the file")
    add_subcommand(sub, "entry", help="refresh the generated \"This world\" block in AGENTS.md from the world's files")
    add_subcommand(sub, "decisions", help="write decisions/INDEX.md")
    for name, text in (("links-to", "pages that link to PAGE (its dependents)"), ("links-from", "pages PAGE links to"),
                       ("show", "name, type, status, summary, headings and facts of one page")):
        add_subcommand(sub, name, help=text).add_argument("page")
    add_subcommand(sub, "facts", help="list ::key:: value fact lines across pages").add_argument("--key", help="only this fact key")
    p = add_subcommand(sub, "search", help="keyword search (case and accent insensitive; every word must match) over pages, facts, decisions and the log: use it before inventing")
    p.add_argument("term", nargs="+", help="the words to find")
    p.add_argument("--type", default="", help="only pages of this type")
    p.add_argument("--status", default="", help="only pages with this status")
    p.add_argument("--limit", type=int, default=20, help="at most this many hits")
    add_subcommand(sub, "stale", help="write ledger/stale.md from changes to protected pages; exit 1 if items are open")
    add_subcommand(sub, "snapshot", help="write ledger/page-hashes.json. Run ONLY at a checkpoint the user approved: it becomes the baseline")
    return parser


def main(argv: list[str]) -> int:
    use_utf8()
    args = parse(build_parser(), argv)
    if isinstance(args, int):
        return args
    root, command = resolve_root(args.world), args.command
    try:
        world = load_world(root)
        if command == "index":
            write_text(root / "INDEX.md", build_index(world))
            write_text(root / SUMMARY_REL, build_session_summary(world))
            refresh_entry(root)
            print(f"INDEX.md written ({len(world.pages)} pages); {SUMMARY_REL} refreshed")
        elif command == "entry":
            print("AGENTS.md facts block refreshed" if refresh_entry(root) else "AGENTS.md facts block is up to date (or has no block)")
        elif command == "summary":
            text = build_session_summary(world)
            if args.print:
                sys.stdout.write(text)
            else:
                write_text(root / SUMMARY_REL, text)
                print(f"{SUMMARY_REL} written")
        elif command == "review-packet":
            text = build_review_packet(world, args.pages.split(",") if args.pages else None)
            if args.print:
                sys.stdout.write(text)
            else:
                write_text(root / PACKET_REL, text)
                print(f"{PACKET_REL} written. Hand it to a read-only reviewer; the reviewer writes nothing.")
        elif command == "decisions":
            write_text(root / "decisions" / "INDEX.md", build_decisions_index(load_decisions(root), root))
            print("decisions/INDEX.md written")
        elif command == "links-to":
            for file in world.reverse_links()[_page(world, args.page).file]:
                print(file)
        elif command == "links-from":
            for file in _page(world, args.page).page_links():
                print(file)
        elif command == "facts":
            for file, page in world.pages.items():
                for k, v, _ in page.facts:
                    if args.key is None or k == args.key:
                        print(f"{file}\t{k}\t{v}")
        elif command == "search":
            found = search(world, " ".join(args.term), args.type, args.status, args.limit)
            for hit in found:
                print(hit)
            if not found:
                print("no match: nothing in the pages, decisions or log mentions it")
        elif command == "show":
            page = _page(world, args.page)
            print(json.dumps({
                "file": page.file, "name": page.name, "type": page.type_key, "status": page.status,
                "summary": page.summary, "headings": [h[1] for h in page.headings if h[0] == 2],
                "facts": page.fact_map(), "links_to": page.page_links(),
                "linked_from": world.reverse_links()[page.file],
            }, indent=2, ensure_ascii=False))
        elif command == "stale":
            open_count = write_stale(world, load_baseline(root))
            print(f"ledger/stale.md written; {open_count} open item(s)")
            return 1 if open_count else 0
        elif command == "snapshot":
            write_text(root / BASELINE_REL, json.dumps(consume_authorizations(root, page_hash_snapshot(world, date.today().isoformat())), indent=2, ensure_ascii=False) + "\n")
            print(f"{BASELINE_REL} written for {len(world.pages)} pages. This is now the baseline; only do this at a user-approved checkpoint.")
    except (OSError, ValueError, IndexError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
