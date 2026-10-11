"""PreToolUse hook for Edit/Write/MultiEdit/NotebookEdit inside a world project (Claude Code).

Two checks. (1) When the user has set a task mode for this session with `/world-mode`, it enforces it: `lock` allows no write
(except under `work/` and the mode state), `explore` allows no change to an existing world page, `extend` allows an
existing page to change only by addition (every original line must survive). No mode set means this check is skipped.
(2) It refuses a write to an existing protected page (manifest status `accepted`, or a core-rule page type) unless a
change record in ledger/changes/ is a T3 record that lists the page and carries the user's authorization words.
It stops the write before it happens; the lint (`L-PROTECTED-CHANGE`) is the backstop for everything this
cannot see (a shell command that writes a file, another provider, a record written without the user's words).

Usage (from .claude/settings.json): py -3 "$CLAUDE_PROJECT_DIR/.world-design/library/tools/write_guard.py"
Reads the hook JSON on stdin. Exit 2 with a message on stderr blocks the call; any error fails open (exit 0).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worlddesign.ledger import is_authorization, load_baseline, load_changes, record_pages  # noqa: E402
from worlddesign.mode import MODE_REFUSAL, MODE_TABLE, STATE_DIR, SWITCH, path_kind, read_mode  # noqa: E402
from worlddesign.types import load_types  # noqa: E402
from worlddesign.paths import hook_root  # noqa: E402
from worlddesign.textio import use_utf8  # noqa: E402


def authorizing_record(root: Path, file: str) -> str | None:
    """Path of a T3 record that lists `file`, has authority words and is not rejected."""
    try:
        baseline = load_baseline(root)
    except (OSError, ValueError):
        baseline = None
    for record in load_changes(root):
        if is_authorization(record, baseline) and file in record_pages(record):
            return record.path
    return None


_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")


def _lines_kept(before: str, after: str) -> bool:
    """True when the text of every original line survives (links or words may be added around it)."""
    def flatten(text: str) -> list[str]:
        return [_LINK.sub(r"\1", line).strip() for line in text.split("\n") if line.strip()]
    haystack = "\n".join(flatten(after))
    return all(line.rstrip(".,;:!?") in haystack for line in flatten(before))


def _changes(target: Path, tool_name: str, tool_input: dict) -> list[tuple[str, str]]:
    """(before, after) text pairs this call would produce; empty when the call shape is unknown."""
    if tool_name == "Write" or ("content" in tool_input and "old_string" not in tool_input):
        try:
            before = target.read_text(encoding="utf-8")
        except OSError:
            return []
        return [(before, str(tool_input.get("content", "")))]
    if "edits" in tool_input:
        return [(str(e.get("old_string", "")), str(e.get("new_string", ""))) for e in tool_input.get("edits") or [] if isinstance(e, dict)]
    return [(str(tool_input.get("old_string", "")), str(tool_input.get("new_string", "")))]


def mode_reason(root: Path, target: Path, mode: str | None, tool_name: str = "", tool_input: dict | None = None) -> str | None:
    """Reason the user's `/world-mode` forbids this write, or None. The rules are the table in worlddesign/mode.py."""
    if mode is None or mode not in MODE_TABLE:
        return None
    try:
        rel = target.relative_to(root.resolve()).as_posix()
    except ValueError:
        return None
    kind = path_kind(rel, target.is_file())
    if kind == "work":
        return None
    rule = MODE_TABLE[mode][kind]
    if rule == "allow":
        return None
    if rule == "append-only" and all(_lines_kept(b, a) for b, a in _changes(target, tool_name, tool_input or {})):
        return None
    return f"Task mode is {mode} (set by the user with /world-mode): {MODE_REFUSAL[mode]} {SWITCH}"


def _manifest_row(root: Path, file: str) -> dict | None:
    """The manifest row of world/<file>, read from manifest.json alone: the guard asks one question, so no page is parsed
    (about 25 ms flat instead of growing with the world). Raises on an unreadable manifest."""
    manifest = json.loads((root / "manifest.json").read_bytes().decode("utf-8-sig"))
    for row in manifest.get("pages") or []:
        if isinstance(row, dict) and row.get("file") == file:
            return row
    return None


def _protected_in_baseline(root: Path, file: str) -> bool:
    try:
        baseline = load_baseline(root)
    except Exception:  # noqa: BLE001
        return False
    return bool(baseline and (baseline["pages"].get(file) or {}).get("protected"))


def _proposed_text(target: Path, tool_name: str, tool_input: dict) -> str | None:
    """The whole text the file would have after this call, or None when it cannot be worked out (then the guard stays out of the way)."""
    try:
        text = target.read_text(encoding="utf-8-sig")
    except OSError:
        return None
    if tool_name == "Write" or ("content" in tool_input and "old_string" not in tool_input):
        return str(tool_input.get("content", ""))
    edits = tool_input.get("edits") if isinstance(tool_input.get("edits"), list) else [tool_input]
    for edit in edits:
        if not isinstance(edit, dict) or "old_string" not in edit:
            return None
        old, new = str(edit["old_string"]), str(edit.get("new_string", ""))
        if not old or old not in text:
            return None
        text = text.replace(old, new) if edit.get("replace_all") else text.replace(old, new, 1)
    return text


def _protected_files(manifest: dict, core: frozenset) -> set[str]:
    return {str(r["file"]) for r in manifest.get("pages") or [] if isinstance(r, dict) and isinstance(r.get("file"), str)
            and (str((r.get("fields") or {}).get("status", "")) == "accepted" or str(r.get("typeKey", "")) in core)}


def _manifest_demotion(root: Path, target: Path, tool_name: str, tool_input: dict) -> str | None:
    """Editing manifest.json must not be the way around the page protection: setting an accepted page back to draft, changing a core-rule
    page's type, or dropping its row would unprotect it for the next write. Blocked unless a T3 record authorizes that page."""
    proposed = _proposed_text(target, tool_name, tool_input)
    if proposed is None:
        return None
    try:
        core = load_types().core_rule_keys()
        before = _protected_files(json.loads(target.read_text(encoding="utf-8-sig")), core)
        after = _protected_files(json.loads(proposed), core)
    except (OSError, ValueError, AttributeError):
        return None  # a broken manifest is the lint's business (and the guard's baseline fallback), not a reason to block here
    try:
        baseline = load_baseline(root)
    except (OSError, ValueError):
        baseline = None
    before |= {f for f, row in ((baseline or {}).get("pages") or {}).items() if isinstance(row, dict) and row.get("protected")}
    lowered = sorted(f for f in before - after if not authorizing_record(root, f))
    if not lowered:
        return None
    return (f"This edit to manifest.json would remove the protection of {', '.join(lowered)} (status `accepted` or a core-rule type changed, or the row dropped). "
            "Protected canon is not unprotected by editing the manifest. Tell the user which page and why, ask for their explicit authorization, and "
            "write a T3 change record in ledger/changes/ that lists the page under `pages` and quotes their words under `authority`, then retry (rules/INVENTION.md).")


def decide(root: Path, file_path: str, mode: str | None = None, tool_name: str = "", tool_input: dict | None = None) -> str | None:
    """Reason to block a write to file_path, or None to allow it."""
    target = Path(file_path)
    target = (root / target if not target.is_absolute() else target).resolve()
    try:
        state = target.relative_to((root / STATE_DIR).resolve())
    except ValueError:
        state = None
    if state is not None:
        return (f"{STATE_DIR}/ holds the task mode the user set with /world-mode; the agent never writes it (the mode hook does, on the user's command). "
                "Ask the user to type `/world-mode <mode>` or `/world-mode off`.")
    blocked = mode_reason(root, target, mode, tool_name, tool_input)
    if blocked:
        return blocked
    if target == (root / "manifest.json").resolve():
        return _manifest_demotion(root, target, tool_name, tool_input or {})
    world_dir = (root / "world").resolve()
    try:
        file = target.relative_to(world_dir).as_posix()
    except ValueError:
        return None  # not a world page
    if not target.is_file():
        return None  # a new page is not protected canon
    try:
        row = _manifest_row(root, file)
    except Exception as error:  # a broken manifest must not switch protection off: fall back to the last checkpoint
        if _protected_in_baseline(root, file) and not authorizing_record(root, file):
            return (f"world/{file} was protected canon at the last checkpoint and manifest.json cannot be read now ({error}). Fix manifest.json "
                    "first (it is allowed), or ask the user for explicit authorization and record it as a T3 change record (rules/INVENTION.md).")
        return None
    if row is None:
        return None
    status, type_key = str((row.get("fields") or {}).get("status", "")), str(row.get("typeKey", ""))
    if status != "accepted" and type_key not in load_types().core_rule_keys():
        return None
    if authorizing_record(root, file):
        return None
    why = "its status is `accepted`" if status == "accepted" else f"its type `{type_key}` is a core-rule type"
    return (f"world/{file} is protected canon ({why}). Do not edit it yet. Tell the user the page, the exact change and the pages "
            "that depend on it, and ask for explicit authorization. Only after the user has said yes, write a T3 change record in "
            f"ledger/changes/ that lists `{file}` under `pages` and quotes their words under `authority`, then retry (rules/INVENTION.md).")


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
        mode = read_mode(root, str(data.get("session_id") or ""))
        reason = decide(root, file_path, mode, str(data.get("tool_name") or ""), tool_input)
    except Exception as error:  # fail open: a broken guard must never block unrelated work
        print(f"write_guard: skipped ({type(error).__name__}: {error})", file=sys.stderr)
        return 0
    if reason:
        print(f"Blocked by write_guard: {reason}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
