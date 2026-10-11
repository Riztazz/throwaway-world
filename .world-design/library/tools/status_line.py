"""Claude Code status line for a world project: the world's name, the task mode set with /world-mode, and open decisions.

Claude Code runs it after each exchange with a JSON object on stdin (it carries `session_id` and `cwd`) and shows the first
line of stdout. It reads files only and never fails loudly: any error prints nothing. To turn it off, set `statusLine` to
something else in `.claude/settings.local.json`.

Usage (from .claude/settings.json): py -3 "$CLAUDE_PROJECT_DIR/.world-design/library/tools/status_line.py"
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worlddesign.ledger import load_decisions  # noqa: E402
from worlddesign.mode import read_mode  # noqa: E402
from worlddesign.paths import hook_root  # noqa: E402
from worlddesign.textio import use_utf8  # noqa: E402


def build_line(root: Path, session_id: str) -> str:
    try:
        name = str(json.loads((root / ".world-design" / "world.json").read_text(encoding="utf-8")).get("name") or root.name)
    except (OSError, ValueError):
        name = root.name
    mode = read_mode(root, session_id)
    open_items = [d for d in load_decisions(root) if not d.error and str(d.meta.get("status", "")) in ("open", "proposed")]
    blocking = sum(1 for d in open_items if d.meta.get("blocking") is True)
    decisions = "no open decisions" if not open_items else f"{len(open_items)} open decision(s)" + (f", {blocking} blocking" if blocking else "")
    return f"{name} | mode: {mode or 'not set (/world-mode)'} | {decisions}"


def main() -> int:
    use_utf8()
    try:
        data = json.load(sys.stdin) if not sys.stdin.isatty() else {}
        root = hook_root(data)
        if root is not None:
            print(build_line(root, str(data.get("session_id") or "")))
    except Exception:  # a status line must never break the UI
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
