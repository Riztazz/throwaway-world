"""SessionStart hook: print a small context block for Claude Code (JSON on stdout).

Injects only what must be fresh in every session: the rules pointer, the ask-the-mode-first
reminder, and the open questions in decisions/INBOX.md. It does NOT inject INDEX.md (that grows
with the world; agents query it). Output stays far below the 10,000-character hook limit.

Usage (from .claude/settings.json):  py -3 "$CLAUDE_PROJECT_DIR/.world-design/library/tools/session_context.py"
Finds the world root by walking up from the current directory to the nearest manifest.json.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worlddesign.paths import hook_root  # noqa: E402
from worlddesign.textio import use_utf8  # noqa: E402

MAX_INBOX_CHARS = 2400
MAX_SUMMARY_CHARS = 2200
RULES = ".world-design/library/rules/INVENTION.md"


def build_context(root: Path | None) -> str:
    lines = [
        "WORLD PROJECT RULES (loaded by the SessionStart hook).",
        f"- Before any narrative task, ask the user for the task mode: explore, extend, edit or lock. Do not infer it. Rules: {RULES}.",
        "- New deliverable: interview first, in facts, function, cost and history. Never ask the user to picture or imagine.",
        "- Only the user marks anything `accepted`. Protected pages need the user's explicit authorization to change.",
        "- Look in INDEX.md before inventing; reuse what exists. Subagents return questions to the coordinator.",
    ]
    if root is None:
        lines.append("- No manifest.json found above the current folder: this is not a world project root.")
        return "\n".join(lines)
    inbox = root / "decisions" / "INBOX.md"
    items: list[str] = []
    if inbox.is_file():
        for raw in inbox.read_text(encoding="utf-8-sig").replace("\r\n", "\n").split("\n"):
            line = raw.strip()
            if re.match(r"^D-\d{4}\b", line):
                items.append(line)
    if items:
        lines.append(f"OPEN QUESTIONS WAITING FOR THE USER ({len(items)}):")
        budget = MAX_INBOX_CHARS
        shown = 0
        for line in items:
            if len(line) + 3 > budget:
                break
            lines.append(f"- {line}")
            budget -= len(line) + 3
            shown += 1
        if shown < len(items):
            lines.append(f"- ... {len(items) - shown} more in decisions/INBOX.md")
        lines.append("Do not work on pages these questions are blocking until the user answers.")
    else:
        lines.append("No open questions in decisions/INBOX.md.")
    try:  # the summary is computed here, not written: a session start must not change the world's files
        from worlddesign.summary import build_session_summary
        from worlddesign.world import load_world
        text = build_session_summary(load_world(root)).split("\n", 4)[-1].strip()
        if len(text) > MAX_SUMMARY_CHARS:
            text = text[:MAX_SUMMARY_CHARS].rsplit("\n", 1)[0] + "\n- ... (more in ledger/last-session.md after `canon_index.py index`)"
        lines += ["", "WHERE WE LEFT OFF (generated from the ledger):", text]
    except Exception:  # noqa: BLE001 - a summary problem must never break the session start
        pass
    return "\n".join(lines)


def main() -> int:
    use_utf8()
    root = hook_root()
    payload = {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": build_context(root)}}
    sys.stdout.write(json.dumps(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
