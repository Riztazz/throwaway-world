"""The data and the few writes behind the review page (`new_world.py`, tab "Review").

The page shows what the bootstrap agent wrote and lets the user judge it with a click: approve or reject the reference map,
`voice.md` and each exemplar, answer open questions, pick a pitch. Reading is a snapshot of the world folder; the only writes
are the status line of those few files (with the user's reason after a rejection) and decisions recorded through `records.py`.
Stdlib only; no network.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from .bootstrap_state import _status, build_state, review_note
from .refcheck import _cards
from .ledger import load_decisions
from .records import RecordError, accept, new_decision
from .textio import read_text, write_text

MAP = "authoring/references/ANALYSIS.md"
VOICE = "voice.md"
EXEMPLARS = "authoring/references/exemplars"
STATUSES = ("approved", "rejected", "proposed")
NOTE_MAX = 600

WHAT_APPROVING_MEANS = {
    "map": "The role split, the blends and how each conflict between references was settled, as written. Reject it with a note to have the agent change a row.",
    "voice": "The rules and limits for bible prose, fiction, in-game text and dialogue, as written. Every role agent writes to it.",
    "exemplar": "A passage the role agents use as a sound-check: 'the world sounds like this'. Different exemplars show different kinds of text; they are not competing options. One approved is enough to start pitching.",
}


class ReviewError(ValueError):
    """A request the page may not make (shown to the user as is)."""


def _rel(rel: str) -> str:
    rel = str(rel).replace("\\", "/")
    if not rel or rel.startswith("/") or ".." in rel.split("/") or ":" in rel:
        raise ReviewError("not a file in this world")
    return rel


def reviewable(root: Path, rel: str) -> bool:
    """The only files the page may change: the reference map, voice.md and one exemplar passage."""
    try:
        rel = _rel(rel)
    except ReviewError:
        return False
    if rel in (MAP, VOICE):
        return (root / rel).is_file()
    parts = rel.split("/")
    return (rel.startswith(EXEMPLARS + "/") and len(parts) == len(EXEMPLARS.split("/")) + 1 and rel.endswith(".md")
            and parts[-1].lower() != "readme.md" and (root / rel).is_file())


def _one_line(note: str) -> str:
    return re.sub(r"\s+", " ", note).strip()[:NOTE_MAX]


def set_status(root: Path, rel: str, status: str, note: str = "") -> str:
    """Set the first status line of a reviewable file; a rejection keeps the user's reason in a `Review note:` line."""
    if status not in STATUSES:
        raise ReviewError(f"status must be one of {', '.join(STATUSES)}")
    if not reviewable(root, rel):
        raise ReviewError("this file cannot be reviewed from the page")
    rel = _rel(rel)
    path = root / rel
    lines = read_text(path).split("\n")
    in_frontmatter = lines[0].strip() == "---"
    lines = [ln for i, ln in enumerate(lines) if not (i < 14 and re.match(r"(?i)^\s*review[ _]note:", ln))]
    index = next((i for i, ln in enumerate(lines[:12]) if re.match(r"(?i)^\s*status:", ln)), None)
    if index is None:
        index = 1 if in_frontmatter else 0
        lines.insert(index, f"status: {status}")
        inside = in_frontmatter
    else:
        label = re.match(r"^(\s*status:\s*)", lines[index], re.I).group(1)
        lines[index] = f"{label}{status}"
        inside = in_frontmatter and "---" not in [ln.strip() for ln in lines[1:index]]
    note = _one_line(note)
    if status == "rejected" and note:
        lines.insert(index + 1, f"{'review_note' if inside else 'Review note'}: {note}")
    write_text(path, "\n".join(lines))
    return status


CARD_REL = re.compile(r"^authoring/references/(roles|categories)/[^/]+\.md$")


def set_card_status(root: Path, rel: str, card_id: str, status: str, note: str = "") -> str:
    """Set the `- Status:` line of one technique card (found by its atom id); a rejection keeps the reason in a `- Review note:` line."""
    if status not in STATUSES:
        raise ReviewError(f"status must be one of {', '.join(STATUSES)}")
    rel = _rel(rel)
    if not CARD_REL.match(rel) or not (root / rel).is_file():
        raise ReviewError("this file holds no cards the page may change")
    path = root / rel
    lines = read_text(path).split("\n")
    starts = [i for i, ln in enumerate(lines) if ln.startswith("## ")] + [len(lines)]
    for a, b in zip(starts, starts[1:]):
        id_at = next((i for i in range(a, b) if re.match(rf"^- Id:\s*{re.escape(card_id)}(\s|$)", lines[i])), None)
        if id_at is None:
            continue
        keep = [ln for i, ln in enumerate(lines[a:b], a) if not re.match(r"^- Review note:", ln)]
        shift = id_at - a - sum(1 for i in range(a, id_at) if re.match(r"^- Review note:", lines[i]))
        section = keep
        at = next((i for i, ln in enumerate(section) if re.match(r"^- Status:", ln)), None)
        if at is None:
            at = shift + 1
            section.insert(at, f"- Status: {status}")
        else:
            section[at] = f"- Status: {status}"
        note = _one_line(note)
        if status == "rejected" and note:
            section.insert(at + 1, f"- Review note: {note}")
        write_text(path, "\n".join(lines[:a] + section + lines[b:]))
        return status
    raise ReviewError(f"no card {card_id} in {rel}")


# ---- reading --------------------------------------------------------------------------------------------------

def _watched(root: Path) -> list[Path]:
    found: list[Path] = [root / MAP, root / VOICE, root / ".world-design" / "world.json", root / "decisions" / "INBOX.md"]
    for folder, pattern in ((EXEMPLARS, "*.md"), ("authoring/references/roles", "*.md"), ("authoring/references/categories", "*.md"),
                            ("decisions", "D-*.md"), ("design/pitches", "*.md")):
        base = root / folder
        if base.is_dir():
            found += sorted(base.glob(pattern))
    return found


def fingerprint(root: Path) -> str:
    """A short hash of the watched files' names, sizes and times: it changes when the agent or the user changes any of them."""
    digest = hashlib.sha1()
    for path in _watched(root):
        try:
            stat = path.stat()
        except OSError:
            continue
        digest.update(f"{path.relative_to(root).as_posix()}|{stat.st_size}|{stat.st_mtime_ns}\n".encode())
    return digest.hexdigest()[:16]


_META = re.compile(r"(?i)^\s*(status|role|purpose|review[ _]note):")


def _split_meta(text: str) -> tuple[dict[str, str], str]:
    """The leading `key: value` lines (status, role, purpose, review note) and the rest of the text."""
    lines = text.split("\n")
    meta: dict[str, str] = {}
    skip = 1 if lines and lines[0].strip() == "---" else 0
    body_from = 0
    for i, line in enumerate(lines[:14]):
        if line.strip() in ("", "---") and i >= skip:
            body_from = i + 1 if line.strip() == "---" else body_from
            continue
        match = _META.match(line)
        if match:
            meta[match.group(1).lower().replace(" ", "_")] = line.split(":", 1)[1].strip()
            body_from = i + 1
        elif i >= skip:
            break
    return meta, "\n".join(lines[body_from:]).strip("\n")


def _item(root: Path, rel: str, kind: str, title: str) -> dict:
    text = read_text(root / rel)
    meta, body = _split_meta(text)
    if kind != "exemplar":  # the status line is shown as a badge, not as part of the text
        shown = body.split("\n")
        body = "\n".join(ln for i, ln in enumerate(shown) if not (i < 14 and _META.match(ln)))
    return {"rel": rel, "kind": kind, "title": title, "role": meta.get("role", ""), "purpose": meta.get("purpose", ""),
            "status": _status(text) or "none", "note": review_note(text), "text": body, "means": WHAT_APPROVING_MEANS[kind]}


def _items(root: Path) -> list[dict]:
    items = []
    if (root / MAP).is_file():
        items.append(_item(root, MAP, "map", "Reference map"))
    if (root / VOICE).is_file():
        items.append(_item(root, VOICE, "voice", "Voice"))
    base = root / EXEMPLARS
    for path in sorted(base.glob("*.md")) if base.is_dir() else []:
        if path.name.lower() != "readme.md":
            items.append(_item(root, f"{EXEMPLARS}/{path.name}", "exemplar", path.stem))
    return items


def _card_items(root: Path) -> list[dict]:
    """Every technique card: hard ones first, then by file."""
    out = []
    for group in ("roles", "categories"):
        base = root / "authoring" / "references" / group
        for path in sorted(base.glob("*.md")) if base.is_dir() else []:
            for heading, fields in _cards(read_text(path)):
                idline = fields.get("Id", "")
                atom = (re.match(r"(\S+)", idline) or re.match(r"()", "")).group(1)
                found = re.search(r"Binding:\s*(\w+)", idline)
                binding = (found.group(1) if found else fields.get("Binding", "")).strip().lower()
                out.append({"rel": f"authoring/references/{group}/{path.name}", "group": group, "name": path.stem, "id": atom, "heading": heading,
                            "binding": binding if binding in ("hard", "soft") else "other",
                            "status": (fields.get("Status", "").lower().split() or ["proposed"])[0], "note": fields.get("Review note", ""),
                            "effect": fields.get("Effect", ""), "test": fields.get("Test", ""), "plain": fields.get("Plain", ""),
                            "applied": fields.get("Applied", ""), "usedBy": fields.get("Used by", "")})
    return sorted(out, key=lambda c: (c["binding"] != "hard", c["rel"], c["id"]))


def _decision_body(text: str) -> str:
    match = re.match(r"^---\n.*?\n---\n", text, re.S)
    return text[match.end():].strip() if match else text.strip()


def _questions(root: Path) -> list[dict]:
    out = []
    for rec in load_decisions(root):
        if rec.error or str(rec.meta.get("status", "")) not in ("open", "proposed"):
            continue
        body = _decision_body(read_text(root / rec.path))
        title = re.match(r"#\s+(.+)", body)
        out.append({"id": str(rec.meta.get("id", "")), "status": str(rec.meta.get("status", "")), "blocking": str(rec.meta.get("blocking", "")).lower() == "true",
                    "title": title.group(1).strip() if title else rec.path, "body": re.sub(r"^#\s+.+\n+", "", body, count=1), "path": rec.path})
    return sorted(out, key=lambda q: (not q["blocking"], q["id"]))


def _round_decisions(root: Path, rel: str) -> list[dict]:
    """Decisions that mention a pitch file (by name), open or decided."""
    stem = Path(rel).stem
    found = []
    for rec in load_decisions(root):
        if rec.error:
            continue
        text = read_text(root / rec.path)
        if stem in text or rel in text:
            found.append({"id": str(rec.meta.get("id", "")), "status": str(rec.meta.get("status", "")), "authority": str(rec.meta.get("authority", ""))})
    return found


def _pitches(root: Path) -> list[dict]:
    base = root / "design" / "pitches"
    rounds = []
    for path in sorted(base.glob("round-*.md")) if base.is_dir() else []:
        rel = f"design/pitches/{path.name}"
        text = read_text(path)
        parts = re.split(r"(?m)^## ", text)
        intro = parts[0]
        pitches, recommendation = [], ""
        for part in parts[1:]:
            heading, _, body = part.partition("\n")
            match = re.match(r"Pitch ([A-Z])\b[^\w]*(.*)", heading)
            if match:
                pitches.append({"key": match.group(1), "title": match.group(2).strip() or heading, "heading": heading.strip(), "text": body.strip()})
            elif heading.lower().startswith("recommendation"):
                recommendation = body.strip()
        decisions = _round_decisions(root, rel)
        decided = next((d for d in decisions if d["status"] == "accepted"), None)
        pending = next((d for d in decisions if d["status"] in ("open", "proposed")), None)
        title = re.match(r"#\s+(.+)", intro.strip())
        rounds.append({"rel": rel, "title": title.group(1).strip() if title else path.stem, "intro": re.sub(r"^#\s+.+\n+", "", intro.strip(), count=1),
                       "pitches": pitches, "recommendation": recommendation, "decided": decided, "pending": pending})
    return rounds


def next_message(snap: dict) -> dict:
    """What the user should send the agent next, as {text, hint, fresh}: `text` is empty while the user still has something to do
    on the page (`hint` says what), and `fresh` says to start a new agent session for it."""
    items = snap["items"]
    if not any(i["kind"] in ("map", "voice") for i in items):
        return {"text": "Read BOOTSTRAP-PROMPT.md in this folder and follow it.", "fresh": True,
                "hint": "The agent has not written the reference map or voice yet."}
    if any(i["status"] == "rejected" for i in items) or any(c["status"] == "rejected" for c in snap["cards"]):
        return {"text": "I judged your bootstrap files on the review page. Run bootstrap_status.py, revise everything I rejected (my reasons are in the Review note lines, on cards too), then continue.",
                "fresh": False, "hint": "You rejected something: the agent revises it, then you judge it again."}
    if not snap["ready"]:
        if any(b.startswith("approve") for b in snap["blockers"]):
            return {"text": "", "fresh": False, "hint": "Approve or reject the items under \"To judge\" first; then this box shows what to send."}
        return {"text": "Run bootstrap_status.py and continue the bootstrap.", "fresh": False,
                "hint": "The agent has not finished writing. If it is still working, wait."}
    rounds = snap["pitches"]
    if not rounds:
        return {"text": "Read PITCH-PROMPT.md in this folder and follow it.", "fresh": True,
                "hint": "Everything is approved. A fresh session keeps the pitch round clean."}
    if any(not r["decided"] for r in rounds):
        return {"text": "", "fresh": False, "hint": "Pick a pitch (or a mix, or none) under \"Pitch rounds\" first; then this box shows what to send."}
    return {"text": "I chose on the review page. Read decisions/ and design/pitches/, record the options I did not choose as rejected, and go on with the next round.",
            "fresh": False, "hint": "Your pick is recorded as a decision."}


def snapshot(root: Path) -> dict:
    """Everything the page shows, as one JSON-able dict."""
    text, blockers = build_state(root)
    lines = text.split("\n")
    snap = {"name": lines[0].removeprefix("BOOTSTRAP STATUS: "), "status": [ln for ln in lines[1:] if ln.strip() and not ln.startswith("NOT READY") and not ln.startswith("READY")
                                                                          and not ln.startswith("  - ")],
            "ready": not blockers, "blockers": blockers, "items": _items(root), "cards": _card_items(root), "questions": _questions(root),
            "pitches": _pitches(root), "fingerprint": fingerprint(root)}
    snap["next"] = next_message(snap)
    return snap


# ---- recording decisions ----------------------------------------------------------------------------------------

def answer_question(root: Path, did: str, answer: str) -> str:
    """Accept an open or proposed decision with the user's own words (a typed answer, or a click on the proposal)."""
    answer = _one_line(answer)
    authority = answer or "Accepted as proposed, by a click on the review page."
    try:
        path = accept(root, did, authority)
    except RecordError as error:
        raise ReviewError(str(error)) from None
    note = f"**Answer (review page):** {answer}" if answer else "**Answer (review page):** accepted as proposed above."
    write_text(path, read_text(path).rstrip("\n") + "\n\n" + note + "\n")
    return did


def pick_pitch(root: Path, rel: str, choice: str, text: str = "") -> str:
    """Record the user's pick for a pitch round: an accepted decision with their choice and words."""
    rounds = {r["rel"]: r for r in _pitches(root)}
    if rel not in rounds:
        raise ReviewError("no such pitch round")
    round_ = rounds[rel]
    keys = [p["key"] for p in round_["pitches"]]
    if choice not in keys and choice not in ("merge", "none"):
        raise ReviewError(f"choose one of {', '.join(keys)}, merge or none")
    words = _one_line(text)
    if choice in ("merge", "none") and not words:
        raise ReviewError("say what to merge, or what you want instead")
    said = {"merge": "Merge", "none": "None of them"}.get(choice, f"Pitch {choice}")
    authority = f"{said}, chosen on the review page." + (f" My words: {words}" if words else "")
    if round_["decided"]:
        raise ReviewError(f"{round_['decided']['id']} already records a choice for this round")
    if round_["pending"]:
        accept(root, round_["pending"]["id"], authority)
        path = next(root / r.path for r in load_decisions(root) if not r.error and r.meta.get("id") == round_["pending"]["id"])
        write_text(path, read_text(path).rstrip("\n") + f"\n\n**Choice (review page):** {said}.{(' ' + words) if words else ''} Not chosen: {', '.join(k for k in keys if k != choice) or 'none'}.\n")
        return round_["pending"]["id"]
    rest = ", ".join(k for k in keys if k != choice) or "none"
    path = new_decision(root, "creative", "accepted", f"{round_['title']}: {said}", affects=[], authority=authority,
                        why=f"Chosen on the review page from `{rel}`. Not chosen: {rest}." + (f" The user's words: {words}" if words else ""))
    return next(str(r.meta.get("id")) for r in load_decisions(root) if not r.error and root / r.path == path)
