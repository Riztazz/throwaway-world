"""UserPromptExpansion hook for the `/world-mode` command (Claude Code).

When the user types `/world-mode explore|extend|edit|lock`, record the mode for this session so the write guard can enforce it; `/world-mode off` removes it.
Other commands are ignored. Exit 2 with a message on stderr refuses the command (a bad mode, or the mode could not be
recorded, so the user does not believe a mode is enforced when it is not).

Usage (from .claude/settings.json): py -3 "$CLAUDE_PROJECT_DIR/.world-design/library/tools/mode_hook.py"
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worlddesign.mode import MODES, OFF_WORDS, clear_mode, write_mode  # noqa: E402
from worlddesign.paths import hook_root  # noqa: E402
from worlddesign.textio import use_utf8  # noqa: E402

COMMAND = "world-mode"  # specific on purpose: a bare `mode` could be shadowed by a personal skill or a built-in command


def main() -> int:
    use_utf8()
    try:
        data = json.load(sys.stdin)
        name = str(data.get("command_name") or "").rsplit(":", 1)[-1]
        if name != COMMAND:
            return 0
        words = str(data.get("command_args") or "").strip().lower().split()
        mode = words[0] if words else ""
        if mode not in MODES and mode not in OFF_WORDS:
            print(f"Usage: /world-mode {' | '.join(MODES)} | off", file=sys.stderr)
            return 2
        root = hook_root(data)
        if root is None:
            print("/world-mode works inside a world project (no manifest.json found above this folder).", file=sys.stderr)
            return 2
        if mode in OFF_WORDS:
            clear_mode(root, str(data.get("session_id") or ""))
        else:
            write_mode(root, str(data.get("session_id") or ""), mode)
    except Exception as error:
        print(f"/world-mode could not record the mode ({type(error).__name__}: {error}); it is not enforced.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
