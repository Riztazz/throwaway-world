"""PostToolUse hook for Edit/Write/MultiEdit/NotebookEdit inside a world project (Claude Code).

After a write to a world file it runs the lint and hands the agent only the findings that concern what it just
touched: the file itself, the pages it links to or that link to it (its dependents), and any finding whose message
names the file (a fact conflict between two pages). The agent sees them in the same turn and can fix them before it
moves on, instead of after a whole session.

It never blocks (the write already happened) and never reports unrelated findings, so a world with old problems does
not nag on every edit. Any error fails open. Claude Code only; the lint (`canon_lint.py`) is the backstop for Codex.

Usage (from .claude/settings.json): py -3 "$CLAUDE_PROJECT_DIR/.world-design/library/tools/lint_feedback.py"
Reads the hook JSON on stdin. Exit 2 with the findings on stderr shows them to the agent; exit 0 is silent.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worlddesign.cache import ParseCache  # noqa: E402
from worlddesign.lint import lint_world  # noqa: E402
from worlddesign.policy import OVERRIDE_REL, Policy, PolicyError, load_policy  # noqa: E402
from worlddesign.world import World, load_world  # noqa: E402
from worlddesign.paths import hook_root  # noqa: E402
from worlddesign.textio import use_utf8  # noqa: E402

_LINE_SUFFIX = re.compile(r":\d+(?::\d+)?$")


def relative_target(root: Path, file_path: str, policy: Policy | None = None) -> str | None:
    """The edited file relative to the world root (posix), or None when it is not a file the lint covers."""
    target = Path(file_path)
    target = (root / target if not target.is_absolute() else target).resolve()
    try:
        rel = target.relative_to(root.resolve()).as_posix()
    except ValueError:
        return None
    watched = tuple((policy or load_policy(root))["feedback.watched_paths"])
    return rel if rel in ("manifest.json", "voice.md", OVERRIDE_REL) or rel.startswith(watched) else None


def related_pages(world: World, rel: str) -> set[str]:
    """Page files (world/<name>.md) the edited page links to or is linked from."""
    if not rel.startswith("world/") or not rel.endswith(".md"):
        return set()
    file = rel[len("world/"):]
    page = world.pages.get(file)
    related = {file}
    if page is not None:
        related |= {link.target.split("#")[0] for link in page.links}
    related |= {other.file for other in world.pages.values() if any(link.target.split("#")[0] == file for link in other.links)}
    return {f"world/{f}" for f in related}


def feedback(root: Path, file_path: str) -> str | None:
    try:
        policy, policy_error = load_policy(root), None
    except PolicyError as error:  # the lint reports it as L-POLICY; the hook keeps working with the defaults
        policy, policy_error = load_policy(None), error
    rel = relative_target(root, file_path, policy)
    if rel is None:
        return None
    if rel == OVERRIDE_REL:
        return f"Lint after your write to {rel}: error L-POLICY: {policy_error}. Fix it; until then the defaults apply." if policy_error else None
    max_shown = policy["feedback.max_shown"]
    needs_world = rel == "manifest.json" or rel.startswith("world/")
    try:
        cache = ParseCache(root) if needs_world else None  # pages whose bytes are unchanged are not parsed again
        world = load_world(root, cache=cache) if needs_world else None
        if cache is not None:
            cache.save()
        issues = lint_world(root, world, policy, [rel])  # only the checks that read this path
    except (ValueError, OSError) as error:  # the manifest is unreadable: say so, a silent hook hides the most useful message
        return (f"Lint could not run after your write to {rel}: {error}. Nothing is checked until manifest.json is valid UTF-8 JSON "
                "without a byte-order mark; fix it first.")
    if rel == "manifest.json":  # a manifest edit can change what any page means (status, type): show every error it left behind
        errors = [i for i in issues if i.level == "error"]
        if not errors:
            return None
        lines = [f"Lint after your write to manifest.json: {len(errors)} error(s)."]
        lines += [f"- {i.level} {i.code} {i.where}: {i.message}" for i in errors[:max_shown]]
        if len(errors) > max_shown:
            lines.append(f"- ... {len(errors) - max_shown} more; run canon_lint.py for the full list.")
        lines.append("Fix errors now.")
        return "\n".join(lines)
    scope = (related_pages(world, rel) if world is not None else set()) | {rel}
    names_me = re.compile(r"(?<![\w-])" + re.escape(rel.rsplit("/", 1)[-1]) + r"(?![\w-])")  # the whole file name: `port.md` is not in `harbour-port.md`
    mine, near = [], []
    for issue in issues:
        where = _LINE_SUFFIX.sub("", issue.where)
        if where == rel or names_me.search(issue.message):
            mine.append(issue)
        elif where in scope:
            near.append(issue)
    shown = (mine + near)[:max_shown]
    if not shown:
        return None
    lines = [f"Lint after your write to {rel}: {len(mine)} finding(s) in this file, {len(near)} in pages it links to or that link to it."]
    lines += [f"- {i.level} {i.code} {i.where}: {i.message}" for i in shown]
    if len(mine) + len(near) > len(shown):
        lines.append(f"- ... {len(mine) + len(near) - len(shown)} more; run canon_lint.py for the full list.")
    lines.append("Fix errors now. A warning about a missing change record or summary can wait until the edit is finished, but not past the end of the task.")
    return "\n".join(lines)


def main() -> int:
    use_utf8()
    try:
        data = json.load(sys.stdin)
        tool_input = data.get("tool_input") or {}
        file_path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
        if not file_path:
            return 0
        root = hook_root(data)
        if root is None:
            return 0
        text = feedback(root, file_path)
    except Exception as error:  # fail open
        print(f"lint_feedback: skipped ({type(error).__name__}: {error})", file=sys.stderr)
        return 0
    if text:
        print(text, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
