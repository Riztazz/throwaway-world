"""Read-only finish check: run it before handing work back (any provider, any mode, including lock).

    py -3 .world-design/library/tools/finish_check.py [WORLD_ROOT]

It runs the lint and lists what still needs the user: protected pages changed without a T3 record are lint errors; open or
proposed decisions (blocking ones marked), change records not yet accepted, story inventions still open, and dependents of
changed protected pages still to check. It writes nothing (refresh INDEX.md and ledger/last-session.md with
`canon_index.py index`). Exit 1 when the lint has errors, so a provider with no hooks (Codex) still has a backstop it can run.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worlddesign.cli import make_parser, parse, resolve_root  # noqa: E402
from worlddesign.ledger import as_list, compute_stale, load_baseline, load_changes, load_decisions  # noqa: E402
from worlddesign.lint import lint_world  # noqa: E402
from worlddesign.summary import story_lines  # noqa: E402
from worlddesign.textio import read_text  # noqa: E402
from worlddesign.world import load_world  # noqa: E402
from worlddesign.textio import use_utf8  # noqa: E402

MAX_WARNINGS = 15


def report(root: Path) -> tuple[str, int]:
    world = load_world(root)
    issues = lint_world(root, world)
    errors = [i for i in issues if i.level == "error"]
    warnings = [i for i in issues if i.level == "warning"]
    lines = [f"FINISH CHECK: {len(errors)} error(s), {len(warnings)} warning(s)"]
    lines += [f"  {i}" for i in errors]
    lines += [f"  {i}" for i in warnings[:MAX_WARNINGS]]
    if len(warnings) > MAX_WARNINGS:
        lines.append(f"  ... {len(warnings) - MAX_WARNINGS} more warning(s); run canon_lint.py for the full list")

    needs: list[str] = []
    for d in load_decisions(root):
        if not d.error and str(d.meta.get("status", "")) in ("open", "proposed"):
            block = " [blocking]" if d.meta.get("blocking") is True else ""
            needs.append(f"decision {d.meta.get('id', d.path)} ({d.meta.get('status')}){block}: affects {', '.join(as_list(d.meta.get('affects'))) or '-'}")
    for r in load_changes(root):
        if not r.error and str(r.meta.get("status", "")) in ("proposed", "integrated"):
            needs.append(f"change record {r.meta.get('id', r.path)} ({r.meta.get('tier', '?')}, {r.meta.get('status')}) is not accepted: {', '.join(as_list(r.meta.get('pages'))) or '-'}")
    needs += [f"story {line[2:]}" for line in story_lines(root)]
    try:
        baseline = load_baseline(root)
    except (OSError, ValueError):
        baseline = None
    stale = root / "ledger" / "stale.md"
    text, open_count = compute_stale(world, baseline, read_text(stale) if stale.is_file() else "")
    if open_count:
        needs.append(f"{open_count} dependent(s) of changed protected pages still to check (see ledger/stale.md after `canon_index.py stale`)")
    lines.append("")
    lines.append("STILL NEEDS THE USER:" if needs else "Nothing is waiting for the user.")
    lines += [f"  - {n}" for n in needs]
    lines.append("")
    lines.append("Not claimed accepted: only the user accepts. " + ("Fix the errors before you hand work back." if errors else "No lint errors."))
    return "\n".join(lines), len(errors)


def main(argv: list[str]) -> int:
    use_utf8()
    parser = make_parser("finish_check.py", __doc__, world=False)
    parser.add_argument("root", nargs="?", help="the world folder (default: the nearest folder above here with a manifest.json)")
    parser.add_argument("--world", help="the same as the positional folder")
    args = parse(parser, argv)
    if isinstance(args, int):
        return args
    root = resolve_root(args.root or args.world)
    try:
        text, errors = report(root)
    except (OSError, ValueError) as error:
        print(f"cannot check {root}: {error}", file=sys.stderr)
        return 2
    print(text)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
