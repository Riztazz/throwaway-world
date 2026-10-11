"""Write decision and change records the way the lint expects them, so an agent never hand-writes frontmatter.

`new_decision`, `accept`, `supersede` and `new_change` produce the files rules/DECISIONS.md and rules/INVENTION.md describe:
the next free id, the right frontmatter, the inbox line for an open question, a refreshed decisions/INDEX.md. They cannot
know whether a quote really is the user's: an accepted decision or a T3 record still needs the user's exact words, and the
tool refuses an empty one.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from .ledger import (CHANGE_MODES, CHANGE_TIERS, DECISION_TYPES, as_list, build_decisions_index, load_changes, load_decisions)
from .textio import read_text, slug, write_text

NEW_STATUSES = ("open", "proposed", "accepted", "rejected")
_INBOX_EMPTY = "(none)"


class RecordError(ValueError):
    pass


def _q(text: str) -> str:
    return '"' + " ".join(text.split()).replace("\\", "\\\\").replace('"', '\\"') + '"'


def _pages(root: Path, pages: list[str]) -> list[str]:
    out = []
    for p in pages:
        p = p.strip()
        if p:
            out.append(p if p.endswith(".md") else f"{p}.md")
    return out


def _lst(items: list[str]) -> str:
    return "[" + ", ".join(items) + "]"


def slugify(title: str) -> str:
    return slug(title)[:40].strip("-") or "decision"


def _create_new(path: Path, text: str) -> bool:
    """Create the file only if it does not exist (one atomic step). False when someone else got there first."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "x", encoding="utf-8", newline="\n") as handle:
            handle.write(text.replace("\r\n", "\n"))
    except FileExistsError:
        return False
    return True


def _taken_numbers(folder: Path, prefix: str, parsed: list[str]) -> list[int]:
    """Numbers already used: from the parsed ids and from the file names, so a record the parser rejects still counts."""
    pattern = re.compile(rf"^{re.escape(prefix)}(\d+)")
    found = [int(m.group(1)) for value in parsed if (m := pattern.match(value))]
    if folder.is_dir():
        found += [int(m.group(1)) for f in folder.iterdir() if (m := pattern.match(f.name))]
    return found


def next_decision_id(root: Path) -> str:
    numbers = _taken_numbers(root / "decisions", "D-", [str(r.meta.get("id", "")) for r in load_decisions(root)])
    return f"D-{max(numbers, default=0) + 1:04d}"


def _refresh_index(root: Path) -> None:
    write_text(root / "decisions" / "INDEX.md", build_decisions_index(load_decisions(root), root))


def _inbox(root: Path) -> Path:
    return root / "decisions" / "INBOX.md"


def _inbox_add(root: Path, did: str, blocking: bool, affects: list[str], title: str) -> None:
    path = _inbox(root)
    text = read_text(path) if path.is_file() else "# Open questions\n\n"
    lines = [l for l in text.rstrip("\n").split("\n") if l.strip() != _INBOX_EMPTY]
    lines.append(f"{did} | blocking {'yes' if blocking else 'no'} | {', '.join(affects) or '-'} | {title}")
    write_text(path, "\n".join(lines) + "\n")


def _inbox_remove(root: Path, did: str) -> None:
    path = _inbox(root)
    if not path.is_file():
        return
    lines = [l for l in read_text(path).rstrip("\n").split("\n") if not l.startswith(f"{did} ")]
    if not any(re.match(r"^D-\d{4}\b", l) for l in lines):
        lines.append(_INBOX_EMPTY)
    write_text(path, "\n".join(lines) + "\n")


def new_decision(root: Path, type: str, status: str, title: str, affects: list[str] | None = None, blocking: bool = False,
                 authority: str = "", why: str = "", supersedes: list[str] | None = None, today: str | None = None) -> Path:
    if type not in DECISION_TYPES:
        raise RecordError(f"type must be one of {', '.join(DECISION_TYPES)}")
    if status not in NEW_STATUSES:
        raise RecordError(f"status must be one of {', '.join(NEW_STATUSES)} (use supersede for the rest)")
    if not title.strip() or "\n" in title:
        raise RecordError("a decision needs a one-line title")
    if status == "accepted" and not authority.strip():
        raise RecordError("an accepted decision needs the user's exact words (--authority); only the user accepts")
    affects = _pages(root, affects or [])
    day = today or date.today().isoformat()
    number = int(next_decision_id(root)[2:])
    while True:
        did = f"D-{number:04d}"
        path = root / "decisions" / f"{did}-{slugify(title)}.md"
        body = (f"---\nid: {did}\ntype: {type}\nstatus: {status}\nblocking: {'true' if blocking else 'false'}\naffects: {_lst(affects)}\n"
                f"supersedes: {_lst(supersedes or [])}\nsuperseded_by: []\ndate: {day}\nauthority: {_q(authority)}\n---\n\n# {title.strip()}\n\n"
                f"{why.strip() or ('The decision, in one or two sentences.' if status != 'open' else 'The question the agent could not settle.')}\n")
        if _create_new(path, body):
            break
        number += 1
    if status == "open":  # an open question waits for the user: it goes in the inbox the SessionStart hook shows
        _inbox_add(root, did, blocking, affects, title.strip())
    _refresh_index(root)
    return path


def _find(root: Path, did: str) -> Path:
    for r in load_decisions(root):
        if not r.error and r.meta.get("id") == did:
            return root / r.path
    raise RecordError(f"no decision {did}")


def _set_fields(path: Path, updates: dict[str, str]) -> None:
    text = read_text(path)
    match = re.match(r"^(---\n)(.*?\n)(---\n)", text, re.S)
    if not match:
        raise RecordError(f"{path.name} has no frontmatter")
    head = match.group(2)
    for key, value in updates.items():
        line = f"{key}: {value}"
        head = re.sub(rf"(?m)^{re.escape(key)}:.*$", lambda _: line, head) if re.search(rf"(?m)^{re.escape(key)}:", head) else head + line + "\n"
    write_text(path, match.group(1) + head + match.group(3) + text[match.end():])


def accept(root: Path, did: str, authority: str, today: str | None = None) -> Path:
    if not authority.strip():
        raise RecordError("accepting needs the user's exact words (--authority)")
    path = _find(root, did)
    status = next((str(r.meta.get("status", "")) for r in load_decisions(root) if not r.error and r.meta.get("id") == did), "")
    if status not in ("open", "proposed"):
        raise RecordError(f"{did} is {status or 'in an unknown state'}: only an open or proposed decision can be accepted "
                          "(a superseded or rejected one is history; record a new decision instead)")
    _set_fields(path, {"status": "accepted", "authority": _q(authority), "date": today or date.today().isoformat(), "blocking": "false"})
    _inbox_remove(root, did)
    _refresh_index(root)
    return path


def supersede(root: Path, did: str, by: str) -> list[Path]:
    old, new = _find(root, did), _find(root, by)
    if did == by:
        raise RecordError("a decision cannot supersede itself")
    _set_fields(old, {"status": "superseded", "superseded_by": _lst([by]), "blocking": "false"})
    meta = next(r.meta for r in load_decisions(root) if r.meta.get("id") == by)
    _set_fields(new, {"supersedes": _lst(sorted(set(as_list(meta.get("supersedes")) + [did])))})
    _inbox_remove(root, did)
    _refresh_index(root)
    return [old, new]


def new_change(root: Path, mode: str, tier: str, pages: list[str], summary: str, dependents: list[str] | None = None,
               authority: str = "", status: str = "proposed", role: str = "", today: str | None = None) -> Path:
    if mode not in CHANGE_MODES:
        raise RecordError(f"mode must be one of {', '.join(CHANGE_MODES)}")
    if tier not in CHANGE_TIERS:
        raise RecordError(f"tier must be one of {', '.join(CHANGE_TIERS)}")
    if status not in ("proposed", "integrated", "accepted", "rejected"):
        raise RecordError("status must be proposed, integrated, accepted or rejected")
    if tier == "T3" and not authority.strip():
        raise RecordError("a T3 record needs the user's exact authorizing words (--authority)")
    if status == "accepted" and not authority.strip():
        raise RecordError("an accepted record needs the user's exact words (--authority)")
    if not summary.strip():
        raise RecordError("a change record needs a summary")
    day = (today or date.today().isoformat())
    stamp = day.replace("-", "")
    taken = _taken_numbers(root / "ledger" / "changes", f"chg-{stamp}-", [str(r.meta.get("id", "")) for r in load_changes(root)])
    number = max(taken, default=0) + 1
    while True:
        cid = f"chg-{stamp}-{number:02d}"
        path = root / "ledger" / "changes" / f"{cid}.md"
        text = (f"---\nid: {cid}\nmode: {mode}\ntier: {tier}\npages: {_lst(_pages(root, pages))}\ndependents: {_lst(_pages(root, dependents or []))}\n"
                     f"status: {status}\nauthority: {_q(authority)}\nrole: {_q(role)}\ndate: {day}\n---\n\n{summary.strip()}\n")
        if _create_new(path, text):
            return path
        number += 1
