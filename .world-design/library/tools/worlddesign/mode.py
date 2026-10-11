"""The task mode a user has set for a Claude Code session with `/world-mode` (explore, extend, edit or lock).

Only the user can set it: the `UserPromptExpansion` hook (tools/mode_hook.py) records it when the user types
`/world-mode <mode>`, and no tool the agent has writes it. It is keyed by session id so a stale mode never leaks into a
later session, and a missing file means "not enforced", never "deny". The write guard reads it.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

MODES = ("explore", "extend", "edit", "lock")
OFF_WORDS = ("off", "none", "clear")  # `/world-mode off` removes the mode: nothing is enforced
STATE_DIR = ".world-design/state"

# What each mode lets a write do, by kind of path. `work/` (the scratch area) is always writable and is not in the table; the
# mode state is never writable by the agent (the guard refuses it before the table is consulted). The write guard only looks
# things up here: changing or adding a mode is an edit to this table and a row in tests/test_mode_table.py.
#   world-existing  a page that already exists in world/
#   world-new       a page that does not exist yet in world/
#   other           everything else: manifest.json, design/, drafts/, ledger/, decisions/, ...
# Rules: "allow", "deny", or "append-only" (every original line of the existing page must survive).
MODE_TABLE: dict[str, dict[str, str]] = {
    "explore": {"world-existing": "deny", "world-new": "allow", "other": "allow"},
    "extend": {"world-existing": "append-only", "world-new": "allow", "other": "allow"},
    "edit": {"world-existing": "allow", "world-new": "allow", "other": "allow"},
    "lock": {"world-existing": "deny", "world-new": "deny", "other": "deny"},
}

# One line per mode: what it means (shown to the agent in the /world-mode skill) and what the guard says when it refuses.
MODE_SUMMARY = {
    "explore": "ideas only; no existing world page may be changed (new drafts and designs are fine).",
    "extend": "add new pages, sections and links; every original line of an existing page must survive.",
    "edit": "change existing pages with a change record; protected pages still need the user's authorization.",
    "lock": "read-only; nothing may be written.",
}
MODE_REFUSAL = {
    "explore": "existing pages are not changed. Put the proposal in design/ or drafts/ and show it.",
    "extend": "an existing page may only grow; every original line must survive. Add around the existing text.",
    "lock": "nothing may be written.",
}
SWITCH = "Ask the user, or tell them they can switch with `/world-mode edit` (or another mode)."
SKILL_LIST_START, SKILL_LIST_END = "<!-- modes:start -->", "<!-- modes:end -->"


def render_mode_list() -> str:
    """The mode list as it appears in the /world-mode skill, generated from the table so the two cannot drift."""
    return "\n".join([SKILL_LIST_START] + [f"- `{mode}`: {MODE_SUMMARY[mode]}" for mode in MODES] + [SKILL_LIST_END])


def path_kind(rel: str, is_file: bool) -> str:
    """`work`, `world-existing`, `world-new` or `other` for a world-relative posix path."""
    if rel.startswith("work/"):
        return "work"
    if rel.startswith("world/"):
        return "world-existing" if is_file else "world-new"
    return "other"


def _safe(session_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]", "", str(session_id or ""))[:64]


def state_path(root: Path, session_id: str) -> Path | None:
    safe = _safe(session_id)
    return root / STATE_DIR / f"mode-{safe}.json" if safe else None


def read_mode(root: Path, session_id: str) -> str | None:
    path = state_path(root, session_id)
    if path is None or not path.is_file():
        return None
    try:
        mode = json.loads(path.read_text(encoding="utf-8")).get("mode")
    except (OSError, ValueError, AttributeError):
        return None
    return mode if mode in MODES else None


def write_mode(root: Path, session_id: str, mode: str) -> Path:
    if mode not in MODES:
        raise ValueError(f"mode must be one of {', '.join(MODES)}")
    path = state_path(root, session_id)
    if path is None:
        raise ValueError("no session id: the mode cannot be recorded")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"mode": mode}) + "\n", encoding="utf-8")
    return path


def clear_mode(root: Path, session_id: str) -> bool:
    """Remove the session's mode so nothing is enforced; True when there was one."""
    path = state_path(root, session_id)
    if path is None:
        raise ValueError("no session id: there is no mode to clear")
    if path.is_file():
        path.unlink()
        return True
    return False
