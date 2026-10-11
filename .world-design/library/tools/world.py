"""One entry point for a world's command-line tools: `world.py COMMAND [options]`.

Every command is also available as its own script (`canon_lint.py`, `record.py`, ...); this just dispatches, so there is one thing to learn
and one `--help`. Commands that `canon_index.py` knows (index, entry, summary, decisions, links-to, links-from, facts, show, search,
stale, review-packet, snapshot) work here unchanged.

Examples:
    world.py search "weir stair"
    world.py record decision --title "Magic costs memory" --affects magic.md
    world.py lint            world.py finish            world.py new story harbour --form novel
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worlddesign.textio import use_utf8  # noqa: E402

# command -> (module, what it does). The module's `main(argv)` does the work.
COMMANDS = {
    "lint": ("canon_lint", "check the world against the import contract and the change rules"),
    "finish": ("finish_check", "the check to run before handing work back: lint plus what still needs the user"),
    "status": ("bootstrap_status", "where the bootstrap stands, and whether the pitch round may start"),
    "record": ("record", "write a decision, accept one, supersede one, or write a change record"),
    "new": ("new_item", "start a story, a series or a game-system spec from the templates"),
    "svg": ("svg_check", "check one SVG map against the handoff rules"),
    "batch": ("batch_draft", "bulk-draft short texts through the Message Batches API (plan, submit, collect)"),
    "context": ("context", "prepare or verify the context packet for one role"),
}
INDEX_COMMANDS = ("index", "entry", "summary", "decisions", "links-to", "links-from", "facts", "show", "search", "stale", "review-packet", "snapshot")
NO_WORLD_FLAG = ("svg", "context")  # these take their own --world / --project


def usage() -> str:
    width = max(len(c) for c in (*COMMANDS, *INDEX_COMMANDS))
    lines = ["usage: world.py [--world PATH] COMMAND [options]", "", "Run from the world folder, or give --world. `world.py COMMAND --help` shows a command's options.", "", "commands:"]
    lines += [f"  {name:<{width}}  {text}" for name, (_, text) in COMMANDS.items()]
    lines += [f"  {name:<{width}}  (canon_index.py) see `world.py {name} --help`" if name != "index" else f"  {name:<{width}}  refresh INDEX.md and the session summary" for name in INDEX_COMMANDS]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    use_utf8()
    world: list[str] = []
    args = list(argv)
    if len(args) >= 2 and args[0] == "--world":
        world, args = ["--world", args[1]], args[2:]
    if not args or args[0] in ("-h", "--help"):
        print(usage())
        return 0
    command, rest = args[0], args[1:]
    if command in COMMANDS:
        module = __import__(COMMANDS[command][0])
        return module.main((world if command not in NO_WORLD_FLAG else []) + rest) if command != "context" else _context(rest)
    if command in INDEX_COMMANDS:
        import canon_index
        return canon_index.main(world + args)
    print(f"world.py: unknown command {command!r}\n\n{usage()}", file=sys.stderr)
    return 2


def _context(rest: list[str]) -> int:
    from worlddesign.context import ContextError, run_project_context
    try:
        sys.stdout.buffer.write((run_project_context(rest, Path.cwd(), Path(__file__).resolve().parents[1]) + "\n").encode("utf-8"))
    except (ContextError, OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
